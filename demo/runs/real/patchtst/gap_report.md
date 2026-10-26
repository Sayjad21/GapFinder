# Gap Report: PatchTST (devset)

Artifact `patchtst` · generated 2026-10-26 05:05 · 100 branch runs (0 build/load setups) · sandbox $2422.0720

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_etth1_96_mse (etth1_96_mse) | Unexplained | +1.5% | +1.5% | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **How the code computes the reported number** (test-score selection, label-based edits, switches fixed for evaluation):
  - `PatchTST_supervised/Formers/Pyraformer/long_range_main.py:275`: the code selects best_mse, best_metrics by comparing best_mse > mse over epoch_i in range(opt.epoch): it scores on TEST data (leakage)
  - `PatchTST_supervised/Formers/Pyraformer/long_range_main.py:303`: the code selects best_mse, best_metrics by comparing best_mse > mse: it scores on TEST data (leakage)
  - `PatchTST_supervised/Formers/FEDformer/data_provider/data_factory.py:20`: `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size
  - `PatchTST_supervised/Formers/Pyraformer/long_range_main.py:207`: `tqdm(..., leave=False)` on evaluation data: it changes how the evaluation is computed
  - `PatchTST_supervised/Formers/Pyraformer/preprocess_elect.py:121`: `prep_data(..., train=False)` on evaluation data: it changes how the evaluation is computed
  - `PatchTST_supervised/data_provider/data_factory.py:19`: `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `n_epochs_pretrain`: "We first apply self-supervised pre-training on the datasets mentioned in Section 4.1 for 100 epochs." (p.6)
  - `context_points`: "PatchTST/64 implies the number of input patches is 64, which uses the look-back window L = 512. PatchTST/42 means the number of input patches is 42, which has the default look-back window L = 336." (p.6)
  - `target_points`: "prediction length T ∈{24, 36, 48, 60} for ILI dataset and T ∈{96, 192, 336, 720} for other datasets" (p.6)
  - `dataset`: "We evaluate the performance of our proposed PatchTST on 8 popular datasets, including Weather, Traffic, Electricity, ILI and 4 ETT datasets (ETTh1, ETTh2, ETTm1, ETTm2)." (p.6)
  - `n_epochs_finetune`: "With (a), we only train the model head for 20 epochs while freezing the rest of the network; With (b), we apply linear probing for 10 epochs to update the model head and then end-to-end fine-tuning th" (p.6)
  - `features`: "We calculate the MSE and MAE of multivariate time series forecasting as metrics." (p.6)

## C_etth1_96_mse: etth1_96_mse (paper 0.37)
**Unexplained** · gap +1.5% → +1.5% · 60 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (60 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `etth1_96_mse` = 0.37.

### What did we measure?
- Naive median 0.3755 over 5 runs; repeats: 0.3778, 0.3753, 0.3749, 0.3756, 0.3755
- Spread: range 0.3749 to 0.3778, noise band ±0.003755 (2 x MAD), CV 0.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +1.5% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: `train_epochs=500`, `train_epochs=250`, `train_epochs=2500`, `train_epochs=5000`, `seq_len=1680`, `seq_len=3360`, `seq_len=16800`, `seq_len=33600`
- Not settable with this harness: `n_epochs_pretrain`, `context_points`, `target_points`, `dataset`, `mask_ratio`, `n_epochs_finetune`, `features`, `scaler`, `random_seed`, `use_gpu`, `loss`, `num_workers`, `gpu`, `itr`, `use_amp`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `batch_size=16` (1.09 noise units, gap +0.4%); `batch_size=32` (1.07 noise units, gap +0.4%); `batch_size=8` (1.07 noise units, gap -0.4%); `learning_rate=0.001` (1.01 noise units, gap -0.5%)
- Near alternatives (closest across all claims):
  - `learning_rate=0.001`: this claim -0.2%, mean |gap| 0.7% (4 runs)
  - `batch_size=8`: this claim +0.0%, mean |gap| 0.7% (4 runs)
  - `batch_size=16`: this claim +0.5%, mean |gap| 0.8% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | no difference in reporting: the numbers as printed at the end of the run | settings | 34% | 0.3 sigma (fits every claim) | the settings search and the other classes |
| 2 | the setting pct_start=0.0 | settings | 17% | 0.1 sigma (fits every claim) | run with pct_start=0.0 |
| 3 | a cause outside every class tested | outside | 10% |  | look for code, data or evaluation differences the classes don't cover |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `pct_start`: pct_start=0.0 (max I 0.16); pct_start=0.93 (max I 0.22)
  - `e_layers`: e_layers=4 (max I 0.16)
  - `batch_size`: batch_size=32 (max I 0.18); batch_size=13 (max I 0.19); batch_size=64 (max I 0.22); batch_size=16 (max I 0.22)
  - `learning_rate`: learning_rate=0.001 (max I 0.21)
  - `d_ff`: d_ff=13 (max I 0.25)
  - `n_heads`: n_heads=16 (max I 0.26)
- Leads outside the settings (static code checks, nothing run; check these first):
  - selection in code: the code selects best_mse, best_metrics by comparing best_mse > mse over epoch_i in range(opt.epoch): it scores on TEST data (leakage) (`PatchTST_supervised/Formers/Pyraformer/long_range_main.py:275`)
  - selection in code: the code selects best_mse, best_metrics by comparing best_mse > mse: it scores on TEST data (leakage) (`PatchTST_supervised/Formers/Pyraformer/long_range_main.py:303`)
  - eval switch: `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size (`PatchTST_supervised/Formers/FEDformer/data_provider/data_factory.py:20`)
  - eval switch: `tqdm(..., leave=False)` on evaluation data: it changes how the evaluation is computed (`PatchTST_supervised/Formers/Pyraformer/long_range_main.py:207`)
  - eval switch: `prep_data(..., train=False)` on evaluation data: it changes how the evaluation is computed (`PatchTST_supervised/Formers/Pyraformer/preprocess_elect.py:121`)
  - eval switch: `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size (`PatchTST_supervised/data_provider/data_factory.py:19`)
  - selection in code: the code selects best_nrmse, best_metrics by comparing best_nrmse > valid_mse over epoch_i in range(opt.epoch): a tuning protocol the paper may describe differently (e.g. a different search, grid or budget) (`PatchTST_supervised/Formers/Pyraformer/single_step_main.py:194`)
  - unexposed setting: `fine_tune(..., freeze_epochs=10)`: fixed in the call; no flag sets it (`PatchTST_self_supervised/patchtst_finetune.py:159`)
- Code constants that differ from a value the paper states (matched by name; tried as patch knobs):
  - `PatchTST_self_supervised/datautils.py:186`: the paper states context_points = 336 (PatchTST/42), 512 (PatchTST/64); code has `context_points = 384` (paper: "PatchTST/64 implies the number of input patches is 64, which uses the look-back window L = 512. PatchTST/42 means the nu")

Notes:
- {'batch_size': '8'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'batch_size': '8'} (gap +0.0%); it did not pass verification
- spec knobs no ledger assumption names (seq_len, fc_dropout, padding_patch, affine, subtract_last, decomposition, kernel_size, individual, lradj, patch_len, stride) were screened too; no better answer
- history matching: the naive configuration is within noise of every claim
- patch round stopped early: run budget of 100 reached (wanted 1 more run(s) of {'pct_start': '0.0', '@ast:PatchTST_self_supervised/src/callback/scheduler.py:13:div_factor': '0.0'} for 'patch screen')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_etth1_96_mse | C_etth1_96_mae | Mean |gap| |
|---|---|---|---|---|
| `learning_rate=0.001` | 4 | -0.2% | -1.1% | 0.7% |
| `batch_size=8` | 4 | +0.0% | -1.4% | 0.7% |
| naive (reproduction as run) | 5 | +1.5% | +0.0% | 0.7% |
| `batch_size=16` | 4 | +0.5% | -1.1% | 0.8% |
| `batch_size=32` | 4 | +0.9% | -0.9% | 0.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `batch_size=1280`: crash, The run produced no metrics output, indicating the program likely crashed (e.g., out-of-memory) when using batch_size=1280, which is ten times the default and exceeds GPU memory capacity
- `d_model=128`: other, The program likely validates d_model and rejected the value 128, possibly due to exceeding an allowed limit or memory constraints. [not taken as invalid_value: the log shows no rejection]
- `d_model=512`: other, The program failed to parse any metrics when d_model was set to 512, indicating the value is not accepted (likely exceeding an internal limit or violating a divisibility constraint). A nearby valid value that preserves the intent of a larger model width is 256. [not taken as invalid_value: the log shows no rejection]
- `d_model=256`: other, The program likely enforces a maximum or divisibility constraint on d_model (e.g., must be ≤128 or divisible by n_heads). The value 256 violated this constraint, causing the setting to be rejected. A nearby valid value preserving the intent of a larger model size is 128. [not taken as invalid_value: the log shows no rejection]
- `d_model=384`: other, The model likely requires d_model to be a power of two (or divisible by certain factors); 384 does not satisfy this constraint, while 256 is the nearest valid value that preserves the intent of a larger dimensionality. [not taken as invalid_value: the log shows no rejection]
- `d_model=2`: other, The model likely requires d_model to be divisible by the number of attention heads (n_heads=4). Setting d_model=2 violates this constraint, causing the program to produce no metrics. [not taken as invalid_value: the log shows no rejection]
- `d_model=160`: other, The program likely expects d_model to be a power of two (or divisible by n_heads); 160 is not accepted, while 128 is a valid nearby value. [not taken as invalid_value: the log shows no rejection]
- `n_heads=12`: other, The model's multi-head attention requires n_heads to evenly divide d_model (16). Setting n_heads=12 violates this constraint, causing the program to reject the value and produce no metrics. [not taken as invalid_value: the log shows no rejection]
- `n_heads=40`: other, The model requires n_heads to evenly divide d_model (16). Setting n_heads=40 violates this constraint, causing the run to produce no metrics. A valid nearby value is 16, which divides d_model and retains the intent of increasing heads. [not taken as invalid_value: the log shows no rejection]
- `train_epochs=100`: other, The training script likely validates that train_epochs does not exceed a maximum allowed value (e.g., 50) and rejected the provided value of 100 as invalid. [not taken as invalid_value: the log shows no rejection]
- `d_ff=2048`: other, The program did not parse any metrics, indicating it likely rejected the d_ff value as invalid (perhaps exceeding allowed limits or not meeting divisibility constraints). [not taken as invalid_value: the log shows no rejection]
- `d_ff=1024`: other, The error output shows the program rejected the value d_ff=1024, indicating it is not a valid setting for the model configuration. [not taken as invalid_value: the log shows no rejection]
- `d_ff=1280`: other, The program rejected d_ff=1280, likely because only certain values (e.g., powers of two up to 1024) are accepted for the feed‑forward dimension. [not taken as invalid_value: the log shows no rejection]
- `e_layers=30`: other, The program likely rejects e_layers=30 because it exceeds the supported number of encoder layers, resulting in no metrics being parsed. [not taken as invalid_value: the log shows no rejection]
- `e_layers=15`: other, The value 15 for e_layers is likely beyond the allowed range for the model's encoder layers, causing the program to reject it. A valid alternative close to the intended depth is 4 layers. [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `train_epochs=500`, `train_epochs=250`, `train_epochs=2500`, `train_epochs=5000`, `seq_len=1680`, `seq_len=3360`, `seq_len=16800`, `seq_len=33600`

## Knob names
- Ledger names mapped to spec knobs: `n_layers` → `e_layers`
- Screened though no assumption named them (low prior, code-derived values): `seq_len`, `fc_dropout`, `padding_patch`, `affine`, `subtract_last`, `decomposition`, `kernel_size`, `individual`, `lradj`
- Code defaults read from the code instead of the ledger: `e_layers` 2 at PatchTST_supervised/run_longExp.py:60 (ledger said 3)

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `e_layers`: count (range() bound at PatchTST_supervised/layers/PatchTST_backbone.py:186)
- 14 sink value(s) shared by several knobs: no role assigned

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `n_epochs_pretrain`, `context_points`, `target_points`, `dataset`, `mask_ratio`, `n_epochs_finetune`, `features`, `scaler`, `random_seed`, `use_gpu`, `loss`, `num_workers`, `gpu`, `itr`, `use_amp`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `601599e7b427a382fe7641afb062e85173610b07b6107e98ec7bd0c9e75e492f`
- Cost: Nemotron billed $0.0141, sandbox reported $2422.0720 (total $2422.0861; this search; ledger extraction is included only if it shared the search's router)
