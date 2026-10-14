# MC Dropout on GapFinder v1.1 (TODO item 16). NOT blind

This is a fresh search from the blind **normal** ledger (`ledgers/normal/`), so the documented values
were not hand-added to the hypotheses. The setup:

- the same spec, targets and claims as the pre-registered arms;
- the v1.1 search;
- the artifact's code read from a local clone (`GF_MCD_SOURCE`), on Token Factory Sandboxes, with a
  budget of 150 branch runs.

**Not blind.** The answer key was revealed before v1.1 was built, and v1.1 was fixed during this run
(below). So this is a test of the new version on a known case, not evidence of blind performance.

**Runs.** 147 branch runs in three pieces:
- [run-v11/](run-v11/): 100 runs;
- [run-v11-resume/](run-v11-resume/): 8 runs. The process was killed by an editor restart;
- [run-v11-resume2/](run-v11-resume2/): 39 runs.

The resumed pieces reuse the earlier runs, so nothing was run twice. Cost: Nemotron billed about
$0.002. Sandboxes reported about $2,850 (diagnostic; not billed in the Beta).

## What the version under test proposed (from the ledger and the code)

**Fixed while running** (committed between the pieces, see `git log`):
- **Code reading for checkpoint bases** (before the first piece). For a sandbox-checkpoint base, the
  search had silently skipped reading the code, so `epochx` was not a multiplier and the factor 10 was
  never proposed. With the code read, the blind ledger alone gives 12 hypotheses, including both
  documented values: `epochx=10` (a multiplier factor) and `hidden=1` (a boundary value).
- **Lost hypothesis** (after the first piece). In the first piece `epochx=10` was lost:
  - a Theano compile-cache race between shards in one VM made it fail;
  - Super's triage read that as "the program rejected the value" and replaced it with 20.

  Now:
  - an environment failure is retried with the same value;
  - "invalid value" swaps a value only when the log shows a rejection;
  - history matching won't label a configuration that has a single run.

  In the resume, `epochx=10` alone gave Energy RMSE 0.53-0.64 over 6 runs. That matches the
  confirmation runs in RESULT.md (0.533 median).

## Result

| | v1.0 blind arms | v1.1 (this run) |
|---|---|---|
| Label (Energy RMSE, target 1.66) | Unexplained | **Explains target, conflicts with held-out**: `epochx=1`, `hidden=10` (5 runs, median 1.85, +11.5%) |
| History matching | none | **out-of-space suspected**: 5 tested configurations fit Energy alone, others fit Yacht alone, none fits both (40 tested) |
| Documented pair `epochx=10`, `hidden=1` | never proposed | proposed, measured once in the combine round (Energy 1.84, Yacht 2.90) |
| Code leads outside the settings | none | grid search per split (rank 1), `batch_size = 128` (rank 2), `T = 10000` (rank 7): the three documented out-of-flag differences |

**The configurations that fit Energy alone,** with the worst claim's implausibility in brackets (lower
is less inconsistent with Yacht):

| Configuration | Worst claim's implausibility |
|---|---|
| **`epochx=10, hidden=1` (the documented pair)** | **5.78** |
| `epochx=1, hidden=20` | 8.4 |
| `epochx=1, hidden=10` | 9.0 |
| `epochx=1, hidden=5` | 9.76 |
| `epochx=2` | 15.59 |

## Verdict

- **Right:**
  - the direction: far fewer epochs than the code's default of 500, and shallower or one-layer
    variants;
  - the diagnosis: no exposed setting matches both datasets, which is the documented truth (the
    paper-era code also tuned hyperparameters shared across splits);
  - the code leads, which name the documented out-of-flag differences.
- **Not right:** the label names `epochx=1, hidden=10`, not the documented `epochx=10, hidden=1`.
  - Energy alone can't tell the five fits apart. The paper's number has its own spread (±0.19 over
    20 splits).
  - The budget ran out in the combine round, before the documented pair got a second run.
- **Fix made after this run:** history matching now picks among the target fits by the
  least-implausible worst claim, the standard history-matching criterion. The report also lists
  every target fit. On the recorded runs it ranks the documented pair first (5.78), but it stays
  unlabelled until it has a second run.
  - This rule was written after seeing this case, so re-labelling these runs with it is not evidence.
    Only a new blind case can test it.
- **Budget:** v1.1's wider value grid costs about 4x the runs of v1.0 here. The combine round alone
  tried up to 36 pairs. A search on an artifact this slow needs either a larger budget, or a combine
  round that confirms the most promising pairs first.
