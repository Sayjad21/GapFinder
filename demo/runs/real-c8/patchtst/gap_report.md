# Gap Report: PatchTST (devset)

Artifact `patchtst` · generated 2026-10-27 02:03 · 97 branch runs (0 build/load setups) · sandbox $2912.3201

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_etth1_96_mse (etth1_96_mse) | Unexplained | +1.4% | +1.4% | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Found, but the test failed**: `PatchTST_supervised/data_provider/data_factory.py:19` `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size; with it switched off the program didn't finish (protocol test | no metrics parsed from output: ''). The code may assume it.
- **Measured: the reported numbers depend on this code**: `PatchTST_supervised/Formers/FEDformer/data_provider/data_factory.py:20` `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size; switched off (3 runs):
  - C_etth1_96_mse (`etth1_96_mse`): paper 0.37, as run 0.3751, without it 0.3755 (difference 95% CI [+1.33e-05, +0.000787])
  - C_etth1_96_mae (`etth1_96_mae`): paper 0.4, as run 0.3997, without it 0.4003 (difference 95% CI [+2e-05, +0.000953])
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `n_epochs_pretrain`: "We first apply self-supervised pre-training on the datasets mentioned in Section 4.1 for 100 epochs." (p.6)
  - `context_points`: "PatchTST/64 implies the number of input patches is 64, which uses the look-back window L = 512. PatchTST/42 means the number of input patches is 42, which has the default look-back window L = 336." (p.6)
  - `target_points`: "prediction length T ∈{24, 36, 48, 60} for ILI dataset and T ∈{96, 192, 336, 720} for other datasets" (p.6)
  - `dataset`: "We evaluate the performance of our proposed PatchTST on 8 popular datasets, including Weather, Traffic, Electricity, ILI and 4 ETT datasets (ETTh1, ETTh2, ETTm1, ETTm2)." (p.6)
  - `n_epochs_finetune`: "With (a), we only train the model head for 20 epochs while freezing the rest of the network; With (b), we apply linear probing for 10 epochs to update the model head and then end-to-end fine-tuning th" (p.6)
  - `features`: "We calculate the MSE and MAE of multivariate time series forecasting as metrics." (p.6)

## C_etth1_96_mse: etth1_96_mse (paper 0.37)
**Unexplained** · gap +1.4% → +1.4% · 58 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (58 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `etth1_96_mse` = 0.37.

### What did we measure?
- Naive median 0.3751 over 5 runs; repeats: 0.3749, 0.3757, 0.3751, 0.3755, 0.3748
- Spread: range 0.3748 to 0.3757, noise band ±0.003751 (2 x MAD), CV 0.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +1.4% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: `train_epochs=500`, `train_epochs=250`, `train_epochs=2500`, `train_epochs=5000`, `seq_len=1680`, `seq_len=3360`, `seq_len=16800`, `seq_len=33600`
- Not settable with this harness: `n_epochs_pretrain`, `context_points`, `target_points`, `dataset`, `mask_ratio`, `n_epochs_finetune`, `features`, `scaler`, `random_seed`, `use_gpu`, `loss`, `num_workers`, `gpu`, `itr`, `use_amp`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `batch_size=8` (1.31 noise units, gap -0.1%); `batch_size=16` (1.2 noise units, gap +0.2%); `batch_size=13` (1.17 noise units, gap +0.2%)
- Near alternatives (closest across all claims):
  - `batch_size=8`: this claim +0.0%, mean |gap| 0.7% (4 runs)
  - `@ast:PatchTST_supervised/Formers/FEDformer/data_provider/data_factory.py:20:drop_last=False`: this claim +1.5%, mean |gap| 0.8% (3 runs)
  - `batch_size=16`: this claim +0.5%, mean |gap| 0.8% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | no difference in reporting: the numbers as printed at the end of the run | settings | 34% | 0.3 sigma (fits every claim) | the settings search and the other classes |
| 2 | the setting learning_rate=0.001 | settings | 17% | 0.2 sigma (fits every claim) | run with learning_rate=0.001 |
| 3 | a cause outside every class tested | outside | 10% |  | look for code, data or evaluation differences the classes don't cover |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `learning_rate`: learning_rate=0.001 (max I 0.17); learning_rate=0.005 (max I 0.19)
  - `dropout`: dropout=0.2 (max I 0.17)
  - `d_ff`: d_ff=256 (max I 0.18)
  - `train_epochs`: train_epochs=100 (max I 0.21)
  - `batch_size`: batch_size=32 (max I 0.21); batch_size=13 (max I 0.23)
  - `n_heads`: n_heads=16 (max I 0.22)
  - `pct_start`: pct_start=0.5 (max I 0.22); pct_start=0.03 (max I 0.22)
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
  - `PatchTST_supervised/layers/PatchTST_backbone.py:150`: paper says Dropout with probability 0.2 is applied in the encoders for all experiments.; code does Dropout layer with p=0.3 instantiated.
- Code constants that differ from a value the paper states (matched by name; tried as patch knobs):
  - `PatchTST_self_supervised/datautils.py:186`: the paper states context_points = 336 (PatchTST/42), 512 (PatchTST/64); code has `context_points = 384` (paper: "PatchTST/64 implies the number of input patches is 64, which uses the look-back window L = 512. PatchTST/42 means the nu")

Notes:
- {'batch_size': '8'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'batch_size': '8'} (gap +0.0%); it did not pass verification
- spec knobs no ledger assumption names (seq_len, fc_dropout, padding_patch, affine, subtract_last, decomposition, kernel_size, individual, lradj, patch_len, stride) were screened too; no better answer
- history matching: the naive configuration is within noise of every claim
- patch round stopped early: run budget of 100 reached (wanted 1 more run(s) of {'@ast:PatchTST_supervised/layers/PatchTST_backbone.py:17:n_layers': '1'} for 'patch screen')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_etth1_96_mse | C_etth1_96_mae | Mean |gap| |
|---|---|---|---|---|
| `batch_size=8` | 4 | +0.0% | -1.4% | 0.7% |
| naive (reproduction as run) | 5 | +1.4% | -0.1% | 0.7% |
| `@ast:PatchTST_supervised/Formers/FEDformer/data_provider/data_factory.py:20:drop_last=False` | 3 | +1.5% | +0.1% | 0.8% |
| `batch_size=16` | 4 | +0.5% | -1.2% | 0.8% |
| `batch_size=13` | 4 | +0.4% | -1.2% | 0.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `d_model=128`: other, The program likely enforces that d_model be a multiple of the number of attention heads (n_heads=4) and within a supported range (e.g., ≤64). The value 128 exceeds this limit, causing the setting to be rejected. A valid alternative close to the original intent is 64, which satisfies divisibility and stays within the allowed range. [not taken as invalid_value: the log shows no rejection]
- `d_model=512`: other, The value 512 for d_model likely exceeds an internal limit (e.g., must be ≤ sequence length or ≤ a maximum allowed width), causing the program to reject it before execution. A nearby valid value preserving the intent of a larger width is 256. [not taken as invalid_value: the log shows no rejection]
- `d_model=256`: other, The program likely validates d_model against allowed values (e.g., must be a power of two within a certain range) and rejected 256. A value of 128 keeps the intent of using a larger model size while being a valid setting. [not taken as invalid_value: the log shows no rejection]
- `n_heads=12`: other, The model likely requires n_heads to divide d_model (16); 12 does not, causing the program to reject the setting and produce no metrics. [not taken as invalid_value: the log shows no rejection]
- `d_ff=2048`: other, The value d_ff=2048 likely exceeds the permissible range for the feed‑forward dimension, causing the program to produce no output. A valid alternative that preserves the intent of a larger feed‑forward layer while staying within typical limits is 1024. [not taken as invalid_value: the log shows no rejection]
- `d_model=384`: other, The program rejected d_model=384, likely because it exceeds the allowed maximum or violates a divisibility constraint; a nearby valid value preserving the intent of increasing model width is 256. [not taken as invalid_value: the log shows no rejection]
- `n_heads=40`: other, The model likely requires n_heads to divide d_model (16); 40 does not satisfy this constraint, causing the run to produce no metrics. [not taken as invalid_value: the log shows no rejection]
- `d_ff=1024`: timeout, The run likely exceeded the time limit due to excessively large feed‑forward dimension (d_ff=1024) causing high memory/computation load
- `e_layers=30`: other, The model likely expects a reasonable number of encoder layers; values excessively high (e.g., 30) cause no output/metrics, indicating the setting is invalid. A value like 12 increases depth while staying within typical limits. [not taken as invalid_value: the log shows no rejection]
- `d_model=2`: other, The model's d_model must be divisible by the number of attention heads (n_heads=4). Setting d_model=2 violates this constraint, resulting in no output metrics. [not taken as invalid_value: the log shows no rejection]
- `batch_size=1280`: crash, The batch_size=1280 likely exceeded available memory, causing the training process to crash before producing any output, resulting in no metrics being parsed
- `d_model=160`: other, The program likely enforces that d_model be a power‑of‑two or not exceed a maximum size (e.g., 128). The value 160 violates this constraint, causing the setting to be rejected. A nearby valid value preserving the intent of a larger model dimension is 128. [not taken as invalid_value: the log shows no rejection]

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
- GapFinder commit: `1b6bf29f1932c85ef4fb628d082c8fc243a37b95` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `878a56155bbb661d8e33149dfc3d6776263ba4fd559f7e95a7e69de9debf466a`
- Cost: Nemotron billed $0.0138, sandbox reported $2912.3201 (total $2912.3339; this search; ledger extraction is included only if it shared the search's router)
