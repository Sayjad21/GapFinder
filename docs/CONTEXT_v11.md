# GapFinder: current context (2026-10-24)

The one current document: what GapFinder is, the rules, the adopted architecture (c5), every test result, and what
is open. Superseded plans and history are in git (`git log`, the tags in section 8) and `docs/learn/07_the_journey.md`.
Paths are relative to the repo root (github.com/Sayjad21/GapFinder).

---

## 1. What GapFinder is

Given a paper and its code, GapFinder explains why running the code doesn't give the paper's numbers.
1. **Read:** Nemotron reads the paper: claims with exact quotes, and the settings they may depend on.
2. **Search:** it runs the code many times in Token Factory Sandboxes, forking from saved checkpoints, over six cause
   classes: settings, reporting rules, library releases and paper-era code, code defects, data pipeline, and
   "outside every class".
3. **Verify:** undoing the change must bring the gap back, the other reported numbers must not get worse, and the
   value needs evidence beyond the code.
4. **Report:** a Gap Report per claim: a label, a ranked differential, the evidence, replayable runs, and an audit.

**Labels:**
- confident: **Explained**, **Paper-artifact inconsistency**, **Explained by the reporting rule**;
- cautious: **Partially explained**, **Fits but unsupported**, **Explains target, conflicts with held-out**;
- no answer: **Inconclusive**, **Unexplained**, **Reproduced**.

**The owner's goal:** give it any paper (and optionally the user's own reproduction) and it finds the actual cause.
Never lying is necessary but not enough.

---

## 2. Rules

- **No patching (for the lifetime of the project).**
  - An engine change must fix a failure *class* seen on at least two papers, or add a capability published work
    shows generalises.
  - Never judge a change on the case that revealed it; progress is a rate on **fresh, frozen** batches.
  - Plumbing and measurement are allowed.
- **Evaluation** (`eval/external/BLIND_CASE.md`):
  - an independent sealer writes the answer key;
  - GapFinder is frozen (a tag, a worktree, `python -P`, the worktree's own `.env`);
  - the harness comes from the paper and the repo only;
  - the run is committed before the key is opened.
  - Development measurements (dev suite, planted curriculum) freeze the same way and are never blind evidence.
- **Sandboxes only** (never local Docker):
  - 4 vCPUs, 3.9 GB, no swap, CPU only;
  - at most 3600 s per operation;
  - about 35-40 new VMs at once is the limit seen.
- **Money:**
  - billed $32.65 of the owner's ~$50 (Nemotron only);
  - `GF_SPEND_CAP_USD=33`, which the owner allows up to $45;
  - a ledger costs $0.1-0.3, a planted round under $0.03;
  - Sandboxes are unbilled in the Beta.
- **Commits** carry no AI attribution; "write it down" means document only; never open sealed keys before the run
  is committed.

---

## 3. The adopted architecture: c5 (tag `planted-c5`, deea98f)

| Step | Module | What it does |
|---|---|---|
| Ledger | `gapfinder/ledger/`, `ingest/tables.py`, `ledger/grounding.py`, `ingest/arxiv_source.py` | Claims with quotes (Ultra, filtered by Super), grounded by number in quote, page or table (LaTeX and PDF grids); assumptions per setting; the appendix in its own call; "as in [X]" setups fetched |
| Links and repo map | `ingest/links.py`, `ingest/repo_map.py` | Paper terms to flags (BM25 with an ML lexicon, a role check on the trace, a lesion dry run); flags, defaults, commented-out alternative blocks |
| Trace | `sandbox/trace_hook.py`, `search/trace.py` | One dry run: where values land, which lines execute; knob roles and role-based candidate values |
| Zero-run probes | `diagnose/reporting.py` | Reporting rules (best epoch, best by validation, best of N) from per-epoch values |
| Library and era | `env_year.py`, `diagnose/library.py` | Paper-date packages and the paper-era commit (or the repo's first commit when it starts after the paper) as knobs; ddmin and bisection |
| Search | `search/engine.py` | Screen (multi-fidelity) **with the repo's declared alternative blocks**; then a **class scheduler** keeps up to 30% of runs for code when no setting looks likely; an **early code screen** (top literal leads, first 6 mutants) when no screened setting fits every claim; confirm (race), combine (once a confirmed combination fits every claim, only candidates within the tie margin get confirmation runs), bisect, verify; a fallback round over knobs no assumption names |
| Discrimination | `diagnose/discriminate.py` | Tied candidates separated by runs at the paper's other conditions (expected information gain); paper priors |
| History matching | `search/history.py` | Every configuration against every claim; "out of space" when none fits within 3 sigma |
| Scale probe | engine `_scale_probe` | "The paper's v is the code's c x v" on swept knobs: the curve read on a log scale for positive knobs over a decade; for an integer knob only factors that give integers; the best two factors verified in turn; factors the curve can't judge run on real-valued knobs; runs held for the verification, one per claim when short. Confident only when at least two swept claims were off as run (judged on the runs' own spread) |
| Patch round | `ingest/code_checks.py`, `sandbox/ast_patch.py`, `search/matcher.py`, `search/op_swaps.py` | Literals, defaults, switches and grounded operation swaps changed in memory; also runs when a patch the early screen ran fits every claim |
| Mutation round | `search/mutation.py` | Small edits (x2, /2, mean <-> sum, bounds, comparisons, data-pipeline switches, **the training data cut to 1/2 or 3/4**) at sites on the knobs' data flow and the **metric's output slice**; the first 6 by priority, then operator classes in turn; **group screening** of the rest when none fits; a fit counts only if it brings at least two claims that were off as run within reach; a fit is a code lead, never Explained |
| Code proposer (off) | `search/proposer.py` | When nothing fits every claim: one Super call on the executed code and the claims' ratios proposes at most 3 line edits, re-parsed and run as patches (`--code-proposer`) |
| Value intervals | engine `_value_intervals` | The answer's knob bisected on both sides to the values that fit every claim |
| Identifiability | engine `_identifiability` | "Not identifiable from the paper's numbers" when other knobs fit every claim as well as the answer (passengers of the answer don't count) |
| Caps and audit | engine, `search/audit.py`, `search/verify.py` | Confidence cap (finished search, evidence beyond code); MDE cap; protocol tests; held-out and relation checks; the audit in every report |
| Runtime shim | `sandbox/runtime_shim.py` | CPU shim; arrays over 50 MB memory-mapped copy-on-write |
| Harness | `harness_build.py` (`gapfinder harness`), `harness_auto.py`, `env_build.py` | Environment (Repo2Run-style), data, command, metric binding, knobs, fit to the VM, self-checks, claims; HARNESS.md records every choice |
| Report and app | `gapfinder/report/`, `gapfinder/api/`, `web/` | Markdown/JSON reports; a replay-only web app |

**Switches** (`SearchConfig`), on in c5:
- `early_code_screen`
- `class_scheduler`
- `value_interval`
- `group_screen`
- `scale_unjudged=2`
- `mutation_keep=6`, `mutation_max=24`

**Off:**
- `code_hold` (c2);
- `paired_seeds` and `adaptive_repeats` (F4: on their toy, 11 and 12 found against 13);
- `mdl_prior` (unmeasured);
- `code_proposer` (barely triggered, see 5.4).

**Harness status:**
- `gapfinder harness` rebuilt 5 of 6 reproduced papers' harnesses without a person; Fair Clustering's objective
  doesn't bind.
- The environment builder ran unaided on about 2 of the last 6 unseen repos.
- Not yet run end to end on an unseen repo.

---

## 4. Versions and what was adopted

Every version was frozen as a tag and worktree before the batch that judged it was made.

| Version | Tag | Main changes | Judged on | Result | Adopted |
|---|---|---|---|---|---|
| c1 | `planted-c1` (1c8f0f8) | the engine after plans D1-D7 (differential over classes, reporting/library/era probes, scale probe, discrimination, mutation hook, data-pipeline mutants) | seeds 2-4 | 12 of 43 gap tasks, 1 confidently wrong | baseline |
| c2 | `planted-c2` (ca4a5e2) | `code_hold`: runs kept for the code rounds | seed 3 vs c1 | 7 vs 4 of 16, but every gain a setting (one a pick among ties), code 0 of 3; dev suite 48 vs 52 | **no** |
| c3 | `planted-c3` (96f43d9) | F1-F10: output-slice mutation ranking, early code screen, value intervals, group screening, class scheduler, the "not identifiable" note, paper-era first commit, mmap shim; full-suite fixes (alternative blocks screened early, confirmation spent only on candidates that can still win) | seed 4 vs c1 | 6 vs 4 of 13; better on 2, worse on 0 (p = 0.5); c1's confidently wrong answer gone | **yes** |
| c4 | `planted-c4` (268e52c) | G1-G8: off-as-run on the runs' own spread, passengers not rivals, log-scale scale probe, training-subset operator with stratified mutants, the code proposer | seed 5 vs c3 | 5 vs 4 of 14, but the 3 gains were training-data cuts its own operator generated; on the other 10 tasks 2 vs 4 | **no** |
| c5 | `planted-c5` (deea98f) | H1-H4: integer-valid scale factors and the runner-up verified, the first 6 mutants in priority order, line-text proposer edits, the probe's verification fitted to the budget | seed 6 vs c3 | 7 vs 5 of 16; better on 2, worse on 0 (p = 0.5); dev suite 99 vs c1's 100 of 138 | **yes, current** |

**Not adopted from reviews:**
- a split-sum conservation check (it fires on the standard Planetoid split);
- test loss as a pygcn claim (the paper reports only accuracy);
- a library-defaults lookup table (a shim can't be found by installing old releases);
- cheaper ledgers by slicing the paper (F11, measured at $0: it would save about 3%, because output tokens are two
  thirds of the cost).

---

## 5. Results

### 5.1 Sealed blind real papers (the only clean evidence)

| Paper | Code | Documented cause | GapFinder | Score |
|---|---|---|---|---|
| FastGCN (blind-1) | v1.3 | lr 0.001 | Fits but unsupported, lr=0.005 | missed |
| GraphMAE (blind-2) | v1.4 | `alpha_l=1` (appendix table) | Explained, mask_rate=0.5 | **confidently wrong** (before the confidence cap) |
| Variational Fair Clustering (batch-3) | 92b1faa | the paper's λ=10 is wrong; the authors' value is 100 | λ=100, four claims exact | **correct** |
| SparseTSF (batch-3) | 92b1faa | `drop_last=True` in the test loader | Reproduced (-0.4%) | missed (correct abstention) |
| RippleNet (batch-4) | bae25f4 | needs lr 1e-3 and l2_weight 1e-5 | lr=0.001; l2 missed (budget) | **partial** |
| GCN topology attack (b5a) | 0586e5c | attack budget counts each edge twice | Fits but unsupported, dropout=0.5 | missed |
| SDCN (b5b) | 74b1fd1 | best epoch chosen on the labels | Unexplained | missed |
| BOND / DOMINANT (b5c) | 74b1fd1 | PyGOD API drift | Unexplained | missed |

1 correct, 1 partial, 5 missed, 1 confidently wrong (8 papers). All predate D1-D7 and c1-c5: **no sealed paper has
been run since**, so none of the planted-curriculum gains has blind evidence.

Frozen dev batches:
- devbatch-1 (5 papers): 1 correct, 0 confidently wrong.
- devbatch-2 (3 papers): 0 causes found, 3 correct abstentions.

### 5.2 Dev suite (GapBench dev tasks: 69 cause runs and 57 abstentions per run; $0, local)

| Run | Code | Cause runs correct | Confidently wrong |
|---|---|---|---|
| 5000 | c1's code (D1-D7) | 52 | 0 |
| 9100 | c1 (fresh replicate) | 48 | 0 |
| 6000 | c2 | 48 | 0 |
| 7000 | c3 | 48 | 0 |
| 8000, 8100 | c4 | 46, 50 | 0 |
| 10000, 10100 | c5 | 52, 47 | 0 |

- **Pooled over two replicates:** c1 100, c4 96, c5 99 of 138.
- **Paired, c5 against c1:** 4 tasks better, 6 worse (p = 0.75).
- Identical code swings by about ±5 per run. Every run has 57 of 57 abstentions correct.
- **No version has moved the dev suite.**

### 5.3 The planted-gap curriculum (development measurement)

**Method** (`eval/planted/curriculum.py`; results `eval/results/planted_curriculum*.md`):
- **Papers:** six papers whose code reproduces, with their hand harnesses (claims per task): pygcn (1), FastGCN (4),
  Fair Clustering b3a (8), SparseTSF b3c (8), RippleNet b4a (2), VGAE (8). Rebuilt `-h` harnesses carry per-epoch
  values, paper-year packages and the paper-era commit.
- **Tasks:** a seeded generator plants one hidden change. The "paper's numbers" are the mean of 3 runs with it; the
  search runs without it.
  - Level 1: at least 5 sd and 0.5% of the value. Level 2: 3-5 sd.
  - About one task in five is a control (nothing planted).
  - A single-claim case (pygcn) also gets a two-point paper sweep on every task.
- **Families:**
  - setting (a flag or literal at x0.25-x10, or another choice);
  - scale convention ("the paper's v is the code's c x v", with a swept pair of claims);
  - code defect (a mutation-operator edit, or DeepCrime: weight decay removed or added, a layer's bias removed or
    added);
  - data pipeline (a data-pipeline mutation, or DeepCrime: training data cut);
  - on `-h` harnesses: reporting rule, paper-era code, package release.
- **Since seed 6 (H5):** code and data tasks come from the operators frozen at c1 (`eval/planted/operators_c1.py`),
  never from the engine under test. The DeepCrime cut keeps a spread 40% or 60%, not the engine's first half or
  three quarters.
- **Search:**
  - the frozen version runs from its worktree with `--hypotheses repomap`: no paper and no ledger;
  - each task gets 150 Sandboxes runs;
  - the only model calls are name matching and, in c4 and c5, the proposer: under $0.03 a round.
- **Scoring:**
  - **Correct:** every planted part found, with a label other than Unexplained, Inconclusive or Reproduced. A
    planted value inside GapFinder's set of equal values or its value interval counts; so does a planted reporting
    rule listed among the equally good readings.
  - **Confidently wrong:** a confident label without the planted cause; on a control, any confident label.
  - Beside the verdict: "tied" (the cause among the configurations the claims can't separate), and the cause in a
    credible set of at most 3.
  - Every batch below was re-scored with the current scorer.

**Every batch** (correct / tasks; the number in brackets is how many correct answers had a confident label):

| | Seed 2 | Seed 3 | | Seed 4 | | Seed 5 | | Seed 6 | |
|---|---|---|---|---|---|---|---|---|---|
| Version | c1 | c1 | c2 | c1 | c3 | c3 | c4 | c3 | c5 |
| Scale convention | 3/4 (2) | 3/3 (3) | 3/3 (3) | 3/6 (2), 1 CW | 4/6 | 3/4 (1) | 2/4 | 1/3 | 2/3 (1) |
| Setting | 1/8 | 1/10 | 4/10 | 1/2 | 1/2 | 0/1 | 0/1 | 3/7 | 3/7 |
| Code defect | 0/2 | 0/3 | 0/3 | 0/2 | 1/2 | 1/3 | 0/3 | 0/1 | 0/1 |
| Data pipeline | - | - | - | 0/3 | 0/3 | 0/6 | 3/6* | 0/4 | 1/4 |
| Reporting rule | - | - | - | - | - | - | - | 1/1 (1) | 1/1 (1) |
| **All gap tasks** | **4/14** | **4/16** | **7/16** | **4/13** | **6/13** | **4/14** | **5/14** | **5/16** | **7/16** |
| Confidently wrong | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| Controls correct | 11/11 | - | - | 11/11 | 11/11 | 9/9 | 9/9 | 9/9 | 9/9 |
| Cause in a credible set of 3 | 2 | 4 | 4 | 3 | 4 | 3 | 3 | 2 | 5 |

\* Two of c4's three data hits were planted with c4's own new operator (the generator then drew from the engine's
operators), so they don't count as evidence. H5 fixed the generator.

**Paired, same batch:**

| Comparison | Better | Worse | Sign test p |
|---|---|---|---|
| c2 vs c1 (seed 3) | 4 | 1 | 0.38 |
| c3 vs c1 (seed 4) | 2 | 0 | 0.5 |
| c4 vs c3 (seed 5) | 3 | 2 | 1.0 (gains circular) |
| c5 vs c3 (seed 6) | 2 | 0 | 0.5 |

**What each round showed:**
- **Seeds 2-3 (c1, c2):**
  - scale conventions found; settings mostly missed (ties on few claims, values off the grid);
  - code defects 0 of 5, because the code rounds were starved by the run budget and the planted sites ranked out;
  - data, reporting, era and library draws never moved a target by 3 sd.
- **Seed 4 (c1 vs c3):**
  - first planted code defect found (RippleNet `np.mean` -> `np.sum`, mutation round);
  - c1's confidently wrong scale answer fixed;
  - c3 lost confident labels on scale answers, through a guard that used the noise floor.
- **Seed 5 (c3 vs c4):**
  - c4's losses were its own: stratified mutants displaced a planted constant from the early screen, and the log
    scale chose an unrunnable 1/3 factor on epochs;
  - the proposer's edits mostly didn't parse (7 of 8).
- **Seed 6 (c3 vs c5):**
  - c5 found a spread 60% training-data cut on VGAE at its site, and FastGCN's epochs convention;
  - confident labels came back on a scale convention;
  - the proposer ran twice, because it triggers only when nothing fits.
  - Infrastructure: four pygcn searches failed on a Sandboxes operation error and were resumed; that error is now
    retried.

**By kind of gap, in the adopted line (c1 -> c3 -> c5):**
- **Scale or unit conventions: mostly found** (c1 9 of 13, labelled as paper-code inconsistencies).
- **Settings: about 3 in 10.** Most misses are ties the claims can't break (pygcn's single number) or values off
  the grid (`test_ratio=0.05`, `test_percent=7.5`).
- **Code defects: from 0 of 7 (c1) to the first ones found (c3: 2 of 6).** c5 missed its one, a layer bias added,
  which no operator does.
- **Data pipeline: from 0 of 13 to 1 of 4 independent training-data cuts (c5).** The engine's 1/2 and 3/4 don't
  match a spread 40% or 60% within noise.
- **Reporting rule: 1 of 1** (both c3 and c5).
- **Never tested:**
  - paper-era code and package releases (never plantable on these papers);
  - two-cause tasks and causes outside every family (levels 3-5: the level-1 gate, 70%, was never passed; the best
    is 44%).
- **Honesty:** one confidently wrong answer in 132 gap-task searches over 73 distinct tasks (c1, seed 4); all 69
  control searches correct.

**The limit of these tests:**
- Each comparison had 13-16 gap tasks, and only 2-5 tasks came out differently between two versions. A sign test
  can't reach p < 0.05 below 5 differing tasks, so **no comparison could show a significant difference**, and none
  did.
- The adopted steps went +2 with 0 losses twice (4 and 0 together, p = 0.13).
- c5 has never been run against c1 on the same batch.

---

## 6. Open

### 6.1 Plan of 2026-10-24 (c6), from seed 6's misses and an outside review

The review's numbers were checked against the code. Its MDE arithmetic assumed df = n - 1 (ours is 2n - 2), its
x0.01 factor was already probed, and its "starvation" chain is only part of the story: two of the four misses had
no lead to starve.

The seed-6 misses (c5, 9 of 16) are mostly one chain:
- a setting matches the few reported numbers by coincidence;
- the settings stages spend the 150 runs confirming it, before the code stages screen the planted constant;
- the fit, though unsupported, keeps the proposer from running.

Each item is class-level with its own toy, and is judged only on a fresh seed 7. Nothing is guaranteed in advance.

| ID | Change | For | Status |
|---|---|---|---|
| I1 | The early code screen right after the settings screen **always**, not only when no setting fits every claim | 4 misses that hit the budget (pygcn lr, RippleNet `test_ratio`, VGAE `test_percent`, RippleNet x2) | built, **off** (`early_code_always`): its toy showed no difference, and where a setting fits every claim a constant screened early can only join the tie. The toy found the real cause of the `test_ratio`/`test_percent` misses instead: split constants were **no leads** (no split word in the lead vocabulary) and their values were **off the patch ladder**. Fixed: split words in `code_checks` (`ratio`, `percent`, `frac`, `split`, ...), and `_lead_secants`, the crossing of a lead's bracketing values screened as the settings secant does (toy test_c6_toys I1: passes, fails on c5) |
| I2 | The code proposer runs on any non-confident result (Fits but unsupported included), with runs held for its edits | 7 of 9 misses never reached it | done: an edit that fits as well as a fitting answer joins the tie, it doesn't replace it (toy I2: passes, fails on c5) |
| I3 | A training-data cut's fraction from the measured cut: the secant through the naive run and the cut, snapped to 0.05 in [0.2, 0.95], one run | 3 cuts at 40% and 60% missed by the fixed 1/2 and 3/4 | done, **on a log scale of the fraction**: the review's straight-line secant put a 40% cut at 30% (learning curves are near linear in log n) (toy I3: passes, fails on c5) |
| I5 | A structural-switch operator: boolean constructor keywords (`bias`, `use_bias`, `affine`, `elementwise_affine`, `track_running_stats`, `normalize`, `residual`) flipped, or set False where the layer's default is True | a layer bias (no operator). DeepCrime WRB/WAB plant the same edit, so those tasks are reported apart | done: its own operator class in the mutation round (toy I5: passes, fails on c5) |
| I4 | Curriculum: plant gaps of at least 1% of the value, the engine's reproduce floor (it was 0.5%) | SparseTSF's bias: 5 run-sd but under 1%, so "Reproduced" | done (`MIN_REL` in curriculum.py) |
| I6 | Evaluation: a fresh seed 7 of about 45 gap tasks (4 tasks per case and level on the hand harnesses, 2 on `-h`), c5 against c6, both frozen. Stated before it runs: a sign test reaches p < 0.05 with at least 6 tasks differing all one way, or 8 of 9 | the tests so far couldn't show significance | todo: about 12 hours of Sandboxes, waiting for the owner's go |

Not adopted from the review, and why:
- **Lowering the 1% reproduce floor to 2.5 run-sd.** The floor keeps real papers from chasing environment noise
  between the paper's machine and ours, which the planted tasks don't have. I4 aligns the curriculum to it
  instead.
- **Five confirmation runs instead of three.** The review's arithmetic assumed df = n - 1; our MDE uses df = 2n - 2,
  and more repeats cost the budget the starvation is about.
- **The model ranking tied candidates.** The curriculum has no paper text and draws its causes uniformly, so this
  can't be measured, and the rule forbids tuning tie-breaks on dev cases.
- **Judging c6 on seeds 4-6 pooled.** Those seeds revealed these errors, so they are a sanity check, never evidence.
- **Crediting VGAE's `test_percent=60` as the planted cut.** A cause at another line is a near miss, not the
  planted site.
- **Two or three claims per task, with validation loss.** pygcn already gets a paper sweep, and papers don't report
  test loss.
- **Era and library tasks from commits that change constants.** The era family means the code as of the paper's
  date, and a later commit's constant is the code family; deferred.

### 6.2 Other open items

- **Measurement first:**
  - a fresh batch large enough to detect a difference: about 50 gap tasks (more tasks per case and level, more
    cases), with the detectable effect stated before it runs;
  - c1 run on seed 6 for a direct c1-vs-c5 comparison (fair: seed 6 was made after every version was frozen);
  - a sealed real paper on c5.
- **Engine classes still missed:**
  - training-data cuts at fractions the operator doesn't try;
  - structural switches (a layer's bias);
  - literal split fractions off the grid;
  - settings ties on single numbers (only more reported numbers can fix these).
- **The code proposer:** unmeasured. It triggers only when nothing fits every claim (twice on seed 6).
- **Harness:** end to end on an unseen repo; SDCN and BOND containers for the reporting and library families
  (40-minute runs).
- **Model-dependent parts not run (budget):** the claim labeller, two-pass prose extraction, link adjudication,
  prose-step reading.

**Discarded** (details in git):
- generic preprocessing knobs;
- the canary half-test;
- best-of-N as a flaw;
- one merged ledger call;
- symlinked datasets;
- patching `train_test_split`;
- a spread penalty;
- vector-PDF curve extraction;
- reproducibility reports as a main source;
- a hard rule against unmentioned knobs;
- "Explained" from one matched multiple;
- a global `OMP_NUM_THREADS`;
- `code_hold`;
- paired seeds and adaptive repeats (on their toy, 11 and 12 found against 13);
- operator stratification of the first 6 mutants (seed 5).

---

## 7. Where things are

| What | Where |
|---|---|
| Engine | `gapfinder/search/engine.py`; `search/mutation.py`; `search/proposer.py`; `search/audit.py`, `trace.py`, `contrast.py`, `matcher.py`, `op_swaps.py`, `difftrace.py`; `sandbox/ast_patch.py`, `runner.py`, `runtime_shim.py`; `gapfinder/diagnose/` (`core.py`, `reporting.py`, `library.py`, `discriminate.py`) |
| Harness | `gapfinder/harness_build.py`, `harness_auto.py`, `env_year.py`, `env_build.py`, `spec_draft.py`; `gapfinder/ingest/` |
| Sealed blind cases | `eval/external/blind-1/`, `blind-2/`, `batch3/`, `batch4/`, `batch5/` |
| Frozen batches | `eval/external/devset/` (CANDIDATES.md holds answers), `eval/external/devbatch2/` |
| Planted curriculum | `eval/planted/curriculum.py` (`make`, `search`, `score`, `report`, all with `--seed`; `GF_CURRICULUM_RUN` names the run folder; `GF_CODE_PROPOSER=1`); `eval/planted/plant.py`; `eval/planted/operators_c1.py`; `eval/planted/rebuild_harnesses.py`; tasks and sealed answers in `eval/planted/curriculum/` (untracked); results `eval/results/planted_curriculum.md` and `planted_curriculum_c{N}_seed{S}.md` |
| Dev suite | `eval/dev_suite.py --base N --code <worktree>`; `eval/compare_suites.py --a ... --b ...`; `eval/results/dev_suite_run*.json` (runs live in the code worktree's `eval/gapbench/runs/`) |
| Other measurements | `eval/claims_tier.py`, `eval/claims_recall.py`, `eval/links_eval.py` |
| Tags and worktrees | `planted-c1` 1c8f0f8 `../gf-c1`; `planted-c2` ca4a5e2 `../gf-c2`; `planted-c3` 96f43d9 `../gf-c3`; `planted-c4` 268e52c `../gf-c4`; `planted-c5` deea98f `../gf-c5` (copy `.env` into a new worktree); also `blind-1`, `blind-2`, `devbatch-1`, `devbatch-2`, `batch-3`, `batch-4`, `planted-1` |
| Learning docs | `docs/learn/` |
