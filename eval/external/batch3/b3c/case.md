# Blind case b3c

- Paper: SparseTSF: Modeling Long-term Time Series Forecasting with 1k Parameters
- Authors: Shengsheng Lin, Weiwei Lin, Wentai Wu, Haojun Chen, Junjie Yang
- Venue/year: ICML 2024
- Paper version URL: https://arxiv.org/abs/2405.00946v1 (PDF: https://arxiv.org/pdf/2405.00946v1). Use v1 only.
- Repo: https://github.com/lss-1138/SparseTSF
- Commit: f5cb1753a2420227378b13f6b77f213789e781d3

## Experiment and claims
Table 2 (multivariate long-term forecasting, MSE, look-back 720, mean of 5 runs), SparseTSF row:
- Main target: ETTh2, horizon 336: 0.312.
- Held-out (same row): ETTh2 horizons 96 / 192 / 720: 0.267 / 0.314 / 0.370.
- Held-out (same row): ETTh1 horizons 96 / 192 / 336 / 720: 0.359 / 0.397 / 0.404 / 0.417.
- Out of scope: the Electricity and Traffic columns, which are too large for the VM.

Entry point: `run_longExp.py`, with the per-dataset settings in `scripts/SparseTSF/etth1.sh` and `scripts/SparseTSF/etth2.sh`. One run covers one dataset and one horizon and prints the test MSE and MAE.

## Data
- ETTh1.csv and ETTh2.csv: 17,420 rows × 8 columns each.
- Public, no login: https://github.com/zhouhaoyi/ETDataset (`ETT-small/`), or the Autoformer Google Drive folder linked in the repo README. Place them in `./dataset/`.

## CPU feasibility (sealer's estimate)
- The model has under 1k parameters. With look-back 720 and batch 256, a laptop CPU took about 25 s per horizon, including up to 30 epochs with early stopping.
- All 8 claims fit in under 5 minutes. Memory is well under 1 GB.
- Environment: Python 3.8+, torch, numpy, pandas, scikit-learn, matplotlib (imported by `layers/`).
- On a CPU-only machine `--use_gpu` falls back automatically. The checkpoint reload in `exp/exp_main.py` hard-codes `map_location="cuda:0"`, so it has to map to the CPU instead.

## Seal
- SHA-256 of the answer key: see `answer_key.sha256` next to this file.
- Date: 2026-10-18

Sealed by an independent model (the sealer). The answer key is held outside the repository until the reveal.
