# Gap Report: Anomaly Transformer (devbatch-2)

Artifact `at` · generated 2026-10-26 12:06 · 8 branch runs (0 build/load setups) · sandbox $425.6767

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_smd_f1 (smd_f1) | Reproduced | -0.4% | n/a | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Measured: the reported numbers depend on this code**: `solver.py:341` `pred` is changed under a test on the ground truth (gt): the score then uses the labels (e.g. point adjustment); switched off (3 runs):
  - C_smd_f1 (`smd_f1`): paper 92.33, as run 91.92, without it 2.55 (difference 95% CI [-89.5, -88.6])
  - C_smd_precision (`smd_precision`): paper 89.4, as run 89.17, without it 11.36 (difference 95% CI [-78, -77.3])
  - C_smd_recall (`smd_recall`): paper 95.45, as run 94.84, without it 1.44 (difference 95% CI [-93.6, -91.9])
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `adjustment_strategy`: "We adopt the widely-used adjustment strategy (Xu et al., 2018; Su et al., 2019; Shen et al., 2020): if a time point in a certain successive abnormal segment is detected, all anomalies in this abnormal" (p.6)
  - `validation_set_for_threshold`: "The threshold δ is determined to make r proportion data of the validation dataset labeled as anomalies." (p.6)
  - `lambda_hyperparameter`: "The hyperparameter λ (Equation 4) is set as 3 for all datasets to trade-off two parts of the loss function." (p.6)
  - `model_architecture_dmodel_h`: "Anomaly Transformer contains 3 layers. We set the channel number of hidden states dmodel as 512 and the number of heads h as 8." (p.6)
  - `gpu_hardware`: "All the experiments are implemented in Pytorch (Paszke et al., 2019) with a single NVIDIA TITAN RTX 24GB GPU." (p.6)
  - `threshold selection method (δ vs r)`: "Table 11: Model performance. Choose by δ means that we fix δ as 0.1 for the SMD, MSL and SWaT datasets, 0.01 for the SMAP and PSM datasets. Choose by r means that we select r as 0.1% for SWaT, 0.5% fo" (p.19)

## C_smd_f1: smd_f1 (paper 92.33)
**Reproduced**: naive gap -0.4% is inside the noise band ±1.0%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `smd_f1` = 92.33.

### What did we measure?
- Naive median 91.92 over 5 runs; repeats: 90.8, 91.92, 91.4, 92.09, 92.15
- Spread: range 90.8 to 92.15, noise band ±0.9192 (2 x MAD), CV 0.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -0.4% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `cudnn.benchmark`, `random_seed`, `adjustment_strategy`, `validation_set_for_threshold`, `loss weight lambda`, `lambda_hyperparameter`, `--dataset`, `model_architecture_dmodel_h`, `--data_path`, `gpu_hardware`, `threshold selection method (δ vs r)`, `pytorch_version`, `prior distribution`, `early_stopping_criterion`, `adam_optimizer_betas_eps_weight_decay`, `multi-layer vs single-layer`, `data_loading_shuffling`, `CUDA_VISIBLE_DEVICES`, `sliding_window_stride`, `--pretrained_model`, `--input_c`, `--model_save_path`, `--mode`, `validation split / anomaly score threshold δ`, `anomaly ratio r for threshold selection`, `eval_batch_size`, `dtype_precision`, `random seed / initialization`, `PyTorch version / CUDA version`, `minimax optimization (enabled/disabled)`, `--output_c`, `--anormly_ratio_default`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `@ast:solver.py:341:@if=False`: this claim -97.2%, mean |gap| 94.3% (3 runs)

Notes:
- naive run is within the noise band of the paper's value

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_smd_f1 | C_smd_precision | C_smd_recall | Mean |gap| |
|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | -0.4% | -0.3% | -0.6% | 0.4% |
| `@ast:solver.py:341:@if=False` | 3 | -97.2% | -87.3% | -98.5% | 94.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `cudnn.benchmark`, `random_seed`, `adjustment_strategy`, `validation_set_for_threshold`, `loss weight lambda`, `lambda_hyperparameter`, `--dataset`, `model_architecture_dmodel_h`, `--data_path`, `gpu_hardware`, `threshold selection method (δ vs r)`, `pytorch_version`, `prior distribution`, `early_stopping_criterion`, `adam_optimizer_betas_eps_weight_decay`, `multi-layer vs single-layer`, `data_loading_shuffling`, `CUDA_VISIBLE_DEVICES`, `sliding_window_stride`, `--pretrained_model`, `--input_c`, `--model_save_path`, `--mode`, `validation split / anomaly score threshold δ`, `anomaly ratio r for threshold selection`, `eval_batch_size`, `dtype_precision`, `random seed / initialization`, `PyTorch version / CUDA version`, `minimax optimization (enabled/disabled)`, `--output_c`, `--anormly_ratio_default`

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f8256b2fc021d10bc532dcdc16df7518e9a190a22b1d1a37e43dc1f2bf2b2dd3`
- Cost: Nemotron billed $0.0029, sandbox reported $425.6767 (total $425.6796; this search; ledger extraction is included only if it shared the search's router)
