# devbatch-2 `at` harness: Anomaly Transformer (Xu et al., ICLR 2022)

Repo: https://github.com/thuml/Anomaly-Transformer at `b0ee470c8012bff857fb600462aec6209c4a18d9`. No repository
file is changed; everything below is environment, data or harness.

## Image

**Automatic image: used, but it could not run the experiment as built.** The stage-1 env builder's checkpoint
`d7884403-4902-42f3-a930-aa1fd59d1d71` (python:3.6-slim + `pip install pillow numpy pandas scikit-learn torch==1.4.0`,
resolved to numpy 1.19.5, pandas 1.1.5, Pillow 8.4.0, scikit-learn 0.24.2, scipy 1.5.4, torch 1.4.0, CPU) has every
import load. Running `scripts/SMD.sh` on it failed in two ways:

1. `model/attn.py` lines 29 and 51 call `Tensor.cuda()` unconditionally, which raises "Found no NVIDIA driver" on
   the CPU-only VM (the rest of the code already selects `cpu` when CUDA is unavailable).
2. Memory: with glibc malloc, training at batch 256, 128, 64 and even 32 was OOM-killed at the VM's 3.9 GB within
   seconds (resident memory grew step after step, i.e. heap fragmentation). One batch-32 forward pass already needs
   about 0.7 GB; batch 256 cannot fit at all.

The search base is a checkpoint layered **on top of the automatic checkpoint** (scratch script `layer.py`, which
runs `case.json`'s `setup` on `auto_checkpoint` and uploads `harness/` as `/work/gf_harness/`). It adds:
- `harness/sitecustomize.py`, copied into site-packages: when CUDA is unavailable, `torch.Tensor.cuda` returns the
  tensor itself (an environment shim, not a code edit);
- `libjemalloc2` (Debian apt) preloaded through `/etc/ld.so.preload`. With it batch 32 peaks at 2.78 GB and runs
  about 15% faster than glibc with `MALLOC_MMAP_THRESHOLD_=1048576` (the other setting that fit batch 32);
- the SMD data (below).

Result: checkpoint **`61cf30fc-9cf7-47ec-899b-edb5abdd748a`** (the search's `GF_DEV_BASE`). `case.json` also
records an equivalent pinned recipe for `build_case.py` (same image and resolved pins), which was not needed.

## Data

From the README's Google Drive folder `1gisthCoE-RrKJ0j3KPV7xiibhHWT9qRm`, file `SMD.zip`
(id `187cjlXCedf4v3-Xm-fK7iTQZ6k6BFaDK`, 194,849,677 bytes, sha256
`124b2b48dafce708e989c224db934b9acb8ba5640051db35a0e77060daf089fc`), downloaded at build time inside the VM with
Python `urllib` from `https://drive.usercontent.google.com/download?id=187cjlXCedf4v3-Xm-fK7iTQZ6k6BFaDK&export=download&confirm=t`.
Only the three files the loader reads are extracted to `/work/dataset/SMD/` and checked with `sha256sum -c`:

| file | shape, dtype | sha256 |
|---|---|---|
| SMD_train.npy | (708405, 38) float32 | `ef3a4a4e9c87c939c23e0cdf1190c18a1d41ef1aadb5d6c5ae909514332ef791` |
| SMD_test.npy | (708420, 38) float32 | `64520f6b9351d609bb395e947a3c98f6c513f608c794c571f9a0176d98cdb671` |
| SMD_test_label.npy | (708420,) float32 | `400a29e062ca8c8f8d7e4801c68c35801f3a2180d5d70fe118d6525a33dd3ed2` |

## Scope

SMD only. Confirmed in `data_factory/data_loader.py` (`get_loader_segment`): SMD is built with the function's
default `step=100`, while MSL, SMAP and PSM are built with `step=1`, i.e. about 100x as many training windows
(hours an epoch on 4 CPUs at the measured ~1.5 s per 32-window step).

## Claims (paper Table 1, page 7, row "Ours", SMD columns)

| claim | metric | paper | role |
|---|---|---|---|
| C_smd_f1 | smd_f1 | 92.33 | target |
| C_smd_precision | smd_precision | 89.40 | held-out |
| C_smd_recall | smd_recall | 95.45 | held-out |

Held-out decision, from the paper's text only: Table 1 reports P, R and F1 of one model per dataset, F1 being "the
harmonic mean of precision and recall", under the single protocol of Section 4 "Implementation details" (r = 0.5%
for SMD). So one shared setting should fit all three.

`harness/emit.sh` parses the last `Accuracy : a, Precision : p, Recall : r, F-score : f` line that `solver.py test()`
prints and reports p, r, f times 100 (2 decimals). Nothing else is computed.

## Run and knobs

One run = `scripts/SMD.sh`'s two commands (train, then test) with the knobs below passed to both (SMD.sh passes
the same flags to both). `--input_c 38` and `--pretrained_model 20` are kept as in SMD.sh.

| knob | value | from | max |
|---|---|---|---|
| lr | 1e-4 | main.py default | |
| num_epochs | 3 | SMD.sh 10, **scaled down** | 3 |
| k | 3 | main.py default | |
| win_size | 100 | main.py default | 100 |
| batch_size | 32 | SMD.sh 256, **scaled down** | 32 |
| anormly_ratio | 0.5 | SMD.sh | |

Left out: `--dataset`, `--data_path`, `--mode`, `--model_save_path` (how to run); `--input_c`/`--output_c`
(fixed by SMD's 38 channels; other values break the model's tensor shapes); `--pretrained_model` (parsed by
argparse, never read anywhere). The code sets no seed (no `torch.manual_seed`/`np.random.seed`), so `RUN_TAG` is
not used: each run's own randomness (weight initialisation, training shuffle) is the noise.

## Deviations (all forced by the VM; `discrepancy: 0.05` in the spec)

- **batch_size 256 -> 32.** Rule: halve SMD.sh's 256 until a training run completes in 3.9 GB. 128 and 64 were
  OOM-killed (64 during the per-epoch validation pass) under both glibc and jemalloc; 32 fits (peak 2.78 GB).
  It happens to equal the batch size stated in the paper's text; it was not chosen for that reason.
- **num_epochs 10 -> 3.** Rule: the largest count whose worst case (no early stop) stays within 80% of both the
  per-process CPU-time guard (`ulimit -t 6000`, applied to every sandbox run) and the 3500 s timeout. Measured at
  batch 32: one epoch (train + validation) costs about 430 s wall and about 1475 CPU-s; the test phase about 220 s.
  4 epochs would be ~5950 CPU-s for the training process (over 4800), 3 is ~4450. The learning rate halves every
  epoch (`adjust_learning_rate`), so epochs 4-10 run at 1/16 of the initial rate or below; early stopping
  (patience 3) is unchanged.
- **win_size max 100**: larger windows multiply the attention memory (the window step stays 100) and run out of
  memory at batch 32; smaller values are allowed.
- Environment only: the CUDA no-op shim and jemalloc preload described above. CPU instead of the paper's GPU.

## Smoke runs (base `61cf30fc`)

- 1 epoch, batch 32 (two runs): F1 91.95 / 91.09, P 89.11 / 89.21, R 94.97 / 93.05; 654 s wall, 2270 CPU-s,
  peak 2.78 GB.
- Defaults (3 epochs, batch 32): see below.

## Search base (added when the search was launched)

GapFinder's trace and patch hooks are a `sitecustomize.py` on `PYTHONPATH`; they would shadow the CUDA shim in
site-packages' `sitecustomize.py`, so traced and patched runs would fail on `Tensor.cuda()`. The shim was moved,
unchanged, to `site-packages/gf_cuda_shim.py`, loaded by `gf_cuda_shim.pth` (`.pth` files run at startup whatever
sitecustomize is used). Checked with a shadowing sitecustomize on PYTHONPATH: the shim still applies.
Script: scratchpad `db2/at/pth_layer.py`. Search base: **`111b6ab0-27dc-4341-8328-aa45b8835814`** (layered on
`61cf30fc`). The hook shadowing is a GapFinder bug (its hooks don't chain to an existing sitecustomize), logged in
`../RESULTS.md` to fix after the batch; the code stays frozen for the batch.
