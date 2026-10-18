# batch-3 b3c harness: SparseTSF (Lin et al., ICML 2024)

Written by the runner, who has not seen the answer key. Inputs: `case.md`, the paper (v1) and the repo. No
repository file is changed.

## Image: automatic, then layered

Stage 1 (`env_build.json`, frozen code at tag `batch-3`, README goal `sh run_all.sh`) succeeded, keeping 3 of 4
commands, for $0.0099:
- python:3.8-slim, system libraries, `pip install -r requirements.txt` and ptflops;
- the README's dataset folder, fetched with gdown;
- `weather.csv`, which `run_all.sh` needs.

Layered on top (scratchpad `b3/layer_b3c.py`):
- ETTh1.csv and ETTh2.csv, copied into `./dataset/` from the fetched `ETT-small/`, each 17,421 lines.
  sha256: ETTh1 `f18de3ad...e066`, ETTh2 `a3dc2c59...218b`.
- A CPU shim, `gf_cpu_shim.py`, loaded by a `.pth` file. The code reloads its best checkpoint with
  `map_location="cuda:0"`, which fails without a GPU, so `torch.load` maps to the CPU instead.
- The harness, as `gf_harness/`.

Checkpoint `73fbaf23-9abd-4621-a4b7-f0c0d970300a`.

## Claims (case.md: Table 2, SparseTSF row, look-back 720, MSE)

| Claim | Metric | Paper | Role |
|---|---|---|---|
| C_h2_336 | etth2_336_mse | 0.312 | target |
| C_h2_96, C_h2_192, C_h2_720 | etth2_{96,192,720}_mse | 0.267, 0.314, 0.370 | held-out |
| C_h1_96, C_h1_192, C_h1_336, C_h1_720 | etth1_*_mse | 0.359, 0.397, 0.404, 0.417 | held-out |

One shared setting should fit every horizon of a dataset. The two datasets differ only in learning rate (the
scripts' 0.02 and 0.03), which is a knob per dataset.

## What a run is

One cell = `scripts/SparseTSF/etth1.sh` and `etth2.sh`:
- 2 datasets × 4 horizons = 8 `run_longExp.py` processes, four at a time, one thread each;
- `--num_workers 0`: speed only;
- `emit.sh` reports what the script prints as its test result (`mse:..., mae:...`), averaged over `--itr`
  iterations.

## Knobs

The flags the SparseTSF model, its training loop and its data loader read, at the scripts' values or the code's
defaults: `seq_len`, `period_len`, `label_len`, `train_epochs`, `patience`, `itr`, `batch_size`, `learning_rate`
(per dataset), `lradj`, `pct_start`, `loss`, `embed`.

Left out:
- the flags that define the claim or the data;
- paths and names;
- GPU flags;
- the flags only other models read (d_model, n_heads and so on).

**Seeds:** each iteration is seeded from a fixed list (2023, 2024, ...). Repeated cells are identical: there is
no run-to-run noise.

## Smoke (naive cell)

69 s, 1.0 GB peak.

| Metric | Measured | Paper |
|---|---|---|
| ETTh2 336 (target) | 0.3107 | 0.312 |
| ETTh2 96 | 0.2778 | 0.267 |
| ETTh2 192 | 0.3152 | 0.314 |
| ETTh2 720 | 0.3708 | 0.370 |
| ETTh1 96 | 0.3539 | 0.359 |
| ETTh1 192 | 0.3978 | 0.397 |
| ETTh1 336 | 0.4051 | 0.404 |
| ETTh1 720 | 0.4177 | 0.417 |
