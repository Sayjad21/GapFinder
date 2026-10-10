# MC Dropout as a blind external case: feasibility check

**Verdict: go, run locally in Docker (decision: TODO "Decision for S" option 2, scaled like
option 1).** The first attempt, in Sandboxes with the code's `T = 10000`, was a no-go on cost
(about 650 CPU-seconds per grid setting). In Docker on a laptop the cost is time, not money, and
the defaults-vs-paper gap exists (clear on Energy, weaker on Yacht and Concrete); see
[Docker run and gap check](#docker-run-and-gap-check) below. No Nemotron was spent and no sandbox
was used for any of it. The sections after that are the earlier Sandboxes findings, kept as
history.

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

## Docker run and gap check

**Why Docker.** The Sandboxes route needed S's approval and a raised cost guard, and the
paper-faithful run costs about $1,700 of reported time. Docker Desktop is free, the old stack
installs from PyPI, and `T = 100` makes one grid setting seconds long instead of 650 CPU-seconds.
The cost is wall-clock time on this machine (12 CPUs, one process per core) and that the run is
no longer "in Sandboxes".

**Image** ([docker/Dockerfile](docker/Dockerfile), build from this folder:
`docker build -t gf-mcdropout -f docker/Dockerfile .`):
- base `python:3.6-slim` (Python 3.6.15; digest `sha256:2cfebc27956e6a55f78606864d91fe527696f9e32a724e6f9702b5f9602d0474` when built, 2026-10-10);
- numpy 1.13.3, scipy 1.1.0, h5py 2.8.0, Theano 0.8.2, Keras 2.2.0 (pulls Keras-Applications 1.0.2
  and Keras-Preprocessing 1.0.1), `g++`; `THEANO_FLAGS='device=cpu,floatX=float32'`,
  `KERAS_BACKEND=theano`;
- the repo at **commit `6eb4497628d12b0f300f4b4f6bdc386bebad565c`** (master on 2026-10-10), in `/work`;
- the one documented patch, applied at build time: `sed -i 's/T = 10000/T = 100/' net/net.py`
  (this is the only change to the artifact; `git status` in the image shows only `net/net.py` modified, one line, plus the added `run_cell.sh`);
- the Debian 11 base's package mirrors have moved to `archive.debian.org`, so the Dockerfile points
  apt at the archive; nothing else about the build differs from the Sandboxes pins.

`scipy.misc.logsumexp` exists in scipy 1.1.0 and the old Keras `nb_epoch` argument works under
Keras 2.2.0 (a deprecation warning only), so no import shim was needed.

**Harness** ([harness/run_cell.sh](harness/run_cell.sh)): takes `dir=<dataset>[,<dataset>...]`,
`epochx`, `hidden` and the data-file knobs (`n_splits`, `n_epochs`, `n_hidden`, `dropout_rates`,
`tau_values[_<dataset>]`), writes the data files only when asked, runs `experiment.py`, and prints
one `key=value` line per metric (`rmse` = MC-dropout RMSE, `rmse_single`, `ll`, `mean_tau`,
`wall_s`, `cpu_s`, each with a `_sd`), prefixed by the dataset name when several run. It creates
`results/` itself (the earlier crash). Two facts found while writing it:
- `experiment.py` reads `dropout_rates.txt` and `tau_values.txt` with `np.loadtxt`, so a list of one
  value crashes (`'float' object is not iterable`); the harness refuses one-value lists.
- `experiment.py` prints no summary and seeds numpy with 1, and Keras/Theano draw from it, so
  **repeating the same settings on the same splits is bit-identical** (tested: two runs gave
  `rmse=9.417667`, `ll=-7.027138`). Run-to-run noise therefore has to come from different splits:
  the repeats below use disjoint split sets (splits 0-2, 3-5, 6-8 of the repo's 20), through a
  development-only `split_offset` argument that renames the index files. It is not a GapFinder knob.

**Timings** ([gapcheck/timings.txt](gapcheck/timings.txt)):
- the small run, `--dir yacht --epochx 1 --hidden 1`, 2 splits: **39 s wall, 39.7 CPU-s**
  (the Sandboxes attempt at `T = 10000` crashed after 658 CPU-s); one split of it: 27 s through
  the local backend, including container start;
- repo defaults (`--epochx 500 --hidden 2`, 3 splits, 13 networks per split), 9 containers in
  parallel, one core each:

| Dataset | Wall per repeat (3 splits) | CPU-s per repeat |
|---|---|---|
| Yacht | 42-45 min | 2,480-2,660 |
| Energy | 79-85 min | 4,670-5,030 |
| Concrete | 91-92 min | 5,390-5,440 |

  One default cell with all three datasets is therefore about 3.6 CPU-hours (about 1.5 h wall with
  the datasets in parallel). Cost scales with `epochx`: at `epochx` 10 it should be a few minutes.

**Gap check** (defaults only, `T = 100`, 3 repeats of 3 splits each on disjoint splits, grid search
as in the repo; MC-dropout test RMSE; raw files in [gapcheck/](gapcheck/), summary by
`gapcheck/summarize.py`). The documented paper setting (`--epochx 10 --hidden 1`) and every other
knob were deliberately **not** run: that is GapFinder's job later, and running it now would leak the
answer into the development loop.

| Dataset | Repeat means (3 splits each) | sd between repeats | All 9 splits: mean (split s.e.) | Paper Table 1 | Defaults minus paper |
|---|---|---|---|---|---|
| Yacht | 0.905, 0.936, 0.902 | 0.019 | 0.914 (0.105) | 1.11 | -0.20 (-18%), 1.9 split s.e. |
| Energy | 0.396, 0.391, 0.394 | 0.003 | 0.394 (0.020) | 1.66 | -1.27 (-76%), 64 split s.e. |
| Concrete | 3.90, 4.93, 4.43 | 0.52 | 4.42 (0.281) | 5.23 | -0.81 (-15%), 2.9 split s.e. |

Reading it honestly:
- The defaults are **better** than the published numbers on all three datasets, which is the
  direction the README and Mukhoti et al. describe (more training and a deeper net beat the paper's
  smaller budget; the paper's budget would give a higher RMSE).
- **Energy** is a clear gap, far outside any noise. **Yacht** clears the repeat noise (0.019) but is
  only about 2 split standard errors, and its per-split sd is 0.3, so treat it as weak.
  **Concrete** is 2.9 split standard errors but only 1.6 times the (3-repeat) sd between repeats,
  so by the strict rule "gap larger than the 3-repeat noise" it does not pass; it is moderate.
- The paper's own spread is large (listed "+-" is a standard deviation over 20 splits: 0.38, 0.19,
  0.53), and we use 9 splits.
- **Consequence for the targets** (Step 4): use **Energy RMSE** as the headline target claim.
  Yacht and Concrete RMSE are held-out claims whose gap should shrink, not grow, under the true
  cause. Yacht alone, the TODO's earlier suggestion, would be a weak target.
- Not measured, because it would leak: that the paper setting moves these metrics toward the
  paper. The answer key's re-run (Step 5) is where that is confirmed.

Seeds: no seed flag exists. `np.random.seed(1)` is fixed in `experiment.py`, so different seeds
cannot be tried without a code edit; disjoint splits are the available noise source.

**Go / no-go for running the GapFinder search locally in Docker: go, with conditions.**
- Cost per run is time on this machine, not money. A default-like cell (all three datasets,
  `epochx` 500) takes about 1.5 h wall and 3.6 CPU-hours; hypotheses with lower `epochx` are far
  cheaper. A search of 15-25 runs will take on the order of 10-20 hours of CPU if several
  hypotheses keep `epochx` at 500 (for example `hidden` alone), and well under that if the screen
  tries small `epochx` first. Cap the concurrency at the core count divided by three (each cell
  runs its three datasets in parallel): `GF_MAX_CONCURRENCY=3` on 12 cores. Set the run `timeout`
  at 4 hours (the draft spec has it).
- If that is too slow, lower `n_splits` (the knob `max` and default can drop to 2), reported as a
  further scaling.
- Noise: the baseline cell is deterministic, so GapFinder's noise band must come from another
  source. The usual rule for knob-only experiments has no stochastic repeat here; use the
  disjoint-split repeats (this folder's `split_offset`, which would have to be exposed as a knob,
  or a per-cell noise estimate from the gap check: Energy 0.003, Yacht 0.019, Concrete 0.52 for
  the repeat sd). That decision belongs to Step 3 (freeze), before the run.
- The engine's `LocalBackend` can now run commands in the image (below); a full search still needs
  a short dry run on `--max-runs 2` first.

**Local backend inside Docker.** Implemented, small: `LocalBackend.base("docker:gf-mcdropout")`
copies `/work` out of the image (`docker create` + `docker cp`) into a checkpoint directory; every
`run` then starts a fresh container of that image with the checkpoint mounted at `/work` and runs
the stage command there (`docker run --rm -v <checkpoint>:/work -w /work ...`), and a timeout
kills the container. Checkpoints stay directories, so forking, the build patch and parsing work as
for any local run. The draft spec [mcd.yaml](mcd.yaml) uses `base: docker:gf-mcdropout`.
Verified with a throwaway script (the spec's build stage and one `run_cell.sh` cell through the
backend gave the same numbers as the plain container) and by `tests/integration/test_local_docker.py`
(skipped when the image is absent). Limits: each run starts a cold container, so Theano recompiles
(not measured separately; check it in the dry run); a cell with `dir=yacht,energy,concrete` uses three cores, so the engine's
concurrency must be capped; the spec's `base` is not valid for `--backend contree`.

## The earlier attempt in Sandboxes

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

## Options that were put to S (decided: option 2, Docker, scaled as in option 1)

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
