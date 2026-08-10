#!/usr/bin/env python3
"""TEI Bayesian Credit Ledger (BCL) — Phase B, implemented per BUDGET_100.md.

Two-head Bayesian bandit credit assignment with Thompson selection over
technique-family x weakest-dimension cells, plus:
  L0  immutable store        : candidates.jsonl (unchanged, lossless)
  L1  credit model           : Jeffreys Beta reliability head + Normal
                               magnitude head (Normal-Inverse-Gamma update),
                               empirical-prior smoothing for n<3 cells,
                               Thompson sampling per proposal slot,
                               closed-form Bayesian surprise per observation
  L2  lessons                : <=12 falsifiable bullets, delta-ops only
                               (add/increment/refute/merge) via one small
                               luna call per batch; ops -> ledger_log.jsonl
  L3  evidence-prioritized historical retrieval : 8 why-records maximizing
                               surprise + |delta| + contextual relevance +
                               recency, diversified by greedy submodular
                               facility-location over why-record embeddings
                               (text-embedding-3-small)
  L4  recency                : last 4 records verbatim

Terminology (paper-binding): Bayesian *bandit* credit assignment (not GP
"Bayesian optimization"); *retrieval* (not attention); *shrinkage* (not
hierarchical modeling).
"""
import hashlib
import json
import math
import os
import random
import urllib.request

FAMILIES = [
    ("verification-tests", ("test", "regression", "verif", "assert", "oracle", "reproduc")),
    ("patch-format", ("format", "diff", "parse", "normaliz", "extract", "apply")),
    ("localization", ("localiz", "fault", "search", "locate", "trace", "root cause")),
    ("retrieval-context", ("retriev", "context", "repo map", "knowledge", "rag", "index")),
    ("prompt-structure", ("prompt", "instruction", "role", "template", "system message")),
    ("invariants-guards", ("invariant", "guard", "check", "validat", "sanity", "pre-", "post-")),
    ("retry-recovery", ("retry", "recover", "fallback", "timeout", "budget", "loop")),
    ("output-contract", ("output", "contract", "schema", "json", "final", "submission")),
    ("decomposition-planning", ("decompos", "plan", "step", "hypothes", "acceptance", "criteria")),
]


def family_of(technique: str) -> str:
    t = (technique or "").lower()
    for fam, keys in FAMILIES:
        if any(k in t for k in keys):
            return fam
    return "other"


ALL_FAMS = [f for f, _ in FAMILIES] + ["other"]


# ---------------------------------------------------------------- math
def digamma(x):
    """Exact digamma via recurrence to x>=6 + asymptotic series (|err|<1e-10).

    scipy is not a dependency; the closed-form KL below needs a real digamma
    (the log(x)-1/2x shortcut is off by ~0.27 at x=0.5, the Jeffreys prior)."""
    r = 0.0
    while x < 6:
        r -= 1 / x
        x += 1
    f = 1 / (x * x)
    return r + math.log(x) - 0.5 / x - f * (1 / 12 - f * (1 / 120 - f * (1 / 252 - f * (1 / 240 - f / 132))))


def kl_beta(a1, b1, a2, b2):
    """KL(Beta(a1,b1) || Beta(a2,b2))."""
    from math import lgamma
    dg = digamma
    lb = lambda a, b: lgamma(a) + lgamma(b) - lgamma(a + b)
    return (lb(a2, b2) - lb(a1, b1)
            + (a1 - a2) * dg(a1) + (b1 - b2) * dg(b1)
            + (a2 - a1 + b2 - b1) * dg(a1 + b1))


def kl_normal(m1, v1, m2, v2):
    return 0.5 * (v1 / v2 + (m2 - m1) ** 2 / v2 - 1 + math.log(v2 / v1))


class Cell:
    """One (family, weakest-dimension) cell: Beta reliability + NIG magnitude."""

    def __init__(self, var0):
        self.w = 0.0   # wins  (delta > 0)
        self.l = 0.0   # losses
        self.n = 0
        self.mu, self.kappa, self.alpha, self.beta = 0.0, 1.0, 2.0, 2.0 * var0

    def beta_params(self):
        return 0.5 + self.w, 0.5 + self.l

    def post_mean_var(self):
        var = self.beta / (self.alpha - 1) if self.alpha > 1 else self.beta
        return self.mu, max(var / self.kappa, 1e-8)

    def update(self, delta):
        """Conjugate updates; returns Bayesian surprise (closed-form KL sum)."""
        a1, b1 = self.beta_params()
        m1, v1 = self.post_mean_var()
        self.w += 1.0 if delta > 0 else 0.0
        self.l += 1.0 if delta <= 0 else 0.0
        k, mu = self.kappa, self.mu
        self.mu = (k * mu + delta) / (k + 1)
        self.kappa = k + 1
        self.alpha += 0.5
        self.beta += 0.5 * k * (delta - mu) ** 2 / (k + 1)
        self.n += 1
        a2, b2 = self.beta_params()
        m2, v2 = self.post_mean_var()
        return kl_beta(a2, b2, a1, b1) + kl_normal(m2, v2, m1, v1)

    def snapshot(self):
        return dict(n=self.n, w=self.w, l=self.l, mu=round(self.mu, 5),
                    kappa=self.kappa, alpha=self.alpha, beta=round(self.beta, 6))


class BayesianCreditLedger:
    def __init__(self, tei_dir, weak_dim, var0, seed=0, call_json=None, embed=None):
        self.dir = tei_dir
        self.weak = weak_dim
        self.var0 = max(var0, 1e-6)
        self.rng = random.Random(seed)
        self.call_json = call_json
        self.embed = embed
        self.cells = {}     # (fam, dim) -> Cell
        self.fam_agg = {}   # fam -> Cell (technique-level aggregate for shrinkage)
        self.lessons = []   # [{id,text,support,refuted}]
        self.records = []   # slim: {vid,fam,dim,delta,surprise,why,phase}
        self.emb = {}
        self._sims = {}     # (vid,vid) -> cosine, cached across retrieve() calls
        p = os.path.join(tei_dir, "ledger.json")
        if os.path.isfile(p):
            st = json.load(open(p))
            self.lessons = st.get("lessons", [])
        ep = os.path.join(tei_dir, "emb.json")
        if os.path.isfile(ep):
            self.emb = json.load(open(ep))

    # ---------- state io ----------
    def _log(self, obj):
        with open(os.path.join(self.dir, "ledger_log.jsonl"), "a") as f:
            f.write(json.dumps(obj) + "\n")

    def save(self):
        json.dump({"lessons": self.lessons,
                   "cells": {f"{k[0]}|{k[1]}": c.snapshot() for k, c in self.cells.items()}},
                  open(os.path.join(self.dir, "ledger.json"), "w"), indent=1)
        json.dump(self.emb, open(os.path.join(self.dir, "emb.json"), "w"))

    def _cell(self, fam, dim):
        if (fam, dim) not in self.cells:
            self.cells[(fam, dim)] = Cell(self.var0)
        if fam not in self.fam_agg:
            self.fam_agg[fam] = Cell(self.var0)
        return self.cells[(fam, dim)]

    # ---------- ingestion ----------
    def ingest(self, rec, log=True):
        """Insert one scored candidate; compute Bayesian surprise; store slim rec.

        Credit goes to the ASSIGNED family when the generation contract chose one
        (rec['bcl_family']); prefix records fall back to keyword inference."""
        fam = rec.get("bcl_family") or family_of(rec.get("technique"))
        dim = rec.get("expected_dimension") or self.weak
        delta = rec.get("delta_vs_baseline", 0.0) or 0.0
        s1 = self._cell(fam, dim).update(delta)
        self.fam_agg[fam].update(delta)
        slim = dict(vid=rec["version_id"], fam=fam, dim=dim, delta=delta,
                    surprise=round(s1, 5), phase=rec.get("phase"),
                    why=(rec.get("why") or "")[:400])
        self.records.append(slim)
        if log:
            self._log({"ev": "ingest", **{k: slim[k] for k in ("vid", "fam", "dim", "delta", "surprise")}})
        return s1

    # ---------- L1: Thompson selection ----------
    def _draw(self, fam):
        cell = self.cells.get((fam, self.weak))
        agg = self.fam_agg.get(fam)
        # empirical-prior smoothing (shrinkage): n<3 cells borrow the
        # technique-level aggregate posterior
        src = cell if (cell and cell.n >= 3) else (agg if (agg and agg.n > 0) else None)
        if src is None:
            src = Cell(self.var0)
        a, b = src.beta_params()
        p = self.rng.betavariate(a, b)
        m, v = src.post_mean_var()
        d = self.rng.gauss(m, math.sqrt(v))
        return p, d

    def choose_slots(self, k):
        """Thompson sampling per slot over both heads; full draw log per slot."""
        chosen = []
        snap = hashlib.sha256(json.dumps(
            {f"{f}|{d}": c.snapshot() for (f, d), c in sorted(self.cells.items())},
            sort_keys=True).encode()).hexdigest()[:12]
        for slot in range(k):
            draws = {}
            best, best_s = None, -1e9
            for fam in ALL_FAMS:
                p, d = self._draw(fam)
                s = p * max(d, 0.0)
                draws[fam] = [round(p, 4), round(d, 5)]
                if s > best_s:
                    best, best_s = fam, s
            chosen.append(best)
            self._log({"ev": "thompson", "slot": slot, "chosen": best,
                       "score": round(best_s, 6), "posterior_hash": snap, "draws": draws})
        return chosen

    # ---------- L2: lessons (delta ops) ----------
    def update_lessons(self, batch_slims):
        if not self.call_json:
            return
        summary = [{"fam": r["fam"], "delta": r["delta"], "why": r["why"][:160]}
                   for r in batch_slims]
        prompt = f"""You maintain at most 12 falsifiable lesson bullets about what kinds of fixes help
THIS agent. Current lessons (id: text [support/refuted counts]):
{json.dumps([{'id': l['id'], 'text': l['text'], 'support': l['support'], 'refuted': l['refuted']} for l in self.lessons], indent=1)}

New scored candidates this batch:
{json.dumps(summary, indent=1)}

Emit DELTA OPERATIONS ONLY (never rewrite the list): add a new falsifiable lesson,
increment support of an existing one the batch confirms, refute one it contradicts,
or merge redundant ones. Max 3 operations.

JSON: {{"ops":[{{"op":"add","text":"..."}} | {{"op":"increment","id":0}} | {{"op":"refute","id":0}} | {{"op":"merge","ids":[0,1],"text":"..."}}]}}"""
        try:
            ops = (self.call_json(prompt, max_out=800) or {}).get("ops", [])[:3]
        except Exception:
            return
        for op in ops:
            kind = op.get("op")
            if kind == "add" and len(self.lessons) < 12 and op.get("text"):
                self.lessons.append({"id": max([l["id"] for l in self.lessons], default=-1) + 1,
                                     "text": str(op["text"])[:180], "support": 1, "refuted": 0})
            elif kind == "increment":
                for l in self.lessons:
                    if l["id"] == op.get("id"):
                        l["support"] += 1
            elif kind == "refute":
                for l in self.lessons:
                    if l["id"] == op.get("id"):
                        l["refuted"] += 1
            elif kind == "merge" and op.get("text"):
                ids = set(op.get("ids") or [])
                keep = [l for l in self.lessons if l["id"] not in ids]
                sup = sum(l["support"] for l in self.lessons if l["id"] in ids)
                keep.append({"id": max([l["id"] for l in keep], default=-1) + 1,
                             "text": str(op["text"])[:180], "support": max(sup, 1), "refuted": 0})
                self.lessons = keep
            self._log({"ev": "lesson_op", **op})

    # ---------- L3: evidence-prioritized historical retrieval ----------
    def _embed(self, texts):
        if not self.embed:
            return [None] * len(texts)
        return self.embed(texts)

    def retrieve(self, query_text, k=8):
        pool = self.records
        if len(pool) <= k:
            return pool
        need = [r for r in pool if r["vid"] not in self.emb]
        if need:
            vecs = self._embed([r["why"] or r["vid"] for r in need])
            for r, v in zip(need, vecs):
                if v is not None:
                    self.emb[r["vid"]] = v
        qv = (self._embed([query_text]) or [None])[0]

        def cos(u, v):
            if u is None or v is None:
                return 0.0
            du = math.sqrt(sum(x * x for x in u)) or 1
            dv = math.sqrt(sum(x * x for x in v)) or 1
            return sum(a * b for a, b in zip(u, v)) / (du * dv)

        def z(vals):
            m = sum(vals) / len(vals)
            sd = math.sqrt(sum((x - m) ** 2 for x in vals) / len(vals)) or 1
            return [(x - m) / sd for x in vals]

        sur = z([r["surprise"] for r in pool])
        mag = z([abs(r["delta"]) for r in pool])
        rel = z([cos(qv, self.emb.get(r["vid"])) for r in pool])
        N = len(pool)
        rec_ = [math.exp(-(N - 1 - i) / max(N / 2, 1)) for i in range(N)]
        prio = [sur[i] + mag[i] + rel[i] + rec_[i] for i in range(N)]

        # greedy submodular facility-location, priority-weighted
        def sim(i, j):
            a, b = pool[i]["vid"], pool[j]["vid"]
            key = (a, b) if a <= b else (b, a)
            if key not in self._sims:
                self._sims[key] = cos(self.emb.get(a), self.emb.get(b))
            return self._sims[key]
        S = []
        covered = [0.0] * N
        for _ in range(k):
            best, best_gain = None, -1e9
            for j in range(N):
                if j in S:
                    continue
                gain = prio[j] + sum(max(0.0, sim(i, j) - covered[i]) * max(prio[i], 0.1)
                                     for i in range(N) if i != j) / N
                if gain > best_gain:
                    best, best_gain = j, gain
            S.append(best)
            for i in range(N):
                covered[i] = max(covered[i], sim(i, best))
        sel = [pool[j] for j in S]
        self._log({"ev": "retrieve", "selected": [r["vid"] for r in sel]})
        return sel

    # ---------- rendering (<=2000 tokens) ----------
    def render(self, query_text):
        lines = ["HOW ALL PRIOR CANDIDATES SCORED AND WHY (posterior-guided)", ""]
        lines.append("L1 POSTERIORS per technique family (weakest-dim cell; shrinkage-smoothed):")
        lines.append("family | mean_delta | P(delta>0) | n")
        for fam in ALL_FAMS:
            cell = self.cells.get((fam, self.weak)) or self.fam_agg.get(fam)
            if not cell or cell.n == 0:
                continue
            a, b = cell.beta_params()
            m, _ = cell.post_mean_var()
            lines.append(f"{fam} | {m:+.4f} | {a/(a+b):.2f} | {cell.n}")
        if self.lessons:
            lines.append("")
            lines.append("L2 LESSONS (falsifiable; support/refuted):")
            for l in self.lessons:
                lines.append(f"- [{l['support']}/{l['refuted']}] {l['text']}")
        sel = self.retrieve(query_text)
        if sel:
            lines.append("")
            lines.append("L3 EVIDENCE-PRIORITIZED HISTORY (surprise+impact+relevance, diversity-selected):")
            for r in sel:
                lines.append(f"- {r['vid']} [{r['fam']}] d={r['delta']:+.4f} s={r['surprise']:.2f}: {r['why'][:200]}")
        last = self.records[-4:]
        if last:
            lines.append("")
            lines.append("L4 MOST RECENT:")
            for r in last:
                lines.append(f"- {r['vid']} [{r['fam']}] d={r['delta']:+.4f}: {r['why'][:160]}")
        out = "\n".join(lines)
        return out[:8000]  # hard budget ~2,000 tokens
