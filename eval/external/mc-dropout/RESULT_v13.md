# MC Dropout on GapFinder v1.3 (2026-10-16). NOT blind

**Setup.** As [RESULT_v12.md](RESULT_v12.md):
- the blind normal ledger, the same spec and targets, the code read from a local clone;
- a budget of 200 runs, then a resume to 260 so the patch round could finish
  ([run-v13](run-v13/), [run-v13-patch](run-v13-patch/));
- code at tag `v1.3`, the same code as the sealed v1.3 GapBench test.

**Cost:** 244 runs. Nemotron about $0.002. Sandboxes reported about $3,960 (unbilled in the Beta).

## Result

| | v1.1 | v1.2 | **v1.3** |
|---|---|---|---|
| Label (Energy RMSE, target 1.66) | `epochx=1, hidden=10` | `epochx=2` (fixed later) | **Explains target, conflicts with held-out: `epochx=10, hidden=1`** (the documented pair) |
| Documented pair's runs | 1 | 1 | confirmed (gap +2.8%) |
| History matching | out-of-space suspected | out-of-space suspected | out-of-space suspected; the documented pair is the least inconsistent of 5 Energy fits |
| Code leads tested | none | none | 3 leads, 36 patch configurations, all run |

**v1.3 names the documented pair for the first time.** The confirmation escrow and the likelihood-ordered
combo confirmation gave it the repeats it lacked in v1.1 and v1.2.

## The patch round: three hard-coded constants tested in memory on the real Sandboxes image

The leads are from `gapfinder/ingest/code_checks.py`:
- `net/net.py:70 batch_size = 128` (training);
- `:71 lengthscale = 0.01`;
- `:122 predict(..., batch_size=500)` (inference).

Each was tested alone and with the documented pair. The hook ran under the image's Python 3.6, and
`net/net.py` was not edited.

| Configuration (1 run each) | Energy RMSE (paper 1.66) | Yacht RMSE (paper 1.11) |
|---|---|---|
| pair alone | ~1.71 | ~2.9 |
| pair + training batch 16 | 0.59 | 0.53 |
| pair + training batch 32 (the paper's value) | 0.75 | 0.76 |
| **pair + training batch 64** | **1.37** | **1.18** |
| pair + training batch 256 / 512 / 1024 | 2.23 / 2.40 / 2.80 | 5.47 / 5.29 / 4.20 |
| pair + lengthscale 0.001-0.1 | 1.66-1.86 | 2.1-3.5 |
| pair + prediction batch 62-4000 | 1.63-1.81 | 2.3-2.9 |
| training batch alone (16-1024), no pair | 0.32-0.45 | 0.62-1.16 |

**Verdict:**
- **The training batch size is the only hard-coded constant that moves the held-out claim.** Smaller
  batches mean more SGD steps, so it interacts with the epoch budget.
- Pair + batch 64 comes closest on both claims, but **no configuration fits both within 3σ**. Energy is
  18% low at 64, while Yacht is 6.6% high. So the patch round correctly adopted nothing, and the label
  stays "Explains target, conflicts with held-out" with out of space suspected.
- **This matches the documented truth.** The paper used batch size 32 (one of the documented out-of-flag
  differences). The remaining documented cause is the per-split grid search over dropout and tau
  (hyperparameters tuned per split), and that is a loop, not a literal, so no patch knob can test it.
- The paper's own batch size, 32, overshoots both claims in our scaled surrogate: T = 100 Monte Carlo
  passes, 3 splits instead of 20, the grid search unchanged. So a clean match would not be expected even
  if batch size were the whole story.

**What this shows about the method (post-hoc, not blind):**
- patch knobs work end to end on a real artifact in a real sandbox;
- the code leads point at a constant with a large, real effect on the held-out claim;
- the engine doesn't overclaim: a partial fit is reported as a lead with its measurements, not as an
  explanation.
