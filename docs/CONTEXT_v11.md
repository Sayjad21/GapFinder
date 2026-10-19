# GapFinder: current context (2026-10-19)

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

**1 correct, 1 partial, 2 missed, 1 confidently wrong.** Nothing has been confidently wrong since the confidence cap
went in. The last three blind papers give 1.5 causes found.

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

---

## 6. Remaining bottlenecks to real generalisation (ordered by impact)

### 6.1 Too few fresh papers to know if anything generalises
- **Evidence:** 5 sealed blind papers; sealers find about one usable paper per 3 hours.
- **Why it matters:** about 15 fixes since the last fresh paper that needed them, none proven. A real rate needs
  about 20-30 papers.
- **What would help:** a ready pool of documented gaps (ML Reproducibility Challenge reports, author-confirmed GitHub
  issues), collected in advance.

### 6.2 The harness is still mostly built by hand
- **Evidence:** the experiment ran unaided on about 2 of the last 6 repos. Every harness needed a person or agent
  for the data, the table-cell command, the parser and the scaling (section 4).
- **Why it matters:** "any paper" breaks here first, and it is a bias risk.

### 6.3 Causes outside what GapFinder can change
- It changes settings, constants, switches and some scoring rules.
- It can't test:
  - a model or algorithm written differently (only `gapfinder diff`, which needs reference code);
  - data preprocessing differences (filtering, splits, normalisation);
  - library version behaviour.
- These are common real causes, and they get "Unexplained" at best.

### 6.4 Few reported numbers mean many equally good answers
- **Evidence:** planted causes, 1 claim 3/11 against 8 claims 6/8. Real targets often have 1-2 numbers.
- **Not built:** the paper's learning curves and figures as extra claims.

### 6.5 CPU only, 3.9 GB, one hour per piece
- Most modern papers need a GPU, so they can't be tested.
- Shards and segments help slow papers; nothing helps models that need a GPU or more memory.

### 6.6 Paper reading still misses things
- **Evidence:** RippleNet's λ1 and GraphMAE's appendix (both fixed, untested).
- Not followed: "as in [X]" to the cited paper (AutoReproduce's paper lineage).

### 6.7 Flawed-but-reproducing papers are only partly covered
- Tested now: test-score selection, label-based edits, evaluation switches.
- Undetected: normalising with test-set statistics, test data leaking into preprocessing, reporting the best of many
  seeds.

### 6.8 When it is right, it still sounds unsure
- **Evidence:** Fair Clustering's λ=100 was right but "Fits but unsupported", because the paper's stated (wrong)
  value was the only evidence.
- It needs a clear label for "this value fits every claim, and the paper's stated value was run and doesn't".

### 6.9 Noise is modelled only from seeds
- **Evidence:** one planted miss came from noise that grows with the configuration.
- Variance from data splits isn't modelled (Bouthillier et al.).

### 6.10 Budget
- About $1.30 left under the cap: 2-3 more papers' ledgers.
- Planted-cause testing costs $0.

**What would move it most:**
1. a pool of 20+ documented gaps (6.1);
2. an end-to-end harness builder, especially data and the table-cell command (6.2, section 4);
3. figures and curves as claims (6.4);
4. GPU access (6.5, a platform question).

6.3 and 6.7 are the hardest: they need understanding of code structure and data pipelines.

---

## 7. Next work (agreed 2026-10-19; status kept up to date here)

From the owner's 10-bottleneck plan, after a web check. Each item names its bottleneck (section 6) and why it is
allowed under the no-patching rule: a recurring class, a published method, or plumbing/measurement.

### 7.1 To do

| # | Item | Bottleneck | Allowed as | Status |
|---|---|---|---|---|
| 1 | **A pool of 20+ cases mined from fix commits.** GitHub search for "match the paper", "fix default", "wrong hyperparameter", "reproduce table". The parent commit is the blind input and the fix diff is the sealed answer, written by the script; the runner never reads it. A case is kept only if the numbers differ beyond noise between the parent and the fix. Each case is tagged by cause type, and rates are reported per type. | 6.1 | measurement (commit mining is an established method, e.g. BugHunter) | |
| 2 | **Read the arXiv `.tex` source** when available (about 93% of arXiv papers): symbols and tables as plain text; pgfplots coordinates and bundled csv files as figure data | 6.6, 6.4 | recurring class (symbols: RippleNet; tables: GraphMAE) | |
| 3 | **Command picker:** match the claim's dataset and model names against the arguments of README and shell commands; propose a script when one claim needs several commands | 6.2 | plumbing | |
| 4 | **Run the repo's download scripts** in env-build (`download*.sh`, `get_data*`), and record sizes and checksums | 6.2 | plumbing | |
| 5 | **Metric binder.** Prefers test over val and final over best; refuses when ambiguous; keeps alternatives as extra metrics | 6.2 | plumbing | |
| 6 | **Fixed shrink rule:** shards and segments first; shrink only if a run won't fit; record a discrepancy allowance | 6.2, 6.5 | plumbing | |
| 7 | **Loader caches** for common datasets (PyG, torchvision, sklearn; they check hashes). Not a generic `/data` symlink | 6.2 | plumbing | |
| 8 | **Built-in CPU shim** (`cuda.is_available` False, `torch.load` to CPU) and allocator and thread settings in every run; `num_workers=0` only after an out-of-memory failure | 6.5 | recurring class (hand-built for Anomaly Transformer and SparseTSF) | |
| 9 | **Static GPU/size filter** before spending on a ledger | 6.5, 6.10 | plumbing | |
| 10 | **Static leakage analysis** after Yang et al. (ASE 2022): test data reaching fitting or preprocessing; feeds the audit and the protocol tests | 6.7 | published method | |
| 11 | **Label "Paper's stated value refuted; unique fit"** when all hold: the stated value was run and fails; every claim fits (at least 2); the counterfactual holds; one island; every knob screened. Must not fire on GraphMAE-like cases; regression-checked | 6.8 | recurring class (cautious labels on right answers) | |
| 12 | **Conservative significance:** the larger of the baseline and candidate spread | 6.9 | recurring class (config-dependent noise) | |
| 13 | **Split variance in calibration,** only through the repo's own split or fold flag | 6.9 | published (Bouthillier et al.) | |
| 14 | **Claims at fixed knob values** (sensitivity-plot points); each candidate is also run at those values | 6.4 | recurring class (identifiability) | |
| 15 | **Learning-curve points as claims,** only when the paper reports the curve and the code logs test metrics per epoch | 6.4 | recurring class | |
| 16 | **Super for claim extraction, Ultra only for assumptions;** section slicing as an option, measured for recall | 6.10 | budget | |
| 17 | **Grounded preprocessing and operation swaps,** only when the paper states the other choice (through the contrast step or the matcher) | 6.3 | grounded extension of the patch round | |
| 18 | **"As in [X]":** the cited paper's arXiv source, its setup section | 6.6 | published (AutoReproduce's paper lineage) | |
| 19 | **Paper-year dependency environment** as one knob | 6.3 | documented class (dependency drift) | |

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

## 8. Where things are

| What | Where |
|---|---|
| Engine | `gapfinder/search/engine.py` (search, protocol tests, alternative configs); `search/audit.py`; `search/trace.py`; `search/contrast.py`; `search/matcher.py`; `search/difftrace.py`; `sandbox/ast_patch.py`; `sandbox/runner.py` (shards and segments) |
| Harness tools | `gapfinder/env_build.py` (`gapfinder env-build`); `gapfinder/spec_draft.py` (`gapfinder spec-draft`); `eval/external/devset/build_case.py`; `eval/env_bench.py` |
| Sealed blind cases | `eval/external/blind-1/`, `blind-2/`, `batch3/` (b3a, b3c), `batch4/` (b4a): each has `case.md`, `answer_key.md` after the reveal, HARNESS.md, the run and RESULT.md |
| Frozen batches | `eval/external/devset/` (devbatch-1 cases; CANDIDATES.md holds answers); `eval/external/devbatch2/` (PROTOCOL.md, RESULTS.md) |
| Planted causes | `eval/planted/plant.py` (`make`, `search`, `score`); tasks in `eval/planted/tasks/`; answers in `eval/planted/sealed/` |
| Synthetic benchmark | `eval/gapbench/`; dev suite `eval/dev_suite.py`; `eval/compare_suites.py`; `eval/results/dev_suite_run*.json` |
| Tags | `blind-1`, `blind-2`, `devbatch-1`, `devbatch-2` (`e0117a2`), `planted-1`, `batch-3` (`92b1faa`), `batch-4` (`bae25f4`) |
| Learning docs | `docs/learn/` (beginner path) |
