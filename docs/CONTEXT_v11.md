# GapFinder: current context (2026-10-18)

This replaces the earlier version-by-version notes. It says what GapFinder is, what it can and can't do
today, every measured result, why the real-paper results are what they are, and the decision about how to
improve it. Paths are relative to the repo root (github.com/Sayjad21/GapFinder). The full history is in git
and in `docs/learn/07_the_journey.md`.

---

## 1. What GapFinder is

Given a paper and its code, GapFinder explains why running the code doesn't give the paper's numbers.
1. **Reading:** Nemotron reads the paper and lists its claims and the settings they may depend on.
2. **Searching:** it runs the code many times in Token Factory Sandboxes, forking from saved checkpoints,
   and changes one thing at a time.
3. **Verifying:** it checks the best candidate three ways (undo it, other numbers mustn't get worse, the
   value must have evidence).
4. **Reporting:** a Gap Report, per claim: a label, the evidence, and replayable runs.

**Labels:**
- confident: **Explained**, **Paper-artifact inconsistency**;
- cautious: **Partially explained**, **Fits but unsupported**, **Explains target / conflicts with held-out**;
- no answer: **Inconclusive**, **Unexplained**, **Reproduced**.

### What a user must provide today

1. **The paper** (PDF).
2. **The code** (a repo at a commit).
3. **A harness**, written by a person or an agent per paper:
   - `case.json`: how to build the Sandboxes image;
   - `spec.yaml`: the run command, the settings it may change, and their defaults;
   - `harness/emit.sh`: how to read the metric from the program's output.
4. **`targets.json`:** the paper's numbers, which ones are held-out checks, and which ones the paper tuned
   separately.
5. **A run budget** and API keys.

Items 3 and 4 are manual. That is the main reason it isn't usable on "any paper" yet (section 6).

### Constraints

- **Sandboxes only** (user decision): 4 vCPUs, 3.9 GB RAM, no swap, at most 3600 s per run, internet only
  during the image build. Running several searches at once slows each VM to about one CPU.
- **Money:** billed so far **$30.40** of about $50 (Nemotron only). A ledger costs about $0.1-0.3; the
  contrast step costs cents. Sandboxes are unbilled in the Beta (they report a diagnostic cost).
  `GF_SPEND_CAP_USD` is set per process, and the sandbox guard has to be raised for searches.
- **Evaluation:**
  - never open a sealed key before the run is committed;
  - no engine change between a freeze tag and its reveal;
  - post-hoc runs are always labelled post-hoc and never counted;
  - "write it down" means document only.
- **Commits:** no AI attribution in commits or pushed files.

---

## 2. Architecture (what runs, in order)

| Step | Module | What it does |
|---|---|---|
| Ledger | `gapfinder/ledger/` | Claims with exact quotes (Ultra, filtered by Super). Assumptions per setting. A stated paper number must appear in a paper quote. Hyperparameter tables anywhere in the paper are appended to the prompt. |
| Repo map | `gapfinder/ingest/repo_map.py` | Flags and defaults: argparse, C++ gflags, absl / tf.app.flags. |
| Runtime trace | `gapfinder/sandbox/trace_hook.py`, `gapfinder/search/trace.py` | One dry run records where config values land (optimizer lr, dropout, batch size, Linear width, loop bounds, seeds). Gives each knob a role (rate, fraction, size, count, multiplier, seed), which sets its candidate values. Seeds are never hypotheses. |
| Candidate values | `gapfinder/search/hypotheses.py` | By role, or by name rules as a fallback: choices, a coarse-first ladder, multiplier factors, edge values. |
| Search | `gapfinder/search/engine.py` | Screen, confirm (racing), combine (pairs, a forward step), bisect, verify. Plus: a **secant step**, only when no screened value fits every claim; a **fallback round** for spec knobs no assumption names and for knobs whose stated value matches the naive run; escrow for confirmation. |
| Verification | `gapfinder/search/verify.py` | Counterfactual; held-out claims (a claim tuned separately is a note, not a veto); relation claims (a stated direction must not reverse); evidence (paper, docs or web; code alone doesn't count). |
| Confidence cap | `engine._cap_confidence` | A confident label needs a finished search, every knob screened, and evidence beyond source code. Otherwise "Fits but unsupported". |
| History matching | `gapfinder/search/history.py` | Every configuration against every claim. The discrepancy allowance comes from the spec (`discrepancy`), and is 0.01 at full scale. |
| Code causes | `gapfinder/ingest/code_checks.py`, `gapfinder/sandbox/ast_patch.py`, `gapfinder/search/contrast.py` | **Static leads:** hard-coded numbers, parameter defaults no call overrides, seeds, split fractions, selection loops. **Contrast:** one Super call matching paper statements to the traced run, grounded to file:line and a verbatim paper quote. **Patch round:** literals and defaults changed in memory, no file edited. Runs when the case is out of space, or the answer is unsupported and leads exist. A patch replaces an answer only with a strictly better label. |
| Report and app | `gapfinder/report/`, `gapfinder/api/`, `web/` | Markdown/JSON report. A replay-only web app (no live runs). |

---

## 3. Results

### 3.1 Synthetic benchmark (GapBench)

| Measure | Result |
|---|---|
| **Sealed tests v1.1-v1.3** (30 runs each) | 0/90 confidently wrong; causes found in 7, 12 and 9 of 15 runs; abstentions 15/15 each time |
| Coding-agent baseline, same tests | confidently wrong in 49 of 90 runs |
| **Dev suite**, 23 public tasks × 3 runs, two replicates | 102/138 at `blind-1` → 99/138 now (`2af0c3a`); the same within noise, 0 confidently wrong, abstentions 114/114 |

The changes since v1.4 neither helped nor hurt here: the practice tasks don't exercise real-repo problems.

### 3.2 Real papers

| Case | Kind | Code | Result |
|---|---|---|---|
| MC Dropout | known answer | v1.3 | names the documented `epochx=10, hidden=1`; "conflicts with held-out" + out of space |
| **blind-1 FastGCN** | sealed blind | v1.3 | **missed:** "Fits but unsupported: lr=0.005", documented 0.001 (not confident) |
| **blind-2 GraphMAE** | sealed blind | v1.4 | **confidently wrong:** "Explained: mask_rate=0.5", documented `alpha_l=1` (ran in Docker: COLLAB doesn't fit Sandboxes) |
| FastGCN | post-hoc | current | names lr=0.001 with the paper's sweep sentence as evidence; capped to "Fits but unsupported" because the budget ran out in the pair stage |
| **VGAE** (devset) | known answer | current | **found end to end:** "Paper-artifact inconsistency", the `mask_test_edges` defaults 30/20 → the paper's 10/5, all 8 claims |
| pygcn (devset) | known answer | current | Unexplained (+2.5%); the cause is code structure |
| **devbatch-1** (5 papers) | frozen, known causes not shown to the harness writers | `devbatch-1` = `2af0c3a` | **1 of 5 correct, 0 confidently wrong** (below) |

**devbatch-1 in detail** (`eval/external/devset/<case>/`, reports in `run/` or `run2/`):

| Paper | Documented cause | GapFinder | Score |
|---|---|---|---|
| G-Mixup, IMDB-B | gain is noise | Reproduced | correct (abstained) |
| GIN, IMDB-B | `--degree_as_tag` + pooling | Inconclusive (-1.6% left) | miss. The README's command already contained the main fix. Contrast found the paper's epoch-selection protocol. |
| GAT, PubMed | lr 0.01, L2 0.001, 8 output heads | Fits but unsupported, lr=0.05 | miss, not confident. Ledger names didn't map to knobs, so the paper's values never became evidence. |
| Informer, ETTh2 | per-dataset hyperparameters | Unexplained (-31%) | miss. Only 28 runs fit the time budget. Contrast flagged the encoder/decoder layer counts. |
| PatchTST, ETTh1 | `drop_last=True` in the test loader | Unexplained | miss: true/false literals aren't leads or patch values |

---

## 4. What keeps it from generalising

Some blockers stop it from *running* on a new paper at all (4.1, 4.6, 4.7). Others make it run but miss
(4.2-4.5), or make the results hard to trust (4.8, 4.9). In order of impact:

### 4.1 The harness (the biggest blocker to "any paper")

**What it is.** Before GapFinder can search, someone must tell it how to run this paper's experiment. Today
that is five hand-written files per paper:

| File | Content | Typical work |
|---|---|---|
| `case.json` | Python version, pinned packages, repo commit, dataset download, for the Sandboxes image | trial and error: old TensorFlow/PyTorch pins, missing data files (GAT's PubMed, PatchTST's CSV), broken system libraries (G-Mixup needed headless OpenCV) |
| `spec.yaml` | the command for one run, every knob with its default, timeout, metrics; the seed taken from the run tag | finding the experiment's entry point and the README's command; deciding which flags define the claim (dataset, model) and which are knobs |
| `harness/emit.sh` | how to read the metric from the output | each repo prints differently; some pick nothing (G-Mixup logs every epoch, so the harness had to choose "test accuracy at the best validation epoch") |
| `targets.json` | the paper's target number, held-out numbers, which rows were tuned separately | reading the paper's tables; deciding from the paper's text whether each row shares one setting |
| `HARNESS.md` | every decision and deviation | writing it honestly |

It takes about 30-90 minutes per paper, for a person or an agent.

**Why it limits generalisation, not just convenience: its choices change the answer.**
- **Which run is "naive"** (the starting point every candidate is compared against):
  - VGAE needed the paper's model (`gcn_vae`), not the repo's default (`gcn_ae`);
  - for GIN, the README's command already contained the main documented fix (`--degree_as_tag`), so little
    gap was left to explain.

  The same paper can look "solved", "reproduced" or "unexplained" depending on this choice.
- **Which numbers are held out, and which are tuned separately.** blind-1 failed because one learning rate
  was shared across rows the paper had tuned separately. Getting this right needs a careful reading of the
  paper.
- **Scope and scale.** Cutting datasets, folds, seeds or epochs to fit Sandboxes changes noise and sometimes
  the cause. G-Mixup's label depended on one seed against two per run. PROTEINS was cut from GraphMAE, and
  REDDIT-B and NCI1 everywhere.
- **Which knobs exist.** "Every flag" is mechanical for argparse. For module constants (GAT) or config files
  (GraphMAE's `configs.yml`, which overrides its flags) the harness writer has to invent a way to set them,
  and that is a judgment call.
- **Bias risk.** A writer who knows the answer can shape any of the above toward it, which is why devbatch-1
  hid the causes from its harness agents.

**What automating it needs** (the devbatch-1 agents showed it's feasible):
1. build the image by iterating on install errors;
2. find the experiment's command from the README and scripts;
3. write and test the metric parser;
4. check itself:
   - the metrics parse;
   - two seeds give different numbers (noise exists);
   - it fits in 3.9 GB and an hour;
   - every flag is a knob;
   - the naive run matches the README's command for the table's row;
5. write HARNESS.md.

The two judgment calls (the naive run, and tuned-separately) should be stated, with the paper's sentence,
for a person to confirm.

### 4.2 Reading the paper (the ledger)

Everything downstream depends on what Nemotron extracts, and it is the least reliable step.
- **Missed content:** GraphMAE's per-dataset values lived in appendix Table 8, after the prompt's cut-off.
  Tables are now appended, but figures, footnotes and "following [X]" references still aren't read.
- **Its own names for settings:** FastGCN's `num_epochs` for `epochs`; GAT's `num_attention_heads`,
  `l2_reg_lambda` and `early_stopping_patience` for `n_heads`, `l2_coef` and `patience`. When names don't
  map, the paper's stated values never become evidence for the right knob. Twice now, so it is a recurring
  class. The structural fix is to give the ledger the code's knob names.
- **Values taken from code, reported as the paper's:** GraphMAE's `alpha_l` "2.0". Now caught when the
  number isn't in the quote.
- **Variance:** the same paper gave 28 assumptions one day and 9 the next (FastGCN), with different names.
  Results depend on which reading came out.

### 4.3 Causes in code structure

A different normalisation (pygcn), a split procedure (pygcn), model selection on the test set (GIN's
protocol, Errica et al.), `drop_last=True` in an evaluation loader (PatchTST), per-split re-tuning (MC
Dropout).
- **What GapFinder can do:**
  - change settings, numeric literals and function defaults in memory;
  - *point to* structural differences, through static checks and the paper-to-trace contrast.
- **What it can't do:** test structural differences. That is deliberate: rewriting code until the number
  fits would explain nothing. So these papers end as "Unexplained" or "out of space" with leads, at best.
- True/false literals (`drop_last = True`) aren't leads or patch values yet. Seen once.

### 4.4 Identifiability (too few numbers)

A paper often gives one or two numbers per experiment, and several different changes can hit them equally
well:
- GraphMAE: `mask_rate=0.5` fit as well as the true `alpha_l=1`;
- VGAE: bigger hidden layers partly made up for the changed edge split;
- GAT: `lr=0.05` against the documented lr + L2 + heads combination.

The confidence rules make this a cautious "Fits but unsupported" instead of a wrong "Explained", but they
can't turn it into the right answer. Only more numbers, the paper's stated relations, or the paper's own
values as evidence break the tie, and many papers simply don't provide enough.

### 4.5 History matching tolerances

How far a configuration may sit from the paper and still "fit" decides whether a case is "reproduced", "in
space" or "out of space".
- **The discrepancy allowance:** 5% hid every real gap below about 15% until it became 1%. 1% is still a
  judgment call. pygcn's 2.5% gap was called "within noise".
- **The paper's own uncertainty:** each paper number is treated as one noisy run, even when the paper
  averaged 10 or 100 runs, which overstates the paper's uncertainty.
- Both shift the diagnosis on small gaps, which are common in real papers.

### 4.6 Compute: Sandboxes limits

- **CPU only.** Most current ML papers need a GPU, so they are out of scope as they are. Others must be
  scaled down, which can hide or change the cause.
- **3.9 GB RAM, no swap:** GraphMAE's COLLAB couldn't even load.
- **At most 3600 s per run.** Informer and GAT runs took 15-50 minutes, so a search affords only a few dozen
  runs.
- **Shared capacity:** with five searches at once each VM delivered about one CPU, runs took 3-4× longer,
  and budgets collapsed (Informer got 28 runs). A batch should run two or three papers at a time.

### 4.7 Environment and data

- Old code needs old stacks: TF 1.15 on Python 3.7, dgl < 1.0, torch 1.x. Pins conflict, wheels disappear,
  base images lack system libraries.
- Datasets are often not in the repo (Google Drive bundles, PyG downloads, other repos' files), and must be
  fetched at build time.
- Some repos don't contain the paper's model at all: G-Mixup's has no GCN, so the case had to switch rows.

Each of these is solvable per paper, but each needs a person or an agent.

### 4.8 Measuring it at all

- **Sample size:** 2 blind real papers and a 5-paper batch. A rate on 5 papers is noisy (1/5 could be 0/5 or
  2/5 next time).
- **Answer keys:** documented causes are themselves sometimes partial (FastGCN's owner gave lr *and* maybe
  epochs; GraphMAE's fix commit also changed pooling), so scoring needs judgment.
- **Leakage:** dev-set papers have known answers. Anyone who has read them (including the builder) can bias
  harnesses or fixes, so only fresh, sealed papers give clean numbers.
- **The synthetic suite doesn't reflect real-paper problems:** it stayed flat (99-102/138) through every
  real-paper improvement, so it guards against regressions but can't show progress.

### 4.9 Infrastructure that broke under real use

- **Parallel processes tore a line in the shared spend ledger,** and every search crashed until it was
  repaired. It needs a file lock.
- **"Frozen" code wasn't frozen at first:** `python -m` imported the main checkout. A frozen worktree needs
  `python -P` and its own `.env`.
- **Provenance records the current folder's commit,** not the code that ran.
- **Agent sessions hit the account's usage limit and stopped mid-run.** Long searches must run as
  independent processes that survive the agent.

---

## 5. The decision: stop patching, measure

Each real paper so far exposed a new failure, and each fix made that paper pass post-hoc. That loop never
converges, and it proves nothing.

**Rules from here on:**
- **No fix is judged on the paper that revealed it.** Post-hoc reruns show only that a fix does what it was
  built to do.
- **Progress is a rate on fresh papers.** Freeze the code, run a new batch nobody has looked at, report
  found / missed / confidently wrong. Compare with the previous batch (devbatch-1: 1/5, 0 wrong).
  - A rising rate means the changes generalise.
  - A flat rate, with new failure kinds each batch, means the approach must change.
- **Fix only failure classes that recur across papers,** and prefer fixes that remove a class over fixes
  that handle a case. Example: give the ledger the spec's knob names, rather than growing a synonym list.
- **Accept the ceiling.** Structural causes and identifiability cap the rate at perhaps half of real papers.
  Past that, the honest product answer is "here is where to look, with evidence".

**Known issues, not yet fixed, kept here instead of patched:**
- **Recurring class (FastGCN, GAT):** ledger names don't match the code's knob names. Structural fix:
  include the spec's knob names in the assumption prompt.
- **Plumbing:**
  - the spend ledger needs a file lock (parallel processes tore a line, repaired losslessly);
  - provenance reports the current folder's commit, not the code that ran;
  - a frozen worktree needs `python -P` and its own `.env`.
- **Seen once, park:** true/false literals as leads; the paper's "mean of N runs" in history matching.

---

## 6. The product question

"Give it any paper (and my own reproduction), get the bug or a report." No product does this today. Nearby
work runs papers' code (CORE-Bench), judges reproducibility (REPRO-Bench) or plans runs (PaperDoctor); none
explains a gap with verified experiments.

What is missing, biggest first:
1. **An automatic harness builder:** build the image, find the experiment's command, write the metric parser,
   and check itself (metrics parse, seeds vary, it fits Sandboxes). The devbatch agents built five harnesses
   from short briefs, so this is feasible.
2. **GPU support:** most modern papers need it.
3. **"Compare with my code" mode:** run the user's implementation and the official one side by side and find
   where they diverge.
4. **A live service:** upload, queue, per-user budgets.
5. **A measured rate on unseen papers.**

---

## 7. The no-patching rule, and what is allowed to change

**Set by the owner on 2026-10-18, for the lifetime of the project** (also in the git-ignored `CLAUDE.md`):
- **No engine change to make a specific paper or task pass.**
- **A change is allowed only if it does one of these:**
  - fixes a failure *class* seen on **at least two different papers**;
  - adds a capability that **published work** shows generalises.

  Prefer removing a class over handling a case.
- **Never judge a change on the case that revealed it.** Post-hoc reruns count as nothing.
- **Progress is a rate on a fresh frozen batch,** compared with the previous one (devbatch-1: 1/5 correct,
  0 confidently wrong).
- **No tuning of tie-break or selection rules on GapBench or dev-set cases.** Every past attempt was neutral
  or harmful.
- **Plumbing and measurement infrastructure are allowed.**

### 7.1 Assessment of the pasted "host-side" proposal (2026-10-18)

It was written against the v1.1/v1.2 logs, so much of it describes problems that are already solved or
measured.

| Proposal | Status today | Verdict under the rule |
|---|---|---|
| 1. Type knobs from how the code uses them, not regex names | Done, more strongly: the runtime trace types knobs from the call their value reaches (optimizer, dropout, loop, seed). The name rules are only a fallback. | Nothing to add. A static AST typer could back up the trace when no dry run is possible, but that is low value. |
| 2A. Stop screening flat knobs after 2 coarse probes | Done (`coarse_stop_bands`, coarse-first ladder). | Nothing to add. |
| 2B. Secant interpolation to the paper's value | Done, and **measured harmful** when always on: it manufactured exact-fit decoys (102 → 92 of 138). Now runs only when nothing fits every claim. | Already settled. |
| 2C. Confirm a promising pair immediately during combine | Not done. A general "anytime" budget rule (confirm leads when they appear). | **Plausible as a class:** budget ran out before confirmation on MC Dropout, FastGCN post-hoc and Informer. It must be measured on a fresh batch, not on MC Dropout. |
| 3A. Penalise configurations whose run-to-run spread inflates | **Rejected before, with data:** the true cause often inflates spread too. | Rejected (tuning; measured "don't"). |
| 3B. Solo-effect gate for passengers in bisect | Tie-break tuning on specific GapBench tasks (v12-08, v11-10). | **Rejected: this is patching.** |
| 3C. Soft ledger prior inside the likelihood tie | Value-level priors were rejected with data: 45% of true values come from coverage only. | Rejected. |
| 4. Match code-check literals against the ledger's paper values, deterministically | Partly done, through the contrast step (an LLM, grounded to file:line and a verbatim quote). | **Plausible:** a deterministic matcher is general and costs $0. But it rests on name matching, the recurring weak spot (4.2), so it inherits that class's fix. |

**Overall:** the proposal doesn't touch the blockers that actually stop generalisation: the harness, reading
the paper, causes in code structure, and measurement. Most of it is search tuning, which the rule forbids.

### 7.2 Existing work that addresses the real blockers (web search, 2026-10-18)

| Blocker | Existing work | What it gives us |
|---|---|---|
| 4.1 Harness / environment | **Repo2Run** (NeurIPS 2025: an agent that iteratively builds Docker images until the repo runs; 86% on 420 Python repos, far above SWE-agent); SWE-Factory, SetupX, EnvPilot; CORE-Bench agents (reproducing outputs from repos is largely saturated) | An automatic harness builder is a proven, general capability. Add our own checks: metrics parse, seeds vary, it fits Sandboxes. |
| 4.2 Reading the paper | **SA-Bench** (2026: single-call extraction skips appendices because attention decays over long papers); **HyperPIE** (hyperparameter extraction as entities + relations; structured YAML beats JSON); **AutoReproduce** (ACL 2026: "paper lineage" pulls settings from cited papers) | Extract section by section, appendix included, with a structured hyperparameter schema, and follow citations for inherited settings ("following [X]"). |
| 4.3 Causes in code structure | **Delta debugging** (Zeller: isolate the minimal difference between a working and a failing version, combinations included); **TTrace** (2025: compare a reference run tensor by tensor, and the first diverging module is the suspect); **TrainCheck** (OSDI 2025: inferred training invariants, 18/20 silent bugs); Paper2Code and AutoReproduce (generate a paper-faithful implementation) | **Differential testing:** with a second implementation (an independent public one, or one generated from the paper), structural causes become testable: localise where the two runs diverge, then delta-debug the minimal difference. This is also the product's "compare with my code" mode. |
| 4.4 Identifiability | TTrace's lesson: intermediate signals (curves, tensors) carry far more information than a final number | Use the paper's figures (learning curves) and intermediate metrics as extra claims. |
| 4.5 Noise tolerances | **Bouthillier et al.** (MLSys 2021): data-sampling, initialisation and hyperparameter variance all matter, and counting them gives fairer comparisons | Our noise varies only the seed, so it should also vary the data split where the protocol allows. |
| 4.8 Measuring | CORE-Bench, PaperBench, LMR-Bench, REPRO-Bench | Pools of real papers whose code runs. |

### 7.3 The plan (each item names its class or source)

1. **Plumbing** (allowed): a lock on the spend ledger, and provenance from the code that ran.
2. **Paper reading** (classes: an unread appendix, GraphMAE, with SA-Bench as the published cause; ledger
   names vs code names, FastGCN and GAT):
   - extract section by section, appendix included;
   - give the assumption step the spec's knob names.
3. **A measurement benchmark on real repos** (allowed, infrastructure): take repos that already run, plant
   one setting or one code change with a known answer, and score GapFinder on it. This gives a rate on real
   code without waiting for rare documented reproduction gaps.
4. **An automatic harness builder** (Repo2Run-style; published capability).
5. **Differential testing against a reference implementation** (TTrace and delta debugging; published).
6. After each of 2-5: freeze, and run a fresh batch. Compare the rate.

### 7.4 Progress on the plan (2026-10-18)

Done, each with tests (full suite 279 passed):
- **Item 1:** ledger lock (`57d6dce`).
- **Item 2, both parts** (`7e46e31`):
  - the appendix is read in its own assumption call and merged; a stated value beats "unstated";
  - ledger names that match no knob are mapped by meaning, one Super call; only existing knob names are
    accepted; skipped offline and in cache-only mode, so dev-suite runs are unaffected.
- **Proposal 2C, early pair confirmation** (`7e46e31`): a pair that fits is confirmed in its own wave of 4-10
  pairs, before later pairs are measured.
- **Proposal 4, the constant matcher** (`7e46e31`, `gapfinder/search/matcher.py`). A deterministic, $0
  companion to contrast. For each paper-stated value that has no knob:
  - the value's number must appear in a verbatim paper quote;
  - the code's named literals with the same core words are compared against it;
  - a literal that differs becomes a patch lead carrying the paper's value and quote.
- **Plumbing** (`fc3c1ce`): an entry script run after a `cd` (as in `cd pygcn && python train.py`) is now
  found, so its literals can be patched. Found by reading, not by a measured case.
- **Item 3, the planted-cause benchmark** (`eval/planted/plant.py`):
  - a seeded generator draws one hidden flag value or literal on a dev-set repo and runs it in Sandboxes;
  - the answer goes to `eval/planted/sealed/`; the search runs with `--hypotheses repomap`;
  - `score` reports correct, missed and confidently wrong.
  - Measurement only: no change is judged on these tasks.
- **Regression check:** dev suite run 3800 at `7e46e31` against run 3700. Cause runs went 48/69 → 51/69
  (6 tasks better, 4 worse, sign test p = 0.75: no change), with 0 confidently wrong and 57 correct
  abstentions in both. No regression; post-hoc data, so not evidence of improvement.
- **Item 4, environment builder** (`c59a701`, `gapfinder/env_build.py`, `gapfinder env-build`), Repo2Run-style:
  - the model picks a base image from a fixed list, given the commit date and the build files;
  - the repo is fetched at the commit inside the VM;
  - the model gives one shell command at a time until every third-party module the entry scripts import
    loads; the module list comes from plain code, no model;
  - a failed command's checkpoint is not built on (a free rollback); the kept commands are the recipe.
  - `spec-draft` self-checks: a second smoke run with another RUN_TAG (identical metrics get one redraft
    with seed advice, then a warning), and memory and time against a Sandboxes VM.
  - Still hand-written: the data step, the run command for one table cell, and the metric parser.
  - `eval/env_bench.py` measures the builder on the 7 dev-set repos, without their hand-picked pins.
  - **First env bench: 1 of 7 runnable from the repo alone** (`eval/results/env_bench_1.json`, $0.02 of
    model calls):

    | Repo | Result |
    |---|---|
    | pygcn | built (Python 3.6, torch 0.4.1) and ran |
    | PatchTST | built, but the hand-written smoke command needs `free`, a system tool the import check doesn't cover |
    | VGAE, GAT | the image picked first (3.8 or 3.9) had no TensorFlow 1 wheels, and the loop could only give up |
    | GIN, Informer, G-Mixup | Sandboxes network errors (DNS, connect timeout) |

    - The two image failures share one design gap: the model can now switch images, at most twice (`64c4aef`).
    - Sandboxes calls are now retried.
    - Not re-judged on these repos: the builder's next number must come from repos it hasn't seen.
    - Known gap (seen once, not fixed): system tools that the commands use are not checked.
- **Item 5, differential trace** (`dff0b0e`, `gapfinder/search/difftrace.py`, `gapfinder diff`):
  - for a user who has the authors' code (or a working earlier version), both programs get one traced dry
    run, and the values that reached the same library calls are compared;
  - each single-value difference becomes a hypothesis: the user's knob, or the literal at the call site,
    set to the reference value;
  - the reference's measured numbers are the targets, and combine plus bisect shrink the differences to the
    ones that matter;
  - multi-valued, missing and structural differences (another optimizer class) are reported, not tested.
  - This is the "give it my reproduction" input from section 6, for the case where reference code exists.

**First planted-cause results** (frozen at tag `planted-1`; seed 2; Sandboxes; `eval/planted/scores.json`):

| Case | Seeds | Tasks kept | Result |
|---|---|---|---|
| pygcn | 2-5 | 11 (of 39 draws) | **3/11 correct, 0 confidently wrong** |
| VGAE | 2 | 0 (of 9) | no draw moved the claim past 3 pooled sd: VGAE is insensitive to the 1/4x to 4x changes drawn |
| GAT | 2 | running | runs take 20-60 min under load |

**What the 8 pygcn misses are** (measurement only; no change is judged on these):
- **4 not identifiable.** The planted change was measured and fits, but other single changes fit the one claim
  (Cora accuracy) equally well. With one number, any knob that lowers accuracy "explains" it (section 4.4).
- **3 never measured.** The planted value lies between ladder points (epochs=50 between 40 and 100;
  weight_decay=0.002; lr=0.0025). The secant step that fills such gaps runs only when nothing fits every
  claim, and with one claim something always fits. This is the same identifiability limit.
- **1 noise depends on the configuration.** The planted runs spread widely (hidden=4: 56 to 76), while the
  noise band comes from the naive runs (tight). The planted configuration then looks like it doesn't fit.
  This is a known general class (per-configuration variance, as in Bayesian history matching): recorded,
  not fixed.

All 11 labels were "Fits but unsupported", which is right: with no paper, nothing backs a value, so a
confident label would be unearned.
- What this measures: the safety property holds on real code (0 confidently wrong).
- On a one-claim repo, the correct rate is bounded by identifiability, not by the search.
- Planted tasks are informative only on repos with several claims that the causes move differently. VGAE
  has 8 claims but barely responds to the drawn changes, so a more sensitive multi-claim repo is needed.
- GAT (planted, seed 2): 0 tasks from 7 draws. PubMed accuracy didn't move past noise either.

### 7.5 devbatch-2 (tag `devbatch-2` = `e0117a2`; `eval/external/devbatch2/`, PROTOCOL.md and RESULTS.md)

Three fresh papers: NCF, PyG GAT vs GCN, and Anomaly Transformer. All in Sandboxes, at least 2 claims each,
scoring fixed before any run.

- **Result: 0 of 3 documented causes found, 3 correct abstentions, 0 confidently wrong.**
  - Every target reproduced within noise on its first 5 runs: NCF -0.8%, PyG 0.0%, AT -0.5%.
  - The documented causes are protocol and noise findings that the paper's number already contains: NCF
    picks the epoch on the test set; AT's point adjustment uses the labels (and the paper states it); PyG's
    ranking depends on the split.
- **Environment builder on unseen repos:** imports loaded on 3/3, but the experiment ran on only 1/3 (PyG).
  NCF is Python 2 code; AT calls `.cuda()` unconditionally and runs out of memory at the paper's batch size.
- **The class it revealed (all three papers): a reproduced number is not audited.** The report says nothing
  about:
  - static leakage findings: NCF's `if hr > best_hr` loop over test evaluations;
  - held-out misses and broken comparisons: PyG CiteSeer, where GCN 71.1 beats GAT 70.8 against the paper's
    72.5 vs 70.3;
  - the paper's own stated protocol: AT's adjustment, extracted with prior 0.8 but listed only as "not
    settable".
- Other bugs: GapFinder's hooks shadow an existing `sitecustomize`; env-build's default goal is too weak; an
  image whose imports load is not a runnable image.

Done after the batch (`b2fe1bd`, `ba82204`; 293 tests). None of it was judged on the three papers:
1. **Audit section in every report**, whatever the label (`gapfinder/search/audit.py`):
   - selection on test data in the code;
   - comparisons the runs reverse beyond noise;
   - held-out claims outside noise;
   - settings the paper states that the harness can't vary.

   The selection check now reads tuple targets.
2. **env-build's default goal:** the README's first experiment command runs 5 minutes without failing
   (`--imports-only` keeps the old goal).
3. **The hooks chain** to the environment's own sitecustomize.
4. **One spend ledger** for every checkout. Worktree runs had their own ledger, so the true billed total was
   **$30.99**, not $30.42. The entries were merged into the main ledger.

Next: a fresh batch. The dev-set candidates are used up, except two weak ones (DKT, unverified; DP-SGD, low
priority). So new papers have to come from a sealer, as in blind-1 and blind-2.

## 8. Where things are

| What | Where |
|---|---|
| Engine | `gapfinder/search/engine.py`; trace `gapfinder/search/trace.py`; contrast `gapfinder/search/contrast.py`; patch knobs `gapfinder/sandbox/ast_patch.py` |
| Blind cases | `eval/external/blind-1/`, `eval/external/blind-2/` (RESULT.md, PRE_REVEAL.md, HARNESS.md) |
| Development set | `eval/external/devset/CANDIDATES.md` (13 papers, with answers: never give it to a harness writer); cases `vgae/`, `pygcn/`, `gin/`, `gat/`, `informer/`, `patchtst/`, `gmixup/`; builder `build_case.py` |
| Synthetic benchmark | `eval/gapbench/`; dev suite `eval/dev_suite.py`; comparison `eval/compare_suites.py`; results `eval/results/dev_suite_run*.json` |
| Tags | `v1.3`, `blind-1`, `v1.4` = `blind-2`, `devbatch-1` (= `2af0c3a`, the code the batch ran) |
| Learning docs | `docs/learn/` (beginner path) |
