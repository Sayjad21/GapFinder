# MC Dropout on GapFinder v1.2 (2026-10-15). NOT blind

**Setup.** The same setup as [RESULT_v11.md](RESULT_v11.md):
- the blind normal ledger, the same spec and targets, the code read from a local clone;
- a budget of 150 branch runs on Token Factory Sandboxes;
- code frozen at tag `v1.2`, the same code as the sealed v1.2 GapBench test.

**Cost:** 148 runs, Nemotron about $0.002, Sandboxes reported $2,947 (unbilled in the Beta). Some
sandbox API timeouts were retried automatically.

## Result

| | v1.1 (147 runs) | v1.2 (148 runs) |
|---|---|---|
| Label (Energy RMSE, target 1.66) | Explains target, conflicts with held-out: `epochx=1, hidden=10` | Explains target, conflicts with held-out: **`epochx=2`** (6 runs, +13.9%) |
| Documented pair `epochx=10, hidden=1` | 1 run, Energy 1.84 | 1 run, **Energy 1.682 (+1.3%): the closest configuration tested** |
| `epochx=10` alone | 6 runs (after the triage fix) | 6 runs |
| `hidden=1` alone | screened | 6 runs |
| History matching | out-of-space suspected | out-of-space suspected (42 configurations tested) |
| Code leads | grid search, batch size 128, T=10000 | the same |

**The configurations that fit Energy alone** (worst claim's implausibility; lower is less inconsistent
with Yacht):

| Configuration | Worst I |
|---|---|
| `epochx=1, hidden=10` | 5.83 |
| `epochx=10, hidden=1` (documented) | 8.71 |
| `epochx=1, hidden=5` | 9.5 |
| `epochx=2` | 24.18 |

## Verdict

- **The search improved.** Both documented values were confirmed alone (6 runs each), and the
  documented pair was the closest configuration of all.
- **The label did not improve**, for two reasons:
  - **The budget.** It ran out while confirming pairs, so the documented pair, measured once in the
    combine round, never got its confirmation runs.
  - **A bad interaction of two rules added after v1.1.** History matching only labels a configuration
    with at least 2 runs, and among those it picks the least inconsistent. Here the only repeated
    Energy fit was `epochx=2`, which breaks Yacht far worse (I = 24) than the unrepeated fits (6-9). It
    was labelled anyway.
- **The fix**, dev work, since this case is not blind:
  - label a repeated fit only when it is about as consistent as the best fit (within the likelihood
    tie);
  - otherwise report the best fit as an unconfirmed lead, under an Unexplained or out-of-space label;
  - and confirm the closest pairs first in the combine round.
- **The least-inconsistent ranking among Energy fits is not stable across runs.** In v1.1 the
  documented pair ranked first; in v1.2 it ranked second. With one target and one held-out claim, the
  honest answer for this paper remains the set of Energy fits plus "out of space", which is what the
  history-matching section reports.
