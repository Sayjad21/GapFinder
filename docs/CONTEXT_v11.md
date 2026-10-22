# GapFinder: current context (2026-10-22)

The one current document: what GapFinder is, the rules, what it can do, where the harness stands, every real
result, what the last bottlenecks were and what fixing them changed, and the current work list. The step-by-step
history is in git and in `docs/learn/07_the_journey.md`. Paths are relative to the repo root
(github.com/Sayjad21/GapFinder).

---

## 1. What GapFinder is

Given a paper and its code, GapFinder explains why running the code doesn't give the paper's numbers.
1. **Read:** Nemotron reads the paper and lists its claims and the settings they may depend on.
2. **Search:** it runs the code many times in Token Factory Sandboxes, forking from saved checkpoints. Candidate
   causes come from six classes: settings, reporting rules, library releases, code defects, data pipeline, and
   "outside every class".
3. **Verify:** it checks the best candidate three ways:
   - undoing the change must bring the gap back;
   - the other reported numbers must not get worse;
   - the value needs evidence.
4. **Report:** a Gap Report per claim, with a label, a ranked differential, the evidence and replayable runs, plus an
   audit of what a matching number doesn't show.

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
2. GapFinder is frozen: a git tag, a worktree, `python -P` and the worktree's own `.env` (git-ignored: copy it in).
3. The harness is built from the paper and the repo only.
4. The run is committed **before** the key is opened.
5. The key's hash is checked, then the run is scored.

Development measurements (the dev suite, planted gaps) follow the same freezing. They are never blind evidence.

### 2.3 Constraints

- **Sandboxes only** (the owner's decision; never local Docker):
  - 4 vCPUs, 3.9 GB RAM, no swap, CPU only;
  - **at most 3600 s per operation**, a platform limit: a longer timeout is rejected;
  - a VM slows to about one CPU when many searches run at once;
  - a burst of about 35-40 new VMs at once was refused (2026-10-21).
- **Money:**
  - billed **$32.61** of the owner's ~$50 (Nemotron only);
  - `GF_SPEND_CAP_USD=33`, which the owner allows up to $45;
  - a ledger costs about $0.1-0.3;
  - Sandboxes are unbilled in the Beta (they report a diagnostic cost, now ~$52k), and the guard
    `GF_SANDBOX_GUARD_USD` is raised for searches;
  - every checkout writes to the main spend ledger.
- **Owner decision:** zero-run log checks are exempt from the two-paper rule when they label only on a fit to
  every claim and pass the dev suite with 0 confidently wrong.
- **Commits:** no AI attribution. "Write it down" means document only.
- **Never open sealed keys before the run is committed.** Never give `eval/external/devset/CANDIDATES.md` (answers)
  to a harness writer.

---

## 3. What runs, in order

| Step | Module | What it does |
|---|---|---|
| Ledger | `gapfinder/ledger/`, `ingest/tables.py`, `ledger/grounding.py`, `ingest/arxiv_source.py` | Claims with exact quotes (Ultra, filtered by Super), and assumptions per setting. A claim is grounded when its number, in any spelling, is in its quote, page or table. Table grids come from the LaTeX source and the PDF, reconciled cell by cell. The appendix gets its own call, and setups cited "as in [X]" are fetched. |
| Paper-to-code links | `ingest/links.py` | Paper terms to flags: BM25 over flags and help text with an ML lexicon, then a role check on the trace (a rate reaches an optimiser) and a lesion dry run. |
| Repo map | `gapfinder/ingest/repo_map.py` | Flags, defaults and help text: argparse, gflags, absl / tf.app.flags. A commented-out block is kept as an alternative. |
| Runtime trace | `gapfinder/sandbox/trace_hook.py`, `search/trace.py` | One dry run records where values land (optimizer, dropout, batch size, width, loops, seeds) and which lines execute. Each knob gets a role and role-based candidate values. |
| Zero-run probes | `diagnose/reporting.py`, the engine's scale probe | Right after the naive runs: reporting rules (best epoch, best by validation, best of N seeds) and scale relations on swept knobs ("the paper's v is the code's c x v"). A fit on every claim is verified, and the settings search is skipped (the calibration gate). |
| Library and era | `env_year.py`, `diagnose/library.py` | The paper-date packages and the paper-era commit as knobs. ddmin over the packages, binary search over releases or commits, and the call site by signature and source diff. |
| Candidate values | `search/hypotheses.py` | By role, by choices, a coarse-first ladder, multipliers, edge values. True/false literals flip. |
| Search | `search/engine.py` | Screen (long runs screened at a quarter of their time, multi-fidelity), confirm (a race over at most a quarter of the budget), combine (the repo's alternative blocks first, pairs, a forward step), bisect and verify. A secant step runs only when nothing fits every claim. A fallback round covers knobs no assumption names. |
| Discrimination | `diagnose/discriminate.py` | When candidates tie: runs chosen by expected information gain at the conditions the paper reports. Priors: a stated value 0.9, a mentioned knob 0.6, an unmentioned one 0.4. An exact hit on the target alone can't beat a close fit on every claim. |
| Verification | `search/verify.py` | Counterfactual; held-out claims (tuned-separately ones are notes, not vetoes); relation claims; evidence (paper, docs or web; code alone doesn't count). |
| Confidence cap | `engine._cap_confidence` | A confident label needs a finished search, every knob screened, and evidence beyond source code. |
| History matching | `search/history.py` | Every configuration against every claim; "out of space" when none comes within 3 sigma. |
| Code causes | `ingest/code_checks.py`, `sandbox/ast_patch.py`, `search/contrast.py`, `search/matcher.py`, `search/mutation.py` | **Static leads:** literals, unoverridden defaults, switches, splits, selection loops, leakage. **Patch round:** literals, defaults and switches changed in memory. **Mutation round:** small edits (x2, /2, mean <-> sum, bounds, comparisons, data-pipeline switches) at sites on the data flow of the knobs and the metric, scored on every claim; a fit is a code lead, never Explained. No file is edited. |
| Differential | `gapfinder/diagnose/core.py` | Every candidate of every class scored by the likelihood of all claims, against "outside every class". The report shows the top 3 with their evidence and how to check them. |
| Protocol tests | `engine._protocol_tests` | Test-score selection, label-based score edits and evaluation switches (`drop_last`) are switched off and measured, whatever the label. |
| Audit | `search/audit.py` | In every report: protocol findings; the paper's own comparisons checked against the runs; held-out misses; stated settings the harness can't vary. |
| Long cells | `sandbox/runner.py` (`run.shards`, `run.segments`) | Past the 3600 s cap: independent jobs in parallel VMs, or resumable training in pieces. |
| Your code vs the authors' | `search/difftrace.py`, `gapfinder diff` | Both programs traced. Each value that reaches the same library call differently becomes a hypothesis. |
| Environment | `gapfinder/env_build.py`, `gapfinder env-build` | Repo2Run-style: one install command at a time in Sandboxes, with free rollback, the CPU shim on every step. The goal is that the README's own command runs for 5 minutes. |
| Report and app | `gapfinder/report/`, `gapfinder/api/`, `web/` | Markdown/JSON reports; a replay-only web app. |

---

## 4. Where the harness stands (the biggest blocker to "any paper")

### 4.1 What the finished harness should be

An agent writes it (Nemotron, in the product), but **the agent only proposes, plain code checks every step, and the
agent has no say in what the search tests.** Inputs: the paper and the repo (and the user's own code). Outputs: a
frozen spec, the image checkpoint, and HARNESS.md recording every choice and its reason.

| # | Step | Plain code checks it | Status today (`gapfinder harness`) |
|---|---|---|---|
| 1 | Environment | each install runs in a Sandbox; a failure rolls back; done when the README's command starts | ✅ `env-build` |
| 2 | Data | the files exist after the step; sizes and checksums recorded | ✅ the repo's download and preprocessing scripts; loader caches kept in the base |
| 3 | Which command makes which number | it runs and prints the claim's metric | ✅ command picker and README procedure graph (deterministic part) |
| 4 | Metric parser | every parsed number appears verbatim in the log; one name per claim | ✅ binder (test over val, final over best; refuses when ambiguous; binding by quote) |
| 5 | Knobs | every flag the command passes or the code reads, at its default; the trace confirms each | ✅ (literals become knobs when a script exposes few flags) |
| 6 | Fit the Sandbox | shards or segments first; halve the scale only if it still doesn't fit, with a discrepancy allowance | ✅ shrink rule applied; parallel copies by measured peak memory |
| 7 | Self-checks | seeds vary, memory and time fit, every claim is printed | ✅ |
| 8 | Claims | the target plus held-outs from the ledger; condition knobs for other datasets | ✅ mostly; ambiguous cases listed for a person |
| 9 | Human approval | a person reads HARNESS.md and approves the commands (about 5 minutes; never the knobs) | — |

**Why an agent doesn't bias it:** the harness agent never sees causes or search results; the choices that could
steer the answer (knobs, defaults, scaling) are rules; the harness is frozen before the search starts. **When the
user brings their own code:** their script is the harness; `gapfinder diff` compares it with the authors'.

### 4.2 Measured reality

- **Environment builder:** the experiment ran unaided on about 2 of the last 6 unseen repos (devbatch-2 1 of 3,
  batch-3 1 of 2, batch-4's goal fixed after it parsed as invalid bash).
- **`gapfinder harness` without a person:**
  - **RippleNet:** it reproduced the hand harness (same command, same 9 knobs, same binding, the same gap).
  - **Planted curriculum (2026-10-21):** it rebuilt 5 of 6 harnesses from their recorded environments. Fair
    Clustering failed: its printed objective doesn't bind to the claim.
  - **Not yet run end to end on an unseen repo,** env-build included. That is the next harness test.
- **Paper-year packages on a newer Python:** a compiled package's source archive is no longer counted as
  installable (2026-10-21; numpy 1.11 on Python 3.10 had failed to build). When nothing before the paper's date
  installs, the first release within 183 days after it is used and labelled.

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
confidence cap went in. All eight predate the D1-D7 work (section 6); **no sealed paper has been run since**, so
D1-D7 has no blind measurement yet.

### 5.2 Frozen dev batches (known causes, not shown to the harness writers)

- **devbatch-1** (5 papers): 1 correct (G-Mixup: the gain is noise), 0 confidently wrong. GIN's README already
  had the fix; GAT's names didn't map; Informer fit only 28 runs; PatchTST was `drop_last`.
- **devbatch-2** (NCF, PyG GAT vs GCN, Anomaly Transformer): 0 causes found, 3 correct abstentions, 0 wrong. All
  three reproduced: the causes are protocol and noise flaws inside the paper's own number.

### 5.3 Synthetic benchmark (GapBench)

- Sealed v1.1-v1.3: 0/90 confidently wrong; a coding-agent baseline was confidently wrong in 49 of 90.
- **Dev suite, the current engine** (run 5000, the code of D1-D7): 52 of 69 cause runs correct, 0 confidently
  wrong, 57 correct abstentions. Run 6000 with `code_hold` (not adopted, 5.4): 48 of 69, 0 confidently wrong.
- It guards against regressions; it doesn't reflect real-paper problems.

### 5.4 Planted-gap curriculum on reproduced papers (2026-10-21/22; development measurement)

The owner's question: which kinds of gaps does GapFinder find, beyond settings? Gaps were planted into papers it
already reproduces, graded from easy to hard, and searched for by a frozen engine. The summary and per-task tables
are in `eval/results/planted_curriculum*.md`, and the failure classes are the work list (7.1). An earlier, smaller
planted run (pygcn 3 of 11 on one claim; Fair Clustering and SparseTSF 6 of 8 on eight claims) had already shown
that one number leaves most planted causes unidentifiable.

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
  - It runs `gapfinder search --hypotheses repomap`: no paper and no ledger. The only model calls are the search's name-matching step: 15 Super calls, under $0.01, for all of seed 4.
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
| Data pipeline, reporting rule, paper-era code, package release | none kept | none kept |
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
- **Some families never produced a task.** 4 data-pipeline draws and 13 reporting, era or library draws were
  measured, and none moved a target by 3 sd. The rebuilt harnesses gave only controls.

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
  site (7.1, E2).
- **Not adopted:** `code_hold` is off by default (`d2a4ca0`); the code and its toy test stay.

### 5.5 What works and what doesn't (2026-10-22)

**Works:**
- Scale and unit conventions, planted: 6 of 7, labelled as paper-code inconsistencies.
- Honesty: nothing confidently wrong in 17 real-paper results since the cap and in 41 planted tasks.
- Blind: λ=100 on Fair Clustering and lr=0.001 on RippleNet (before D1-D7).
- The automatic harness rebuilt 5 of 6 reproduced papers' harnesses.

**Doesn't yet:**
- Code defects: 0 of 5 planted. The code rounds are starved by the budget (E1), and the planted site is ranked out
  (E2).
- Settings: 2 of 18 planted. Values come off a coarse grid (E3), and causes tie on few claims (E4).
- Reporting rules, paper-era code and library drift: proven on toys only. The curriculum couldn't plant them (E7),
  and the blind cases that had them (SDCN, BOND) predate D1.
- A harness built end to end on an unseen repo; sealers' throughput (about one usable paper per 3 hours).

---

## 6. The bottlenecks of 2026-10-20: what was done and what it changed

Found after batch-5 (8 sealed papers: settings causes 1 correct of 4; code, evaluation and library causes 0 of 4).
Plan 7.2 (D1-D7) addressed them; every item has its code and an acceptance toy. "After" is the latest measurement;
none is a sealed paper.

| # | Bottleneck | What was done | Before | After |
|---|---|---|---|---|
| 6.1 | Hypotheses were settings only | D1: a differential over six classes, zero-run reporting probes, library and paper-era probes, data-pipeline mutants | 0 of 4 non-settings causes on sealed papers | toys pass for every class. Planted: code defects 0 of 5; data, reporting, era and library not plantable on those papers |
| 6.2 | Equal fits: the wrong one picked | D2: a discrimination scheduler, the exact-hit guard, the scale probe; D7.3 paper priors | 3 sealed misses picked a wrong equal fit | toys pass. Planted: scale conventions 6 of 7, but settings 2 of 18, mostly ties on few claims (E4) and coarse values (E3) |
| 6.3 | Paper reading unreliable | D3: numeric grounding, table grids from LaTeX and PDF, double entry, a recall harness | most claims dropped as ungrounded (b5a 57 of 67, b5b 48 of 95) | re-grounding the cached ledgers recovered about 350 claims, 0 newly dropped (b5a 18 -> 73 kept). The model labeller and two-pass prose: not run (budget) |
| 6.4 | Terms not linked to flags by meaning | D4: BM25 retrieval with an ML lexicon, a role check and a lesion dry run | name matching only | recall@1 0.86 on a 47-term dev link set; decisive links 9 of 9 right (10 of 16 before the role check) |
| 6.5 | Only simple code changes testable | D5: a node-addressed mutation hook, site selection on the data flow, screening on every claim, code leads | literal and a few operation swaps | toys found (an edge counted twice, mean vs sum, a loop bound). Planted: 0 of 5 (E1, E2) |
| 6.6 | The harness needed a person | D6 and `gapfinder harness`: steps 2-8 automatic (section 4) | every harness hand-built | 5 of 6 curriculum harnesses rebuilt without a person; not yet end to end on an unseen repo |
| 6.7-6.8 | Evaluation size; machine and budget | owner's | | |

Overall: the dev suite went from 50 to 52 of 69 (no significant change), 0 confidently wrong throughout. The
remaining failure classes, measured on the planted curriculum, are 7.1.

---

## 7. Work plans

### 7.1 Current work list: the planted curriculum's failure classes (2026-10-22)

These come from section 5.4, c1's 22 misses out of 30 gap tasks. Every miss is in exactly one class; where a second
blocker stands behind the first, the evidence column says so. Counts are of misses unless stated.

**The rules for solving them:**
- Every fix is class-level and gets its own acceptance toy.
- It is judged on a **fresh seed** (4 or later; seeds 2 and 3 are dev data), searched by the old and the new frozen
  version, both into their own run folders.
- It must also hold the dev suite with 0 confidently wrong.
- c2 showed why both checks matter: its gains came from somewhere other than its target.

| ID | Class | Evidence | Mechanism | Direction (to be designed and tested) | Status |
|---|---|---|---|---|---|
| E1 | **Code rounds starved by the run budget** | 5 misses: the patch round stopped 1-2 runs short of the planted literal (VGAE `val_percent=40`, VGAE `test_percent=7.5`, RippleNet `eval_ratio=0.05`); the patch round never got to VGAE's code edit; RippleNet's mutation round reported "no room left". Across all 30 searches a code round was cut in 19. | Rounds run in a fixed order (screen, confirm, combine, verify, spec knobs, history matching, patch, mutation), and the code rounds get what is left. The patch reserve is held only once the claims look out of space. | Choose each next run by expected information per run across classes, extending the D2 discrimination scheduler: a settings screen, a patch value and a mutant compete on one scale, instead of the code rounds getting leftovers. At least try the few literal leads early: they are the top 3 leads x 6 values. | open. c2's fixed hold was not adopted (5.4) |
| E2 | **Mutation sites ranked out** | 1 miss on its own (VGAE `gae/layers.py:30` `1.0 -> 0.0`: c2's round ran 22 mutants, none at that site). It also stands behind 2 E1 code misses. The planted sites rank 37, 110 and 289 among 121-332 candidates, and at most 24 are tried. | Candidate sites come from the data flow of the known knobs and the metric code, ranked by distance. A defect off those paths, or ranked low, is never run. | Group screening of sites: apply many mutants at once and bisect (group testing, delta debugging; O(k log N) runs over all N sites). Rank by executed lines and a cheap sensitivity probe. | open |
| E3 | **Right knob, value off the grid** | 6: SparseTSF patience 25 for 20; FastGCN hidden1 160 for 4 (the other side of the default; 6 was tied); pygcn weight_decay 0.0025 for 0.002; FastGCN weight_decay 1e-4 for 1.25e-4; VGAE val_percent 4 for 5; RippleNet `item_update_mode` `replace` for `replace_transform` (a choice) | The candidate ladder (x0.4, x2, x10 ... and the knob's choices) rarely holds the planted value. The secant step is off when a ladder value fits, because on the dev suite it made decoys (102 -> 92). The equal-value set lists only measured values. | Report the interval of values consistent with every claim (profile the answer's knob on both sides of the default), not a point; the answer stays. A categorical knob that moves the target has all its choices screened. | open |
| E4 | **Equifinality: the planted cause is tied, another is chosen** | 6: pygcn epochs=50 (lr chosen), lr=0.0025 (hidden chosen), weight_decay=0.002 (lr chosen); VGAE epochs=800 (hidden1 chosen); pygcn's two level-2 code tasks (c1: an unsupported fit doesn't open the mutation round; c2: it ran, and other mutants fit equally). 5 of 6 are on pygcn, which has one claim. | One number can't separate causes that move it alike. GapFinder says so (Fits but unsupported, with the tied set), and the scorer counts it missed. | Not an engine fix on one number. Curriculum: score "tied" apart (done) and give pygcn's harness more claims (more datasets or printed metrics the paper reports). Engine: discriminating runs at conditions the paper reports (D2) need those claims. | curriculum: open |
| E5 | **A wrong knob with no tie, on a multi-claim task** | 1: SparseTSF batch_size=512, answered patience=25 (c2 found it) | Unclear from one case | Watch on fresh seeds | watch |
| E6 | **Below the detection limit (level 2)** | 3: FastGCN learning_rate x0.5 (Inconclusive); FastGCN learning_rate=0.005 (no answer); VGAE epochs=800 (Inconclusive) | Gaps of 3-5 sd sit near the minimum detectable effect at 3 confirmation repeats, and the MDE rule calls them Inconclusive (correct abstentions, but misses) | Adaptive repeats when a gap lies between 1 and 3 MDE, as in sequential testing (SPRT), before calling it Inconclusive | open |
| E7 | **Families the curriculum could not plant** | Data pipeline, reporting rule, paper-era code, package release: 17 draws measured, none moved a target 3 sd. The b3a rebuild doesn't bind, and pygcn's pins don't install. | On these papers those choices barely change the numbers | Plant them where they matter: SDCN (best epoch on the labels), BOND (PyGOD drift), GraphMAE, SparseTSF (`drop_last`). Or plant synthetic versions (a shim that changes a library default). | open |

**Plan of 2026-10-22: the fixes (agreed with the owner).** Each is a published method or a class seen on
several papers. Each gets an acceptance toy that is a new instance of its class, then the full suite. Then comes a
new test round: planted seed 4 (fresh), the frozen c1 against the new frozen version, plus the dev suite.

| ID | Fix | For | Published basis | Status |
|---|---|---|---|---|
| F1 | Rank mutation sites by a backward slice from the line that prints the metric, not by function names | E2 | thin slicing; mutation-based fault localisation (MUSE, Metallaxis) | done: mutation.py output slice (toy: test_mutation_output_slice) |
| F2 | Literal leads early: the patch round's top leads (at most 3 x 6 runs) run as soon as screening shows no single setting closes the gap | E1 | value of information in sequential diagnosis (GDE, de Kleer & Williams 1987) | done: `early_code_screen`, on (toy: test_early_code_screen) |
| F3 | Value interval for the answer's knob (a level-set search, about 6-10 runs, after the answer is chosen; the answer stays); all choices of a categorical knob that moves the target | E3 | level-set estimation (Gotovos et al. 2013); probabilistic bisection (Frazier, Henderson & Waeber 2019) | done: `value_interval`, on; the scorer takes a planted value inside the interval (toy: test_value_interval) |
| F4 | Sequential testing on paired seeds: the j-th repeat of every configuration uses the same seed; repeats added while a gap is between 1 and 3 MDE, under an anytime-valid test; the same test cuts slow screening runs (replacing the fixed 2-band rule) | E6, D7.7 | common random numbers; anytime-valid t-tests (Wang & Ramdas); SPRT (Wald 1945) | built, **off**: on its toy (16 noise draws per variant) pairing found the planted value 11 times against 13, and once labelled a wrong answer confidently; adaptive repeats 12 against 13 |
| F5 | Paper-era code for repositories that start after the paper (the first commits, the code as first published), and HARNESS.md says why a knob is missing | E7 | time-travel environments (mining software repositories) | done: env_year.paper_era_commit, "before" or "first" commit, HARNESS.md says why (test_paper_era) |
| F6 | Large arrays memory-mapped (copy-on-write) by the runtime shim | harness | zero-copy mmap | done: runtime shim, arrays of 50 MB and more (test_runtime_mmap) |
| F7 | Group screening of mutation sites: small compatible groups in one run, split when they move every claim toward the paper | E2 | sequential bifurcation (Bettonvil & Kleijnen 1997); ProbDD (FSE'21) | done: `group_screen`, on, when no single mutant fits (toy: test_group_screen) |
| F8 | One scheduler across cause classes: each batch to the class with the highest posterior x detection gain / cost; failed screens lower a class's posterior | E1 | Bayesian search theory (Koopman, Stone); cost-aware active hypothesis testing (Vershinin et al. 2025) | done: `class_scheduler`, on, code share at most 0.3 (toy: test_class_scheduler) |
| F9 | Ties: bind every metric the target run prints and the other reported cells as claims; when no reported condition separates the tied set, the report says "not identifiable from the paper's numbers"; paper priors from MDL codelengths (a weight, never a veto) | E4 | practical identifiability (profile likelihood, Liu, Maini & Baker 2025); GLUE; MDL (Rissanen 1978) | done: the "not identifiable" note and `identifiable` in the report (toy: test_identifiability); MDL priors built, **off** (`mdl_prior`: no paper in the curriculum to measure it) |
| F10 | Curriculum: multi-claim tasks for settings; DeepCrime's real-fault operators for code and data; dev containers where reporting and library drift matter (SDCN, BOND); a reason when a family can't be planted | E4, E7 | DeepCrime (ISSTA'21); gDefects4DL (ICSE'22) | done: DeepCrime RRW, RAW, WRB, WAB and TRD on the files the run reaches; single-claim cases get a two-point paper sweep on every task, controls too; a printed reason per family (test_curriculum_deepcrime). SDCN and BOND containers deferred: 40-minute runs |
| F11 | Cheaper ledgers: the paper sliced to the target table, setup and appendix tables, adopted only if the recall harness (D3.5) shows no loss | budget | (measured, not assumed) | measured at $0, **not adopted**: over the 19 cached ledgers, input tokens are 33% of the Ultra cost (output 67%); references and related work are about 29% of the claim call's text, and that call's input is about 10% of a ledger's cost, so slicing saves about 3% (under $0.005 a ledger). Output is the cost, and the claim prompt keeps baselines and every table row on purpose |

**The full suite after F1-F10 (2026-10-22)** found four regressions, each fixed at its class:
- **F2's early code screen ran before the repo's declared alternative settings blocks.** Those blocks ran only in
  the combine round, after the early screen and F8's hold had taken their runs, and the budget ended before a
  fitting block was verified (`test_alternative_configs`, which failed 1 time in 3 on c1 and every time with F2).
  The blocks are now screened with the single settings, before either decision. Its older 1-in-3 failure had a
  second cause: after the block's early confirmation, two dozen clearly worse pairs were raced and confirmed, and
  the budget ended before the block's bisection. Once a confirmed combination fits every claim, only candidates
  within the likelihood tie margin of it get confirmation runs now. The test passes 6 of 6.
- **F2 changed which rounds run.** A patch the early screen ran that fits every claim puts the claims "in space",
  so the patch round, which adopts it, was skipped. The patch round now also runs when the joint fits hold a
  patch (`test_op_swaps`).
- **F9 counted target-only ties as alternatives.** The "not identifiable" note now counts only configurations
  no worse than the answer on every held-out claim.
- **F2's interference guard judged "off as run" with the noise floor and the model discrepancy.** A 1% gap at a
  spread of 0.001 counted as matched. It now uses the naive runs' own spread (`test_data_pipeline`). The
  no-cause toy that motivated the guard still comes out Unexplained.
- Two counterfactual tests ("without X the code isn't found") now switch F8 off, so they test only their own
  feature.

**The test round on planted seed 4 (2026-10-22, `eval/results/planted_curriculum.md`).** The batch was fresh, made
after c3 was frozen, with 13 gap tasks and 11 controls.
- **Result:**
  - c1 got 4 of 13 correct, with 1 confidently wrong;
  - c3 got 6 of 13, with 0 confidently wrong;
  - controls were 11 of 11 for both;
  - paired, c3 is better on 2 tasks and worse on none (p = 0.5).
- **Dev suite:** run 7000 (c3) got 48 of 69 against run 5000's 52 (p = 0.45), with 0 confidently wrong on both.
- **Gains:**
  - the first planted code defect found (RippleNet `np.mean` -> `np.sum`, by the mutation round);
  - c1's confidently wrong scale answer (pygcn weight decay) answered right.
- **Seed-4 misses, by class** (c3, 7 of 13):
  - 3 cut the training data (DeepCrime training-index cuts);
  - 1 shifts an evaluation split: SparseTSF's `30 -> 15` in `border1s`, the start of the validation and test
    periods (`12 * 30 * 24`). The mutation round was cut by the budget;
  - 2 are scale conventions of x0.01 that the scale probe chose and then rejected (pygcn, FastGCN);
  - 1 is a tie on pygcn's single number (`epochs=100`).
- **Plan of 2026-10-23 (c4), agreed with the owner after a review of an outside proposal.** Each item is
  class-level, has its own acceptance toy, and is judged on seed 5 (fresh). Seed 4 is dev data: re-searching it is
  a sanity check, never evidence.

| ID | Fix | Why | Status |
|---|---|---|---|
| G1 | The scale probe's "swept claims off as run" uses the naive runs' own spread, as the mutation round's guard does (one helper for both) | Seed 4: "0 of 3 off" on clear scale gaps, so no correct scale answer kept its confident label | done: one helper (`_off_as_run`) for both guards; a single naive run at a condition borrows the spread of the same metric where it was repeated (toy test_scale_probe_c4: passes, fails on c3) |
| G2 | The "not identifiable" note treats a configuration that holds the answer's knobs plus passengers (knobs whose removal leaves every claim within noise, as measured) as the same explanation. Not "drop every knob that is flat alone": a knob can matter only together with another (RippleNet's lr + l2) | Supersets of the answer were counted as rival causes | done (toy in test_identifiability: passes, fails on c3) |
| G4 | Scale probe: interpolate the measured curve on a log scale for a positive knob whose measured values span a decade; when the swept claims are off as run, a factor whose g(v) the curve can't judge (outside its range) is run, unit conventions first | The x0.01 factor was picked on both misses, then rejected by a straight-line extrapolation of the learning-rate curve to near 0 (26-32 sigma) | done: `scale_unjudged`=2, on real-valued knobs only: the full suite found x100 and x10 of an integer list length run and taking the budget (toys in test_scale_probe_c4: pass, fail on c3) |
| G5 | A data-amount operator: the training data cut to a fraction (assignments to training indices), fractions 1/2 and 3/4 | 3 of the 7 misses. The class is in published fault taxonomies (DeepCrime TRD). Its results on DeepCrime tasks are not independent of the generator, so they are reported apart | done, with operator-stratified mutant selection (Zhang et al., ASE 2013): the first mutants are taken from each class in turn (data, metric, loop, flow), because the cut ranked 32nd of 38 under metric-output mutants. Toy test_training_subset (passes, fails on c3). Found with it: a mutant the early screen ran that fits every claim never reached the round that adopts it; fixed as for patches |
| G6 | A residual-guided code proposer: one Super call, only when the deterministic rounds end with no explanation in space. The prompt has the executed lines only (from the trace), and the ratios between the paper's and the naive numbers set against traced integers (batch size, batches, sizes, 2, 10, 100). It returns at most 3 structured edits, run by the patch runner. Behind a flag | The proven pattern in program repair (localise, propose candidates, validate by execution: Agentless, AutoFL) at about $0.03 a task | built, behind `code_proposer` (CLI `--code-proposer`, curriculum `GF_CODE_PROPOSER=1`): the answer before it is kept in `pre_proposer`, so one c4 batch scores both arms. About $0.0015 a call (toys with a fake model: test_code_proposer, test_proposer) |
| G7 | Scorer: a credible-set metric beside the verdict (the planted cause in the answer or its tied set, with the set at most 3) and the reciprocal rank | Honest scoring of ties the claims can't break | done: `in_set3` and `rr` in the scorer's rows and the report |
| G8 | Curriculum: the reporting-rule family is planted only where the naive runs' best epoch and final epoch differ by more than the noise band | The rebuilt harnesses produced only controls for it | done: the case's naive runs decide, with a printed reason |

Not adopted from that review:
- A split-sum conservation check. In the curriculum the paper's side has the cut, not the code we run, and the
  standard Planetoid split uses 140 + 300 + 1000 of 2708 nodes, so the check would fire on every naive pygcn run.
- Binding test loss as a pygcn claim. The paper reports only accuracy, so this would make the curriculum easier
  than real papers.
- Adding x0.01 and x100 to the scale probe: both are already there (`UNIT_FACTORS`).
- A lookup table of breaking library defaults: a planted shim can't be found by installing old releases, which is
  what the library probe does.

**Problems with the curriculum itself:**
- Controls first took about half the slots. Fixed: at most one in five per case, and gap tasks and controls are
  scored apart.
- pygcn's tasks have one claim each (E4). Open: a multi-claim pygcn harness.
- The scorer's value tolerance (10%) is strict against the engine's coarse grid; E3 counts those cases rather than
  passing them. Open: score against a reported interval once E3 exists.
- The rebuilt harnesses offer few distinct draws (one era commit, one reporting rule, one to three package
  directories), so a new seed replants the same causes there.

**Infrastructure seen during the run (handled):**
- The machine lost DNS for minutes at a time. Task making waits for the API's name to resolve and redraws lost
  draws; searches rerun on an InfraError and resume from `run.cut*`.
- Windows killed background processes when the session ended (exit code 1073807364).
- `tests/integration/test_alternative_configs.py` fails in about 1 run in 3 on c1 as well: a flaky test, not a
  regression.

### 7.2 Done: the plans of 2026-10-19 and 2026-10-20

Details are in the commits and the modules' docstrings.

**Plan of 2026-10-19** (19 items, from the owner's 10-bottleneck plan):
- **Done (17):**
  - arXiv LaTeX source;
  - the command picker; download scripts; the metric binder; the shrink rule; loader caches;
  - the CPU shim; the GPU/size filter; static leakage checks;
  - the "stated value refuted" label; conservative significance; split variance;
  - claims at fixed knob values; learning-curve points as claims;
  - grounded operation swaps; "as in [X]" cited setups; the paper-year environment.
- **Not adopted:** Super for claim extraction. It found 27 of Ultra's 61 numeric claims on b3a.
- **Open:** the commit-mined case pool. `eval/pool/mine.py` has 33 sealed candidates and a pre-filter, but no case
  has run yet: the mined repos are mostly GPU projects.

**Plan of 2026-10-20** (D1-D7, for bottlenecks 6.1-6.6):

| ID | Capability now | Commit |
|---|---|---|
| D1.1-D1.2 | Differential over cause classes; zero-run reporting probes (best epoch, best by validation, best of N) | 158e474 |
| D1.3-D1.5, D7.2 | Paper-year packages (per-package directories, import redirect), the repo's own package, the paper-era commit; ddmin over packages, binary search over releases and commits, the call site by signature diff | 19b2039 |
| D1.6 | Data-pipeline mutants (`drop_last`, `shuffle`, split fractions, fit-on-train vs all, filter thresholds) | 19b2039 |
| D2.1-D2.3, D7.3 | Condition knobs for other datasets; the discrimination scheduler; the exact-hit guard; paper priors | 3ea5520, 41c91b6 |
| D2.4 | Scale probe on swept knobs | e07ca83 |
| D3.1-D3.5 | Numeric grounding, table grids, cell claims (deterministic part), double entry (grids), the recall harness | 456f78a |
| D4.1-D4.4 | Paper-term to flag links: BM25, the role and lesion check, used for names and conditions | 456f78a |
| D5.1-D5.4 | Mutation hook, site selection, screening on every claim, code-lead reporting | 15aaaf0 |
| D6.1-D6.3, D7.5 | CPU shim in env-build; failure reporting; CPU-time limit from the timeout; pip without a cache | 1d77dd4 |
| D6.4-D6.7, D7.6, D7.7 | Memory-aware parallelism; README procedure graph (deterministic); binding by quote; literals as knobs; miner pre-filter; multi-fidelity screening | 34e5146 |
| D7.1 | Calibration gate | 158e474 |
| D7.4 | Planted archetypes: tooling `b09e41b`, run as the curriculum (5.4) | 1c8f0f8, 894d1ef |

### 7.3 Discarded, and why

| Idea | Why |
|---|---|
| Generic preprocessing knobs (normalisation, clipping, split type) | Untargeted changes manufacture fits that look like answers (the secant step's measured harm) |
| Canary half-test (for now) | Its preconditions fail on most repos (exact determinism, a data hook, weight access) |
| Best-of-N as a reported flaw | It can't tell a best seed from a real cause; at most a note when nothing else fits |
| Merging the ledger calls into one | Brings back the appendix miss (SA-Bench; GraphMAE) |
| Symlinking datasets everywhere | A wrong-format copy silently creates a new gap |
| Patching `train_test_split` for split noise | It changes the experiment being measured |
| A penalty on configurations whose spread grows | Measured harmful: the true cause often raises the spread too |
| Curve extraction from vector PDFs (for now) | No validated accuracy; arXiv source covers about 93% of papers |
| Reproducibility-challenge reports as the main source | Measured near-zero yield; secondary only |
| A hard rule against unmentioned knobs in ties | Unstated settings are the commonest real cause; a prior instead (D7.3) |
| "Explained" from one target matched at a multiple of a stated value | The scale probe needs the same factor on every swept point |
| A global `OMP_NUM_THREADS=2` | It slows every run |
| A fixed code-round budget hold (`code_hold`, c2) | Planted seed 3: 7 of 16 vs 4, but the gains were settings, code 0 of 3; dev suite 52 -> 48 (5.4). Kept behind a flag, off |

### 7.4 Open outside the engine

- **Model calls** ($0.39 left under the $33 cap; about $12 if it is raised to the $45 the owner allows): D3.3's
  labeller, D3.4's two-pass prose extraction, D4.2's
  adjudication, D6.5's reading of prose steps. Each has its interface and a deterministic part that runs now.
- **Sandboxes:** D6.4's 1.5 GB toy on a Linux VM; the harness end to end on an unseen repo.
- **Measurement:** a fresh sealed batch, the only evidence of progress (2.1).

---

## 8. Where things are

| What | Where |
|---|---|
| Engine | `gapfinder/search/engine.py` (search, protocol tests, alternative configs, claims at fixed values `Target.at`, split variance, code rounds); `search/audit.py`; `search/trace.py`; `search/contrast.py`; `search/matcher.py`; `search/op_swaps.py`; `search/difftrace.py`; `search/mutation.py`; `sandbox/ast_patch.py`; `sandbox/runner.py` (shards and segments); `gapfinder/diagnose/` (the differential `core.py`, `reporting.py`, `library.py`, `discriminate.py`) |
| Harness tools | `gapfinder/harness_build.py` (`gapfinder harness`, end to end); `gapfinder/harness_auto.py` (its fixed rules); `gapfinder/env_year.py` (paper-year and paper-era knobs); `gapfinder/ingest/arxiv_source.py`; `gapfinder/env_build.py` (`gapfinder env-build`); `gapfinder/spec_draft.py`; `gapfinder/ingest/tables.py`; `gapfinder/ingest/links.py`; `eval/env_bench.py` |
| Sealed blind cases | `eval/external/blind-1/`, `blind-2/`, `batch3/` (b3a, b3c), `batch4/` (b4a), `batch5/`: each has `case.md`, `answer_key.md` after the reveal, HARNESS.md, the run and RESULT.md |
| Frozen batches | `eval/external/devset/` (devbatch-1; CANDIDATES.md holds answers); `eval/external/devbatch2/` |
| Planted gaps | `eval/planted/plant.py` (the first planted run); `eval/planted/curriculum.py` (`make` with `--seed`, `--control-rate`; `search` with `--seed`, `--watch`; `score` and `report` with `--seed`; `GF_CURRICULUM_RUN` names the run folder); `eval/planted/rebuild_harnesses.py` (the `-h` harnesses); tasks, sealed answers and work files in `eval/planted/curriculum/`; results `eval/results/planted_curriculum.md` and `planted_curriculum_c{1,2}_seed{2,3}.md` |
| Case pool | `eval/pool/mine.py` (miner; answers sealed in `eval/pool/sealed/`); `eval/pool/verify.py`; `eval/pool/candidates.json` |
| Measurements | `eval/claims_tier.py`; `eval/claims_recall.py` (re-grounding, table recall); `eval/links_eval.py` (dev link set) |
| Synthetic benchmark | `eval/gapbench/`; dev suite `eval/dev_suite.py`; `eval/compare_suites.py`; `eval/results/dev_suite_run*.json` |
| Tags | `blind-1`, `blind-2`, `devbatch-1`, `devbatch-2` (`e0117a2`), `planted-1`, `batch-3` (`92b1faa`), `batch-4` (`bae25f4`), `planted-c1` (`1c8f0f8`, worktree `../gf-c1`), `planted-c2` (`ca4a5e2`, worktree `../gf-c2`) |
| Learning docs | `docs/learn/` (beginner path) |
