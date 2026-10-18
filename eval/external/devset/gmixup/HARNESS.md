# gmixup harness: how G-Mixup is run, and every deviation

Devset case, run as part of devbatch-1 with GapFinder frozen at tag `devbatch-1` (`2af0c3a`). Written before
the search. The runner did not open `../CANDIDATES.md`.

- **Paper:** Han, Jiang, Liu, Hu, "G-Mixup: Graph Data Augmentation for Graph Classification", ICML 2022.
  arXiv has only v1 and v2 (the `2202.07179v3` link returns an error page), so the ledger reads the ICML
  camera-ready from PMLR (`proceedings.mlr.press/v162/han22c/han22c.pdf`). Its Table 2 is the same as
  arXiv v2's.
- **Repo:** `ahxt/g-mixup` at `0813bb32319abbfb29fe82b9ee0c353a6862a1ad`, fetched inside the sandbox.

## Change of target: the released code has no GCN

The batch assigned "Table 2, GCN + G-Mixup on IMDB-B" (72.87). The released code can't run it:
- `src/models.py` defines only `GIN`, and `src/gmixup.py` builds a model only `if model == "GIN"`;
- with `--model GCN` it logs "No model." and crashes at the optimizer:
  `AttributeError: 'str' object has no attribute 'parameters'` (checked in the built image, see `case.json`'s
  setup step).

The README says "run the run_vinilla.sh for vanilla GIN". Writing a GCN into the harness would be the
runner's own code, not the released code, so the case uses the GIN rows of the same table instead:

- **Target:** GIN w/ G-Mixup, IMDB-B, **71.94** (Table 2, ledger claim C34).
- **Held-out:** GIN vanilla IMDB-B **71.55** (C29); GIN w/ G-Mixup IMDB-M **50.46**; GIN vanilla IMDB-M **48.83**.
- **No PROTEINS:** Table 2 has no PROTEINS column (IMDB-B, IMDB-M, REDD-B, REDD-M5, REDD-M12). PROTEINS
  appears only in Table 7, which uses the GMT code, not this repo. IMDB-M is the other small Table 2 dataset
  (1500 graphs, 13 nodes on average), so it takes PROTEINS' place.
- **Left out:** the REDDIT datasets, which are too large for a Sandboxes VM.

## Image (Token Factory Sandboxes)

`../build_case.py case.json`, checkpoint `d6cea2d6-3592-4331-b6f4-0564404bd77d`:
- `python:3.7-slim`, with this folder's `harness/` as `/work/gf_harness/`;
- `torch==1.7.1+cpu` and PyG 1.6.3 with the README's extension versions (`torch-scatter 2.0.5`,
  `torch-sparse 0.6.8`, `torch-cluster 1.5.8`, `torch-spline-conv 1.2.0`, CPU wheels from data.pyg.org for
  torch 1.7.0), `scikit-image 0.18.3`, `numpy 1.19.5`, `scipy 1.5.4`;
- **one deviation:** `opencv-python-headless==4.5.3.56` instead of `opencv-python==4.5.3.56`. It's the same
  version and the same `cv2` module, without the GUI libraries, which the slim image lacks (`libGL`). The
  code only imports `cv2` in `graphon_estimator.py`, for a resize the G-Mixup path doesn't call;
- IMDB-BINARY and IMDB-MULTI fetched at build time through PyG's `TUDataset`, into the same
  `./<name>/<name>` folders the run uses.

**No repository file is changed.**

## The naive run and the cell

**Naive run:** the README's scripts at full scale:
- `run_vanilla.sh` (vanilla) and `run_gmixup.sh` (G-Mixup) with `--model GIN`, and `--dataset` set to the
  metric's dataset (the scripts name GIN and REDDIT-BINARY);
- their flags: `--lr 0.01 --batch_size 128 --num_hidden 64 --aug_ratio 0.15 --aug_num 10 --ge USVT`;
- the code's defaults for the rest: `--epoch 800` (the loop runs epochs 1-799), `--lam_range "[0.005, 0.01]"`.

**One cell:**
- the four rows, one seed each, as four parallel processes (one thread each);
- `gf_harness/emit.sh` prints `gin_imdbb_gmixup_acc`, `gin_imdbb_vanilla_acc`, `gin_imdbm_gmixup_acc` and
  `gin_imdbm_vanilla_acc` in percent. It averages over a cell's seeds, which is one seed since the rescope
  below.

**Model selection (a harness decision):** `src/gmixup.py` logs validation and test accuracy every epoch
and selects nothing. The paper says "Note that best test epoch is selected on a validation set, and we report
the test accuracy on ten runs." So a run's accuracy is the test accuracy at the epoch with the highest
validation accuracy. On ties, the first such epoch counts (validation accuracy moves in steps of 1/100 on
IMDB-B and 1/150 on IMDB-M).

**Seeds:**
- `S = cksum(RUN_TAG) % 100000`, and the cell's seed is `S` (the command keeps the
  scripts' `S + 10000*k` pattern for `k` in `0`);
- `--seed` sets `torch.manual_seed` and `random.seed` (the split and the shuffles);
- numpy is not seeded by the code (λ draws and graph sampling), as shipped;
- GapFinder gives every run a fresh `RUN_TAG`, so every run, the calibration runs included, uses different
  seeds.

**Scope, from the smoke runs (Sandboxes, 4 vCPUs, 3.9 GB):**
- one seed of all four rows in parallel took 380 s, and peaked at about 0.5 GB per process (`max_rss_kb`
  492k and 528k);
- a two-seed cell took 778 s (spec-smoke-1). The first search used two seeds per cell, and was stopped
  (see "Rescope" below);
- now one seed per cell, not the scripts' eight: GapFinder repeats cells anyway. A cell's value has the same
  expectation as the paper's ten-run mean, with more noise;
- every training run is at full scale (epochs, data, model), so this is not a scaled-down surrogate, and
  `discrepancy` is left unset.

Smoke values:
- smoke-a and smoke-b: `build_case.py`, one seed each;
- spec-smoke-1: the spec's own command, a full two-seed cell. It took 778 s and peaked at 516k KB.

| Metric | smoke-a | smoke-b | spec-smoke-1 | Paper |
|---|---|---|---|---|
| IMDB-B G-Mixup | 74.50 | 74.50 | 70.00 | 71.94 |
| IMDB-B vanilla | 75.50 | 74.00 | 72.75 | 71.55 |
| IMDB-M G-Mixup | 52.00 | 51.67 | 47.33 | 50.46 |
| IMDB-M vanilla | 50.67 | 45.67 | 50.50 | 48.83 |

## Knobs

**Knobs** are every argparse flag of `src/gmixup.py` that the code reads to train or evaluate, at the run
scripts' values. That gives eight knobs:
- `epoch` 800, `batch_size` 128, `lr` 0.01, `num_hidden` 64, `aug_ratio` 0.15 and `aug_num` 10;
- `lam_lo` 0.005 and `lam_hi` 0.01. `--lam_range` is one flag holding a two-number list (`eval`ed). Its
  bracketed spelling can't pass GapFinder's shell-safety check, so it is split into its two numbers, and the
  command passes `--lam_range "[{lam_lo},{lam_hi}]"`.

**Left out, and why:**
- `--data_path`, `--log_screen`: how to run;
- `--seed`: it comes from `RUN_TAG`;
- `--dataset`, `--model`, `--gmixup`: they say which row a metric belongs to;
- `--ge` and `--gnn`: read nowhere. `ge` is only logged, and the graphon is always
  `universal_svd(..., threshold=0.2)`; `gnn` is never used. Setting them can't change a run.

**Cost caps, fixed before the search:**
- `epoch` ≤ 1600 (2× the default). It was 2400 in the stopped first search; lowered so a cell fits the
  timeout at the slow speed seen there;
- `num_hidden` ≤ 256 (512 in the first search);
- run timeout 3500 s.

Hard-coded values in `src/gmixup.py` are not flags, so they are not knobs. They include Adam's
`weight_decay=5e-4`, `StepLR(step_size=100, gamma=0.5)`, the 0.7/0.1/0.2 split and the USVT threshold
0.2.

## Held-out claims: one shared setting

**From the paper's text only**, one setting is expected to fit all four numbers, so none is
`tuned_separately`:
- "To ensure a fair comparison, we use the same hyperparater for modeling training and the same architecture
  for vanilla model and other baselines." (Appendix F.1);
- "Note that G-Mixup and baseline models adopt the same architecture of GNNs (e.g., layers, activation
  functions) and the same training hyper-parameters (e.g., optimizer, learning rate)." (Section 5.3);
- Appendix F.1 gives one training setting and one G-Mixup setting ("we generate 20% more graphs ... We use
  different λ ∈ [0.1, 0.2]") and doesn't mention tuning per dataset.

## Disclosure: what the runner noticed before the search

While reading the code to write this harness, the runner saw three things:
- Appendix F.1 states λ ∈ [0.1, 0.2] and 20% more graphs, while the scripts run `lam_range` at the code
  default [0.005, 0.01] and `aug_ratio` 0.15;
- the code has no GCN;
- `--ge` is dead.

None of this shaped the harness. The knobs are the flags, chosen mechanically, at the scripts' and the
code's values.

## Search

`gapfinder search` at `devbatch-1`, Sandboxes backend:
- `--concurrency 8 --max-runs 80`, stated here before the run (it replaces the first search's 150; see
  "Rescope"). At the speed seen under the batch's load, a one-seed cell takes about 25 minutes, so this is
  10 rounds, roughly 4 hours;
- `GF_SPEND_CAP_USD=33`;
- defaults for everything else.

## Rescope after the first search (before any result beyond calibration)

The first search (`run0-aborted/`, `search0.*`) used two seeds per cell and `--max-runs 150`. It was stopped
after its five default-setting calibration runs:
- each took 2958-3062 s, against 778 s for the same command in spec-smoke-1;
- user CPU time was about equal to wall time (for example 2947 s of 2963 s). So a VM gave about one CPU's
  worth of time, not four, while the rest of the batch ran in Sandboxes at the same time;
- at that speed a cell is close to the 3500 s timeout, costlier screens (`batch_size=32`, `num_hidden=256`,
  `epoch=1000`) would time out, and 150 runs would take about 16 hours.

Its calibration values (two-seed means; the paper's values are 71.94, 71.55, 50.46 and 48.83):

| Run | IMDB-B G-Mixup | IMDB-B vanilla | IMDB-M G-Mixup | IMDB-M vanilla |
|---|---|---|---|---|
| B0001 | 71.00 | 70.75 | 48.33 | 48.17 |
| B0002 | 70.00 | 71.75 | 51.17 | 49.00 |
| B0003 | 69.25 | 71.25 | 49.17 | 51.67 |
| B0004 | 69.50 | 71.00 | 47.83 | 49.50 |
| B0005 | 74.25 | 74.75 | 46.33 | 51.17 |

What changed, before the second search started:
- one seed per cell, not two;
- `epoch` max 1600, and `num_hidden` max 256;
- `--max-runs 80`.

Nothing else changed: knobs, defaults, targets and selection rule are the same. The search starts afresh
in `run/`.
