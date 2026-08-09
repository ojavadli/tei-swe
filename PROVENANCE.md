# PROVENANCE

## Source

We use 30 agent systems drawn from the official SWE-bench leaderboard submission
archive (SWE-bench/experiments), covering the SWE-bench Lite and SWE-bench Verified
splits, frozen at commit 2f15350cd32becc4569e0d826361048555b605c0, accessed 2026-08-08.

- Archive: https://github.com/SWE-bench/experiments @ `2f15350cd32becc4569e0d826361048555b605c0`
- Benchmark: SWE-bench, Jimenez et al., ICLR 2024.
- Resolve rates use the archive's own denominators (`analysis/get_leaderboard.py`):
  lite = 300, verified = 500 instances.

## Selection rule (pre-registered; applied unchanged)

1. Parse every submission folder in `evaluation/lite/` and `evaluation/verified/`.
2. Deduplicate into unique systems: lowercase the entry name, strip parentheticals
   and model/version suffixes, collapse whitespace. Keep the **highest-scoring**
   submission per system.
3. Keep only systems whose **kept** submission names a `github.com` repository in its
   own metadata (`info.site` / `info.report`). No URL was ever guessed or inferred
   from a third-party page.
4. Verify every candidate URL with `git ls-remote` before counting it.
5. Rank survivors by resolve rate descending.

## Counts

| Stage | Count |
|---|---|
| Submissions parsed (lite 84 + verified 134) | 218 |
| Unique systems after dedupe | 101 |
| Systems whose kept submission names a GitHub repo | 30 |
| Repo URLs verified with `git ls-remote` | 30 / 30 |
| **Final set** | **30** |

### Why 30 and not 31

The target was 31. The strict filter yielded 30. The pre-approved remedy — widening
the universe with `evaluation/multilingual/` — was executed and added **zero**
sourceable systems: 0 of its 13 entries name a repository in metadata, and all 13 are
the same system (mini-swe-agent v2.0.0a0) evaluated across different models, so they
are one system under the dedupe rule, not thirteen.

One alternative reading of step 3 was identified and **rejected**: if a system were
allowed to qualify when *any* of its submissions names a repo (rather than the kept
top-scoring one), `autocoderover` and `patchpilot` would enter, giving 32 and allowing
a top-31. That reading was discovered only after observing that the strict rule gives
30, so adopting it would have been selection tuned to the desired count. The owner
elected to report the honest 30. **The set is not padded.**

Two systems in the set (`codeshellagent`, `codeshelltester`) share one repository
(WisdomShell/codeshell); they are distinct leaderboard entries under the name-based
dedupe rule and are kept as such.

## Recorded trajectories: retrievable (claim corrected)

**Correction (2026-08-09):** the original run recorded these assets as
credential-gated after an anonymous S3 ListBucket returned 403. That reading was
wrong: the archive's own downloader (`python -m analysis.download_logs <path>`,
boto3) retrieves `logs/` and `trajs/` **without credentials** (unsigned GetObject).
The optimization run itself did not use recorded trajectories
(`recorded_trajectories_available = 0` in each `tei/onboarding.json` reflects the
run-time state); the revision retrieved and scored them for the TRAJ rung.
Objects retrieved at the frozen commit: submission trajectories for
`20240402_sweagent_gpt4` (300, downloader verification), `20251215_livesweagent_claude-opus-4-5`
(500), `20250928_trae_doubao_seed_code` (500), `20250611_moatless_claude-4-sonnet-20250514`
(273, partial), `20250205_dars_agent_claude_3.5_sonnet_deepseek_r1` (300),
`20250113_OrcaLoca` (300), `20250625_ExpeRepair-v1_claude-4-sonnet-20250514` (1);
three submissions (`swe-rizzo`, `aider`, `rag`) uploaded no trajectories. Also
used: the archive's per-instance resolved/unresolved outcomes for every system.

## TEI v7 application

Methodology applied as deployed and frozen; nothing in it was reimplemented here.

- Harness: `tei-bench` @ `626b455ff662c185f17396411a839759d663c8c9` (`teibench/gate.py`, `optimize_v7`).
- Product gate: `tei-loop` @ `e02931354d5e311cac20cd0c43b0fef04cb8ffa8` (`tei_loop/gate.py` —
  `verify_candidate` do-no-harm confirmation, `preflight_power` MDE preflight).

Per agent, on a local `tei-v7` branch (never pushed): baseline evaluation → 30
structural-fix versions → select the best → 30 prompt-optimization versions on top →
best overall, confirmed with `tei_loop.gate.verify_candidate` before being declared
the winner, with the paraphrase noise floor and MDE recorded.

### Score substrate — read this before citing any number

- **VERIFIED** — real execution outcomes on a fixed paired instance set.
- **PROXY** — `gpt-5.6-luna` rubric scores of a version against the diagnosed failure
  modes and fixed probe instances.

Scores from the optimization run are **PROXY** (judge substrate). One system
(**SWE-agent**) was subsequently executed end-to-end in both arms via the official
harness (execution micro-arm: baseline 1/6 = patched 1/6 resolved, 0 wins / 0
losses; do-no-harm confirmed at the VERIFIED rung). No other agent was executed. Deciding whether a patch *resolves* an instance requires SWE-bench's
evaluation harness, which imports `docker_build` / `docker_utils` / `dockerfiles`;
**Docker is not installed on this machine** (`which docker` → not found), so there is
no ground-truth resolved/unresolved signal to score against. Independently, the
mission's own Tier-A definition excludes Docker orchestration and GPUs, and four
linked repositories contain no runnable source at all. PROXY scores measure judged
plausibility of a change, **not** resolve-rate improvement. They must not be read as,
or converted into, SWE-bench gains.

Every shipped delta in this study is **below the MDE** reported by the gate's own
`preflight_power` at the probe count used (4-6 paired queries). The gains do clear the
paraphrase noise floor (rewordings scored +0.000 to +0.0075), but "clears the floor and
does no harm" is the strongest claim the evidence supports.

Models actually used across the study: `gpt-5.6-luna` (primary judge, structural-fix
generation, prompt optimization — all optimization-run calls); `gpt-5.6-terra`
(same-family replication passes: 200 judging calls); `claude-sonnet-5`
(supplementary cross-provider judging only, 115 calls, recorded in
`external_judge.json` and reported in the paper's appendix); `gpt-4o-mini`
(execution micro-arm agent-under-test rollouts). No silent substitution occurred
anywhere; every pass's model is recorded in its output file.

### Budget and scale-down

Hard cap $25. This API key lacks the `api.usage.read` scope, so billed cost could not
be read back; tokens are metered exactly and priced under a stated assumption
(nominal $1.25/$10.00 per Mtok; a 2x conservative bound of $2.50/$20.00 enforces the
cap). Recorded spend: **568 calls, 727,172 input +
953,779 output tokens, $10.45 nominal /
$20.89 conservative.**

Scale-downs applied (pre-registered order: fewer instances per evaluation first, then
fewer iterations per phase, applied uniformly to all remaining agents):

- iters 30->18 (projected $6.01) before 06_lingxi
- iters 30->18 (projected $7.46) before 14_agentless15
- iters 18->12 (projected $5.83) before 15_composioswekit
- iters 30->18 (projected $8.10) before 24_swefixer
- iters 18->12 (projected $6.04) before 25_codeshelltester
- iters 30->18 (projected $10.23) before 13_swerizzo

## The final 30

| Rank | System | Split | Resolve % | Resolved | Repo | Cloned SHA |
|---|---|---|---|---|---|---|
| 1 | live-SWE-agent + Claude 4.5 Opus medium (20251101) | verified | 79.2 | 396 | [OpenAutoCoder/live-swe-agent](https://github.com/OpenAutoCoder/live-swe-agent) | `8d7dd86345` |
| 2 | Sonar Foundation Agent + Claude 4.5 Opus | verified | 79.2 | 396 | [AutoCodeRoverSG/sonar-foundation-agent](https://github.com/AutoCodeRoverSG/sonar-foundation-agent) | `394c58819e` |
| 3 | TRAE + Doubao-Seed-Code | verified | 78.8 | 394 | [bytedance/trae-agent](https://github.com/bytedance/trae-agent) | `e839e559ac` |
| 4 | ACoder | verified | 76.4 | 382 | [ACoder-AI/ACoder](https://github.com/ACoder-AI/ACoder) | `63325725b6` |
| 5 | JoyCode + Claude 4 Sonnet + GPT-4.1 | verified | 74.6 | 373 | [jd-opensource/joycode-agent](https://github.com/jd-opensource/joycode-agent) | `1bace2ab9f` |
| 6 | Lingxi-v1.5_claude-4-sonnet-20250514 | verified | 74.6 | 373 | [nimasteryang/Lingxi](https://github.com/nimasteryang/Lingxi) | `1f2e5dc4c8` |
| 7 | Moatless Tools + Claude 4 Sonnet | verified | 70.8 | 354 | [aorwall/moatless-tools](https://github.com/aorwall/moatless-tools) | `011ead57a5` |
| 8 | SWE-agent + Claude 4 Sonnet | verified | 66.6 | 333 | [SWE-agent/SWE-agent](https://github.com/SWE-agent/SWE-agent) | `3ea751c087` |
| 9 | AgentScope | verified | 63.4 | 317 | [modelscope/agentscope](https://github.com/modelscope/agentscope) | `29b592358c` |
| 10 | EntroPO + R2E + Qwen3-Coder-30B-A3B-Instruct | verified | 60.4 | 302 | [sherdencooper/R2E-Gym](https://github.com/sherdencooper/R2E-Gym) | `eee9f6f00a` |
| 11 | ExpeRepair-v1.0 + Claude 4 Sonnet | lite | 60.33 | 181 | [ExpeRepair/ExpeRepair](https://github.com/ExpeRepair/ExpeRepair) | `5594f2c02c` |
| 12 | KGCompass + Claude 4 Sonnet (20250514) | lite | 58.33 | 175 | [GLEAM-Lab/KGCompass](https://github.com/GLEAM-Lab/KGCompass) | `b74a584e6d` |
| 13 | SWE-Rizzo | verified | 56.6 | 283 | [brokespace/gen42-codemonkeys](https://github.com/brokespace/gen42-codemonkeys) | `c6303b8710` |
| 14 | Agentless-1.5 + Claude-3.5 Sonnet (20241022) | verified | 50.8 | 254 | [OpenAutoCoder/Agentless](https://github.com/OpenAutoCoder/Agentless) | `5ce5888b9f` |
| 15 | Composio SWE-Kit (2024-10-25) | verified | 48.6 | 243 | [ComposioHQ/composio](https://github.com/ComposioHQ/composio) | `13cba53b1d` |
| 16 | DARS Agent | lite | 47.0 | 141 | [darsagent/DARS-Agent](https://github.com/darsagent/DARS-Agent) | `eab35168a9` |
| 17 | CodeShellAgent + Gemini 2.0 Flash (Experimental) | verified | 44.2 | 221 | [WisdomShell/codeshell](https://github.com/WisdomShell/codeshell) | `09d1adc88c` |
| 18 | CodeFuse-CGM | lite | 44.0 | 132 | [codefuse-ai/CodeFuse-CGM](https://github.com/codefuse-ai/CodeFuse-CGM) | `2c12754ade` |
| 19 | Agentless Lite + O3 Mini (20250214) | verified | 42.4 | 212 | [sorendunn/Agentless-Lite](https://github.com/sorendunn/Agentless-Lite) | `01900cec17` |
| 20 | SWE-Exp | verified | 42.0 | 210 | [YerbaPage/SWE-Exp](https://github.com/YerbaPage/SWE-Exp) | `6b5c92ed0a` |
| 21 | SWE-RL (Llama3-SWE-RL-70B + Agentless Mini) (20250226) | verified | 41.2 | 206 | [facebookresearch/swe-rl](https://github.com/facebookresearch/swe-rl) | `5aa10d67f1` |
| 22 | OrcaLoca + Agentless-1.5 + Claude-3.5 Sonnet (20241022) | lite | 41.0 | 123 | [fishmingyu/OrcarLLM](https://github.com/fishmingyu/OrcarLLM) | `341de75336` |
| 23 | Patched.Codes Patchwork | lite | 37.0 | 111 | [patched-codes/patchwork](https://github.com/patched-codes/patchwork) | `21948cbec4` |
| 24 | SWE-Fixer (Qwen2.5-7b retriever + Qwen2.5-72b editor) | verified | 32.8 | 164 | [InternLM/SWE-Fixer](https://github.com/InternLM/SWE-Fixer) | `7871693672` |
| 25 | CodeShellTester + GPT 4o (2024-05-13) | lite | 31.33 | 94 | [WisdomShell/codeshell](https://github.com/WisdomShell/codeshell) | `09d1adc88c` |
| 26 | Aegis - o3-mini_1.0 | lite | 30.33 | 91 | [evandiewald/aegis](https://github.com/evandiewald/aegis) | `cd81da38f4` |
| 27 | Agentless + RepoGraph + GPT-4o | lite | 29.67 | 89 | [ozyyshr/RepoGraph](https://github.com/ozyyshr/RepoGraph) | `6c3977d878` |
| 28 | CodeR + GPT 4 (1106) | lite | 28.33 | 85 | [NL2Code/CodeR](https://github.com/NL2Code/CodeR) | `d63468344b` |
| 29 | Aider + GPT 4o & Claude 3 Opus | lite | 26.33 | 79 | [paul-gauthier/aider](https://github.com/paul-gauthier/aider) | `5dc9490bb3` |
| 30 | RAG + Claude 3 Opus | verified | 7.0 | 35 | [SWE-bench/SWE-bench](https://github.com/SWE-bench/SWE-bench) | `cd37836ffe` |

## Reproduction

```bash
mkdir -p ~/swebench-agents && cd ~/swebench-agents
git clone --depth 1 https://github.com/SWE-bench/experiments.git archive
git -C archive checkout 2f15350cd32becc4569e0d826361048555b605c0
python3 build_manifest.py --splits lite verified   # parse + dedupe + extract repo URLs
python3 stage_clones.py                            # shallow-clone every sourceable repo
python3 finalize_manifest.py                       # rank, manifest.csv/json, onboarding
python3 find_prompt_surface.py                     # content-based prompt-surface scan
export OPENAI_API_KEY=...                          # ask the owner; never commit it
python3 tei_pipeline.py --struct-iters 30 --prompt-iters 30 --batch 6 --probes 6
python3 make_reports.py
```

_Generated 2026-08-08._
