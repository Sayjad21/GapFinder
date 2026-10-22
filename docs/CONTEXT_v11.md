# GapFinder: current context (2026-10-22)

The one current document: what GapFinder is, the rules, what it can do, where the harness stands, every real
result, and the bottlenecks still in the way of generalising. The step-by-step history is in git and in
`docs/learn/07_the_journey.md`. Paths are relative to the repo root (github.com/Sayjad21/GapFinder).

---

## 1. What GapFinder is

Given a paper and its code, GapFinder explains why running the code doesn't give the paper's numbers.
1. **Read:** Nemotron reads the paper and lists its claims and the settings they may depend on.
2. **Search:** it runs the code many times in Token Factory Sandboxes, forking from saved checkpoints.
3. **Verify:** it checks the best candidate three ways:
   - undoing the change must bring the gap back;
   - the other reported numbers must not get worse;
   - the value needs evidence.
4. **Report:** a Gap Report per claim, with a label, the evidence and replayable runs, plus an audit of what a
   matching number doesn't show.

**Labels:**
- confident: **Explained**, **Paper-artifact inconsistency**;
- cautious: **Partially explained**, **Fits but unsupported**, **Explains target, conflicts with held-out**;
- no answer: **Inconclusive**, **Unexplained**, **Reproduced**.

**The goal (the owner's):** give it any paper, and optionally the user's own reproduction, and it finds the actual
cause. Never lying is necessary but not enough.

---

## 2. Rules

### 2.1 No patching (set by the owner for the lifetime of the project; also in the local, git-ignored project instructions)

- **No engine change to make a specific paper or task pass.**
- **A change is allowed only if:**
  - it fixes a failure *class* seen on **at least two different papers**; or
  - it adds a capability that **published work** shows generalises.
- **Plumbing and measurement infrastructure are allowed.**
- **Never judge a change on the case that revealed it.** Post-hoc reruns count as nothing.
- **Progress is a rate on fresh, sealed, frozen papers.**
- **No tuning of tie-break or selection rules on GapBench or dev-set cases.**

### 2.2 Evaluation protocol (`eval/external/BLIND_CASE.md`)

1. An independent sealer (another agent with no part in GapFinder) picks the paper and writes a private answer key
   with a pre-registered scoring rule. Only its hash and a neutral `case.md` are published.
2. GapFinder is frozen: a git tag, a worktree, `python -P` and the worktree's own `.env`.
3. The harness is built from the paper and the repo only.
4. The run is committed **before** the key is opened.
5. The key's hash is checked, then the run is scored.

### 2.3 Constraints

- **Sandboxes only** (the owner's decision; never local Docker):
  - 4 vCPUs, 3.9 GB RAM, no swap, CPU only;
  - **at most 3600 s per operation**, a platform limit: a longer timeout is rejected;
  - a VM slows to about one CPU when many searches run at once.
- **Money:**
  - billed **$31.69** of the owner's ~$50 (Nemotron only); `GF_SPEND_CAP_USD=33`;
  - a ledger costs about $0.1-0.3;
  - Sandboxes are unbilled in the Beta (they report a diagnostic cost), and the guard `GF_SANDBOX_GUARD_USD` is
    raised for searches;
  - every checkout writes to the main spend ledger.
- **Commits:** no AI attribution. "Write it down" means document only.
- **Never open sealed keys before the run is committed.** Never give `eval/external/devset/CANDIDATES.md` (answers)
  to a harness writer.

---

## 3. What runs, in order

| Step | Module | What it does |
|---|---|---|
| Ledger | `gapfinder/ledger/` | Claims with exact quotes (Ultra, filtered by Super), and assumptions per setting. A stated paper number must be in a verbatim quote. The appendix gets its own call. Hyperparameter tables from anywhere in the paper are included. Flag help text is shown, so a paper's symbols map to flags. |
| Repo map | `gapfinder/ingest/repo_map.py` | Flags, defaults and help text: argparse, gflags, absl / tf.app.flags. A flag declared twice is listed twice; a commented-out block is kept as an alternative. |
| Name mapping | `engine._map_names`, `knob_family` | Ledger names to knobs: exact or core words; by meaning (one Super call, existing names only); one flag split into several knobs (`--lr` → `gat_lr`, `gcn_lr`). |
| Runtime trace | `gapfinder/sandbox/trace_hook.py`, `search/trace.py` | One dry run records where values land: optimizer, dropout, batch size, width, loops, seeds. Each knob gets a role and role-based candidate values. The hook chains to the environment's own sitecustomize. |
| Candidate values | `search/hypotheses.py` | By role, by choices (categorical knobs' other choices), a coarse-first ladder, multipliers, edge values. True/false literals flip. |
| Search | `search/engine.py` | Screen, then confirm. The confirmation race takes at most a quarter of the budget (successive halving). Then combine: the repo's alternative settings blocks first, pairs, a forward step and early confirmation. Then bisect and verify. A secant step runs only when nothing fits every claim. A fallback round covers knobs no assumption names. |
| Verification | `search/verify.py` | Counterfactual; held-out claims (tuned-separately ones are notes, not vetoes); relation claims; evidence (paper, docs or web; code alone doesn't count). |
| Confidence cap | `engine._cap_confidence` | A confident label needs a finished search, every knob screened, and evidence beyond source code. A stated value that was run and doesn't fit is said in the notes. |
| History matching | `search/history.py` | Every configuration against every claim. The discrepancy allowance comes from the spec, 0.01 at full scale. |
| Code causes | `ingest/code_checks.py`, `sandbox/ast_patch.py`, `search/contrast.py`, `search/matcher.py` | **Static leads:** literals, unoverridden defaults, switches, seeds, splits, selection loops, label-based edits, evaluation switches. **Contrast:** one Super call matching paper to trace. **Constant matcher:** $0, deterministic. **Patch round:** literals, defaults, switches and `@if` conditions changed in memory; no file edited. |
| Protocol tests | `engine._protocol_tests` | Test-score selection, label-based score edits (point adjustment) and evaluation switches (`drop_last`) are switched off and measured, whatever the label. |
| Audit | `search/audit.py` | In every report: protocol findings; the paper's own comparisons checked against the runs ("improves upon GCN by 1.6%": measured -0.3, reversed); held-out misses; paper-stated settings the harness can't vary. |
| Long cells | `sandbox/runner.py` (`run.shards`, `run.segments`) | Past the 3600 s cap: independent jobs in parallel VMs with their outputs joined, or resumable training in pieces from checkpoints. |
| Your code vs the authors' | `search/difftrace.py`, `gapfinder diff` | Both programs traced. Each value that reaches the same library call differently becomes a hypothesis, tested against the authors' measured numbers. |
| Environment | `gapfinder/env_build.py`, `gapfinder env-build` | Repo2Run-style: one install command at a time in Sandboxes, with free rollback. The model may switch images and use apt-get. The goal is that the README's own command runs for 5 minutes. |
| Report and app | `gapfinder/report/`, `gapfinder/api/`, `web/` | Markdown/JSON reports; a replay-only web app. |

---

## 4. Where the harness stands (the biggest blocker to "any paper")

### 4.1 What the finished harness should be

An agent writes it (Nemotron, in the product), but **the agent only proposes, plain code checks every step, and the
agent has no say in what the search tests.**
- Inputs: the paper and the repo (and the user's own code, if any).
- Outputs: a frozen spec, the image checkpoint, and HARNESS.md recording every choice and its reason.

| # | Step | The agent proposes | Plain code checks it | Status today |
|---|---|---|---|---|
| 1 | Environment | install commands, one at a time | each runs in a Sandbox; a failure rolls back; done when the README's command starts | ✅ built (`env-build`) |
| 2 | Data | how to get it (README, scripts, loaders) | the files exist after the step; sizes and checksums recorded; the same on rebuild | ❌ by hand |
| 3 | Which command makes which number | the command for the target table cell | it runs and prints a value with the claim's metric and unit, of plausible size | ❌ by hand |
| 4 | Metric parser | how to read the numbers | every parsed number appears verbatim in the log; one name per claim | ⚠️ half (`spec-draft`) |
| 5 | Knobs | nothing: mechanical | every flag the command passes or the code reads, at its default; the trace confirms each reaches the code | ✅ mostly |
| 6 | Fit the Sandbox | nothing: a fixed rule | shards or segments first; if it still doesn't fit, halve the scale until it fits, and record a discrepancy allowance | ⚠️ the rule exists; not applied automatically |
| 7 | Self-checks | nothing | seeds vary, memory and time fit, every claim is printed | ✅ (`spec-draft --self-check`) |
| 8 | Claims | the target plus held-outs, from the ledger | at least 2 claims; "tuned separately" only from a quoted sentence | ⚠️ the ledger exists; selection by hand |
| 9 | Human approval | nothing | a person reads HARNESS.md and approves the commands (about 5 minutes; never the knobs) | — |

**Why an agent doesn't bias it:**
- the harness agent never sees causes or search results;
- the choices that could steer the answer (knobs, defaults, scaling) are rules, not judgment;
- the harness is frozen before the search starts.

**When the user brings their own code:** their script *is* the harness. Only steps 3-4 are needed, and
`gapfinder diff` compares it with the authors' code.

### 4.2 Measured reality

**Environment builder:**

| Repos | Imports load | Experiment runs |
|---|---|---|
| Dev set (7) | — | 1/7 (first version) |
| devbatch-2 (3 unseen) | 3/3 | 1/3 (NCF: Python 2 code; Anomaly Transformer: `.cuda()` and memory) |
| batch-3 (2 unseen) | — | 1/2 (Fair Clustering failed on an unbuildable `matplotlib==3.0` pin) |
| batch-4 (1 unseen) | yes | the environment worked, but the README goal parsed as invalid bash (fixed) |

- Overall, the experiment ran unaided on about 2 of the last 6 unseen repos.
- **Every harness since devbatch-1 needed a person or agent** for the data, the table-cell command, the parser,
  the claim selection and the scaling. In batch-3 and batch-4 the runner (who knows what kinds of causes are being
  hunted) wrote them. That is the bias risk the design above removes.
- **`gapfinder harness` (2026-10-20), steps 2-8 automatic.** On RippleNet (batch-4, already revealed), from its
  built environment and the case's two Table 3 claims, with no model call: the same command, the same 9 knobs at
  the same defaults, the same exclusions (`--dataset`; `--using_all_hops`, `type=bool`), the dataset switched from
  movie to book, the preprocessing step found, and the same binding (final-epoch test AUC and ACC). Naive AUC
  0.64-0.66 against the paper's 0.729, the gap the hand harness measured. 5 runs fit one operation as is (306 s).
  Not yet run end to end on an unseen repo (env-build included).

---

## 5. Results

### 5.1 Sealed blind real papers (the only clean evidence)

| Paper | Code | Documented cause | GapFinder | Score |
|---|---|---|---|---|
| FastGCN (blind-1) | v1.3 | lr 0.001 | Fits but unsupported, lr=0.005 | missed |
| GraphMAE (blind-2) | v1.4 | `alpha_l=1` (appendix table) | Explained, mask_rate=0.5 | **confidently wrong** (before the confidence cap) |
| **Variational Fair Clustering** (batch-3) | `92b1faa` | the paper's λ=10 is wrong; the authors' value is 100 | **λ=100**, all four K-means claims exact | **correct** (labelled Fits but unsupported) |
| SparseTSF (batch-3) | `92b1faa` | `drop_last=True` in the test loader | Reproduced (-0.4%) | missed (correct abstention) |
| **RippleNet** (batch-4) | `bae25f4` | README runs MovieLens settings; needs lr 1e-3 and l2_weight 1e-5 | **lr=0.001**; l2 missed (budget) | **partial** |
| GCN topology attack (b5a, batch-5) | `0586e5c` | the attack budget counts each edge twice (`--perturb_ratio` at half) | Fits but unsupported, dropout=0.5 (the true value was a lead) | missed |
| SDCN (b5b, batch-5) | `74b1fd1`, `e925a0f` | the paper reports the best epoch by the labels | Unexplained, out of space | missed |
| BOND / DOMINANT (b5c, batch-5) | `74b1fd1`, `e925a0f` | PyGOD API drift: the auto-balanced `alpha` silently dropped | Unexplained, out of space | missed |

**1 correct, 1 partial, 5 missed, 1 confidently wrong** (8 papers). Nothing has been confidently wrong since the
confidence cap went in. Batch-5 (the first blind cases with the automatic harness) found none of 3; each miss is a
different class whose answer was already in the run's data (eval/external/batch5/RESULT.md).

### 5.2 Frozen dev batches (known causes, not shown to the harness writers)

- **devbatch-1** (5 papers): 1 correct (G-Mixup: the gain is noise), 0 confidently wrong.
  - GIN: the README already contained the fix.
  - GAT: names didn't map.
  - Informer: only 28 runs fit the time.
  - PatchTST: `drop_last`, a switch.
- **devbatch-2** (NCF, PyG GAT vs GCN, Anomaly Transformer): 0 causes found, 3 correct abstentions, 0 wrong.
  - All three reproduced: the causes are protocol and noise flaws inside the paper's own number.
  - Post-hoc, the current audit names NCF's test-set selection, shows PyG's reversed CiteSeer comparison, and
    quotes Anomaly Transformer's adjustment. These don't count.

### 5.3 Planted causes in real repos (`eval/planted/`; measurement only)

| Harness | Claims | Correct | Confidently wrong |
|---|---|---|---|
| pygcn | 1 | 3/11 | 0 |
| Fair Clustering + SparseTSF | 8 each | 6/8 | 0 |

- Both multi-claim misses were `loss=mae`, which never ran: categorical choices weren't candidates. Fixed.
- **Several claims per paper matter:** one number leaves most planted causes unidentifiable.
- The larger, graded run of 2026-10-22 (six papers, every family, 41 tasks) is section 5.6.

### 5.4 Synthetic benchmark (GapBench)

- Sealed v1.1-v1.3: 0/90 confidently wrong; a coding-agent baseline was confidently wrong in 49 of 90.
- Dev suite: 53/69 cause runs correct at `bc1814a` (51 before), 0 confidently wrong.
- It guards against regressions; it doesn't reflect real-paper problems.

### 5.5 Latest successes and failures (what to build on, what to fix)

**Worked:**
- First sealed blind cause found (λ=100, Fair Clustering), with the exact corrected value.
- The right learning rate on RippleNet (0.001).
- No confidently wrong answer in 17 real-paper results since the cap.
- 6/8 planted causes on multi-claim repos.
- `env-build` with image switching, apt-get and a real goal.
- Protocol tests and the audit name flaws post-hoc, on papers where they were invisible before.

**Failed:**
- SparseTSF: a reproduced target means the evaluation switch is never tested (now protocol-tested; unmeasured).
- RippleNet's l2_weight:
  - confirmation ate the budget (capped now);
  - the λ1 symbol wasn't linked to its flag (help text now shown);
  - the answer sat in a commented-out block (now tried as one configuration).
- Fair Clustering's label: right value, cautious label.
- Harnesses: still hand-built (section 4).
- Sealers: about one usable paper per 3 hours. Most documented flaws live in papers whose code already reproduces
  them.

None of the fixes listed above is measured on a fresh paper yet.

### 5.6 Planted-gap curriculum on reproduced papers (2026-10-21/22; development measurement)

The owner's question: which kinds of gaps does GapFinder find, beyond settings? Gaps were planted into papers it
already reproduces, graded from easy to hard, and searched for by a frozen engine. The summary and per-task tables
are in `eval/results/planted_curriculum*.md`, and the failure classes are section 7.4.

**How the tests were run**

- **Papers:** six whose code reproduces, with their hand harnesses (claims per task in brackets): pygcn (1), FastGCN
  (4), Variational Fair Clustering b3a (8), SparseTSF b3c (8), RippleNet b4a (2), VGAE (8).
  - Each was also rebuilt by `gapfinder harness` (`eval/planted/rebuild_harnesses.py`, cases named `<case>-h`).
    The rebuilt spec has per-epoch values, the paper-year packages and the paper-era commit, which the reporting,
    library and era families need.
  - b3a's rebuild could not bind its printed objective to the claim.
  - pygcn's paper-year pins can't install, because 2016's compiled packages have no wheels for Python 3.10.
- **Generator** (`eval/planted/curriculum.py make`, seeded):
  - Each draw picks a family, then a change applied as hidden knob values or as an in-memory code edit; no file is
    changed.
  - The "paper's numbers" are the mean of 3 runs with the change (2 when the target is deterministic). The
    reproduction runs without it.
  - Families:
    - **setting:** a flag or a literal constant at another value (x0.25 to x10, or another choice);
    - **scale convention:** "the paper's v is the code's c x v", with a two-point sweep as held-out claims;
    - **code defect:** a mutation-operator edit (x2, /2, mean <-> sum, a constant);
    - **data pipeline:** a data-loading or split edit;
    - on the `-h` harnesses only: **reporting** (the best epoch, chosen on the test labels), **paper-era code**,
      and **a package release from the paper's date**.
- **Levels, by measured effect:**
  - L1: at least 5 pooled sd, and more than 0.5% of the value.
  - L2: 3 to 5 sd.
  - L3: two causes of one family.
  - L4: two causes of different families.
  - L5: a cause outside every family (a string choice such as `relu` -> `tanh`), alone or with a setting.
  - A single-cause draw is measured once and banked at L1 or L2 by its effect, so no measured draw is wasted.
- **Controls:** nothing planted, and the "paper" is another batch of the same runs. About one task in five on seed
  2, none on seed 3.
- **Guards:**
  - A run is cut at 5x the slowest baseline run.
  - A draw lost to Sandboxes or the network is drawn again, not counted.
  - The maker's log never says what a task is.
  - Answers are sealed in `eval/planted/curriculum/sealed/` and read only by `score`.
- **Search:**
  - The frozen engine runs from its own worktree (`planted-c1` at `../gf-c1`, `python -P`).
  - It runs `gapfinder search --hypotheses repomap`: no paper, no ledger, no model call.
  - Each task gets 150 runs, in Sandboxes.
  - A search cut off by the machine resumes from its earlier runs (`--resume` on `run.cut*`).
- **Scoring** (`curriculum.py score`):
  - **Correct:** every planted part is found, with a label other than Unexplained, Inconclusive or Reproduced.
    A setting part counts when its knob is in the answer at the planted value within 10%, or the value is in
    GapFinder's set of equally good values. A code part counts when its edit is in the answer, or is named with its
    site as a code change.
  - **Partial:** some parts found. **Missed:** none found.
  - **Confidently wrong:** a confident label without the planted cause; on a control, any confident label.
  - Reported beside the verdict:
    - "right knob": the answer changes the planted knob, at another value;
    - "tied": the planted knob is among the configurations the report says the target can't tell apart from its
      answer.
- **Gate:** a level opens only when the previous one reaches 70% of its gap tasks correct, with nothing confidently
  wrong.
- **Batches:**
  - Seed 2: 14 gap tasks and 11 controls.
  - Seed 3: 16 gap tasks and no controls, made after c2 was frozen and searched by both c1 and c2 (c2 into
    `run-c2/`, with `GF_CURRICULUM_RUN=run-c2`).
  - Both seeds' answers are now public, so they are dev data.

**Results, c1 (seeds 2 and 3, 30 gap tasks and 11 controls)**

| Family | Level 1 | Level 2 |
|---|---|---|
| Scale or unit convention | 4 of 4 | 2 of 3 |
| Setting | 0 of 9 | 2 of 9 |
| Code defect | 0 of 3 | 0 of 2 |
| Reporting rule, paper-era code, package release | none plantable | none plantable |
| **All** | **4 of 16** | **4 of 14** |

- **0 confidently wrong:** none of the 30 gap tasks, and none of the 11 controls (all reported as reproduced).
  Every miss carried an unconfident label.
- **Per seed:** seed 2 had L1 1 of 7 and L2 3 of 7; seed 3 had L1 3 of 9 and L2 1 of 7.
- **The gate was not passed:** level 1 got 25% against 70%. Levels 3 to 5 were not run.
- **Scale conventions are found:** the scale probe names the knob and the factor, labelled Paper-artifact
  inconsistency.
- **Settings miss narrowly:** 10 of the 16 setting misses name the planted knob at another value (6), or have it
  among the tied configurations (7).
- **A code round was cut by the run budget in 19 of the 30 searches:** the patch round in 14, the mutation round
  in 5.
- **The reporting, era and library families couldn't be tested:** on the five rebuilt harnesses, no draw from them
  moved a target by 3 sd. The rebuilt harnesses gave only controls.

**c2 against c1 on the fresh batch (seed 3)**

c2 (tag `planted-c2`, `ca4a5e2`) added `code_hold`:
- When the code has leads, the patch round's share and the mutation round's minimum are kept out of the settings
  exploration.
- An unsupported fit also opens the mutation round, and a fitting mutant is then reported as an alternative,
  not as the answer.

| | c1 | c2 |
|---|---|---|
| Seed 3, level 1 | 3 of 9 | 6 of 9 |
| Seed 3, level 2 | 1 of 7 | 1 of 7 |
| Seed 3, code-defect tasks | 0 of 3 | 0 of 3 |
| Dev suite cause runs (c1 = run 5000, c2 = run 6000) | 52 of 69 | 48 of 69 |
| Confidently wrong, either measure | 0 | 0 |

- **By task:** on seed 3, c2 is better on 4 and worse on 1 (sign test p = 0.38). On the dev suite it is better on
  2 and worse on 6 (p = 0.29).
- **Every gain was a setting task.** One of them (pygcn, `lr=0.0025`) was a pick among tied configurations. Code
  defects stayed at 0 of 3.
- **The rounds now ran, but missed the planted sites:** VGAE's mutation round tested 22 mutants, none at the planted
  site (7.4, E2).
- **Not adopted:** `code_hold` is off by default (`d2a4ca0`); the code and its toy test stay.

---

## 6. Remaining bottlenecks (2026-10-20, after batch-5; ordered by impact on finding the cause)

The planted curriculum of 2026-10-22 (5.6) measured 6.1, 6.2 and 6.5 directly on six reproduced papers. Its failure
classes, E1-E7, are the current work list (7.4).

Evidence base: 8 sealed blind papers. Causes that are settings: 4 (1 correct, 1 partial, 1 close miss, 1 wrong
before the cap). Causes that are code, evaluation or library: 4 (none found). In all three batch-5 misses the
information that answers the case was already in data GapFinder had collected.

### 6.1 The hypothesis space is settings only
- GapFinder searches flags, config values, literal constants and a few switches.
- Missed classes: evaluation and reporting choices (b5b: the paper reports the best epoch chosen with the labels),
  code defects (b5a: edges counted twice), library API drift (b5c: a renamed parameter silently dropped), data
  pipeline switches (SparseTSF: `drop_last`).

### 6.2 Equally good fits: it picks the wrong one
- FastGCN (lr 0.005 against 0.001), GraphMAE (a wrong setting), b5a (a decoy that hit the number exactly, among 14
  fits). Ties are broken on the target alone; deterministic programs make the noise band the floor.

### 6.3 Paper reading is unreliable
- Claims dropped as ungrounded: 57 of 67 (b5a), 48 of 95 (b5b), 24 of 58 (b5c). Missing table cells (RippleNet's
  Table 3); garbled conditions (RippleNet's Tables 4-5). Claims for batch-5 had to come from the sealer's case.md.

### 6.4 Paper terms are not linked to code by meaning
- λ1 against `--l2_weight` (RippleNet), "% perturbed edges" against `--perturb_ratio` (b5a): name matching only.

### 6.5 Only simple code changes can be tested
- Literal swaps and a few operation swaps. Not: loop bounds (`range(200)`), structure (early stopping, averaging),
  arithmetic (`x / 2`), keyword routing.

### 6.6 The harness needs a person on harder repos
- Two-command experiments (b5a), ambiguous printed lines (b5b), command choice (b5c), memory-heavy parallel copies,
  scripts whose settings live in code (b5c); env-build gave up wrongly (no CPU shim in its own steps) and reported the
  wrong checkpoint on failure; the default CPU-time limit (300 s) killed long runs.

### 6.7 Evaluation size and 6.8 machine and budget
- Owned by the project owner (2026-10-20): more sealed papers and more budget.

---

## 7. Work plans (status kept up to date here)

7.1 and 7.2: the plan of 2026-10-19 (done). 7.3: the plan of 2026-10-20.

From the owner's 10-bottleneck plan, after a web check. Each item names its bottleneck (section 6) and why it is
allowed under the no-patching rule: a recurring class, a published method, or plumbing/measurement.

### 7.1 To do

| # | Item | Bottleneck | Allowed as | Status |
|---|---|---|---|---|
| 1 | **A pool of 20+ cases mined from fix commits.** GitHub search for "match the paper", "fix default", "wrong hyperparameter", "reproduce table". The parent commit is the blind input and the fix diff is the sealed answer, written by the script; the runner never reads it. A case is kept only if the numbers differ beyond noise between the parent and the fix. Each case is tagged by cause type, and rates are reported per type. | 6.1 | measurement (commit mining is an established method, e.g. BugHunter) | ⏳ miner built (`eval/pool/mine.py`): 33 sealed candidates, about 1 in 60 search hits. Free check (`eval/pool/verify.py --dry`): 15 ready, 10 with no experiment command, 7 blocked (GPU-only requirements, CUDA extensions), 1 unfetchable. Gap check run on 4 ($0.07): 0 runnable (a CUDA extension, now caught statically; a git submodule, now fetched; data not public; env-build failed after 8 commands). The mined repos are mostly 2025-26 GPU projects: the miner needs a CPU-feasibility filter before more is spent |
| 2 | **Read the arXiv `.tex` source** when available (about 93% of arXiv papers): symbols and tables as plain text; pgfplots coordinates and bundled csv files as figure data | 6.6, 6.4 | recurring class (symbols: RippleNet; tables: GraphMAE) | ✅ `ingest/arxiv_source.py`; RippleNet's table now reads `$\lambda_1 = 10^{-5}$` |
| 3 | **Command picker:** match the claim's dataset and model names against the arguments of README and shell commands; propose a script when one claim needs several commands | 6.2 | plumbing | ✅ `harness_auto.pick_commands` (a `cd` line carried down to the commands under it; data-preparation scripts never picked as the experiment); in `gapfinder harness` |
| 4 | **Run the repo's download scripts** in env-build (`download*.sh`, `get_data*`), and record sizes and checksums | 6.2 | plumbing | ✅ `download_steps` and the preprocessing commands written before the picked one: in env-build's goal, then run again for the base checkpoint |
| 5 | **Metric binder.** Prefers test over val and final over best; refuses when ambiguous; keeps alternatives as extra metrics | 6.2 | plumbing | ✅ `bind_metrics`; the emitter in the VM (`gf_harness/emit.py`) reads the same labels, alternatives as extra metrics |
| 6 | **Fixed shrink rule:** shards and segments first; shrink only if a run won't fit; record a discrepancy allowance | 6.2, 6.5 | plumbing | ✅ `shrink_plan`, applied by `gapfinder harness`: in-VM parallel runs, else shards (`run.shard_mean`), else halve the epochs with a 5% allowance |
| 7 | **Loader caches** for common datasets (PyG, torchvision, sklearn; they check hashes). Not a generic `/data` symlink | 6.2 | plumbing | ✅ in `gapfinder harness`: new files under data directories and loader caches stay in the base checkpoint; outputs, logs and model files are deleted; sizes and sha256 recorded in HARNESS.md |
| 8 | **Built-in CPU shim** (`cuda.is_available` False, `torch.load` to CPU) and allocator and thread settings in every run; `num_workers=0` only after an out-of-memory failure | 6.5 | recurring class (hand-built for Anomaly Transformer and SparseTSF) | ✅ `sandbox/runtime_shim.py`, every run (and env-build's goal) |
| 9 | **Static GPU/size filter** before spending on a ledger | 6.5, 6.10 | plumbing | ✅ `compute_blockers`, step 0 of `gapfinder harness` |
| 10 | **Static leakage analysis** after Yang et al. (ASE 2022): test data reaching fitting or preprocessing; feeds the audit and the protocol tests | 6.7 | published method | ✅ `code_checks._leakage_leads` (family `preprocessing_leakage`), in the audit |
| 11 | **Label "Paper's stated value refuted; unique fit"** when all hold: the stated value was run and fails; every claim fits (at least 2); the counterfactual holds; one island; every knob screened. Must not fire on GraphMAE-like cases; regression-checked | 6.8 | recurring class (cautious labels on right answers) | ✅ c1268b5. Dev suite run 4000 against 3900: 50/69 against 53/69 cause runs correct (sign test p = 0.73), 0 confidently wrong; the label did not fire there |
| 12 | **Conservative significance:** the larger of the baseline and candidate spread | 6.9 | recurring class (config-dependent noise) | ✅ c1268b5 (same regression run) |
| 13 | **Split variance in calibration,** only through the repo's own split or fold flag | 6.9 | published (Bouthillier et al.) | ✅ c1268b5; fixed after run 4000: a bare `--split` (a fraction) was taken for a seed and the split runs became candidates. Now seed or index names only, and the runs are kept out of the candidates |
| 14 | **Claims at fixed knob values** (sensitivity-plot points); each candidate is also run at those values | 6.4 | recurring class (identifiability) | ✅ `Target.at`: checked in verification like a held-out; optional per configuration in history matching; an answer they rule out is swapped for a tested configuration that fits every claim. `gapfinder harness` finds them in the ledger when the setting's name maps to a knob, and lists the rest for a person |
| 15 | **Learning-curve points as claims,** only when the paper reports the curve and the code logs test metrics per epoch | 6.4 | recurring class | ✅ an `epoch` condition becomes a per-epoch metric read from the same run (no extra runs), kept only when the smoke log prints that epoch |
| 16 | **Super for claim extraction, Ultra only for assumptions;** section slicing as an option, measured for recall | 6.10 | budget | ❌ measured (`eval/claims_tier.py`), not adopted: Super found 27 of Ultra's 61 numeric claims on b3a (44%; it dropped whole baseline rows and Table 3 cells) and returned nothing on a longer paper (reasoning used the 32k output limit). Ultra stays; `--claims-tier super` exists. Section slicing not tried |
| 17 | **Grounded preprocessing and operation swaps,** only when the paper states the other choice (through the contrast step or the matcher) | 6.3 | grounded extension of the patch round | ✅ `search/op_swaps.py`: seven families of drop-in replacements (activations, pooling, 2-D pooling, scalers, optimisers, initialisers, regression losses); a file-wide `@call.` patch or a keyword string; patch round only, the paper's choice only |
| 18 | **"As in [X]":** the cited paper's arXiv source, its setup section | 6.6 | published (AutoReproduce's paper lineage) | ✅ `arxiv_source.cited_setups`: sentences that defer the setup to a citation; the arXiv id from the .bbl/.bib or an exact-title search; the cited paper's setup sections appended to the supplement |
| 19 | **Paper-year dependency environment** as one knob | 6.3 | documented class (dependency drift) | ✅ `env_year.py`; `gapfinder harness --arxiv/--paper-date` adds knob `gf_paper_year_env` (imported packages at the paper's month, `pip --target`, no dependencies), dropped if the old set doesn't import |

### 7.2 Discarded, and why

| Idea | Why |
|---|---|
| Generic preprocessing knobs (normalisation, clipping, split type) | Untargeted changes manufacture fits that look like answers (the secant step's measured harm) |
| Canary half-test (for now) | Its preconditions fail on most repos (exact determinism, a data hook, weight access); item 10 covers the main cases |
| Best-of-N as a reported flaw | It can't tell a best seed from a real cause; at most a note when nothing else fits |
| Merging the ledger calls into one | Brings back the appendix miss (SA-Bench; GraphMAE) |
| Symlinking datasets everywhere | A wrong-format copy silently creates a new gap |
| Patching `train_test_split` for split noise | It changes the experiment being measured |
| A penalty on configurations whose spread grows | Measured harmful: the true cause often raises the spread too |
| Curve extraction from vector PDFs (for now) | No validated accuracy; arXiv source covers about 93% of papers |
| Reproducibility-challenge reports as the main source | Measured near-zero yield; secondary only |

### 7.3 Plan of 2026-10-20: bottlenecks 6.1-6.6 (status kept here)

Rules for every item:
- **Allowed as:** a published method or a class seen on two or more papers (2.1).
- **Acceptance test:** a new instance of the class (a toy or a planted case), never the batch-5 case that revealed it.
- **Regression check:** the dev suite (69 cases, $0) shows no loss and still 0 confidently wrong.
- **Progress:** measured only on fresh sealed papers.

Ordered by dependency; each line is one commit or more.

#### D1. A differential diagnosis over cause classes (6.1)

The baseline from the sources:
- the irreproducibility taxonomies (Gundersen & Kirkpatrick 2022; Liao et al. 2021);
- sequential diagnosis that orders tests by value of information (MAI-DxO 2025; Singh et al. 2025).

Beyond them: explicit Bayesian bookkeeping over measured likelihoods instead of an LLM panel; a cost per test; an
"outside every class" hypothesis that keeps prior mass (the honest label); an adversarial step that searches for the
best rival before any confident label.

| ID | Item | Design | Acceptance | Status |
|---|---|---|---|---|
| D1.1 | Diagnosis core | `gapfinder/diagnose/`: hypotheses (class, changes or transform, prior, evidence, posterior); probes per class (applicability, cost, likelihood from all claims with a model-discrepancy term); a scheduler by expected information per cost, batched for parallel Sandboxes, adaptive stop; the settings search becomes one probe family; the report becomes a ranked differential (top 3, evidence, how to check) | a toy where the true cause is in each class in turn, with decoys in the others: the true class ranked first, and in the top 3 on every toy | ✅ 158e474 (`gapfinder/diagnose/core.py`; mutual information per cost for the next test) |
| D1.2 | Reporting probes, zero runs | the emitter reports, per claim and run, the final, best (by direction), best-by-validation, last-k mean and argbest epoch; across runs the mean, median and max-of-N with order-statistics likelihoods ("Show your work", Dodge et al. 2019). Hypotheses: best epoch chosen with the test labels (a flaw), best-by-validation (a protocol difference), best of N seeds, another aggregate | toys for each, including a legitimate early-stopping one that must not be called a flaw | ✅ 158e474 (`diagnose/reporting.py`; emitter trajectory statistics) |
| D1.3 | Library drift: time-travel environment | the paper-date environment resolved by the resolver itself (`uv pip install --exclude-newer <date>`), including the repository's own package when it is on PyPI, in a separate target, one knob | a toy package with two releases whose default changes | ✅ 19b2039 Built as per-package directories, not one resolver-made target: each import's newest release before the paper's date (PyPI upload dates, the VM's Python), the repo's own package from setup.py/pyproject, torch from the CPU index, wheels over 400 MB left out; then a date-bounded resolution of only the conflicting part (each old release's own `requires_dist`; the installed compiled stack kept unless excluded) instead of `uv --exclude-newer` on everything, which reinstalls torch and numpy into the target and leaves no way to switch one package. Switched by an import redirect in the runtime shim (`GF_LIB_DIRS`), so an old release wins even over a package beside the script. Knob values: `0`, `all`, any comma list, `dist==version` on demand. Tests: `tests/unit/test_library.py`, `tests/integration/test_harness_paper_year.py` (a repo that is its own package) |
| D1.4 | Library drift: which package, which release | delta debugging (ddmin) over the packages whose versions differ, then binary search over that package's releases between the paper's and the installed | a toy with two drifting packages, one of them a decoy | ✅ 19b2039 `gapfinder/diagnose/library.py`: ddmin with each round in parallel and known outcomes reused (the screen's single-package runs cost nothing extra); a package travels with the dependencies it brought; binary search over releases with a sequential same-numbers test on every claim (another run only when borderline), up to two change points. Before the settings search, so a release-localised effect is evidence for the knob (the paper predates the release that changed the numbers). Toys: the culprit found and the decoy cleared; no drift, no probe; a drift that is not the cause, where the answer stays the setting |
| D1.5 | Library drift: which parameter | at every call site the entry closure executes, the callee's signature under both releases (imported in the VM): removed or renamed parameters, changed defaults, keywords that land in `**kwargs` and are never read (a runtime check that records reads) | a toy with a renamed keyword swallowed by `**kwargs`, and one with a changed default | ✅ 19b2039 Call sites from each file's import map and instances of the package's classes; in the VM, both releases' signatures and source, the package functions they call and their base classes' `__init__`. Leads: a keyword that lands in `**kwargs` and is never read (string reads checked, forwarding to a base class followed), its likely new name (default, name similarity, position), changed defaults the call doesn't pass, moved positional parameters, changed source with a diff. Each signature lead becomes an in-memory edit (`kw.OLD.NEW`, new `kwset.NAME.VALUE`) run on the newer release; one that gives the older release's numbers is reported verified at that line. Toy: alpha renamed to weight in 0.5.0, found at the release and the line, verified, labelled Explained |
| D1.6 | Data-pipeline probes | mutation operators tagged "data": `drop_last`, `shuffle`, split fractions, normalisation fit on train versus all, filtering thresholds; existing leakage checks feed priors | a toy whose test loader drops the last batch | ✅ 19b2039 Mutants tagged "data pipeline": loader switches also where the call leaves them at the default (`drop_last`, `shuffle` on training loaders); split fractions in keywords, parameter defaults and `0.8 * len(x)` (the complement first, then the common fractions); what a scaler, normaliser or encoder is fit on, both ways; filter thresholds in data code, subscripts and keywords like `min_count` (odd counts never halved); lines a static check flagged (split fractions, evaluation switches, selection on test data) first. Toys: a test loader whose missing `drop_last` explains the gap; a scaler fit on everything where the paper fit on the train split; both found as code leads |

#### D2. Discriminating experiments (6.2)

The baseline from the sources: Bayesian optimal design for model discrimination, i.e. the mutual information
between the hypothesis and the outcome (Box & Hill; T-optimality; the 2024 survey; classifier-based estimators;
EGIG under misspecification, Catanach & Das).

Beyond them: a transfer surrogate learned from the runs already made, predicting a candidate's value under another
reported condition without simulating it; batch selection for parallel runs; only conditions the paper reports
count as evidence.

| ID | Item | Design | Acceptance | Status |
|---|---|---|---|---|
| D2.1 | Condition knobs | the harness turns the dataset flag (and other claim-defining flags) into condition knobs, so claims on other rows (other datasets, other budgets) become claims at fixed conditions (`Target.at`) | a toy with two datasets where one candidate fits both | ✅ 3ea5520 Only where the README has that dataset's own command (its settings come with it: no guessed per-dataset tuning); the dataset flag becomes a `condition` knob, never screened or assumed; the other datasets' data is prepared. Toy: the harness end-to-end test (C3 at dataset=alpha) |
| D2.2 | Discrimination scheduler | when 2 or more hypotheses are within the equivalence threshold: the predictive distribution per hypothesis and condition (transfer surrogate plus run noise plus discrepancy), the expected information gain per cost, greedy batch selection, posterior update; the posterior includes priors (paper-stated values, round numbers, code evidence) | equifinal toys (two settings, three settings with one decoy hitting the target exactly): the truth ranked first | ✅ 3ea5520, 41c91b6 `gapfinder/diagnose/discriminate.py`: a transfer surrogate learned from the runs made (slope through the origin, its residual as spread; the as-run ratio when too few), expected information by Gauss-Hermite draws, greedy batches, stop at 0.9; parsimony first (a candidate that only adds an effectless change is merged). Toy: three equal fits, the truth's effect grows with a sweep the search can't reach; without the scheduler the answer is a decoy, with it the truth after 8 chosen runs |
| D2.3 | Exact-hit decoy guard | a likelihood with a model-discrepancy floor, so an exact hit can't beat the truth on the target alone; ties go to the held-outs | the exact-hit toy | ✅ 3ea5520, 41c91b6 Target ties judged with the discrepancy floor, then the held-outs and claims at other conditions, before the prior and parsimony; at verification a target-only tie keeps the earlier candidate. Toy: an exact hit that leaves the held-out unchanged loses to the truth |
| D2.4 | Scale hypotheses on swept knobs | when claims sweep a knob, fit the paper's v = the code's g(v) for g in {c·v, v + c, v^c}, with c snapped to paper-meaningful values (2, 10, 100, 1/2...); verify by running g at every point; feeds D5's operators | a toy with a percent-against-fraction knob and one with a doubled count | ✅ e07ca83 (scale probe; claims at fixed values join the differential) |

#### D3. Paper reading (6.3)

The baseline from the sources: vision models for table structure and LLMs for cell text (XLLM 2025); LLMs
hallucinate cells (DTBench); LLM grading agrees with humans at r = 0.93 (Horn & Keuper 2026).

Beyond them: claims built deterministically from the table grid (the LLM only labels coordinates and never writes a
number); two independent grids (LaTeX and PDF) reconciled cell by cell.

| ID | Item | Design | Acceptance | Status |
|---|---|---|---|---|
| D3.1 | Numeric grounding | a claim is grounded when its number (in any spelling: 0.729, 72.9, 72.9%) appears in the quoted window or in its table's cells; fuzzy quote matching | re-grounding the cached ledgers recovers dropped true claims, adds no false ones (checked against LaTeX tables) | ✅ 456f78a A number in any spelling (0.729/72.9/72.9%, ±, K/M, powers of ten, Unicode minus) in the quote, its page or its table; paraphrased quotes recovered by a fuzzy match that keeps every number, or by the cell. Re-grounding every cached ledger (`eval/claims_recall.py regound`): about 350 dropped claims recovered, every checkable one a cell of the table it names, 0 kept claims newly dropped (b5a: 18 -> 73 kept) |
| D3.2 | Table grids | LaTeX tables with `\multicolumn`/`\multirow` to grids with header rows and columns; PDF tables via PyMuPDF's table finder; mean±std and bold parsed | grid tests on the cached sources | ✅ 456f78a `gapfinder/ingest/tables.py`: multicolumn, multirow placeholders, nested tabulars, rules with arguments, the paper's macros expanded, `\bf`, sensitivity-table axes as headers, header rows from data-free rules; PyMuPDF tables; tested on synthetic tables and on RippleNet's source |
| D3.3 | Cell claims plus LLM labels | every numeric cell is a candidate claim; Super labels which rows and columns are the paper's method, the datasets and the metrics, by coordinate; conditions from the headers | recall of Table 3/4/5 cells on RippleNet, GraphMAE and b5a against the LaTeX ground truth | ✅ 456f78a (deterministic part) Method rows by the paper's name (or bold majority), metric axis by a lexicon, other headers as conditions; `ledger --table-claims` adds the method rows' cells the model missed. The model labeller is not run (the model budget is spent): the interface takes coordinates, never numbers |
| D3.4 | Double entry | LaTeX and PDF grids reconciled; prose claims from two independent passes, agreement kept, disagreement flagged | mismatches injected into a grid are found | ✅ 456f78a (grids) LaTeX and PDF grids matched by label or numbers and reconciled cell by cell (`table_mismatches.json`); injected mismatches found, other precisions and fraction/percent not flagged. The two-pass prose extraction needs model calls: not run |
| D3.5 | Recall harness | `eval/claims_recall.py` scores any extractor against LaTeX ground truth, with an LLM judge for header semantics | runs on the cached papers | ✅ 456f78a `eval/claims_recall.py recall`: the extractor's recall of the method rows' cells against the LaTeX source; baseline on eight cached papers from 8% (b5c) to 100% (b5a, b3a) |

#### D4. Paper-to-code links (6.4)

The baseline from the sources: LiSSA (RAG plus LLM, ICSE 2025); Alor et al. 2025 (LLM F1 around 80%; most false links
come from naming assumptions).

Beyond them: every link verified by execution, with a dry run perturbing the candidate and the trace showing the
value reaching a sink of the right role.

| ID | Item | Design | Acceptance | Status |
|---|---|---|---|---|
| D4.1 | Candidate retrieval | paper terms with their definitions (LaTeX "where λ1 is the L2 weight", table headers); code entities (flags with help text, config keys, named literals, parameters with defaults and comments); BM25 over split identifiers plus an ML synonym lexicon | recall of the true flag in the top 5 on a link set built from the dev-set specs | ✅ 456f78a `gapfinder/ingest/links.py`: BM25 over split flags and help texts (argparse and tf flags) with an ML lexicon, the term weighted over its own sentences; on a hand-labelled dev link set (`eval/links_eval.py`, 47 terms, 28 linkable): recall@1 = recall@5 = 0.86 |
| D4.2 | LLM adjudication | Super chooses among the retrieved candidates with quotes, or none | precision and recall on the same link set | ✅ 456f78a (interface) the model is given the retrieved candidates per name and chooses among them or none; not run (budget) |
| D4.3 | Lesion verification | a dry run with the candidate changed; its trace must show the value reaching a sink of the term's role (a rate to an optimiser, a weight to a loss term, a ratio to a count); links failing it are dropped | a toy with a name decoy (a flag named like the term that feeds something else) | ✅ 456f78a Role check (the term's role from its words against the trace's: rate, rate0, fraction, size, count); a decisive link's untraced knob gets a lesion dry run (a distinctive value: the sink it reaches is its role). A decisive link must also cover every content word of the term: 9 of 9 decisive links right, none for unlinkable terms (was 10 of 16 with 4 for unlinkable). Toy: a `weight` flag that is a class weight is not linked to weight decay |
| D4.4 | Use everywhere | links feed the assumptions' knob names, the claims at fixed conditions (D2.1) and the reporting of stated values | the end-to-end toy | ✅ 456f78a Unmatched ledger names linked before any model call (`link_names`); toy: `l2_reg_lambda` linked to `l2_coef` with no model, its stated value explains the gap |

#### D5. Code-change localisation (6.5)

The baseline from the sources: mutation-based fault localisation (MUSE, Metallaxis; FLIM 2025 on interference
mutants); metamorphic testing of ML code (Murphy et al.; Dwarakanath et al. 2018, 71% of bugs).

Beyond them:
- the "failing test" is the paper's whole set of claims, scored by history matching;
- sites restricted to executed lines on the data flow of the swept knob or of the metric (trace coverage plus a
  slice);
- operators from the metamorphic relations D2.4 finds;
- interference mitigation by held-out validation and invariants (claims the cause must not move).

| ID | Item | Design | Acceptance | Status |
|---|---|---|---|---|
| D5.1 | A general mutation hook | node-addressed AST edits (file, line, column, node kind, operator) in the in-memory patch hook: constants ×2 ÷2 ×10 ÷10 ±1, range and loop bounds, reductions (mean/sum/max, torch/numpy/tf, functions and methods), `dim`/`axis`, comparisons, boolean keywords, keyword routing (pass a swallowed keyword as the parameter it maps to) | unit tests per operator; the repo on disk never changes | ✅ 15aaaf0 |
| D5.2 | Site selection | executed lines from the runtime trace; a static slice from the swept knob and from the metric's computation; ranking by distance | the slice of a toy's knob contains its budget line | ✅ 15aaaf0 (with trace line coverage) |
| D5.3 | Mutation localisation and screening | successive halving over the mutants (one run each, then repeats for the best); score = gain in joint fit over every claim; interference control (screen on the target, validate on the held-outs, invariant claims must not move, minimal edits first, D2.4-derived operators first) | toys: an edge counted twice, a mean that should be a sum, an off-by-one loop bound; each found, no confident label on a decoy mutant | ✅ 15aaaf0 |
| D5.4 | Reporting | a mutant that fits is a code lead with its diff and evidence, never "Explained" | report tests | ✅ 15aaaf0 |

#### D6. Harness (6.6)

The baseline from the sources: Repo2Run (86% of 420 projects, NeurIPS 2025); ResearchEnvBench 2026 (verification by
running); PIPer 2025.

| ID | Item | Design | Acceptance | Status |
|---|---|---|---|---|
| D6.1 | CPU shim in every env-build step | the shim's environment and files on every command, not only the goal | a toy that calls `.cuda()` in its import path | ✅ 1d77dd4 |
| D6.2 | Failure reporting | env-build returns its last good checkpoint; `env_build.json` is written in the harness folder; an infrastructure error at any harness step writes HARNESS.md with the step | tests | ✅ 1d77dd4 |
| D6.3 | CPU-time limit from the timeout | `ulimit -t` = timeout × vCPUs × 1.2 unless set | test | ✅ 1d77dd4 |
| D6.4 | Memory-aware parallelism | the smoke run measures each copy's peak memory; parallel copies = floor(0.8 × 3.9 GB / peak) | a toy that allocates 1.5 GB | ✅ 34e5146 Each smoke copy reports its peak (ru_maxrss of its children); the cell runs floor(0.8 x 3.9 GB / peak) at once. The 1.5 GB acceptance toy needs a Linux VM (no peak locally on Windows): open |
| D6.5 | README procedure graph | Super reads the README's blocks and prose into ordered steps grounded to verbatim commands (setup, data, train, evaluate) with the files each writes and reads; the cell is the chain ending at the step whose output binds the claims; knobs from every python step (prefixed on collision); verified by running | toys: train then evaluate; preprocess, train, attack | ✅ 34e5146 (deterministic) An evaluation or attack command, or one reading a checkpoint, runs after the README's training step that writes it, in one cell; shared flags one knob, conflicting defaults prefixed by script. The model's reading of prose steps is not run (budget). Toy: train then evaluate, one cell, the training's settings are knobs |
| D6.6 | Binding by quote | when the binder ties, Super chooses with a quoted paper sentence ("we choose distribution Z"); no quote, no binding (never by closeness to the paper's number) | a toy with Z/Q lines and a paper sentence | ✅ 34e5146 (deterministic) A tie between printed labels is settled only by a paper sentence that reports, uses or chooses one of them; none, or several, stays a refusal. Toys: one sentence binds Z; sentences for both, or no reporting verb, refuse |
| D6.7 | Literals as knobs | when a script exposes few flags, the named literals the run executes (trace roles: epochs, rate, size, weight, count) become patch knobs in the spec | a toy whose settings are module constants | ✅ 34e5146 With fewer than three flags, named settings in the files the run imports (lr, epochs, hidden, dropout ...) become patch knobs. Toy: EPOCHS and LR from config.py, not SEED or NAME_LEN |

**Order:** D6.1-D6.3 and D7.5 (small); D1.1-D1.2 with D7.1; D2.4 with D5.1-D5.4; D1.3-D1.6 with D7.2; D2.1-D2.3 with
D7.3; D7.4 (the acceptance suite); D3; D4; D6.4-D6.7; D7.7; D7.6. Then the dev suite, the planted suite and a fresh
sealed batch.

#### D7. Additions of 2026-10-20 (owner's review, assessed)

| ID | Item | Design | Acceptance | Status |
|---|---|---|---|---|
| D7.1 | Calibration gate | the zero-run probes (D1.2 reporting, D2.4 scale on the measured curve) run right after the naive calibration; a hypothesis that fits the target and every held-out is verified and the settings search is skipped | a slow toy whose paper number is its best epoch: no settings search runs | ✅ 158e474 |
| D7.2 | The repository's own package and its paper-era commit | the paper-year knob includes the repo's own package when it is on PyPI (from setup.py/pyproject); a second knob runs the repo at its last commit before the paper's date (only history before the given commit is read) | a toy library whose release changed a default; a toy repo whose later commit changed the code | ✅ 19b2039 Own package: D1.3. Paper-era code: the last commit before the paper's date through GitHub's API from the given commit backward (ancestors only), its code files under 1 MB fetched in the harness's last step; `gf_paper_era_code` = 0, 1 or a commit sha fetched on demand; a binary search over the commits up to the given one and the changing commit's diff. Toy: the commit that changed a constant found among four |
| D7.3 | Paper-discussed knobs as a prior | in ties (D2.2), a knob the paper states or varies gets a higher prior than an unmentioned ladder value; a weight, never a veto (unstated settings are the commonest real cause) | equifinal toys both ways (the truth mentioned; the truth unmentioned) | ✅ 3ea5520 A stated value 0.9, a mentioned or swept knob 0.6, an unmentioned one 0.4, a round number x1.2, the code's docs x1.1; used in tie order and in the discrimination posterior. Toys: a tie goes to the mentioned knob; when the paper mentions the other, the truth is still listed as equally good and nothing is confirmed |
| D7.4 | Planted archetypes in real repos | plant scale conventions (x2, x100), best-epoch reporting, library drift and code defects into working dev containers (pygcn, GAT, VGAE, GraphMAE, SDCN, BOND...), several cells each, as the acceptance suite of D1, D2 and D5 (development only: known to the builder, not blind evidence) | the suite runs end to end for $0 of model calls | ✅ b09e41b (tooling) `eval/planted/plant.py --kinds scale,code,reporting,library` beside settings, a scorer per kind, a local backend for tests; the make-search-score loop passes on a toy for scale and reporting (code edits are not identifiable from one shifted number: the toy only requires no confident wrong answer). Running it on the dev containers is a Sandboxes job: open |
| D7.5 | pip without a cache in env-build | `PIP_NO_CACHE_DIR=1` on every env-build command | test | ✅ 1d77dd4 |
| D7.6 | Miner pre-filter | the GitHub tree API before any download: total data size, large files, GPU-only requirements; a ranking by CPU-friendly ecosystems | the pool's free check agrees with the pre-filter | ✅ 34e5146 GitHub's recursive tree plus raw requirement and README files, the free check's own rules, before any download; on the 33 public candidates 32 agree with the free check (the other errs toward ready, which the free check still catches) |
| D7.7 | Multi-fidelity screening | for runs over 10 minutes that print per-epoch metrics: screening runs cut at a fraction of the naive run's time leave their per-epoch log; a candidate behind the naive run's curve at the same epoch by more than 2 bands is dropped (successive halving, Hyperband/ASHA); one bracket keeps full-length runs so late effects (schedules, regularisers) are not lost | a toy whose true cause helps only late, and a slow toy where the screen's time halves | ✅ 34e5146 Runs over 10 minutes whose spec can be cut in time (`run.time_cut`, set by the harness with the target's per-epoch series): screened at a quarter of the as-run time, dropped when behind its curve at the same epoch by 2 bands; the strongest quarter always run in full. Toy: decoys that hurt from the start dropped, a schedule that helps only after epoch 14 kept and found, cut runs under 60% of a full one |

Not adopted as proposed: a hard rule against unmentioned knobs in ties (D7.3 instead); "Explained" from one target matched at a
multiple of the stated value (D2.4 requires the same factor on every swept point); `--resume` on the batch-5 cases as
validation (a smoke test only: a fix is never judged on the case that revealed it); a global `OMP_NUM_THREADS=2` (it
slows every run). Two owner decisions are pending: the cap ($45 proposed), and exempting zero-run log checks from the
two-paper rule when they label only on a fit to every claim and pass the dev suite with 0 confidently wrong.

#### Status of 2026-10-21

Every item of D1-D7 has its code and acceptance toys (the status column). The regression check on the dev suite
(`eval/dev_suite.py --base 5000`, the code of D1.3-D7.4 and the D2 fixes, against run 4000): 52 of 69 cause runs
correct against 50 (4 tasks better, 3 worse, sign test p = 1.0: no change), 0 confidently wrong on both, 57
correct abstentions on both. Fixes found while building the toys, each with its own acceptance case: the
calibration gate stood down for an as-run miss between 2 and 3 sigma (now the posterior decides there); a
reporting rule the runs can't read on every claim took posterior from the ones that can (now not proposed); the
local backend joined hook paths with ":" (now the interpreter's separator, `GF_PATHSEP`).

Open, by what they need:
- **Sandboxes runs** (unbilled, the owner's go): D7.4 on the dev containers, run on 2026-10-22 as the planted
  curriculum on six reproduced papers (section 5.6; failure classes in 7.4). GAT, GraphMAE, SDCN and BOND are not in
  it yet. D6.4's 1.5 GB toy on a Linux VM is still open.
- **Model calls** (the $33 cap is spent to $0.40): D3.3's labeller, D3.4's two-pass prose extraction, D4.2's
  adjudication, D6.5's reading of prose steps. Each has its interface and a deterministic part that runs now.
- **Measurement** (the owner's budget): a fresh sealed batch, the only evidence of progress (section 7.3's rules).

### 7.4 Plan of 2026-10-22: the planted curriculum's failure classes (to solve)

These come from section 5.6, c1's 22 misses out of 30 gap tasks. Every miss is in exactly one class; where a second
blocker stands behind the first, the evidence column says so. Counts are of misses unless stated.

**The rules for solving them:**
- Every fix is class-level and gets its own acceptance toy.
- It is judged on a **fresh seed** (4 or later; seeds 2 and 3 are dev data), searched by the old and the new frozen
  version, both into their own run folders.
- It must also hold the dev suite with 0 confidently wrong.
- c2 showed why both checks matter: its gains came from somewhere other than its target.

| ID | Class | Evidence | Mechanism | Direction (to be designed and tested) | Status |
|---|---|---|---|---|---|
| E1 | **Code rounds starved by the run budget** | 5 misses: the patch round stopped 1-2 runs short of the planted literal (VGAE `val_percent=40`, VGAE `test_percent=7.5`, RippleNet `eval_ratio=0.05`); the patch round never got to VGAE's code edit; RippleNet's mutation round reported "no room left". Across all 30 searches a code round was cut in 19. | Rounds run in a fixed order (screen, confirm, combine, verify, spec knobs, history matching, patch, mutation), and the code rounds get what is left. The patch reserve is held only once the claims look out of space. | Choose each next run by expected information per run across classes, extending the D2 discrimination scheduler: a settings screen, a patch value and a mutant compete on one scale, instead of the code rounds getting leftovers. At least try the few literal leads early: they are the top 3 leads x 6 values. | open. c2's fixed hold was not adopted (5.6) |
| E2 | **Mutation sites ranked out** | 1 miss on its own (VGAE `gae/layers.py:30` `1.0 -> 0.0`: c2's round ran 22 mutants, none at that site). It also stands behind 2 E1 code misses. The planted sites rank 37, 110 and 289 among 121-332 candidates, and at most 24 are tried. | Candidate sites come from the data flow of the known knobs and the metric code, ranked by distance. A defect off those paths, or ranked low, is never run. | Group screening of sites: apply many mutants at once and bisect (group testing, delta debugging; O(k log N) runs over all N sites). Rank by executed lines and a cheap sensitivity probe. | open |
| E3 | **Right knob, value off the grid** | 6: SparseTSF patience 25 for 20; FastGCN hidden1 160 for 4 (the other side of the default; 6 was tied); pygcn weight_decay 0.0025 for 0.002; FastGCN weight_decay 1e-4 for 1.25e-4; VGAE val_percent 4 for 5; RippleNet `item_update_mode` `replace` for `replace_transform` (a choice) | The candidate ladder (x0.4, x2, x10 ... and the knob's choices) rarely holds the planted value. The secant step is off when a ladder value fits, because on the dev suite it made decoys (102 -> 92). The equal-value set lists only measured values. | Report the interval of values consistent with every claim (profile the answer's knob on both sides of the default), not a point; the answer stays. A categorical knob that moves the target has all its choices screened. | open |
| E4 | **Equifinality: the planted cause is tied, another is chosen** | 6: pygcn epochs=50 (lr chosen), lr=0.0025 (hidden chosen), weight_decay=0.002 (lr chosen); VGAE epochs=800 (hidden1 chosen); pygcn's two level-2 code tasks (c1: an unsupported fit doesn't open the mutation round; c2: it ran, and other mutants fit equally). 5 of 6 are on pygcn, which has one claim. | One number can't separate causes that move it alike. GapFinder says so (Fits but unsupported, with the tied set), and the scorer counts it missed. | Not an engine fix on one number. Curriculum: score "tied" apart (done) and give pygcn's harness more claims (more datasets or printed metrics the paper reports). Engine: discriminating runs at conditions the paper reports (D2) need those claims. | curriculum: open |
| E5 | **A wrong knob with no tie, on a multi-claim task** | 1: SparseTSF batch_size=512, answered patience=25 (c2 found it) | Unclear from one case | Watch on fresh seeds | watch |
| E6 | **Below the detection limit (level 2)** | 3: FastGCN learning_rate x0.5 (Inconclusive); FastGCN learning_rate=0.005 (no answer); VGAE epochs=800 (Inconclusive) | Gaps of 3-5 sd sit near the minimum detectable effect at 3 confirmation repeats, and the MDE rule calls them Inconclusive (correct abstentions, but misses) | Adaptive repeats when a gap lies between 1 and 3 MDE, as in sequential testing (SPRT), before calling it Inconclusive | open |
| E7 | **Families the curriculum could not plant** | Reporting rule, paper-era code, package release: no draw moved a target 3 sd on five rebuilt harnesses. The b3a rebuild doesn't bind, and pygcn's pins don't install. | On these papers those choices barely change the numbers | Plant them where they matter: SDCN (best epoch on the labels), BOND (PyGOD drift), GraphMAE. Or plant synthetic versions (a shim that changes a library default). | open |

**Problems with the curriculum itself (fixed during the run, or open):**
- Controls first took about half the slots: a control was accepted on every try, while most real draws were
  redrawn. Fixed: at most one in five per case, and gap tasks and controls are scored apart.
- pygcn's tasks have one claim each (E4). Open: a multi-claim pygcn harness.
- The scorer's value tolerance (10%) is strict against the engine's coarse grid; E3 counts those cases rather than
  passing them. Open: score against a reported interval once E3 exists.
- The rebuilt harnesses offer few distinct draws (one era commit, one reporting rule, one to three package
  directories), so a new seed replants the same causes there.

**Infrastructure seen during the run (handled):**
- The machine lost DNS for minutes at a time. Task making waits for the API's name to resolve and redraws lost
  draws; searches rerun on an InfraError and resume from `run.cut*`.
- A Sandboxes burst refused new VMs at about 40 simultaneous creations.
- Windows killed background processes when the session ended (exit code 1073807364).
- A new worktree needs `.env` copied in (it is git-ignored).
- `tests/integration/test_alternative_configs.py` fails in about 1 run in 3 on c1 as well: a flaky test, not a
  regression.

## 8. Where things are

| What | Where |
|---|---|
| Engine | `gapfinder/search/engine.py` (search, protocol tests, alternative configs, claims at fixed values `Target.at`, split variance); `search/audit.py`; `search/trace.py`; `search/contrast.py`; `search/matcher.py`; `search/op_swaps.py`; `search/difftrace.py`; `sandbox/ast_patch.py`; `sandbox/runner.py` (shards and segments); `gapfinder/diagnose/` (the differential `core.py`, `reporting.py`, `library.py`, `discriminate.py`); `search/mutation.py` |
| Harness tools | `gapfinder/harness_build.py` (`gapfinder harness`: the automatic harness end to end); `gapfinder/harness_auto.py` (its fixed rules); `gapfinder/env_year.py` (paper-year and paper-era knobs); `gapfinder/diagnose/library.py` (which package, release and call site); `gapfinder/ingest/arxiv_source.py` (LaTeX source, cited setups); `gapfinder/env_build.py` (`gapfinder env-build`); `gapfinder/spec_draft.py` (`gapfinder spec-draft`); `eval/external/devset/build_case.py`; `eval/env_bench.py`; `gapfinder/ingest/tables.py` (table grids, cell claims, double entry); `gapfinder/ingest/links.py` (paper terms to flags) |
| Sealed blind cases | `eval/external/blind-1/`, `blind-2/`, `batch3/` (b3a, b3c), `batch4/` (b4a): each has `case.md`, `answer_key.md` after the reveal, HARNESS.md, the run and RESULT.md |
| Frozen batches | `eval/external/devset/` (devbatch-1 cases; CANDIDATES.md holds answers); `eval/external/devbatch2/` (PROTOCOL.md, RESULTS.md) |
| Planted causes | `eval/planted/plant.py` (`make`, `search`, `score`); tasks in `eval/planted/tasks/`; answers in `eval/planted/sealed/`; `--kinds setting,scale,code,reporting,library` (plan D7.4) |
| Planted curriculum | `eval/planted/curriculum.py` (`make` with `--seed`, `--control-rate`; `search` with `--seed`, `--watch`; `score` and `report` with `--seed`; `GF_CURRICULUM_RUN` names the run folder); `eval/planted/rebuild_harnesses.py` (the `-h` harnesses); tasks, sealed answers and work files in `eval/planted/curriculum/`; results `eval/results/planted_curriculum.md` and `planted_curriculum_c{1,2}_seed{2,3}.md` (section 5.6, classes 7.4) |
| Case pool | `eval/pool/mine.py` (miner; answers sealed in `eval/pool/sealed/`, never opened by the runner); `eval/pool/verify.py` (parent against fix, verdict only); `eval/pool/candidates.json` (public); `mine.py prefilter-check` (plan D7.6) |
| Measurements | `eval/claims_tier.py` -> `eval/results/claims_tier.json` (item 16); `eval/claims_recall.py` (re-grounding, table recall); `eval/links_eval.py` (dev link set) |
| Synthetic benchmark | `eval/gapbench/`; dev suite `eval/dev_suite.py`; `eval/compare_suites.py`; `eval/results/dev_suite_run*.json` |
| Tags | `blind-1`, `blind-2`, `devbatch-1`, `devbatch-2` (`e0117a2`), `planted-1`, `batch-3` (`92b1faa`), `batch-4` (`bae25f4`), `planted-c1` (`1c8f0f8`, worktree `../gf-c1`), `planted-c2` (`ca4a5e2`, worktree `../gf-c2`) |
| Learning docs | `docs/learn/` (beginner path) |
