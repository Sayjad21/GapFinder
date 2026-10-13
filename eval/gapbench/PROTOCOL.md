# GapBench test protocol (pre-registration)

This file is committed before any test-set run. It fixes what is run, how it is scored and what
may be claimed, so that none of it can be chosen after the results are seen. Any change after the
first test run goes in the "Amendments" section at the bottom, with the date and the reason, and
the results are then labelled as run under the amended protocol.

## 1. What is tested

The test set is every task in `eval/gapbench/tasks/` whose `split` is `test`, from two sources
that are reported separately and together:

| Source | Task ids | Who chose the tasks |
|---|---|---|
| Sealed random generator (`gen_tasks.py`) | `test-gen-*` | a seed drawn after GapFinder was frozen |
| Independent AI task author | `test-ai-*` | a model from another vendor, written to fool GapFinder |

The dev tasks (`dev-*`) are the ones GapFinder was tuned on. They appear in the results as their
own group and are never mixed into the test numbers. Every task uses one of our two toy artifacts
(`rlbench`, `mlbench`), so these are called "blind tasks", not outside papers.

The answer keys stay out of the task folders. The scorer reads them from
`eval/gapbench/sealed/<task>/` (`--answers eval/gapbench/sealed`). Nobody who tunes GapFinder
opens them before scoring.

## 2. Arms

| Arm | What it is |
|---|---|
| `gapfinder` | claim ledger (Ultra), assumption space, then the full search with verification |
| `gapfinder-noverify` | the same, without the counterfactual, held-out and plausibility checks |
| `baseline-super` | mini-swe-agent with Nemotron 3 Super |
| `gapfinder-random` | the same hypothesis space and budget as `gapfinder`, in random order, with no ledger ranking and no strong-lead skip, seed 0 (`--rank random`) |
| `gapfinder-noevidence` | the full search with the evidence step off (`--no-evidence-gate`): a closing value is at most "Fits but unsupported" |
| `baseline-ultra` | mini-swe-agent with Nemotron 3 Ultra (included only if the budget allows and S agrees) |

An arm that is not run is simply absent from the results. No arm is dropped after its results are
seen.

## 3. Equal budgets

Every arm gets the same inputs and limits for each task:

- the same model family and tier where the arms are comparable (the baselines differ from
  GapFinder in tier by design, and the arm names say so);
- the same paper text, the same claims table with the paper's numbers and the same naive numbers;
- the same repo map of the artifact: the baseline prompt carries the same `build_repo_map` summary
  the ledger step uses (`eval/baseline/prompt.md`), though not the source excerpts the ledger step
  also reads;
- the same sandbox type and tools (`--backend local` for the toy artifacts);
- a per-task dollar cap of `--cap 0.5`, enforced for every arm through the spend ledger;
- the baseline step limit `--steps 40`;
- the same sealed answer key, read only by the scorer.

Two limits are reported but not enforced by the harness at the time of writing: the number of
experiment runs (GapFinder is capped at 200 by `SearchConfig`; the baseline is limited by steps and
dollars only) and wall time. Both are recorded for every run and reported per arm, so a difference
in budget is visible. If enforcement is added before the first test run it is listed under
Amendments.

GapFinder repeats use `--fresh`, so that repeats do not reuse cached model answers. Baseline
repeats always call the model.

## 4. Runs

Each arm runs each task 3 times (`--run 1`, `--run 2`, `--run 3`). All runs are scored; a run that
crashes or produces no usable answer is scored as missed, never dropped. The scorer also reports
how often an arm's answer changes across its 3 runs (answer stability).

## 5. Scoring rule

A task has a category. It comes from the `category` field of the answer key, and from the task's
`type` if there is none (`single_unstated` and `stated_code_differs` are known cause, `interaction`
is interaction, `no_cause` is no cause). Only the primary claims are scored. A prediction is
**confident** if its label is Explained, Paper-artifact inconsistency, Partially explained or
Attributed (a baseline answer that names knobs), and it names at least one knob. The labels
Unexplained, Inconclusive and Reproduced, and a missing prediction, are not answers.

**Unexplained, Inconclusive and Reproduced all count as abstentions.** A hedged "Fits but
unsupported" is not confident either: it counts as an abstention when the task has no findable
cause, and as found only when its knobs are exactly right (see below).

Each run gets one outcome per task:

| Category | How it is built | Correct | Partial | Confidently wrong | Correct abstention | Missed |
|---|---|---|---|---|---|---|
| Known cause (`known_cause`) | one hidden knob | the proposed knobs equal the hidden knob and value, at any label that is not an abstention | n/a | a confident answer with other knobs | n/a | no answer, an abstention, or a hedged answer with the wrong knobs |
| Interacting settings (`interaction`) | two knobs, neither enough alone | both knobs, with their values | only some of the true knobs, none of them wrong | a confident answer containing a knob that is not part of the cause | n/a | as above |
| Several plausible causes (`decoy`) | a decoy knob also moves the target but breaks a held-out claim | the true knob, not the decoy | n/a | a confident answer naming the decoy or any other knob | n/a | as above |
| No supported explanation (`no_cause`) | an offset no knob explains | n/a | n/a | a confident attribution | no confident attribution | no prediction at all (crashed run) |
| Measurement noise only (`noise_only`) | the paper value is inside the noise of the naive run | n/a | n/a | a confident attribution | no confident attribution (the ideal labels are Reproduced or Inconclusive) | no prediction at all |
| Incomplete paper or artifact (`incomplete`) | the true knob is not exposed by the harness spec | n/a | n/a | a confident attribution | no confident attribution (the ideal label is Unexplained, with the reason in the report) | no prediction at all |

Knob names and values are compared after normalising dashes, underscores, case and numeric format
(`same_knobs` in `score.py`). Values are compared as numbers when both parse.

For tasks with a cause, each proposed configuration is also re-run by the scorer (3 repeats, never
the arm's own report) to compute `gap_closed`, the share of the paper gap that the proposed
configuration closes.

### Trust matrix

For each arm, rows are the truth (a cause exists, or none) and columns are what the arm said:
correct cause, partly correct cause, wrong cause stated confidently, abstained, missed. It is a
view of the same counts, and shows whether the arm knows when to abstain.

## 6. Reported numbers

Per arm, for the test set as a whole and for each source separately: counts of correct
attributions, partial, confidently wrong, correct abstentions and missed; the rates with 95%
Wilson intervals; `gap_closed`; experiments used; wall time; cost; answer stability across the 3
runs. Rates over runs treat the 3 runs of a task as independent, which they are not, so the
intervals are optimistic. For that reason the number of tasks solved in the median run is also
reported with its own interval over tasks, and counts are always shown next to rates.

## 7. How many times the test set is run

The test set is run **exactly twice**: once now (`eval/results/gapbench_test_v1.json`), and once on
the frozen v1.0 release. Both results are published, whatever they show. No task is added, removed
or edited between the two, and GapFinder changes between them are listed in the commit history.
Dry runs on throwaway seeds (generator checks) are not test runs and their tasks are deleted.

## 8. What may be claimed

- With a few dozen task-runs, no comparison is statistically conclusive, and the results never
  claim it. Counts and intervals are reported; where intervals overlap, the text says the data do
  not separate the arms.
- Generator tasks, AI-authored tasks and both together are reported as three results. A win on one
  source and not the other is reported as such.
- The generator's categories and value pools were designed by us, and the tasks use toy artifacts.
  The honest summary is "tasks drawn at random by a generator from a seed created after GapFinder
  was frozen, and tasks written by an independent AI model with no part in building GapFinder".
- A confidently wrong answer is reported next to every correct one. A system that is right more
  often but also confidently wrong more often is described as exactly that.

## Amendments

- 2026-10-11, after test run 1 (reporting only, no change to arms or scoring): until the second
  (v1.0) test run, only aggregate scores are published (`eval/results/gapbench_test_v1_summary.json`).
  Per-task rows, categories, `eval/gapbench/sealed/` and the seed are committed after the v1.0 run,
  so the answers are not public while GapFinder could still change. `eval/gapbench/sealed.sha256`
  pins them in the meantime. Any GapFinder change between the two runs is listed here.
- Run 1 arms: gapfinder, baseline-super, gapfinder-noverify, gapfinder-random,
  gapfinder-noevidence. baseline-ultra was not run (budget), decided before any run.
- 2026-10-13, test run 2 on the frozen tag `v1.0` (runs 4-6; reporting and logistics only, no change to
  arms or scoring):
  - **Same design as run 1.** The same five arms (gapfinder, gapfinder-noverify, baseline-super,
    gapfinder-random, gapfinder-noevidence; baseline-ultra again not run), the same 8 generator tasks,
    the same `--cap 0.5`, the same `--steps 40` for the baseline, `--fresh` for every GapFinder run, and
    3 runs per arm per task, scored with `score.py --runs 4,5,6`. No task was added, removed or edited
    between the two runs. The code changes between run 1 and `v1.0` (checked with
    `git diff pre-tasks-1 v1.0 -- gapfinder eval/baseline eval/gapbench/harness.py eval/gapbench/score.py scripts`):
    `gapfinder/sandbox/backend.py` (the local backend passes one-thread BLAS caps to Docker containers
    only, commit 4817c70, needed by the MC Dropout case), `score.py` (the `--runs` option, commit
    594ef85) and a launcher script for the MC Dropout arms. None touches the search, the prompts or the
    baseline, and `git diff v1.0 -- gapfinder eval/baseline eval/gapbench/harness.py` is empty at the time
    of scoring.
  - **A failed first attempt, and the guard variable.** The first launch of run 2 on `v1.0` failed:
    GapFinder's sandbox guard (`GF_SANDBOX_GUARD_USD`, default $60) refused every GapFinder run with
    `BudgetExceeded`, because the sandbox cost reported in the spend ledger had reached $1,932.00 from
    the earlier MC Dropout Sandboxes work. The guard counts reported Sandboxes `cost`, which is not billed
    during the Beta, and GapBench's toy artifacts run on the local backend, so it is unrelated to these
    runs. About 3 runs were launched and wasted (about $0.15 of billed inference); their logs are
    `runs/gapbench-test-v1.0-attempt1-*.log` and are not committed (`runs/` is git-ignored). The run was
    relaunched in full with `GF_SANDBOX_GUARD_USD=20000`. That changes no behaviour of the search, the
    prompts or the scoring; it only lets the guard pass. The failed attempt produced no scored output,
    and no run was kept or dropped on the basis of its result.
  - **One failed run, scored missed.** `gapfinder-random`, `test-gen-01`, run 6 crashed with a
    `BadJSONError` (a truncated model answer in the claim-ledger step; the file is
    `eval/gapbench/runs/test-gen-01/gapfinder-random/run6/error.txt`). Per section 4 it is scored as
    missed, not dropped and not re-run. `test-gen-01` has no cause, so this shows up as one "missed"
    where run 1 had a correct abstention (`gapfinder-random`: 8 of 9 correct abstentions in run 2).
  - **Published as promised.** The per-task rows, categories, the sealed answer folder
    (`eval/gapbench/sealed/`, its hash equals `eval/gapbench/sealed.sha256`) and the seed are now
    committed, as the 2026-10-11 amendment said they would be. Per-task results are in
    `eval/results/gapbench_test_v1.json` (run 1, runs 1-3) and `eval/results/gapbench_test_v2.json`
    (run 2 on `v1.0`, runs 4-6). Per section 7, the test set is not run a third time.
  - **Independent AI-authored tasks: still pending.** No `test-ai-*` task exists yet, so every number
    above is from the generator tasks only. If a team member runs the AI-authored tasks later (two arms,
    on `v1.0`, runs 4-6), that result is reported separately and gets its own amendment.

## Amendment for the next sealed test (v1.1), written before its seed exists

- **Generator changes since the v1.0 set:**
  - 10 tasks: the v1.0 eight, plus 2 `out_of_space` tasks. In those, the paper's numbers come from a
    code-level bug in an older, patched copy of the artifact (`eval/gapbench/variants.py`; mlbench
    `drop_scaled`: the loader reads only the unit-scale columns). The artifacts themselves are unchanged,
    so neither the repo map nor any spec shows the bug. The rlbench candidates were rejected in a dry
    run: its held-out claim is too noisy to rule anything out, so a single setting mimicked every one.
  - Rivals are checked over GapFinder's whole search space (pools plus v1.1 coverage values), not only
    the pools.
- **Reproducing the published v1.0 set:** it was drawn with the generator at tag `pre-tasks-1`. Check
  out that tag to regenerate it from `eval/gapbench/sealed/seed.txt`. The current generator draws
  differently by design.
- **Scoring additions (reported next to the v1.0 numbers, never instead of them):**
  - `correct_set`: right knobs, and each true value inside the run's equally-good set;
  - `in_space_recall`, `no_cause_specificity`, and their mean `balanced_accuracy`;
  - `out_of_space_diagnosed`: the run's history-matching diagnosis says out of space on an
    `out_of_space` or `incomplete` task;
  - the **always-Unexplained row**: recall 0, specificity 1, balanced 0.5, diagnosis 0.
- `out_of_space` is scored as an abstention category: any confident attribution is confidently wrong.
