# MC Dropout as a blind external case: feasibility check

**Verdict: no-go as the artifact stands.** The software environment works in Sandboxes, but one
hyperparameter setting costs about 650 CPU-seconds, so the paper's experiment would cost far more
than our budget. Options are below. No Nemotron was spent; sandbox cost is reported, not billed
(Beta).

## The case

- Paper: Gal & Ghahramani, "Dropout as a Bayesian Approximation", ICML 2016. We use the ICML
  proceedings version (proceedings.mlr.press/v48/gal16.pdf). The later arXiv version
  (1506.02142v6) adds an October 2016 update and a Table 2 that state the effect outright, so it
  would give the answer away.
- Code: https://github.com/yaringal/DropoutUncertaintyExps at `6eb4497` (current master).
- Claimed numbers (ICML Table 1, dropout, test RMSE): Concrete 5.23, Energy 1.66, Yacht 1.11.
  The "±" values in the ICML version are standard deviations (0.53, 0.19, 0.38), although the
  header says standard errors. The arXiv version corrects them to standard errors.

## What the paper and code say (written down before any GapFinder run)

- **Paper (ICML p.6):** "50 units", dropout 0.05 and 0.005; "The BO runs used 40 iterations
  following the original setup, but after finding the optimal parameter values we used 10x more
  iterations". The number of hidden layers isn't stated; it is implied by "following
  (Hernández-Lobato & Adams, 2015)", which used one hidden layer.
- **Paper-era code** (commit `a6259f1`, `yacht/net/experiment.py`): `n_epochs*10` (40 x 10 = 400
  epochs) and `[n_hidden]`, i.e. one hidden layer of 50 units.
- **Current code defaults:** `--epochx 500` and `--hidden 2`. Two other differences are code
  changes GapFinder can't test: grid search over dropout {0.005, 0.01, 0.05, 0.1} x tau
  {0.25, 0.5, 0.75}, instead of Bayesian optimisation; and the per-split re-tuning.
- **So the expected finding**, for a scored run, is `epochx=10` and `hidden=1` (paper-artifact
  inconsistency), with only partial closure because of the grid-search change. The scoring rule
  must be committed before any run.

## Checks

| Check | Result |
|---|---|
| Python 3.6 image in Sandboxes | yes: `python:3.6-slim` (Python 3.6.15), 4 CPUs |
| Network inside a sandbox | yes: `pip download` and https://pypi.org both work |
| Old stack installs | yes, in 65 s ($0.12): numpy 1.13.3, scipy 1.1.0 (still has `scipy.misc.logsumexp`), Theano 0.8.2, Keras 2.2.0 (with Keras-Applications 1.0.2, Keras-Preprocessing 1.0.1), h5py 2.8.0, plus `g++` from apt. Checkpoint `c6fbd1fc-a3aa-4aad-91c8-2ed7b35f65ff` |
| One small run | **failed**: `--dir yacht --epochx 1 --hidden 1` with 2 splits crashed after 658 CPU-s ($6.58 reported) |
| Gap vs the paper | not measured |

**Why it crashed:** our upload dropped empty folders, so `UCI_Datasets/yacht/results/` didn't
exist. Fixed in GapFinder: `ContreeBackend.base` now creates empty directories from a `local:`
folder, with a unit test.

**Why it costs so much:** the crash came after the **first** of 12 grid settings on the first
split. In `net/net.py`, `predict()` makes `T = 10000` separate `model.predict` calls (hard-coded),
and it runs once per grid setting plus once for the final model: 13 times per split. At about
650 s per setting, this is the estimate (at roughly $0.01 per CPU-second):

| Scope | CPU time | Reported cost |
|---|---|---|
| one split | ~2.3 h | ~$85 |
| the paper's 20 splits, one dataset | ~47 h | ~$1,700 |

The training itself (40 epochs on about 250 rows) should be small; the 10,000 calls dominate.

## Options (need S's decision; the sandbox guard is at $55.40 of $60)

1. **Scaled run with fewer Monte Carlo samples:**
   - set `T` to e.g. 100 through a harness wrapper that patches `net.py` at run time;
   - use 3-5 splits instead of 20.
   - This is a deviation from the artifact, like RusKey's 2M keys instead of 100M, and must be
     reported as such. 100 samples estimate the predictive mean (RMSE) well; the test
     log-likelihood is affected more.
   - Expected cost, to be measured: a few dollars of reported time per search. GapFinder itself
     still edits no code; the harness patch is fixed and documented before the run.
2. **Run it locally** (Docker with the same pins and GapFinder's local backend). It costs no
   sandbox money, but loses the "in Sandboxes" part and needs a laptop for many hours.
3. **Switch to Candidate B** (Paragraph Vector, about 15-25 min per run, unverified).
4. **Fall back to the RusKey positive control** (about $5-10 reported; needs the guard raised).
