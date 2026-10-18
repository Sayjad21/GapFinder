# Gap Report: Anomaly Transformer (ICLR 2022), devbatch-2

Artifact `at` · generated 2026-10-18 16:33 · 5 branch runs (0 build/load setups) · sandbox $267.4214

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_smd_f1 (smd_f1) | Reproduced | -0.5% | n/a | ±1.0% | — |

## C_smd_f1: smd_f1 (paper 92.33)
**Reproduced**: naive gap -0.5% is inside the noise band ±1.0%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `smd_f1` = 92.33.

### What did we measure?
- Naive median 91.9 over 5 runs; repeats: 92.1, 91.7, 91.9, 91.21, 91.99
- Spread: range 91.21 to 92.1, noise band ±0.919 (2 x MAD), CV 0.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -0.5% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `cudnn.benchmark`, `random_seed`, `adjustment_strategy`, `validation_set_for_threshold`, `loss weight lambda`, `lambda_hyperparameter`, `--dataset`, `model_architecture_dmodel_h`, `--data_path`, `gpu_hardware`, `threshold selection method (δ vs r)`, `pytorch_version`, `prior distribution`, `early_stopping_criterion`, `adam_optimizer_betas_eps_weight_decay`, `multi-layer vs single-layer`, `data_loading_shuffling`, `CUDA_VISIBLE_DEVICES`, `sliding_window_stride`, `--pretrained_model`, `--input_c`, `--model_save_path`, `--mode`, `validation split / anomaly score threshold δ`, `anomaly ratio r for threshold selection`, `eval_batch_size`, `dtype_precision`, `random seed / initialization`, `PyTorch version / CUDA version`, `minimax optimization (enabled/disabled)`, `--output_c`, `--anormly_ratio_default`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

Notes:
- naive run is within the noise band of the paper's value

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_smd_f1 | C_smd_precision | C_smd_recall | Mean |gap| |
|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | -0.5% | -0.0% | -1.0% | 0.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `cudnn.benchmark`, `random_seed`, `adjustment_strategy`, `validation_set_for_threshold`, `loss weight lambda`, `lambda_hyperparameter`, `--dataset`, `model_architecture_dmodel_h`, `--data_path`, `gpu_hardware`, `threshold selection method (δ vs r)`, `pytorch_version`, `prior distribution`, `early_stopping_criterion`, `adam_optimizer_betas_eps_weight_decay`, `multi-layer vs single-layer`, `data_loading_shuffling`, `CUDA_VISIBLE_DEVICES`, `sliding_window_stride`, `--pretrained_model`, `--input_c`, `--model_save_path`, `--mode`, `validation split / anomaly score threshold δ`, `anomaly ratio r for threshold selection`, `eval_batch_size`, `dtype_precision`, `random seed / initialization`, `PyTorch version / CUDA version`, `minimax optimization (enabled/disabled)`, `--output_c`, `--anormly_ratio_default`

## Provenance
- GapFinder commit: `e0117a22e2449e3a3f83893083a771a58c49de9f`
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `84326a9581df38145f8418fba4e3fd3d22e5a906e48809255f73a2c1739585ee`
- Cost: Nemotron billed $0.0035, sandbox reported $267.4214 (total $267.4248; this search; ledger extraction is included only if it shared the search's router)
