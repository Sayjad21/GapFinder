# PatchTST harness (devbatch-1)

**Paper:** Nie et al., "A Time Series is Worth 64 Words: Long-term Forecasting with Transformers", ICLR 2023,
arXiv 2211.14730v2.
**Code:** github.com/yuqinie98/PatchTST at `204c21efe0b39603ad6e2ca640ef5896646ab1a9`. The supervised code
is in `PatchTST_supervised/`. The artifact's code is not changed.

## Claims

All values come from Table 3, the supervised multivariate results, PatchTST/64 row.

| claim | metric | paper | role |
|---|---|---|---|
| `C_etth1_96_mse` | `etth1_96_mse` | 0.370 | target |
| `C_etth1_96_mae` | `etth1_96_mae` | 0.400 | held-out (same run, MAE) |

ETTh1 horizons 192/336/720 (0.413/0.429, 0.422/0.440, 0.447/0.468) were left out because we can't afford them;
see "Cost" below.

**Tuned separately?** No. The paper describes one setting for PatchTST/64 on ETTh1, for every horizon:
- "PatchTST/64 implies the number of input patches is 64, which uses the look-back window L = 512. [...]
  Both of them use patch length P = 16 and stride S = 8." (Sec. 4.1, Model Variants)
- "For very small datasets (ILI, ETTh1, ETTh2), a reduced size of parameters is used (H = 4, D = 16 and
  F = 128) to mitigate the possible overfitting. Dropout with probability 0.2 is applied in the encoders for
  all experiments." (A.1.4)

The paper says that "the entire model is trained for each prediction horizon" (Sec. 4.2). That means a
separate training run per horizon, not separate hyperparameters. The MAE comes from the same run as the
MSE. So `tuned_separately` is not set.

## Image (`case.json`)

- `python:3.10-slim` with `torch==2.1.2+cpu`, `numpy==1.23.5`, `pandas==1.5.3`, `scikit-learn==1.2.2` and
  `matplotlib==3.7.1`.
- The repo pins `torch==1.11.0`, but its CPU wheel fails to import in Sandboxes ("libtorch_cpu.so: cannot
  enable executable stack"). That is why the image uses 2.1.2.
- `ETTh1.csv` is fetched at build time into `PatchTST_supervised/dataset/`, the script's `--root_path`. It has
  17421 lines, which is 17420 timesteps, matching Table 2.

## Naive run

The naive run is `scripts/PatchTST/etth1.sh` from the README, at `pred_len 96`, with every flag the script
sets. It differs from the script in one way:

- **`train_epochs` 100 → 50 (scale-down, so `discrepancy: 0.05`).** The reason is the CPU-time limit:
  - Sandboxes runs each process under `ulimit -t 6000` (CPU seconds), and a VM has 4 vCPUs.
  - Measured on the image, `seq_len 336`, horizon 96:
    - 4 threads: about 75 CPU-s per epoch, so 100 epochs is about 7500 CPU-s and gets killed.
    - 2 threads: about 41 CPU-s and about 19 s wall per epoch.
    - 1 thread: about 31 s wall per epoch.
  - At the paper's own `seq_len 512`, 2 threads take about 54 CPU-s per epoch, so 100 epochs is about 5400
    CPU-s. That is at the limit before any larger model is tried.
  - With 50 epochs, the defaults take about 1000 s wall and about 2100 CPU-s. `seq_len 512` takes about 2700
    CPU-s.
- **Why 50 epochs is close to 100:**
  - The script's `lradj type3` sets lr = 1e-4 · 0.9^(epoch−3), which is about 7e-7 by epoch 50.
  - With `patience 100`, early stopping never triggers.
  - The checkpoint is the best one on validation, and it is picked across epochs.
  - So the second 50 epochs train at a learning rate below 1% of the start.
- `train_epochs` stays a knob, with `max: 100`.

## Knobs

**Rule:** every `run_longExp.py` flag that reaches PatchTST's training or evaluation path
(`models/PatchTST.py`, `exp/exp_main.py`, `utils/tools.py`). The default is the script's value, or the
argparse default when the script does not set the flag. 23 knobs:

- model: `seq_len 336`, `e_layers 3`, `n_heads 4`, `d_model 16`, `d_ff 128`, `dropout 0.3`, `fc_dropout 0.3`,
  `head_dropout 0`, `patch_len 16`, `stride 8`, `padding_patch end`, `revin 1`, `affine 0`, `subtract_last 0`,
  `decomposition 0`, `kernel_size 25`, `individual 0`
- training: `train_epochs 50` (scaled down, see above), `patience 100`, `batch_size 128`,
  `learning_rate 0.0001`, `lradj type3`, `pct_start 0.3`

Ranges:
- `choices` are the values the code branches on: 0/1 flags, `padding_patch` `end`/`None`, and the `lradj`
  names in `adjust_learning_rate`.
- `max` is set only where cost forces it: `seq_len` 720 and `train_epochs` 100.

**Left out, and why:**
- How to run:
  - `random_seed`: each run passes `$(cksum RUN_TAG) % 100000`, as in pygcn. The paper fixes seed 2021, and
    its Table 14 reports variation across seeds.
  - `is_training`, `model_id`, `des`, `itr`, `checkpoints`, `root_path`, `data_path`, `num_workers`
    (argparse default 10, as in the script).
  - Device: `use_gpu`, `gpu`, `use_multi_gpu`, `devices`, and `use_amp`, which is CUDA autocast only.
  - `test_flop`, `do_predict`.
  - `OMP_NUM_THREADS=2` is how-to-run too: it keeps CPU time under the limit.
- Define the claim: `model PatchTST`, `data ETTh1`, `features M`, `pred_len 96` (the horizon the metric
  belongs to), and `enc_in 7` (the dataset's channel count; any other value breaks the run).
- Read only for tensors PatchTST never uses:
  - `label_len`, `embed` and `freq` only build the decoder input and time stamps, and
    `PatchTST.forward(x)` does not see them.
  - `target` is used only for `features S`/`MS`.
  - `output_attention` and the Former-only flags (`embed_type`, `dec_in`, `c_out`, `d_layers`, `moving_avg`,
    `factor`, `distil`, `activation`) are not read on the PatchTST path.
  - `loss` is not read: the criterion is always `nn.MSELoss`.

## Cell

- One cell is one horizon-96 training: `OMP_NUM_THREADS=2`, one process.
- `gf_harness/emit.sh` parses `mse:x, mae:y` from `Exp_Main.test()`. These are normalised-scale test
  metrics, like the paper's tables.
- Timeout is 3300 s.
- Two concurrent `seq_len 512` processes were killed by OOM (about 1.56 GB each, plus DataLoader workers), so
  a cell runs only one.

## Cost

- Horizons 192/336/720 each need their own training of the same length. A cell cannot hold two at full
  epochs within 3600 s, or two concurrently in 3.9 GB.
- So only the horizon-96 MSE and MAE are claims.

## Running the frozen code

- The frozen worktree has no `.env`, and `gapfinder/config.py` reads `.env` from its own root, so Sandboxes
  returned 403. The repo's `.env` is loaded into the process environment (`set -a; . ./.env`) before the
  ledger and search commands.
- `python -m` puts the current directory ahead of `PYTHONPATH`, so it would import the repo's `gapfinder/`.
  The search uses `python -P` so the frozen code is the one imported.
- The two copies were identical (`diff -r`) when the ledger ran.

## Smoke (checkpoint `23e57d5c-44df-4710-8692-505e45c6d102`)

| run | etth1_96_mse | etth1_96_mae | wall | peak RSS |
|---|---|---|---|---|
| smoke-a | 0.3746 | 0.3991 | 956 s | 1.08 GB |
| smoke-b | 0.3745 | 0.4000 | 1041 s | 1.09 GB |

Paper PatchTST/64: 0.370 / 0.400. For reference, the paper's PatchTST/42 (L = 336) row is 0.375 / 0.399.

## Search

`--max-runs 100 --concurrency 8`. At about 1000 s per default run, that is about 13 rounds, roughly 4 hours.
