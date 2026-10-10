# GapFinder — Implementation Plan, Tests & Demo Guide

Oct 2, 2026 · @Sayjad Rahman

> **Planning document, written before any code.** Numbers in this plan and in
> [STRATEGY.pdf](STRATEGY.pdf) (gaps closed, run times, budgets, scores) are targets or
> illustrations, not results. Measured results, each with its log, are in the
> [README](../README.md#results) and [eval/results/](../eval/results/).

## Snapshot

Completion is milestone-based. Each milestone ends at an exit gate, and the next milestone starts only when that gate passes.

The plan has seven milestones (M0–M6). M0 is the feasibility gate. Nothing else gets built until it passes, because the whole idea rests on two facts nobody has verified yet: that Token Factory Sandboxes can fork a built RocksDB state reliably, and that your RusKey reproduction has a real, measurable gap.

**Definition of done (at submission):**

- [ ] GapFinder takes a paper PDF + repo URL and produces a Gap Report for RusKey: claim ledger, attributed assumptions, noise bands, and replayable checkpoint IDs.
- [ ] GapBench-mini results: planted-gap tasks with known answers, scored for GapFinder vs. a standard coding agent vs. a no-fork ablation.
- [ ] A hosted demo URL with replay mode and a capped live mode that stays up until judging ends.
- [ ] A public YouTube video of 3 minutes or less, a public repo with an open-source license, a README, and the tool-feedback write-up.

**The demo must prove three things, in this order of importance:**

1. **It finds the right hidden assumption when a standard agent doesn't.** Proven on planted tasks where the true answer is known, so this is not a matter of opinion.
2. **Forking is load-bearing.** The same pipeline without forks costs more and finishes fewer tasks within the same budget.
3. **It works on a real paper.** RusKey, told as your own story.

Scope rule for the whole project: GapFinder changes only experimental conditions (configs, flags, workload, build options, environment). It never edits the paper's algorithm code. That keeps the search space finite and the attributions honest.

## Can the demo show a standard agent failing? Yes, as a fair controlled comparison

Yes, and it should be the centrepiece of the video. It only works if it is fair, logged and repeated. Your judges include NVIDIA engineers, and a rigged baseline would cost you more than it gains.

Frame it precisely. The baseline does not "fail to reproduce the paper". It **fails to explain the gap**. Expect its most damaging failure to be a *false success*: it reports that the paper was reproduced, or gives an untested excuse.

**The baseline:** [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent), from the Princeton/Stanford team behind SWE-bench. It is a \~100-line agent that gets only a bash shell, keeps a linear message history, and works with any model through litellm ([overview](https://openapps.pro/packages/mini-swe-agent)). It is a neutral, respected standard, and the Artisan paper also used it as its comparison point. Run it against the Token Factory endpoint with Nemotron 3 Super, inside the same sandbox type GapFinder uses.

Add a second arm with mini-swe-agent on Nemotron 3 Ultra. If GapFinder still wins, the difference is the method, not the model.

**Fairness rules (publish these in the repo):**

| Rule | Why it matters |
| --- | --- |
| Same inputs: paper text, repo, and the naive reproduction numbers | Neither side gets extra information |
| Same task prompt, published word for word | Judges can check you didn't word it to mislead |
| Same dollar cap and wall-clock cap per task | The comparison is about method under equal resources |
| Same sandbox machine type | Hardware noise affects both equally |
| Same benchmark helper script available to both | The baseline isn't punished for not knowing how to run db\_bench |
| 5 runs per arm; report median and best, never only the worst | Prevents cherry-picking |
| Every transcript committed to `eval/baseline_logs/` | Anyone can audit it |

**Failure modes to look for.** These are expected, not scripted. Record them only if they actually happen:

| Baseline failure | What it looks like | How GapFinder handles it |
| --- | --- | --- |
| False success | "Reproduced successfully" after exit code 0, or compared against the wrong figure | Claim ledger plus numeric comparison against a noise band |
| Untested excuse | "The difference is likely due to hardware" | Every attribution needs a counterfactual branch; "unexplained" only after hypotheses run out |
| Confounded changes | Changes three settings at once, then can't say which mattered | One knob per branch, then bisection on combinations |
| Budget burned on rebuilds | Rebuilds and reloads the dataset for every attempt | Checkpoint tree; forks at the deepest checkpoint still valid |
| Overfitting | Pushes a setting to an implausible value until the number matches | Plausibility gate (evidence required) plus held-out claims |
| Editing the algorithm | Changes source code so the output matches | Diff check rejects edits outside configs and flags |
| Noise blindness | Treats a 3% difference as meaningful | Noise calibration from identical forks |

**Don't:** use a deliberately weak model for the baseline, show only its worst run, or write your own crippled agent and call it "typical AI".

If the baseline does well on some tasks, report it. A scoreboard like 2/12 vs. 9/12 is more believable than 0 vs. 12. If the baseline matches GapFinder overall, your planted tasks are too easy; harder ones are described in M4.

## System architecture

GapFinder is one pipeline built around one shared object: a checkpoint tree in Token Factory Sandboxes. Nemotron reads and judges; Sandboxes does every execution.

**Pipeline stages:**

1. **Ingest.** Paper PDF to text plus figure images; repo to a repo map (file tree, configs, run scripts, defaults).
2. **Claim ledger.** Every quantitative claim in the paper, with its figure or table and its conditions.
3. **Assumption space.** Every experimental knob, with the paper's stated value (or "unstated"), the code default, candidate values and evidence.
4. **Checkpoint tree.** Source checkpoint, then built, then data loaded. A naive run produces the gap vector; identical forks produce the noise band.
5. **Search loop.** Fan out one knob per branch, prune, combine the survivors, bisect to the minimal set, verify on held-out claims.
6. **Gap Report.** Per-claim attribution with evidence, noise band, cost and replayable checkpoint IDs.

**What the Sandboxes docs imply for the design:**

| Fact from the docs | Design consequence |
| --- | --- |
| Each command runs in a VM and the full filesystem is snapshotted afterwards; snapshots form a tree you can branch from ([Contree CLI](https://pypi.org/project/contree-cli/)) | Processes don't survive between runs. Anything a branch needs must be on disk. A "warm-up" hypothesis must run warm-up and measurement inside one command |
| In the docs' example, the same command from the same image returned the same UUID ([branching guide](https://docs.tokenfactory.nebius.com/sandboxes/sdk/python_sdk/branching.md)) | Identical runs may be deduplicated. Give every noise-calibration repeat a unique run tag. Verify in M0 |
| Writable layer defaults to 12 GiB; stdout and stderr are capped at 1 MiB by default, 10 MiB max ([spawn API](https://docs.tokenfactory.nebius.com/api-reference/sandboxes/instances/spawn-a-new-container-instance.md)) | Keep the loaded dataset under \~10 GB. Write benchmark logs to files and fetch them through the inspect API |
| Every result returns cost, elapsed time, CPU times, max RSS, block I/O and involuntary context switches (same page) | Free per-branch cost accounting, plus a noise flag for runs that were starved of CPU |
| The spawn request sets timeout and layer size, but no CPU, memory or GPU (same page) | Measure `nproc` and memory in M0. Plan for CPU-only workloads |
| Beta: 50 simultaneous operations; untagged, unreferenced checkpoints may be deleted after 180 days; access must be requested ([overview](https://docs.tokenfactory.nebius.com/sandboxes/overview)) | Cap fan-out at 40. Tag the demo checkpoints. Request access first |

**Model routing:**

| Model (Token Factory ID; confirm via the list-models API) | Job in GapFinder | Why this size | List price per 1M tokens, in / out |
| --- | --- | --- | --- |
| Nemotron 3 Ultra, `nvidia/Nemotron-3-Ultra-550b-a55b` | Claim ledger, assumption space, final adjudication | Few calls, hardest reasoning over paper and code | $1.00 / $3.00 |
| Nemotron 3 Super, `nvidia/nemotron-3-super-120b-a12b` | Per-branch diagnosis, writing each config change, failure triage | Many calls, moderate reasoning | $0.30 / $0.90 |
| Nemotron 3 Nano, `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B` | Parsing benchmark output into JSON, classifying logs | Most calls, simple extraction | $0.06 / $0.24 |
| Nemotron 3 Nano Omni, `nvidia/Nemotron-3-Nano-Omni` | Reading values off figures | Needs image input | $0.06 / $0.24 |

IDs and prices are from [Lava's Nebius list](https://www.lava.so/docs/gateway/providers/nebius.md), a third-party mirror; confirm both on Token Factory before you rely on them.

Two model gotchas to design for from day one:

- **Reasoning traces eat the token budget.** All Nemotron models on Token Factory are reasoning models; a small `max_tokens` can be used up by the reasoning, leaving the content empty ([Nebius issue #211](https://github.com/nebius/api/issues/211)). Set generous limits, use structured JSON output, and separate reasoning from content before parsing.
- **Don't design around a 1M context.** Sources disagree on Ultra's window (one router lists 128K). Give Ultra the paper text, a repo map and the 10–30 files that matter, not the whole repo.

**Core data objects** (pydantic schemas, defined in M1 and frozen after it):

| Object | Key fields |
| --- | --- |
| Claim | id, figure or table, metric, unit, reported value, conditions, type (absolute, ratio or trend), page |
| Assumption | id, knob, layer (build, config, workload or environment), paper value or "unstated", code default, candidate values, evidence (page or file:line), prior score |
| Branch | id, parent checkpoint, knob changes, command, parsed metrics, resource stats, status |
| Attribution | claim id, assumption set, gap before and after, noise band, held-out result, confidence label |

**Stack:** Python 3.11 with FastAPI and asyncio; `contree-sdk` for Sandboxes; the `openai` SDK pointed at `https://api.tokenfactory.nebius.com/v1/` ([API intro](https://docs.tokenfactory.nebius.com/api-reference/introduction)); SQLite plus a JSON event log for runs; a React (Vite) front end fed by server-sent events.

**Repo layout:**

```
gapfinder/
  ingest/     pdf.py  figures.py  repo_map.py
  ledger/     claims.py  assumptions.py  schemas.py
  sandbox/    tree.py  runner.py  noise.py  cost.py
  search/     planner.py  fanout.py  bisect.py  verify.py
  models/     router.py   # tier routing, retries, token accounting
  report/     gap_report.py
  api/        server.py   # FastAPI + SSE event stream
web/          # React UI
eval/
  gapbench/   tasks/  harness.py  score.py
  baseline/   mini_swe_env.py  prompt.md  logs/
papers/ruskey/  gold_ledger.json  gold_assumptions.json
tests/
```

## M0 — Feasibility gate

M0 answers seven yes/no questions. Each spike is a small script in `tests/spikes/` that you keep as a smoke test for the rest of the project.

**Before any code:**

- [ ] Request Sandboxes Beta access; it is gated ([overview](https://docs.tokenfactory.nebius.com/sandboxes/overview)).
- [ ] Create a Token Factory API key and check whether the hackathon's Resources page offers credits.
- [ ] Join the Sandboxes Discord channel linked from the docs. You'll need it if you hit Beta limits.
- [ ] Open a running `FEEDBACK.md`. Every rough edge you hit goes in it; it becomes the feedback submission.

**The seven spikes:**

| # | Spike | Pass condition | If it fails |
| --- | --- | --- | --- |
| S1 | Sandbox lifecycle: base image, chained runs, 3 branches from one checkpoint, file written in branch A absent in branch B, 40 concurrent runs, timeout, log download | All behave as documented; record `nproc`, memory and disk speed inside a sandbox | Ask in Discord; keep fan-out at whatever concurrency works |
| S2 | Dedup: same command twice from the same image, then with a unique tag | You know whether identical commands re-execute or return a cached result | If cached, every repeat gets a `RUN_TAG` env var |
| S3 | Build the RusKey RocksDB fork in release mode, checkpoint it, load the dataset, checkpoint again | Build and load both succeed; loaded image fits in the 12 GiB layer; time and cost recorded | Smaller dataset scaled to the paper's ratios; state the scaling in the report |
| S4 | Noise: 5 identical forks of the loaded checkpoint run the same benchmark | Coefficient of variation ≤ 10% on throughput, or stable ratios between configurations | Shift claims to hardware-independent metrics (below) |
| S5 | Models: each of the four Nemotron tiers returns valid JSON for a schema task; Ultra handles a \~100K-token prompt | Valid JSON from all four; real context limit known; latency and cost per call recorded | Smaller prompts with a repo map; use Super where Ultra is too slow |
| S6 | RusKey gap check: list the paper's 5–10 headline claims, put your current numbers next to them | At least 2 claims differ by more than twice the S4 noise band | Use a second paper as the real case; RusKey becomes the founder story only |
| S7 | Baseline harness: mini-swe-agent with a Token Factory model, running commands inside a sandbox | One full task completes and the transcript is saved | Write the thin environment adapter described below |

**Two facts that shape S4 and S7:**

- **Use hardware-independent metrics where you can.** LSM-tree papers often report write amplification, compaction counts, bytes read per lookup or space amplification. These depend on configuration and workload far more than on CPU speed, so microVM noise barely touches them. Throughput and latency are the noisy ones; treat them as ratios between configurations measured in the same branch.
- **The official baseline integration is currently broken.** The Token Factory docs say mini-swe-agent's `ContreeEnvironment` still imports a removed `contree_sdk` type and can't accept an explicit client ([integration page](https://docs.tokenfactory.nebius.com/sandboxes/sdk/integrations/mini-swe-agent.md)). Plan for a \~50-line custom environment class, and put the issue in `FEEDBACK.md`.

**Exit gate (go/no-go):** Go if S1, S3 and S5 pass and either S4 or its fallback works. S6 decides whether RusKey is the live case or only the story. If S1 or S3 fails outright, stop and tell me; the plan needs a different shape.

## M1 — Claim ledger and assumption space

M1 ends with one command, `gapfinder ledger paper.pdf --repo <url>`, that writes a grounded claim ledger and a ranked assumption list. No sandbox is involved yet, so this can run in parallel with M2.

**Build:**

1. **PDF ingest.** Text with page numbers via PyMuPDF; figures rendered as PNG crops around their captions; tables kept as text.
2. **Claim extraction (Ultra).** Paper text in, `Claim[]` JSON out, each claim carrying the exact sentence or cell it came from.
3. **Figure reading (Nano Omni).** For each figure a claim cites: axis range, series names, values with a stated reading error.
4. **Repo map (plain code, no LLM).** File tree, build files, config files, every CLI flag and its default (grep for gflags `DEFINE_*`, `argparse` `add_argument`, YAML keys).
5. **Assumption space (Ultra).** The paper's experimental-setup section, the repo map and the 10–30 relevant files in; `Assumption[]` out. Each assumption is tagged unstated, stated-and-matches, or stated-but-code-differs. The last one is a paper–artifact inconsistency and gets flagged on its own.
6. **Grounding checker (plain code).** Every quoted paper sentence must string-match the PDF text. Every `file:line` must exist and contain the cited flag. Anything ungrounded is dropped, never shown.
7. **LLM response cache.** Key on hash(model, prompt, schema). Tests become deterministic and you stop paying Ultra twice for the same paper.

**Tests:**

| Test | Type | Pass bar |
| --- | --- | --- |
| Schema round-trip for all four objects | Unit | 100% |
| Grounding checker rejects a planted fake quote and a fake `file:line` | Unit | Both rejected |
| Reasoning-trace handling: empty-content and `<think>`-wrapped responses parse correctly | Unit | No crash, no silent empty JSON |
| Claim recall against your hand-labelled RusKey gold ledger | Eval | ≥ 85% of headline claims |
| Claim precision (extracted claims that are real) | Eval | ≥ 90% |
| Figure values vs. your manual readings | Eval | Within 5% of the axis range |
| Assumption recall: gold knobs that appear in Ultra's top 30 | Eval | ≥ 80% |
| Ungrounded citations in the final output | Eval | 0 |
| Cost per paper (all tiers) | Logged | Recorded in `eval/results/` |

**Gold sets you create by hand:** RusKey plus the two small repos chosen for GapBench-mini in M4. For each paper: every headline claim with value and figure, and every knob you know of. These gold files are also what makes your evaluation credible, so commit them.

**Exit gate:** the ledger command runs on all three papers, the bars above pass on RusKey, and the outputs are frozen as test fixtures.

## M2 — Sandbox orchestrator and noise calibration

M2 ends when one command forks 24 branches from the loaded RusKey checkpoint, parses every result, computes a noise band, and leaves a replayable event log. It runs in parallel with M1.

**Build:**

1. **Checkpoint tree** (`tree.py`). Nodes are image UUIDs plus metadata: layer, applied changes, parent. Key nodes get tags such as `gf/ruskey/built` and `gf/ruskey/loaded`, so the 180-day cleanup never touches them.
2. **Depth planner.** Each assumption forks from the deepest checkpoint still valid for it. Build-flag knobs start from source (and share a build when they need the same flags); dataset knobs start from the built image; config and workload knobs start from the loaded image. This is where forking saves the most time, so log the savings.
3. **Harness spec.** One small YAML per paper: build command, load command, run-command template with `{knob}` placeholders, output file paths. Super drafts it from the README and scripts; a human confirms it. Say so openly in the README: it is the one human checkpoint.
4. **Runner** (`runner.py`). Async spawn and poll, per-run timeout, a semaphore at 40 concurrent runs, a unique `RUN_TAG` per run, retries only on infrastructure errors, never on experiment failures.
5. **Metric parser.** Regex first for known formats (db\_bench output, RocksDB statistics dump); Nano only for unknown formats. Every parsed number must appear verbatim in the raw log, otherwise it is rejected.
6. **Noise calibration** (`noise.py`). Five identical forks of the naive configuration. Noise band per metric = 2 × the median absolute deviation of those five runs. A branch effect counts as real only if its median moves by more than the noise band, with at least 3 repeats for any finalist. Runs with unusually high involuntary context switches are flagged and re-run.
7. **Cost meter.** Sandbox `cost` from each result, plus tokens per tier from the API usage fields times the price table.
8. **Event log.** Append-only JSONL: branch created, started, finished, metrics, pruned, verified. The live UI and replay mode in M5 both read this file, so design it now.

**Tests:**

| Test | Type | Pass bar |
| --- | --- | --- |
| Hidden-knob toy: a 20-line script whose output depends on flags and env vars, with one planted default | Integration | Orchestrator forks, runs and parses every branch |
| Isolation: a file written in one branch is absent in its sibling | Integration | Absent |
| Concurrency: 45 branches requested | Integration | 40 run, 5 queue, none dropped |
| Failure injection: crash, timeout, malformed output | Integration | Each gets the right status; nothing hangs |
| Dedup behaviour from spike S2 | Integration | Repeats with distinct `RUN_TAG`s re-execute |
| Parser grounding: a hallucinated value injected into Nano's output | Unit | Rejected |
| Noise estimator on the toy with known injected noise | Unit | Estimated band within ±30% of the true spread |
| Cost meter vs. the Nebius console for one batch | Integration | Within 5% |
| Replay: event log rebuilds the final tree state | Unit | Identical tree |

**Exit gate:** `gapfinder fanout --spec ruskey.yaml --knobs knobs.json` completes 24 branches from the loaded checkpoint, every branch has parsed metrics and a cost, and the noise band for each headline metric is written to the run record.

## M3 — Search, attribution and verification

M3 is the brain, and the part judges will probe hardest. Finding a setting that makes the number match is easy. Proving that setting is the *reason* is the product. Every step below exists to stop GapFinder from fooling itself.

**Search, in five rounds:**

1. **Screen.** Top 24 assumptions × 1–2 candidate values, one run each. Score each branch in noise units: (naive gap − branch gap) ÷ noise band. Prune anything under 1.
2. **Confirm.** Survivors get 3 repeats each. Effects that fade are pruned.
3. **Combine.** All survivors together in one branch, then pairs among the top 3–4. This catches gaps that need two knobs at once.
4. **Bisect.** If a combination closes the gap, remove one knob at a time to find the minimal set that still closes it. This is delta debugging applied to experimental conditions, and it is where the "git bisect" name comes from.
5. **Verify.** Four checks before anything is called *explained*:
   1. **Held-out claims.** Choose the explanation using one figure, then check it on a different figure or table. It must not make those worse beyond noise.
   2. **Plausibility gate (Ultra).** The value must be backed by evidence: paper text, another script in the repo, the authors' other artifacts, or a GitHub issue. A value that fits but has no evidence is labelled *fits but unsupported*.
   3. **Counterfactual.** Revert the knob in the final branch; the gap must come back.
   4. **Hypothesis count.** Every attribution reports how many hypotheses were tested, so a lucky match among 40 tries is visible as such.

**Labels in the Gap Report:** Explained · Partially explained · Fits but unsupported · Unexplained (likely hardware or environment) · Paper–artifact inconsistency.

**Super's role:** when a branch fails (build error, crash, missing dependency), Super reads the log tail and proposes a fix, at most 2 attempts. A diff guard compares each branch with its parent and rejects any change outside the harness spec's allowed paths, so algorithm source files can't be touched.

**Tavily (Should, not Must):** search the repo's GitHub issues, errata and the authors' slides for evidence about candidate values. Results feed the priors and the plausibility gate. That is a genuine use and the basis for the $3,000 bonus.

**Budget control:** successive halving across rounds, a hard dollar cap per task, and an early stop once every divergent claim has a label. Hitting the cap produces a partial report, never a crash.

**Tests (toy suite with known answers):**

| Behaviour | Planted setup | Pass condition |
| --- | --- | --- |
| Single cause | One knob with a changed default | Found as top-1 and labelled Explained |
| Interaction | Two knobs that only matter together | Found in the combine round |
| Decoy | A knob that moves the metric in the wrong direction | Pruned in the screen |
| Overfit trap | A knob that matches only at an absurd value | Labelled Fits but unsupported |
| Minimal set | 4 knobs combined, only 2 matter | Bisect returns exactly those 2 |
| No cause | Gap from a random offset no knob can explain | Labelled Unexplained; no false attribution |
| Counterfactual | Revert the winning knob | Gap reappears |
| Diff guard | A branch edits a `.cc` source file | Branch rejected |
| Budget cap | Cap set below what the task needs | Partial report written, clean exit |

**Exit gate:** all nine behaviours pass on the toy suite, and a first end-to-end Gap Report exists for RusKey. It can be rough; M4 hardens it.

## M4 — Evaluation: GapBench-mini, RusKey and the baseline

M4 produces the numbers the video and README rest on. GapBench-mini gives tasks with known answers; RusKey gives the real story; the baseline and ablations show what each part of GapFinder is worth.

**GapBench-mini: 12 planted-gap tasks across 3 small artifacts.** Each must run in minutes on CPU inside a sandbox:

| Artifact | Why it's here | Metric family | Example knobs to plant |
| --- | --- | --- | --- |
| RocksDB `db_bench`, on the same build as RusKey | Shares your checkpoints; tests build-layer knobs | Write amplification, compaction bytes (low noise) | Memtable size, L0 compaction trigger, bloom bits, value size, build mode |
| A small RL training script (CartPole-scale) | Mirrors LERP; RL is noisy, so it stresses the noise logic | Mean final reward over seeds | Discount factor, learning-rate schedule, reward normalisation, training steps |
| A small CPU-trainable ML script (MNIST-scale or tabular) | A different domain, so it isn't a RocksDB-only trick | Test accuracy | Input normalisation, weight decay, LR schedule, data split |

**How to plant a task:** run the artifact with a hidden configuration (1–2 knobs changed to plausible values). Its outputs become the "paper numbers". Write a 1–2 page mini-paper whose setup section omits or misstates the hidden knob. Agents receive the mini-paper and the repo at its defaults; the hidden configuration is the answer key.

**Task mix:** 4 single unstated knobs, 4 stated-but-code-differs, 3 two-knob interactions, and 1 with no explaining knob at all.

**Keep it honest:**

- [ ] Split into 4 dev tasks and 8 test tasks. Tune prompts and thresholds on dev only; the person tuning never opens the test answer keys.
- [ ] Run a leakage script that greps every mini-paper and repo for the hidden values.
- [ ] Same number of runs per arm (5 if the budget from M0 allows, otherwise 3).

**Arms:**

| Arm | What it shows |
| --- | --- |
| GapFinder, full | The headline result |
| GapFinder, no fork (every branch rebuilds and reloads) | Forking is load-bearing: same answers, far more cost and time |
| GapFinder, no verification step | Without M3's checks, false attributions rise |
| mini-swe-agent + Nemotron 3 Super | The standard-agent baseline |
| mini-swe-agent + Nemotron 3 Ultra | The gap is the method, not the model |

**Scored per task:** top-1 and top-3 attribution accuracy, false-attribution rate, share of the gap closed, dollars, wall time, and the number of expensive setup runs (fork vs. rebuild).

**RusKey, the real case:**

1. Run GapFinder 3 times. The top attribution should be the same in at least 2 of 3 runs.
2. Check the top attribution yourself; you know this paper better than any model.
3. Run the baseline 5 times on RusKey too.
4. Once the attribution is stable, email the RusKey authors a short, polite note with the finding and the replayable checkpoint. A reply before you submit is a bonus; author confirmation is the strongest evidence you can show.

**Tests for the evaluation itself:**

- [ ] Scoring unit tests on synthetic outputs with known scores.
- [ ] Rescoring from saved logs reproduces every number exactly.
- [ ] Leakage script passes on all 12 tasks.

**Exit gate:** the results table is filled for every arm, the RusKey Gap Report is stable across runs, and all transcripts are committed under `eval/`.

## M5 — Product, replay mode and deployment

M5 turns the pipeline into something a judge can open during judging and understand in a minute. The report leads; the fork tree is the evidence behind it, not the main screen.

**Screens, in the order a user meets them:**

1. **Input.** Upload the paper PDF, paste the repo URL, confirm the drafted harness spec.
2. **Claim ledger.** Claims as a table; each figure shown with Nano Omni's extracted values drawn as dots on the original plot, so a reader can check them at a glance.
3. **Live fork tree.** Source → built → loaded → branches, coloured by status (running, pruned, survivor, explained). Beside it, the target figure as bars: paper vs. naive vs. best branch, with the noise band shaded. A budget meter shows tokens per Nemotron tier and sandbox dollars.
4. **Gap Report.** One card per claim: label, gap before and after, evidence quotes with page or `file:line`, hypotheses tested, and the checkpoint ID with a copy-paste command to replay that branch. Export to Markdown and JSON.
5. **Comparison.** Baseline transcript excerpts beside GapFinder's, plus the GapBench-mini scoreboard.

**Replay mode** is the default landing page for judges. It plays a recorded event log at 1×, 4× or 16×, clearly labelled as a replay with the date it was recorded. It costs nothing and cannot break.

**Live mode** runs one small GapBench dev task end to end. Protect it with an access code in the submission notes, a per-run dollar cap, a daily global cap and a kill switch.

**Deployment:** host the backend container on Nebius AI Cloud; check during M0 whether a Serverless Endpoint accepts a CPU-only web container, otherwise use a small VM. Keep the Token Factory key and Sandboxes token server-side only. The rules count the project as running on Nebius as long as it calls the Token Factory inference API at runtime, so hosting is a bonus, not a gate. Set budget alerts, and add a daily health check that loads the replay and makes one tiny live call, because judging happens weeks after submission.

**README, in this order:**

- [ ] License badge at the very top (MIT or Apache-2.0), visible on the repo page as the rules require.
- [ ] Pitch in one paragraph, then a judge path: "open the URL, press Replay".
- [ ] Local setup in under 10 commands, with a toy task that runs in a few minutes.
- [ ] Architecture diagram.
- [ ] "How we use Nemotron and Token Factory": the routing table with real tokens and dollars per tier from your runs.
- [ ] "How we use Sandboxes": the checkpoint tree, fork counts, and setup time saved vs. the no-fork arm.
- [ ] Results table with links to every log.
- [ ] Limitations, stated plainly (CPU only, the harness spec needs human confirmation, noise on timing metrics).
- [ ] A note that GapFinder was built during the submission period, while the RusKey reproduction is your prior research, used here as a test case.

**Tests:**

| Test | Pass bar |
| --- | --- |
| End-to-end browser test (Playwright): upload, ledger, replay, report | All screens render; replay ends on the same report as the live run |
| Judge-path test: someone outside the team follows the README on a fresh machine | Replay visible in under 1 minute; local toy task running in under 15 minutes |
| Cost guard: live mode with the cap already reached | Refuses politely; spends nothing |
| 20 simultaneous replay viewers | No errors |
| Narrow screen | Report readable on a phone |

**Exit gate:** public URL live, README complete apart from final numbers, judge-path test passed once.

## M6 — Video and submission package

M6 is mostly not code. It starts with a code freeze: tag v1.0, and after that only bug fixes and README numbers change. Submit with a margin before the deadline, so a broken upload or a Devpost hiccup costs you nothing.

Check the exact cut-off time and its time zone on the Devpost page, and convert it to Dhaka time (UTC+6).

**Steps, in order:**

| Step | Work | Done when |
| --- | --- | --- |
| 1 | Code freeze: tag `v1.0` and deploy that tag | Demo URL serves `v1.0` |
| 2 | Final eval runs on frozen code; record the RusKey run that replay mode will play; capture screen recordings | Every number in the README has a log behind it |
| 3 | Record the voiceover from the script in the Demo guide; edit the video | Cut is 2:50 or shorter |
| 4 | Upload to YouTube as public; write the Devpost text; write the feedback; fill the Devpost form as a draft | Video plays in a logged-out browser |
| 5 | Submit | Devpost shows the entry as submitted |

**Devpost description, in this structure:**

1. **Inspiration:** the RusKey story in four sentences.
2. **What it does:** one paragraph and the Gap Report screenshot.
3. **How we built it:** the Nemotron routing table, the checkpoint tree, and where Serverless or hosting fits.
4. **Evaluation:** the GapBench-mini scoreboard against the baseline and ablations, with a link to the logs.
5. **Challenges, and what we learned:** be specific (noise handling, reasoning-trace parsing, dedup).
6. **What's next:** artifact-evaluation committees, more paper types.

**Feedback write-up:** turn `FEEDBACK.md` into a structured list: product, issue, steps to reproduce, impact, suggestion. Include only issues you actually hit, such as the broken mini-swe-agent integration if you hit it. Ten $100 awards go to the most valuable feedback, and good feedback also reads well to the Nebius judges.

**Submission checklist:**

- [ ] Track: Coding and Agentic Engineering.
- [ ] Repo public; license visible at the top of the repo page; README complete.
- [ ] Demo URL works logged out and lands on replay mode.
- [ ] Live-mode access code in the private judging notes, if Devpost offers a field for it.
- [ ] YouTube video public, 3:00 or shorter, audio explaining Token Factory and Nemotron usage.
- [ ] Description covers what you built, why, and how it works.
- [ ] Feedback on Token Factory, Sandboxes and Nemotron submitted.
- [ ] If you attended a Builders & Brews event, its city selected.
- [ ] Budget alerts and the daily health check running until judging ends.

## Test strategy at a glance

Seven levels of tests, from free and fast to costly and rare. The milestone sections hold the individual tests; this table says when each level runs.

| Level | What it covers | When it runs | Cost |
| --- | --- | --- | --- |
| Unit | Schemas, grounding checker, metric parser, noise estimator, diff guard, scoring | Every commit (GitHub Actions) | Free |
| Sandbox integration | Spikes S1–S4, hidden-knob toy, isolation, concurrency, failure injection | Nightly, and before merging orchestrator changes | Small; logged |
| LLM evals | Ledger and assumption quality against the gold sets | On any prompt change; cached otherwise | Ultra tokens, cached |
| GapBench-mini dev | The 4 dev tasks, full pipeline | Nightly from M3 | Moderate |
| GapBench-mini test | The 8 held-out tasks, all arms | Exactly twice: once in M4, once on frozen `v1.0` | Largest single spend |
| Product | Playwright end-to-end, judge-path test, cost guard | M5, and again after the freeze | Small |
| Production health | Replay loads; one tiny live call | Daily until judging ends | Tiny |

Three rules hold everywhere:

- **Cache every LLM call in tests.** Key on model, prompt and schema; tests stay deterministic and cheap.
- **Touch the test set twice, no more.** Running it after every tweak quietly overfits GapFinder to your own benchmark.
- **Log seeds, image UUIDs and costs for every run,** so any number in the README can be traced back to a log.

## Demo guide

The video has one job: show a real gap, a standard agent failing to explain it, and GapFinder explaining it with evidence, in under 3 minutes. Aim for 2:50, about 420 spoken words at a calm pace.

**Video script** (numbers in brackets come from your real runs; never fill them in before you have them):

| Time | On screen | Voiceover |
| --- | --- | --- |
| 0:00–0:15 | You, then the RusKey figure with your numbers overlaid in red | "I'm Sayjad, from BUET. For weeks I've been reproducing RusKey, a SIGMOD 2024 paper. My numbers don't match its figures, and the paper doesn't say why." |
| 0:15–0:30 | Two statistics, one line each | "This is normal: only about a third of code-backed systems papers even build in 30 minutes. Everyone asks whether a paper reproduces. We ask why it doesn't." |
| 0:30–1:00 | Baseline split screen: mini-swe-agent transcript, budget meter, overlay "Nemotron 3 Super · same budget · median run of 5 · all logs in repo" | "First, a standard coding agent on the same model, sandbox and budget." Then narrate only what it actually did, e.g. "\[it reran twice, then blamed the hardware without testing it\]". |
| 1:00–1:20 | Claim ledger; figure with Nano Omni's dots on it | "GapFinder starts by reading. Nemotron 3 Ultra turns the paper and code into a claim ledger and a list of unstated assumptions. Nano Omni reads the values off the figures." |
| 1:20–1:50 | The fork moment: one checkpoint fanning out into branches; bars growing; pruned branches greying out | "We build RocksDB once, load the data once, and checkpoint it in Token Factory Sandboxes. Five identical forks give the noise band. Then \[24\] branches fork from that exact state, one hypothesis each." |
| 1:50–2:15 | Bisect and verification; then the Gap Report card turning green | "Survivors are combined, then bisected to the minimal set. Nothing counts as explained until it holds on another figure, has evidence, and the gap returns when it's reverted." Then: "\[real attribution\]. Gap: \[X\]% to \[Y\]%." |
| 2:15–2:40 | Scoreboard; cost per Nemotron tier | "On \[8\] held-out planted tasks, GapFinder found the cause in \[N\]; the baseline in \[M\]. Without forking, the same pipeline needed \[K\]× more setup runs. Nano handles most calls, Super diagnoses, Ultra reasons. Total cost: \[$Z\]." |
| 2:40–2:55 | Back to you; repo and demo URL | "It's open source, every result is a replayable checkpoint, and it says 'unexplained' when it should." |

**Choose the baseline clip by a rule fixed in advance:** show the median-scoring run, and say so on screen. If the baseline's median run did reasonably well, show that honestly; the scoreboard still makes the point.

**Recording rules:**

- Every clip comes from a real run. Sped-up footage carries an on-screen label such as "4×".
- Record at 1920×1080 with browser zoom at 125% or more; hide notifications, bookmarks and any API keys.
- Put model names on screen whenever the voiceover says them. The rules require the audio to explain how you used Token Factory and Nemotron, and this makes it unmissable.
- Record the voiceover separately in a quiet room, from the script, timed. Add captions.
- Watch the final cut once on a phone before uploading.
- Upload as **public**, not unlisted, and test the link in a logged-out browser.

**Live demo path for judges:**

1. The demo URL opens on the RusKey replay, labelled with its recording date, with a three-line judge's guide: what to click, what to look for, where the logs are.
2. A "Try it live" button runs one small GapBench dev task in about 5–10 minutes, behind the access code, with a dollar cap.
3. If the live run fails, replay still works. If the whole site is down, the README carries a GIF of the run and the RusKey Gap Report as Markdown in the repo.

## Risks, cut lines and fallbacks

The biggest risks are all checked in M0, which is why M0 comes first. After that, the main danger is scope, so the cut lines below are decided now, not under pressure.

**Risk register:**

| Risk | Early warning | Fallback |
| --- | --- | --- |
| Sandboxes Beta access arrives late | No access when the M0 spikes are ready to run | Write `tree.py` against an interface with a local Docker stand-in so M1–M3 continue; email contree@nebius.com and ask in Discord |
| RusKey has no clear, measurable gap | Spike S6 fails | A second paper is the live case; RusKey stays the founder story; GapBench-mini carries the evidence |
| Timing noise too high in microVMs | S4 coefficient of variation above 10% | Hardware-independent metrics, and timing only as ratios within a branch |
| RocksDB build too slow or too large in a sandbox | S3 over budget or over the 12 GiB layer | Build a Docker image locally, push it to a registry, import it as the sandbox base (OCI import is supported) |
| Ultra slow, rate-limited or short on context | S5 latency or limit problems | Chunked prompts, Super for the first draft, Ultra only for adjudication; cache everything |
| Credits run short | Spend after M0 projects past your budget | Lower repeats, Nano wherever its accuracy holds, test set run twice only |
| Baseline harness won't run | S7 fails | The \~50-line custom environment adapter |
| GapFinder gives confident wrong answers | False-attribution rate on dev tasks above 10% | Tighten the verification step; never relax the labels to make results look better |
| A rival ships something close | A search of Devpost and GitHub at every milestone gate for "reproduction" and "artifact evaluation" | Lead with the evidence: planted-task scores, verification, author contact |
| Demo site fails during judging | Daily health check alerts | Replay is static and keeps working; README has a GIF and the Markdown report |

**Scope:**

| Priority | Items |
| --- | --- |
| Must | Claim ledger (text and figures, for RusKey); checkpoint tree with depth planner; fan-out; noise calibration; screen, confirm and bisect; held-out and counterfactual checks; Gap Report; replay UI; GapBench-mini with at least 8 tasks; mini-swe-agent baseline; no-fork ablation; video; README |
| Should | Combine round; plausibility gate with Tavily evidence; live mode; Ultra baseline arm; no-verification ablation; email to the RusKey authors |
| Could | Importing the authors' own Docker images; a mode for artifact-evaluation committees; more paper types |

**Cut lines, decided now:**

- **M2 can't pass its gate with everything in scope:** drop live mode (replay only) and the Ultra baseline arm, then re-run the gate.
- **M3 can't pass its gate:** drop the combine round and Tavily; keep screen, confirm and bisect on single knobs.
- **M4 can't pass its gate:** shrink the test set to 6 tasks and the baseline to 3 runs per task. Never cut the baseline itself or the no-fork ablation; they carry the argument.
- **M5 can't pass its gate:** ship the report page and the replayed tree only; the comparison page becomes a README table.

## Milestone gates

Completion is tracked by gates, not dates: a milestone is done when its exit gate passes, and the next one starts then.

&#91;embedded content: milestone gates · 7 milestones, M1 and M2 in parallel\]

M1 and M2 don't depend on each other (M2 can start from a hand-written knob list), so they can be built side by side; every other milestone waits for the gate above it.
