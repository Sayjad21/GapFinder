# GapFinder: context handover after v1.1 (2026-10-14)

This document is written so that someone with no prior context can design the next fix. It covers:
- what the system is;
- how we measure it;
- every change made in the v1.1 cycle: the decision, the evidence, the test that exposed each bug, the
  fix and the measured effect;
- where the system stands now, and the current bottleneck with concrete cases.

Paths are relative to the repo root (github.com/Sayjad21/GapFinder).

---

## 1. What GapFinder is

**Input:**
- a paper (PDF);
- its code artifact;
- a human-confirmed harness spec (YAML: how to build, load and run the artifact, plus the "knobs",
  i.e. the command-line flags and settings that can be changed);
- target claims, i.e. the paper's numbers to match.

**Question:** the reproduction gives different numbers from the paper. Which unstated or mis-stated
setting explains the gap?

**Pipeline** (`docs/ARCHITECTURE.md` has the full picture):
1. **Claim ledger.** Nemotron 3 Ultra extracts claims, and Super filters them.
2. **Assumption space.** Ultra lists settings the results could depend on, each tied to paper evidence,
   with candidate values (`gapfinder/ledger/`).
3. **Repo map.** Static: argparse flags, defaults, choices and env vars (`gapfinder/ingest/repo_map.py`).
4. **Search** (`gapfinder/search/engine.py`, class `GapSearch`). It runs on forked Token Factory
   Sandboxes, or on the local backend for GapBench. The phases:
   - **calibrate:** about 5 naive runs give a noise band (2×MAD);
   - **screen:** one run per (knob, value) hypothesis;
   - **confirm:** repeats plus a bootstrap test that the effect isn't noise;
   - **combine:** pairs of the top knobs, for interactions;
   - **bisect:** drop knobs that don't matter;
   - **verify:** counterfactual reversal, held-out claims must not get worse, evidence or plausibility check.
5. **Gap Report** (`gapfinder/report/gap_report.py`). One card per claim, with a label:
   - **Explained**, **Paper-artifact inconsistency**, **Partially explained**: confident;
   - **Fits but unsupported**: a hedge. A configuration closes the gap, but no paper or code evidence
     supports it;
   - **Explains target, conflicts with held-out**: new in v1.1, also a hedge;
   - **Unexplained**, **Inconclusive**, **Reproduced**: abstentions.

**Design principle:** never attribute confidently unless verified. The confidently-wrong count is the
headline safety metric.

---

## 2. How we measure (the evidence sources)

### GapBench: a synthetic benchmark with known answers (`eval/gapbench/`)

**Artifacts** (fast, local, run with the local backend at $0 sandbox cost):
- **rlbench:** CartPole tabular Q-learning (`artifacts/rlbench/cartpole_q.py`). Claims: C1 `mean_reward`
  (target) and C2 `min_reward` (held out).
- **mlbench:** logistic regression with SGD on synthetic data (`artifacts/mlbench/train.py`). Claims: C1
  `test_accuracy` (target) and C2 `balanced_accuracy` (held out).

**Task generator** (`gen_tasks.py`): sealed and seeded. Each task plants a hidden setting from a value
pool; the "paper" numbers are the median of 7 (ml) or 11 (rl) runs at that setting. Categories:

| Category | What is planted |
|---|---|
| `known_cause` | one knob, unstated or stated differently from the code |
| `decoy` | a cause plus a distracting knob that closes the target but breaks the held-out claim |
| `interaction` | two knobs that only close the gap together |
| `no_cause` | the numbers are offset artificially |
| `noise_only` | the paper's number is within noise of the naive run |
| `incomplete` | the true knob is removed from the spec |
| `out_of_space` | new in v1.1: a code-level bug no knob can reach |

Validity checks reject a draw when:
- the gap is under 3 noise bands;
- a rival configuration explains the claims as well as the planted answer;
- the paper text leaks the answer.

**Arms** (`harness.py`):
- `gapfinder` (full);
- `gapfinder-noverify` (no verification);
- `gapfinder-noevidence` (no evidence gate);
- `gapfinder-random` (random hypothesis order);
- `baseline-super` (a mini-SWE-agent with Nemotron Super that edits and runs the code itself).

**Scorer** (`score.py`). Per run, the outcome is one of:
- `correct`: the proposed knob set equals the hidden one, at any label except an abstention. A hedged
  "Fits but unsupported" with the right knobs counts as correct;
- `partial`: a strict subset of the true knobs;
- `confidently_wrong`: a confident label with the wrong knobs, or any confident label on an abstention
  task;
- `correct_abstention`;
- `missed`.

Note: on generated tasks the paper is silent about the planted value, so the evidence gate can almost
never support it. Most correct GapFinder answers are therefore the hedge "Fits but unsupported".

**Protocol** (`PROTOCOL.md`): the system is frozen with a git tag, then the seed is made, then tasks are
generated and the answers sealed (hashed, git-ignored), then the runs, then the reveal. Any task set
whose answers are published becomes dev data.

### External case: MC Dropout (Gal & Ghahramani 2016) (`eval/external/mc-dropout/`)

- **Run setup:** the real Theano code (repo yaringal/DropoutUncertaintyExps at 6eb4497), run on Token
  Factory Sandboxes from checkpoint `gf/mcd/base-v2`. It is scaled down: T=100 MC samples, 3 splits.
- **Targets:** Energy RMSE 1.66 (target) and Yacht RMSE 1.11 (held out).
- **The documented cause** (sealed answer key, revealed): `--epochx 10 --hidden 1`. The paper used 10×
  epochs over a 40-epoch base and one hidden layer; the code's defaults are epochx=500 and hidden=2.
  - The documented pair fixes Energy (1.716, +3.4%) but breaks Yacht (2.996, +170%).
  - The rest of the gap is out of space: the authors' README says the paper-era code tuned
    hyperparameters shared across splits. The code also uses grid search instead of the paper's
    Bayesian optimisation, a hard-coded batch size of 128 instead of 32, and T=10000 Monte Carlo samples.
  - So the best possible honest answer is "partly explained by `epochx=10, hidden=1`, and the rest is
    out of space".

### Real system: RusKey (an LSM-tree tuning paper)

The reproduction lives on the user's PC (WSL `/root/ruskey`). Its database load is NOT reproducible:
12 loads gave 12 different checkpoints. Only claim C5 has a gap above the minimum detectable effect.
It's a positive-control candidate, not used in the v1.1 test.

---

## 3. Where v1.0 stood (the starting point)

- **Two blind GapBench tests on v1.0** (8 tasks × 3 runs per arm, done by a teammate):
  - GapFinder: 0/24 confidently wrong both times; 5/15 and 7/15 correct causes; 9/9 correct
    abstentions;
  - Super baseline: 14/24 and 12/24 confidently wrong.
- **MC Dropout blind arms (v1.0):** all "Unexplained". `epochx=10` was never proposed: the ledger
  proposed only higher values (500, 1000, 2000).
- **Diagnosed failure mode: hypothesis coverage.** The true value was often never tested.
  - Measured with `eval/reachability.py`, which reads run logs and asks whether the true value was
    measured. Results in `eval/results/reachability_v10.json` and `reachability_v11.json`.
  - On the v1.0 test tasks: 0 of 6 interaction runs ever reached both true values, and 1 decoy miss
    never reached the true value.
  - Cause: candidate values came only from the ledger (the LLM) plus a small fixed grid. Choices, order
    of magnitude, multipliers ("10× more iterations") and boundary values (1, 0) were systematically
    missing.

---

## 4. What was done in v1.1, in order

The format of each entry: decision → evidence or test → fix → effect.

### 4.1 Value coverage: generate candidate values from the code, not only the LLM (`gapfinder/search/hypotheses.py`)

**Decision:** keep the ledger's candidates, and add deterministic ones derived from the code and the
knob's default. `coverage_values(knob)` returns, in order:
- **Choices:** every argparse `choices` value, read from the repo map into `Knob.choices`, and parsed
  across multi-line `add_argument` calls.
- **Integers:** a coarse-first log ladder around the default. The multipliers `LADDER = (10, 2, 50, 5,
  100)` are applied as both ×k and ÷k, alternating, plus the boundary value `1`.
- **Floats:** the ladder, plus `0.0`.
- **Fractions** (defaults in (0, 1)): ladder values kept below 1, plus `0.0`.
- **Multipliers:** for a knob that scales another quantity (e.g. `epochx` in
  `n_epochs * epochs_multiplier`), the literal factors `MULTIPLIER_FACTORS = (1, 2, 5, 10, 100)` first.
  Multipliers are detected by:
  - the name (`_MULT_NAME`) or help text;
  - static config flow (`gapfinder/ingest/config_flow.py`): a Python `ast` pass that follows a flag
    through aliases into multiplications by count-like quantities (epochs, iterations, steps). On MC
    Dropout it finds `{'epochx': ['n_epochs']}`.
- **Cap:** `coverage_candidates = 6` values per knob after the ledger's own candidates; the paper's
  stated values come first.

**Bugs found while building it:**
- *Cache miss in the offline quick-start.* `tests/integration/test_try_it.py` failed: adding choices to
  the repo-map summary changed the LLM prompts, so the cached demo answers no longer matched. Fix: the
  summary deliberately excludes choices. Lesson: anything that enters a prompt invalidates the demo
  cache.
- *Multi-line argparse default lost* when choices were a tuple spanning lines. Fix: parenthesis-balanced
  parsing, up to 6 lines.
- *Regression on dev-ml-threshold.* The ladder value `threshold=5` (meaningless for a probability)
  took the knob's slot in the combine round, and the true value lost its place. Fix: fraction-aware
  values (a default in (0, 1) stays in (0, 1)) and two values per knob in the combine round.

### 4.2 Strict confirmation, parsimony and value sets (`engine.py`)

- **Strict confirm.** The screening run that selected a hypothesis can't also confirm it: confirmation
  uses fresh runs only, and the bootstrap interval is Bonferroni-corrected over the hypotheses
  confirmed together. Reason: with 6 values per knob, many more hypotheses mean many more chances to
  hit noise.
- **Parsimony tie-break.** Among configurations within the same noise bucket, prefer fewer knobs, then
  the smaller log change from the default.
- **Value sets** (`ClaimResult.value_sets`): every value of a chosen knob that fits as well as the
  chosen one is reported. The scorer's `correct_set` credits a run whose set contains the truth. Reason:
  equifinality. On v1.0's task gen-03, `max_steps` 400, 500 and 1000 all land within noise; parsimony
  picks 400, and the truth is 500.

### 4.3 Adaptive combine width

The combine round now pairs as many values per knob as fit in `combine_max_pairs = 40`. Evidence:
v1.0's gen-05 (interaction `eps_start=0.1` + `lr_schedule=inv`) needed a third value of one knob.

### 4.4 A generator validity bug: tasks that weren't identifiable

- **Evidence:** on gen-05, GapFinder's answer `eps_start=0.0` alone reproduced both claims better (C1
  +5.1%, C2 +0.8%) than the planted pair (C1 +36%). The scorer marked a valid explanation wrong.
- **Fix:** `gen_tasks.py` now checks rivals over GapFinder's whole search space
  (`RIVALS_OVER_SEARCH_SPACE`, `rival_values()`: pools plus every coverage value), not only the value
  pools. A draw is rejected if any single setting reproduces both claims within one noise band.
- **Limitation, found later in the v1.1 test (§4.13):** this check covers single settings only, not
  pairs.

### 4.5 Post-hoc v1.1 result on the former v1.0 test tasks (NOT blind; `eval/results/gapbench_v11_posthoc.md`)

Like for like: the same recorded ledgers (`harness.py --ledger-from`), with only the search re-run, at
$0.
- **Correct causes:** 7 → 10-11 of 15, plus 1 partial.
- **Confidently wrong:** 0 → 0. Abstentions 9/9; dev 4/4.
- **Reachability:** v1.1 measures every true value on those tasks. The remaining misses are selection
  misses.

### 4.6 Multi-claim history matching: turn a bare "Unexplained" into a diagnosis (`gapfinder/search/history.py`)

For every measured configuration x and every claim i, the implausibility is

    I_i(x) = |z_i - m_i(x)| / sqrt(s_i^2/p + s_i^2/n_x + (d*z_i)^2)

- z is the paper's value; m is the mean of the n_x runs at x;
- s is the naive run-to-run SD; p is the number of runs behind the paper's number (1 by default, 4.5
  for GapBench);
- d is a discrepancy fraction for scaled surrogates (0.05 by default).

A configuration is NROY (Not Ruled Out Yet) for claim i if I_i ≤ 3. The diagnoses:

| Diagnosis | When |
|---|---|
| `reproduced` | the naive run is jointly NROY |
| `in_space` | some tested configuration is jointly NROY |
| `out_of_space_suspected` | every claim fits some configuration, but none fits all |
| `out_of_space_likely` | some claim fits nothing |

In the engine (`_history_match`): when the label would be Unexplained and the diagnosis is
out_of_space_suspected, the result becomes **"Explains target, conflicts with held-out"** with the best
target fit, plus a note that the rest lies in code, data or evaluation.

- **Offline validation** (recorded runs, `eval/results/history_match_offline.md`): 11 of 12 GapBench
  diagnoses correct. The one miss, dev-rl-nocause, is equifinality on a noisy RL metric: 7
  configurations fit both claims. MC Dropout is out_of_space_suspected under every discrepancy setting
  above 0.

### 4.7 Honest noise model and MDE → Inconclusive (`eval/noise_model.py`; `gapfinder/sandbox/noise.py` `mde()`)

- **Analysis.** A one-way random-effects ANOVA splits run-to-run variance into within-load (forks) and
  between-load (fresh setups) parts. On RusKey, forks saw only a quarter of the real spread for C5b.
- **Minimum detectable effect:** MDE = (t_{.975,df} + t_{.8,df}) · σ · sqrt(2/n).
- **Engine rule** (`SearchConfig.mde_inconclusive`): if nothing explains the gap, and the gap is below
  the MDE at the confirmation repeats, the label is **Inconclusive**, not Unexplained. A cause that
  closed a gap that small couldn't have been confirmed anyway.
- **Effect:** score-neutral (both labels are abstentions). On the recorded runs it re-labels 13 of 70
  Unexplained claims, all gaps of 8-10%.

### 4.8 Report views (`gap_report.py`)

- **Equifinality map:** the jointly-NROY configurations, grouped by which knobs changed.
- **NROY islands** (`history.islands`): connected components under single-knob moves (a BFS). Two
  islands mean two genuinely different explanations.
- **Every target-only fit**, with its worst-claim implausibility. Added after MC Dropout (§4.11).

### 4.9 GapBench out-of-space category and balanced scoring

- **Design.** The paper's numbers come from a buggy copy of the artifact.
  - **First attempt:** dormant bugs inside the artifact, switched on by an env var (`GAPBENCH_VARIANT`).
  - **The bug this exposed:** the repo map lists env vars, so GapFinder could see the switch. Editing the
    artifact also changed the repo map, and so the prompts, which broke the demo cache (test_try_it
    failed).
  - **Fix:** the artifacts stay byte-identical. A variant is a text patch applied to a temporary copy
    (`eval/gapbench/variants.py`), used only by the generator and `make_task.py`. A unit test asserts
    that the artifact is untouched and that its repo map has no switch.
- **rlbench rejected entirely:**
  - its held-out claim `min_reward` has a noise band of about 90 on a median of about 62, so it rules
    nothing out;
  - every bug tried (a missing reset, exploration left on, an evaluation step cap, a reward-unit bug)
    was mimicked by a single knob;
  - a best-seed reporting bug moved the target by under 2 bands, because the reward is capped at 200.
- **mlbench variants kept:** `drop_scaled` (the loader keeps only the unit-scale columns; 12.3 bands)
  and `clip5` (a leftover outlier filter clips features to [-5, 5]; 14.3 bands). Rejected:
  test-set epoch selection (under 3 bands) and dropping only the ×400 column (a single knob mimics it).
  The two out-of-space tasks in a set must use different bugs.
- **Scoring additions:**
  - in-space recall, no-cause specificity and balanced accuracy;
  - the out-of-space diagnosis rate;
  - an always-Unexplained row (recall 0, specificity 1, balanced 0.5);
  - an exact Clopper-Pearson interval for confidently wrong.

### 4.10 Static out-of-space code checks (`gapfinder/ingest/code_checks.py`)

When history matching says out of space, the engine attaches leads with file:line evidence. It reads
the code with `ast` and never runs it. The lead families:
- hyperparameter-like literals no flag sets (`batch_size = 128`, `T = 10000`);
- settings read from data files;
- selection loops (grid search or best-of), and whether they score on test data;
- fixed seeds;
- split fractions.

The spec field `source:` points at a local copy of the code when the base is an image or checkpoint.

- **Validation on MC Dropout** (not blind): 8 leads. The 3 documented out-of-flag differences rank 1
  (grid search per split), 2 (`batch_size = 128`) and 7 (`T = 10000`).
- **Limit:** leads can't be tested yet. The diff guard forbids source edits during the search.

### 4.11 MC Dropout on v1.1: a real sandbox run that exposed four bugs (`eval/external/mc-dropout/RESULT_v11.md`)

The run started from the blind normal ledger: 147 Sandboxes runs, about $2,850 reported sandbox
cost (unbilled in the Beta), $0.002 billed.

| # | Symptom | How it was found | Root cause | Fix |
|---|---|---|---|---|
| 1 | `epochx` not a multiplier, so 10 was never proposed | Offline dry run of `hypotheses()` on the blind ledger, before spending | Code reading (choices and multipliers) only ran for `local:` bases; MC Dropout runs from a checkpoint | `HarnessSpec.code_root()` uses `source:` (commit abfe507) |
| 2 | `epochx=10` lost; replaced by 20 | Report's "Failed hypotheses"; branch log tail | A Theano compile-cache race between parallel shards in one VM (`ModuleNotFoundError: No module named 'tmp…'`). Super's triage called it `invalid_value` and swapped the value | Infra signatures → the same value is retried once, in every phase; `invalid_value` is accepted only if the log shows a rejection (argparse error, ValueError…) (3f82ad6) |
| 3 | The label rested on one unconfirmed run | Report: "1 of 5 confirmation runs" | History matching relabelled from a single screening run | Relabel only configurations with ≥2 successful runs (3f82ad6) |
| 4 | The run died midway | No process running, events stopped | A background process was killed by an editor restart | Long runs are launched detached, and `--resume` (repeatable) reuses earlier events |

**Final result:**
- **Label:** "Explains target, conflicts with held-out: `epochx=1, hidden=10`" (5 runs, Energy median
  1.85, +11.5%).
- **Diagnosis:** out_of_space_suspected. 40 configurations were tested, and none fits both claims.
- **The documented pair** was measured once (Energy 1.84, Yacht 2.90), and the 150-run budget ran out
  in the combine round, where up to 36 pairs were tried.

The configurations that fit Energy alone, ranked by worst-claim implausibility (lower is less
inconsistent with Yacht):

| Configuration | Worst I |
|---|---|
| `epochx=10, hidden=1` (documented) | 5.78 |
| `epochx=1, hidden=20` | 8.4 |
| `epochx=1, hidden=10` (chosen) | 9.0 |
| `epochx=1, hidden=5` | 9.76 |
| `epochx=2` | 15.59 |

**Change made after seeing this** (so it is NOT evidence): the relabel now picks, among repeated
target fits, the one with the smallest worst-claim implausibility (the standard history-matching
criterion), not the best target fit. Re-labelling these runs ranks the documented pair first, but it
stays unlabelled because it has only one run.

### 4.12 Shared ledger across arms (`eval/gapbench/run_arms.py`)

The `gapfinder` arm pays for each task's ledger (`--fresh`). The other GapFinder arms re-use the
recorded model answers (`--ledger-from`), so the ablations differ only in the search. A blind test cost
about $7.50 per test in v1.0, and $3.86 for 10 tasks in v1.1.

### 4.13 The sealed v1.1 blind test (`eval/results/gapbench_test_v11.md`, raw data `gapbench_test_v11.json`)

Frozen at tag `v1.1`; seed made after the tag; 10 tasks (`test-v11-01`…`10`); 5 arms × 3 runs; the
sealed hash was checked at the reveal.

| Arm | Confidently wrong (exact 95% CI) | Correct + partial (of 15 cause runs) | Correct abstentions (of 15) | Balanced acc. |
|---|---|---|---|---|
| GapFinder | **0/30** (0-11.6%) | 7 + 1 | 15 | 0.73 |
| GapFinder, evidence off | 0/30 | 6 + 1 | 15 | 0.70 |
| GapFinder, random order | 0/30 | 6 + 0 | 15 | 0.70 |
| GapFinder, verification off | 16/30 | 5 + 2 | 6 | 0.37 |
| Super baseline agent | 19/30 | 3 + 0 | 4 | 0.23 |
| Always Unexplained | 0/30 | 0 | 15 | 0.50 |

**Coverage, measured directly:** the exact true configuration was tested in **12 of the 15** GapFinder
cause runs. So coverage is largely solved; the misses are now mostly selection.

---

## 5. The current bottleneck: selection among equally good fits (equifinality)

**The pattern.** The true configuration is now usually measured, but GapFinder reports a different
configuration that fits the target about as well. The available claims, often one target plus one
noisy held-out claim, can't separate them, and the tie-breaks (parsimony, closest gap, first confirmed)
pick the wrong one.

### Every miss in the sealed v1.1 test (GapFinder arm)

| Task | Truth | What GapFinder said | Kind of miss |
|---|---|---|---|
| 01 run 1 | interaction `max_steps=500` + `gamma=0.999` | `max_steps=2000` alone (Fits but unsupported) | selection. The exact pair was tested. The held-out `min_reward` is too noisy to separate configurations; the target alone is matched by max_steps alone |
| 01 run 2 | (same) | `max_steps=2000`, value set {500, 1000, 2000} | selection; the true value is in the set, but gamma is missing |
| 01 run 3 | (same) | `max_steps=500` alone | partial |
| 04 run 2 | decoy, `max_steps=100` | `lr=0.91` | selection: an odd value (not on the ladder) won |
| 05 runs 1-3 | interaction `normalize=minmax` + `epochs=75` | `lr_schedule=cosine` + `epochs=150` (all 3 runs) | **coverage**: `epochs=75` (×5 the default of 15) was never tested, cut by the 6-value cap; the chosen pair was an equally good alternative |
| 10 run 2 | known cause, `max_steps=100` | `max_steps=100` + `lr_schedule=linear` | minimisation failure: the extra knob wasn't dropped by bisect or parsimony |

### The same pattern elsewhere

- **MC Dropout (§4.11):** 5 configurations fit Energy; the wrong one was chosen and confirmed first.
  The budget ran out before the documented pair had a second run. Selection is driven by which
  configuration's first run happens to land closest. On a CV of 8.5%, that's noise.
- **v1.0 post-hoc gen-03:** `max_steps` 400, 500 and 1000 are within noise; parsimony picks 400; the
  truth is 500.
- **RusKey:** 11 configurations are jointly not ruled out at the measured noise. The claims are
  non-identifiable without more claims or more repeats.
- **dev-rl-nocause:** 7 configurations fit both claims; this is the one history-matching mistake
  offline.

### Why the current machinery doesn't resolve it

- **Ordering by one noisy run.** Confirmation order, and the choice of which pairs get repeats, comes
  from single screening runs. With many candidates, the first winner is often a noise winner (winner's
  curse).
- **Weak held-out claims.** Held-out claims are the only discriminator, and on rlbench `min_reward` is
  extremely noisy (band about 90 on 62). On MC Dropout every Energy fit breaks Yacht, so Yacht ranks
  them but can't accept any.
- **Arbitrary parsimony.** "Fewest knobs, smallest log change" picks arbitrarily among
  same-size changes, and is wrong when the truth is a larger change (gen-03, task 01).
- **Budget burn.** The combine round tries up to 40 pairs at one run each, which uses most of the
  budget before the leading candidates get confirmation runs. This hurt on MC Dropout: about 4× the
  runs of v1.0.
- **Hedge labels can't express a tie.** The output is a single configuration plus value sets per knob.
  There's no first-class "these K configurations are indistinguishable given these claims" answer, and
  no scoring credit for a correct set of configurations (only `correct_set` for per-knob values).

### Secondary open problems (smaller)

1. **The out-of-space tasks are pair-mimicable.** In the v1.1 test, a two-knob combination (e.g.
   `normalize=zscore` + `positive_rate=0.5`) fit both out-of-space tasks, so `out_of_space_diagnosed`
   was 0/9 for every arm. The generator's rival check needs to cover the pairs the combine round can
   test.
2. **The 6-value cap** cut a ×5 rung (task 05). The ladder order, or a cap that depends on how many
   knobs are open, would decide this.
3. **Relative wording** ("10× more epochs than the reference") needs an anchor-aware resolver (TODO
   item 4, not built).
4. **Out-of-space leads are untested.** Testing one requires exposing it, e.g. as a patch knob, which
   the diff guard forbids today.

---

## 6. Constraints anyone working on the next fix must respect

- **Money.**
  - The whole project has about $50 of Token Factory credit. **$21.04 is billed so far**; only Nemotron
    inference is billed.
  - `GF_SPEND_CAP_USD` in `.env` is a hard cap (11 in `.env`, which is below the current spend, so paid
    calls are blocked unless it's raised per process).
  - Sandboxes are unbilled in the Beta but report a diagnostic cost. `GF_SANDBOX_GUARD_USD` refuses runs
    past a reported total; that total is about $5,500 now. GapBench runs locally, at $0 sandbox cost.
  - `GF_CACHE_ONLY=1` makes every model call free (cache only).
- **Free evaluation loops already exist. Use them before any paid run:**
  - `harness.py --ledger-from <run dir>` re-runs only the search on recorded model answers ($0, local);
  - `gapfinder search --resume <events.jsonl>` (repeatable) re-labels from recorded branch runs, with no
    new runs if `--max-runs` equals the recorded count;
  - `eval/reachability.py` and `eval/history_match.py` read logs only.
- **Honesty protocol.**
  - The v1.0 (`test-gen-*`) and v1.1 (`test-v11-*`) task sets are now public, so they are **dev data**.
    Tuning on them is allowed, but any claim about a fix needs a NEW sealed set: tag, then seed, then
    generate (`gen_tasks.py --set <name>`), then run, then reveal.
  - Never open the sealed answers before scoring.
  - The MC Dropout case is not blind any more.
- **Don't change the GapBench artifacts or prompt-visible text without regenerating caches.** The
  offline quick-start (`tests/integration/test_try_it.py`) depends on cached model answers.
- **Commits:** no AI-tool attribution anywhere (no co-author lines, no tool names).
- **Tests:** `pytest tests/unit tests/integration`. At the time of writing, 269 pass, 3 skipped, in
  about 4 minutes.

## 7. Key files

| What | Where |
|---|---|
| Search engine (phases, labels, history-match hook, MDE rule, triage) | `gapfinder/search/engine.py` |
| Candidate values (coverage) | `gapfinder/search/hypotheses.py` |
| History matching (implausibility, diagnoses, islands) | `gapfinder/search/history.py` |
| Verification (held-out rule, plausibility) | `gapfinder/search/verify.py` |
| Failure triage (Super, plus the deterministic gates) | `gapfinder/search/triage.py` |
| Noise band, bootstrap, MDE | `gapfinder/sandbox/noise.py` |
| Static config flow / code checks | `gapfinder/ingest/config_flow.py`, `gapfinder/ingest/code_checks.py` |
| Report | `gapfinder/report/gap_report.py` |
| GapBench generator / variants / scorer / harness / arms runner | `eval/gapbench/gen_tasks.py`, `variants.py`, `score.py`, `harness.py`, `run_arms.py` |
| Pre-registration and amendments | `eval/gapbench/PROTOCOL.md` |
| Results | `eval/results/gapbench_test_v11.md`, `gapbench_v11_posthoc.md`, `history_match_offline.md`, `noise_model_ruskey.md`, `code_checks_mcdropout.md`; `eval/external/mc-dropout/RESULT_v11.md` |
| Roadmap | `TODO.md` section B |

## 8. The question for the next step

How should GapFinder choose among, or honestly report, configurations that fit the target equally
well? A good answer should:
- turn the 5 selection misses above into correct answers, or into honest set answers the scorer can
  credit;
- keep confidently wrong at 0;
- fit the budget (one target, one held-out claim, about 100-200 runs);
- be checkable for free on the recorded runs first (`--ledger-from`, `--resume`) before a new sealed
  test.

Ideas noted earlier but **not** pursued, for reference:
- a 16-run resolution-IV fractional-factorial interaction screen (TODO item 7; deferred until a power
  study says it helps);
- evidence as a prior with racing confirmation (item 15).
