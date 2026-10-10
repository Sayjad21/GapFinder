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

None yet.
