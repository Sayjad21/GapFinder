# Informer (AAAI 2021): ETTh2 multivariate, horizon 24

Paper: Zhou et al., "Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting",
AAAI 2021 (arXiv 2012.07436v3). Repo: zhouhaoyi/Informer2020 at 29f2a739226a509202a092b464163da81fa74960.

## Claims

| claim | metric | paper | role |
| --- | --- | --- | --- |
| Table 2, Informer, ETTh2, horizon 24, MSE | `etth2_24_mse` | 0.720 | target |
| Table 2, Informer, ETTh2, horizon 24, MAE | `etth2_24_mae` | 0.665 | held out (same run, shared setting) |

The MAE is computed by the same test pass as the MSE, so one setting has to fit both: not tuned separately.

The other ETTh2 horizons (48: 1.457/1.001, 168: 3.489/1.515, 336: 2.723/1.340, 720: 3.467/1.473) are left out.
From the paper's text they were tuned per setting: "We conduct grid search over the hyper-parameters, and
detailed ranges are given in Appendix E.3", and Appendix E.3: "The length of encoder's input sequence and
decoder's start token is chosen from {24, 48, 96, 168, 336, 480, 720} for the ETTh1, ETTh2, Weather and ECL
dataset" and "the layer of encoder is chosen from {6, 4, 3, 2}". The sensitivity section says the best input
length depends on the horizon ("when predicting short sequences (like 48), initially increasing input length
... degrades performance ... the MSE gets lower with longer inputs in predicting long sequences (like 168)").
They would be `"tuned_separately": true`, so they could only be reported, never used to check a fit. Running
them would double or triple each cell's cost (each takes its own input lengths and depth from
scripts/ETTh2.sh, and the 168+ horizons use 336-step inputs, which would not fit a 3600 s run on 4 vCPUs).

## Image

`python:3.7-slim` with the README's pins: torch 1.8.0+cpu, numpy 1.19.4, pandas 0.25.1, scikit-learn 0.21.3,
matplotlib 3.1.1. torch 1.8.0 also keeps `models/embed.py`'s `torch.__version__>='1.5.0'` string test right
(it picks padding 1; a 1.10+ version string would compare as older and break the shapes). The repo is fetched
at the commit; `ETT-small/ETTh2.csv` (17420 rows) is fetched from zhouhaoyi/ETDataset (main) into
`data/ETT/` during the build. No repository file is changed.

## Harness

- `harness/run.py` (uploaded as `gf_harness/run.py`): seeds python, numpy and torch from `GF_SEED`, changes
  directory to `/work/out` (so the hard-coded `./results/` folder lands under `out/`), and runs
  `main_informer.py` unchanged as `__main__` with the given flags.
- The run command derives `GF_SEED` from RUN_TAG (cksum mod 100000), as pygcn's spec does. The code has no seed
  flag and sets no seed, so without this every process would draw its own; with it, repeats differ in weight
  init, ProbSparse key sampling and the shuffled train loader, reproducibly.
- `harness/emit.sh`: reads the `mse:x, mae:y` line `exp.test` prints and emits `etth2_24_mse`, `etth2_24_mae`
  (normalized scale, as the paper's tables). It deletes the saved checkpoint and predictions.
- Fixed in the command: the claim's data, task and horizon (`--data ETTh2 --features M --pred_len 24`), `--itr 1`,
  `--des Exp`, paths, `--num_workers 0`.

## Naive run

The repo's command for this exact experiment is the first multivariate line of `scripts/ETTh2.sh` (the README's
Results section: "the experiment parameters of each data set are formated in the .sh files in the directory
./scripts/"; its Reproducibility section runs those scripts):

    python -u main_informer.py --model informer --data ETTh2 --features M --seq_len 48 --label_len 48 \
        --pred_len 24 --e_layers 2 --d_layers 1 --attn prob --des 'Exp' --itr 5

with every other flag at `main_informer.py`'s default. The README's shorter usage line
(`--model informer --data ETTh2 --attn prob --freq h`) is a generic example using the defaults (seq_len 96);
the script is the per-experiment setting, so it is the naive run. `--itr 5` becomes `--itr 1`: one run per
cell, the repeats give the spread (the paper averages 5 runs).

Full scale: the full ETTh2 split (12/4/4 months), full epochs (6, early stopping patience 3), batch 32, d_model
512. Smoke runs (checkpoint 606f7469-d5af-4faa-8b21-56836e791ca1): about 200-210 s per epoch, early stop after
epoch 4 and 5, 1020 s and 1220 s wall, 1.46 GB peak RSS (VM 3.9 GB); MSE 0.631 and 0.485, MAE 0.623 and 0.540.
No scale-down, so `discrepancy` is left unset.

## Knobs

Every argparse flag of `main_informer.py` that changes training or evaluation, default from the script line
above or else the code:

model (informer; choices informer, informerstack), freq h, seq_len 48, label_len 48, d_model 512, n_heads 8,
e_layers 2, d_layers 1, s_layers 3,2,1 (read only by informerstack), d_ff 2048, factor 5, padding 0, distil True,
dropout 0.05, attn prob, embed timeF, activation gelu, mix True, train_epochs 6, batch_size 32, patience 3,
learning_rate 0.0001, lradj type1, inverse False.

`distil`, `mix` (store_false) and `inverse` (store_true) are True/False knobs that the command turns into the
flag. Choices come from the help strings / code branches.

Left out, and why:
- claim-defining (they pick the table cell): `--data`, `--features`, `--pred_len`;
- overwritten for ETTh2 by `main_informer.py`'s `data_parser` (setting them does nothing): `--enc_in`,
  `--dec_in`, `--c_out`, `--target`, `--data_path`;
- never read on this path: `--loss` (`exp_informer._select_criterion` always returns `nn.MSELoss`), `--cols`
  (`Dataset_ETT_hour` ignores it), `--output_attention` (only returns attention maps), `--do_predict` (an extra
  forecast after the test);
- how to run: `--root_path`, `--checkpoints` (paths), `--num_workers`, `--itr`, `--des`, `--use_gpu`, `--gpu`,
  `--use_multi_gpu`, `--devices`, `--use_amp` (CUDA only; the VM is CPU-only).

`max` caps (values above are reported, not run), so one run stays under the 3500 s timeout: seq_len and
label_len 96, d_model 512, d_ff 2048, e_layers 4, d_layers 3, train_epochs 12. The paper's stated values
(2-layer decoder, 3-layer + 1-layer encoder stack, 8 epochs, lr 1e-4, batch 32, 16 heads in Table 7) are all
under the caps.

## Deviations

- `--itr 1` instead of the script's 5; repeats are separate cells with RUN_TAG-derived seeds.
- Seeds set by the harness wrapper (the code sets none).
- CPU instead of the authors' GPU (torch 1.8.0 CPU build), 2 torch threads in the search (4 in the smoke and the resumed naive runs).
- Input-length / width caps above, for cost only.

## Budget and the first search attempt

First attempt (`run_a/`, `--max-runs 90`): the five naive repeats took 67-100 min each from launch to result
(Sandboxes reported elapsed 4021-5995 s, user CPU 3981-5946 s, while the run's own log shows about 220 s per
epoch, the smoke's speed: other dev-set searches were running at the same time). One of the five was killed
by the per-process CPU-time limit (`ulimit -t 6000`, GF_SANDBOX_CPU_LIMIT_S): a 4-thread run that goes past
about 5-6 epochs uses about 6000 CPU-seconds. Naive results: MSE 0.504, 0.309, 0.456, 0.494 (median 0.475),
MAE 0.556, 0.416, 0.527, 0.545 (median 0.536). At that pace 90 runs would take about 16 hours, so it was
stopped after the naive repeats.

Second search (`run/`): resumes those five naive results (`--resume run_a/events.jsonl`; they count against
the run budget) and runs torch with 2 threads (`OMP_NUM_THREADS=2 MKL_NUM_THREADS=2` in the command, how to
run only: same model, same data, same seeds), which uses fewer CPU-seconds per run than 4 threads, so fewer
runs reach the CPU-time limit. At about 80-90 min per wave of 8, about 4 hours is about 3 waves:
`--max-runs 28` (5 resumed + 23 new). `GF_SPEND_CAP_USD=33` on the ledger and search.
