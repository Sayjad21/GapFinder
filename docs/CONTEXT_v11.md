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

## 4. Why real papers fail (the patterns, not the cases)

1. **Reading the paper.** The ledger misses or misreads values: appendix tables (GraphMAE), its own names
   for settings (FastGCN, GAT), a stated value taken from code. Every downstream step depends on it.
2. **Causes in code structure.** A normalisation, a split procedure, model selection on the test set, an
   evaluation detail. GapFinder can point to these, never test them. This is by design: rewriting code until
   the number fits would explain nothing.
3. **Identifiability.** With one or two numbers, several settings fit equally well (GraphMAE's `mask_rate`
   against `alpha_l`, VGAE's bigger layers against the edge split). Only more numbers, relations or paper
   evidence break the tie.
4. **The harness.** Hand-written per paper. Its choices change results: which run is "naive", which rows are
   held out, which were tuned separately, whether it is scaled down.
5. **Compute.** CPU-only Sandboxes; budgets collapse when several searches share them.

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

## 7. Where things are

| What | Where |
|---|---|
| Engine | `gapfinder/search/engine.py`; trace `gapfinder/search/trace.py`; contrast `gapfinder/search/contrast.py`; patch knobs `gapfinder/sandbox/ast_patch.py` |
| Blind cases | `eval/external/blind-1/`, `eval/external/blind-2/` (RESULT.md, PRE_REVEAL.md, HARNESS.md) |
| Development set | `eval/external/devset/CANDIDATES.md` (13 papers, with answers: never give it to a harness writer); cases `vgae/`, `pygcn/`, `gin/`, `gat/`, `informer/`, `patchtst/`, `gmixup/`; builder `build_case.py` |
| Synthetic benchmark | `eval/gapbench/`; dev suite `eval/dev_suite.py`; comparison `eval/compare_suites.py`; results `eval/results/dev_suite_run*.json` |
| Tags | `v1.3`, `blind-1`, `v1.4` = `blind-2`, `devbatch-1` (= `2af0c3a`, the code the batch ran) |
| Learning docs | `docs/learn/` (beginner path) |
