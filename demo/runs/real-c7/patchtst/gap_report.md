# Gap Report: PatchTST (devset)

Artifact `patchtst` · generated 2026-10-26 15:29 · 100 branch runs (0 build/load setups) · sandbox $2470.8446

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_etth1_96_mse (etth1_96_mse) | Unexplained | +1.6% | +1.6% | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Found, but the test failed**: `PatchTST_supervised/data_provider/data_factory.py:19` `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size; with it switched off the program didn't finish (protocol test | no metrics parsed from output: ''). The code may assume it.
- **How the code computes the reported number** (test-score selection, label-based edits, switches fixed for evaluation):
  - `PatchTST_supervised/Formers/Pyraformer/long_range_main.py:275`: the code selects best_mse, best_metrics by comparing best_mse > mse over epoch_i in range(opt.epoch): it scores on TEST data (leakage)
  - `PatchTST_supervised/Formers/Pyraformer/long_range_main.py:303`: the code selects best_mse, best_metrics by comparing best_mse > mse: it scores on TEST data (leakage)
  - `PatchTST_supervised/Formers/FEDformer/data_provider/data_factory.py:20`: `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size
  - `PatchTST_supervised/Formers/Pyraformer/long_range_main.py:207`: `tqdm(..., leave=False)` on evaluation data: it changes how the evaluation is computed
  - `PatchTST_supervised/Formers/Pyraformer/preprocess_elect.py:121`: `prep_data(..., train=False)` on evaluation data: it changes how the evaluation is computed
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `n_epochs_pretrain`: "We first apply self-supervised pre-training on the datasets mentioned in Section 4.1 for 100 epochs." (p.6)
  - `context_points`: "PatchTST/64 implies the number of input patches is 64, which uses the look-back window L = 512. PatchTST/42 means the number of input patches is 42, which has the default look-back window L = 336." (p.6)
  - `target_points`: "prediction length T ∈{24, 36, 48, 60} for ILI dataset and T ∈{96, 192, 336, 720} for other datasets" (p.6)
  - `dataset`: "We evaluate the performance of our proposed PatchTST on 8 popular datasets, including Weather, Traffic, Electricity, ILI and 4 ETT datasets (ETTh1, ETTh2, ETTm1, ETTm2)." (p.6)
  - `n_epochs_finetune`: "With (a), we only train the model head for 20 epochs while freezing the rest of the network; With (b), we apply linear probing for 10 epochs to update the model head and then end-to-end fine-tuning th" (p.6)
  - `features`: "We calculate the MSE and MAE of multivariate time series forecasting as metrics." (p.6)

## C_etth1_96_mse: etth1_96_mse (paper 0.37)
**Unexplained** · gap +1.6% → +1.6% · 58 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (58 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `etth1_96_mse` = 0.37.

### What did we measure?
- Naive median 0.3758 over 5 runs; repeats: 0.3779, 0.3748, 0.3763, 0.3758, 0.374
- Spread: range 0.374 to 0.3779, noise band ±0.003758 (2 x MAD), CV 0.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +1.6% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: `train_epochs=500`, `train_epochs=250`, `train_epochs=2500`, `train_epochs=5000`, `seq_len=1680`, `seq_len=3360`, `seq_len=16800`, `seq_len=33600`
- Not settable with this harness: `n_epochs_pretrain`, `context_points`, `target_points`, `dataset`, `mask_ratio`, `n_epochs_finetune`, `features`, `scaler`, `random_seed`, `use_gpu`, `loss`, `num_workers`, `gpu`, `itr`, `use_amp`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `learning_rate=0.001` (1.38 noise units, gap +0.2%); `batch_size=8` (1.33 noise units, gap -0.2%)
- Near alternatives (closest across all claims):
  - `batch_size=8`: this claim +0.2%, mean |gap| 0.8% (4 runs)
  - `learning_rate=0.001`: this claim -0.2%, mean |gap| 0.8% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | no difference in reporting: the numbers as printed at the end of the run | settings | 34% | 0.3 sigma (fits every claim) | the settings search and the other classes |
| 2 | the setting pct_start=0.0 | settings | 17% | 0.1 sigma (fits every claim) | run with pct_start=0.0 |
| 3 | a cause outside every class tested | outside | 10% |  | look for code, data or evaluation differences the classes don't cover |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `pct_start`: pct_start=0.0 (max I 0.13); pct_start=0.93 (max I 0.18)
  - `batch_size`: batch_size=64 (max I 0.16); batch_size=32 (max I 0.21); batch_size=16 (max I 0.22)
  - `dropout`: dropout=0.2 (max I 0.2); dropout=0.15 (max I 0.21)
  - `patience`: patience=1000 (max I 0.21); patience=10 (max I 0.22)
  - `train_epochs`: train_epochs=100 (max I 0.23)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `__init__(..., max_seq_len=1024)`: a default no call in the repo overrides (160 call(s)) (`PatchTST_supervised/layers/PatchTST_backbone.py:17`)
  - unexposed setting: `__init__(..., n_layers=3)`: a default no call in the repo overrides (160 call(s)) (`PatchTST_supervised/layers/PatchTST_backbone.py:17`)
  - unexposed setting: `__init__(..., max_seq_len=1024)`: a default no call in the repo overrides (160 call(s)) (`PatchTST_supervised/layers/PatchTST_backbone.py:129`)
  - unexposed setting: `__init__(..., n_layers=3)`: a default no call in the repo overrides (160 call(s)) (`PatchTST_supervised/layers/PatchTST_backbone.py:129`)
  - unexposed setting: `__init__(..., eps=1e-05)`: a default no call in the repo overrides (160 call(s)) (`PatchTST_supervised/layers/RevIN.py:7`)
  - unexposed setting: `__init__(..., max_seq_len=1024)`: a default no call in the repo overrides (160 call(s)) (`PatchTST_supervised/models/PatchTST.py:16`)
  - unexposed setting: `shuffle_flag = True` is a switch passed on to a call; no flag sets it (`PatchTST_supervised/data_provider/data_factory.py:29`)
  - unexposed setting: `drop_last = True` is a switch passed on to a call; no flag sets it (`PatchTST_supervised/data_provider/data_factory.py:30`)
- Where the code differs from the paper (model-proposed, checked against the repo; literal ones were tried as patch knobs, structural ones are not tested):
  - `PatchTST_supervised/layers/PatchTST_backbone.py:150`: paper says Dropout with probability 0.2 is applied in the encoders for all experiments.; code does dropout = 0.3
  - `PatchTST_supervised/layers/PatchTST_backbone.py:33`: paper says The stride length is set 14; code does stride = 8
- Code constants that differ from a value the paper states (matched by name; tried as patch knobs):
  - `PatchTST_self_supervised/datautils.py:186`: the paper states context_points = 336 (PatchTST/42), 512 (PatchTST/64); code has `context_points = 384` (paper: "PatchTST/64 implies the number of input patches is 64, which uses the look-back window L = 512. PatchTST/42 means the nu")

Notes:
- {'batch_size': '8'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'batch_size': '8'} (gap +0.2%); it did not pass verification
- spec knobs no ledger assumption names (seq_len, fc_dropout, padding_patch, affine, subtract_last, decomposition, kernel_size, individual, lradj, patch_len, stride) were screened too; no better answer
- history matching: the naive configuration is within noise of every claim
- patch round stopped early: run budget of 100 reached (wanted 1 more run(s) of {'pct_start': '0.0', '@ast:PatchTST_supervised/layers/PatchTST_backbone.py:17:n_layers': '48'} for 'patch screen')
- mutation round stopped early: run budget of 100 reached (wanted 1 more run(s) of {'@ast:PatchTST_supervised/exp/exp_main.py:101:@mut.35.Call.xdiv2': '1'} for 'mutation screen')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_etth1_96_mse | C_etth1_96_mae | Mean |gap| |
|---|---|---|---|---|
| `batch_size=8` | 4 | +0.2% | -1.3% | 0.8% |
| `learning_rate=0.001` | 4 | -0.2% | -1.3% | 0.8% |
| naive (reproduction as run) | 5 | +1.6% | +0.1% | 0.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `d_model=128`: other, The error indicates the program rejected d_model=128, likely because the model implementation requires d_model to be no greater than 64 (or to be a multiple of certain constraints). A value of 64 preserves the intent of increasing model capacity while staying within allowed limits. [not taken as invalid_value: the log shows no rejection]
- `d_model=512`: other, The program did not parse any metrics, indicating it likely rejected the d_model=512 value (perhaps due to memory or divisibility constraints). A smaller but still large value like 256 maintains the intent of increasing model capacity while being valid. [not taken as invalid_value: the log shows no rejection]
- `d_model=256`: other, The program likely rejected d_model=256 because it exceeds allowed dimensions or causes memory issues; a valid alternative close to the intended increase is 128. [not taken as invalid_value: the log shows no rejection]
- `n_heads=12`: other, The model's multi-head attention requires n_heads to evenly divide d_model (16). Setting n_heads=12 violates this, causing the program to produce no output metrics. [not taken as invalid_value: the log shows no rejection]
- `d_ff=2048`: other, The program did not produce any metrics when d_ff was set to 2048, indicating the value was rejected as invalid (likely exceeding allowed dimensions or causing shape errors). [not taken as invalid_value: the log shows no rejection]
- `d_model=384`: other, The value 384 for d_model likely exceeds the allowed maximum (e.g., must be a power of two ≤256) causing the program to reject it; a nearby valid value preserving the intent of increasing model size is 256. [not taken as invalid_value: the log shows no rejection]
- `n_heads=40`: other, The model likely requires n_heads to evenly divide d_model (16). Setting n_heads=40 violates this constraint, causing the run to produce no output metrics. [not taken as invalid_value: the log shows no rejection]
- `d_ff=1024`: other, The program likely enforces a maximum allowable feed‑forward dimension (e.g., 512) and rejected the value 1024 as exceeding that limit. [not taken as invalid_value: the log shows no rejection]
- `e_layers=30`: other, The model likely cannot handle 30 encoder layers given the other hyperparameters, causing an early exit or error before any metrics are produced. [not taken as invalid_value: the log shows no rejection]
- `d_model=2`: other, The model's d_model must be divisible by the number of attention heads (n_heads=4). Setting d_model=2 violates this constraint, causing the model to produce no parsable metrics. [not taken as invalid_value: the log shows no rejection]
- `batch_size=1280`: other, The program failed to parse metrics when batch_size was set to 1280, indicating the value is not accepted (likely exceeds allowed batch size or causes resource exhaustion). [not taken as invalid_value: the log shows no rejection]
- `d_model=160`: other, The model implementation likely expects d_model to be a power of two (or within a supported set) and divisible by n_heads; 160 is not accepted, while 128 is the closest valid value preserving the intent of increasing dimensionality. [not taken as invalid_value: the log shows no rejection]

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
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `6f7f073810f4967019b05fe3e65a3d0df680f1c67dea20d7a030b079601c6545`
- Cost: Nemotron billed $0.0161, sandbox reported $2470.8446 (total $2470.8607; this search; ledger extraction is included only if it shared the search's router)
