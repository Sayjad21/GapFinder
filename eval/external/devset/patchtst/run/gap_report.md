# Gap Report: PatchTST (ICLR 2023), devbatch-1

Artifact `patchtst` · generated 2026-10-18 03:56 · 100 branch runs (0 build/load setups) · sandbox $1920.6207

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_etth1_96_mse (etth1_96_mse) | Unexplained | +1.6% | +1.6% | ±1.0% | — |

## C_etth1_96_mse: etth1_96_mse (paper 0.37)
**Unexplained** · gap +1.6% → +1.6% · 54 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (54 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `etth1_96_mse` = 0.37.

### What did we measure?
- Naive median 0.3758 over 5 runs; repeats: 0.3755, 0.3767, 0.3758, 0.3755, 0.3777
- Spread: range 0.3755 to 0.3777, noise band ±0.003758 (2 x MAD), CV 0.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +1.6% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: `train_epochs=500`, `train_epochs=250`, `train_epochs=2500`, `train_epochs=5000`, `seq_len=1680`, `seq_len=3360`, `seq_len=16800`, `seq_len=33600`
- Not settable with this harness: `n_epochs_pretrain`, `context_points`, `target_points`, `dataset`, `mask_ratio`, `n_epochs_finetune`, `n_layers`, `features`, `scaler`, `random_seed`, `use_gpu`, `loss`, `num_workers`, `gpu`, `itr`, `use_amp`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `batch_size=8` (1.28 noise units, gap -0.3%); `batch_size=13` (1.22 noise units, gap +0.3%); `batch_size=16` (1.2 noise units, gap +0.4%)
- Near alternatives (closest across all claims):
  - `batch_size=13`: this claim +0.2%, mean |gap| 0.7% (4 runs)
  - `batch_size=16`: this claim +0.3%, mean |gap| 0.8% (4 runs)
  - `batch_size=8`: this claim +0.3%, mean |gap| 0.8% (4 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size`: batch_size=64 (max I 0.18); batch_size=32 (max I 0.19); batch_size=16 (max I 0.25); batch_size=13 (max I 0.26); +1 more
  - `patience`: patience=50 (max I 0.19)
  - `pct_start`: pct_start=0.0 (max I 0.22)
  - `n_heads`: n_heads=2 (max I 0.24)
  - `train_epochs`: train_epochs=100 (max I 0.26)
  - `dropout`: dropout=0.05 (max I 0.27)
- Leads outside the settings (static code checks, nothing run; check these first):
  - selection in code: the code selects best_mse, best_metrics by comparing best_mse > mse over epoch_i in range(opt.epoch): it scores on TEST data (leakage) (`PatchTST_supervised/Formers/Pyraformer/long_range_main.py:275`)
  - selection in code: the code selects best_mse, best_metrics by comparing best_mse > mse: it scores on TEST data (leakage) (`PatchTST_supervised/Formers/Pyraformer/long_range_main.py:303`)
  - selection in code: the code selects best_nrmse, best_metrics by comparing best_nrmse > valid_mse over epoch_i in range(opt.epoch): a tuning protocol the paper may describe differently (e.g. a different search, grid or budget) (`PatchTST_supervised/Formers/Pyraformer/single_step_main.py:194`)
  - unexposed setting: `fine_tune(..., freeze_epochs=10)`: fixed in the call; no flag sets it (`PatchTST_self_supervised/patchtst_finetune.py:159`)
  - unexposed setting: `__init__(..., base_momentum=0.85)`: a default no call in the repo overrides (160 call(s)) (`PatchTST_self_supervised/src/callback/scheduler.py:13`)
  - unexposed setting: `__init__(..., max_momentum=0.95)`: a default no call in the repo overrides (160 call(s)) (`PatchTST_self_supervised/src/callback/scheduler.py:13`)
  - unexposed setting: `__init__(..., div_factor=25)`: a default no call in the repo overrides (160 call(s)) (`PatchTST_self_supervised/src/callback/scheduler.py:13`)
  - unexposed setting: `__init__(..., final_div_factor=10000)`: a default no call in the repo overrides (160 call(s)) (`PatchTST_self_supervised/src/callback/scheduler.py:13`)

Notes:
- {'batch_size': '13'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'batch_size': '13'} (gap +0.2%); it did not pass verification
- spec knobs no ledger assumption names (seq_len, e_layers, fc_dropout, kernel_size, patch_len, stride) were screened too; no better answer
- history matching: the naive configuration is within noise of every claim
- patch round stopped early: run budget of 100 reached (wanted 1 more run(s) of {'@ast:PatchTST_self_supervised/src/callback/scheduler.py:13:base_momentum': '0.085'} for 'patch screen')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_etth1_96_mse | C_etth1_96_mae | Mean |gap| |
|---|---|---|---|---|
| `batch_size=13` | 4 | +0.2% | -1.3% | 0.7% |
| `batch_size=16` | 4 | +0.3% | -1.2% | 0.8% |
| `batch_size=8` | 4 | +0.3% | -1.3% | 0.8% |
| naive (reproduction as run) | 5 | +1.6% | +0.1% | 0.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `batch_size=1280`: other, The batch size of 1280 likely exceeds the maximum allowed batch size for the program, causing it to produce no metrics (likely exiting early). A valid batch size close to the intended increase is 1024. [not taken as invalid_value: the log shows no rejection]
- `d_model=128`: other, The program likely enforces an upper bound on d_model (e.g., ≤64) or requires it to be a power of two within a supported range; providing 128 exceeded this limit, causing the run to produce no metrics. A value of 64 retains the intent of increasing model width while staying within the accepted range. [not taken as invalid_value: the log shows no rejection]
- `d_model=512`: other, The value d_model=512 likely exceeds the supported model dimension (e.g., memory or shape constraints), causing the run to produce no output. A valid alternative that preserves the intent of increasing model width is d_model=256, which is compatible with the default n_heads=4 and stays within typical limits. [not taken as invalid_value: the log shows no rejection]
- `d_model=256`: other, The program likely expects d_model to be compatible with other dimensions (e.g., divisible by n_heads and patch_len). Setting d_model=256 produced no output, indicating the value was rejected. A nearby valid value that preserves the intent of a larger model size is 128. [not taken as invalid_value: the log shows no rejection]
- `d_model=384`: other, The program likely requires d_model to be a multiple of the number of attention heads (n_heads=4) and/or other internal dimensions; 384 caused the model to fail early, producing no output. [not taken as invalid_value: the log shows no rejection]
- `d_model=2`: other, The model requires d_model to be a multiple of n_heads (4) so that each attention head has an integer dimension. Setting d_model=2 violates this constraint, leading to no metrics being parsed. A valid value close to the intended small size is 4. [not taken as invalid_value: the log shows no rejection]
- `d_model=160`: other, The program likely requires d_model to be a power of two (or meet other divisibility constraints); using 160 resulted in no metrics output, indicating an invalid value. A nearby valid value preserving the intent is 128. [not taken as invalid_value: the log shows no rejection]
- `n_heads=12`: other, The value 12 for n_heads does not evenly divide d_model=16, causing the model to fail to produce metrics. [not taken as invalid_value: the log shows no rejection]
- `n_heads=40`: other, The model requires n_heads to evenly divide d_model (16). Setting n_heads=40 violates this constraint, leading to no metrics being parsed. [not taken as invalid_value: the log shows no rejection]
- `d_ff=2048`: crash, Setting d_ff to 2048 (16× the default) likely exceeded memory resources, causing the program to crash before producing any output, which resulted in no metrics being parsed
- `d_ff=1280`: other, The program likely validates d_ff as a power-of-two or within a supported range; 1280 fails validation, causing no output. A nearby valid power-of-two is 1024, which retains the intent of a larger feed‑forward dimension. [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `train_epochs=500`, `train_epochs=250`, `train_epochs=2500`, `train_epochs=5000`, `seq_len=1680`, `seq_len=3360`, `seq_len=16800`, `seq_len=33600`

## Knob names
- Screened though no assumption named them (low prior, code-derived values): `seq_len`, `e_layers`, `fc_dropout`, `kernel_size`

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `e_layers`: count (range() bound at PatchTST_supervised/layers/PatchTST_backbone.py:186)
- 14 sink value(s) shared by several knobs: no role assigned

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `n_epochs_pretrain`, `context_points`, `target_points`, `dataset`, `mask_ratio`, `n_epochs_finetune`, `n_layers`, `features`, `scaler`, `random_seed`, `use_gpu`, `loss`, `num_workers`, `gpu`, `itr`, `use_amp`

## Provenance
- GapFinder commit: `2af0c3af6b131fabc2f3684594cf852b93fe6830`
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `4be3cee4006dd11cd99ba26154f348ddbe79d10c0323c7ebdd6e4c4fc10a78b3`
- Cost: Nemotron billed $0.0099, sandbox reported $1920.6207 (total $1920.6306; this search; ledger extraction is included only if it shared the search's router)
