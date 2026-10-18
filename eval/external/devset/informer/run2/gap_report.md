# Gap Report: Informer (AAAI 2021), devbatch-1

Artifact `informer` · generated 2026-10-18 04:54 · 28 branch runs (0 build/load setups) · sandbox $265.6207

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_etth2_24_mse (etth2_24_mse) | Unexplained | -31.4% | -31.4% | ±9.6% | — |

## C_etth2_24_mse: etth2_24_mse (paper 0.72)
**Unexplained** · gap -31.4% → -31.4% · 15 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (15 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `etth2_24_mse` = 0.72.

### What did we measure?
- Naive median 0.4941 over 5 runs; repeats: 0.5043, 0.3089, 0.4563, 0.4941, 0.5286
- Spread: range 0.3089 to 0.5286, noise band ±0.069 (2 x MAD), CV 19.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.4% (noise band ±9.6% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: `d_model=1024`, `d_model=2048`, `d_model=4096`, `d_model=8192`, `d_model=5120`, `d_model=2560`, `d_model=25600`, `d_model=51200`, `seq_len=168`, `seq_len=336`, `seq_len=720`, `seq_len=1440`, `seq_len=2880`, `seq_len=480`, `seq_len=240`, `seq_len=2400`, `seq_len=4800`, `train_epochs=20`, `train_epochs=30`, `train_epochs=50`, `train_epochs=60`, `train_epochs=300`, `train_epochs=600`, `e_layers=20`, `e_layers=10`, `e_layers=100`, `e_layers=200`, `d_layers=10`, `d_layers=5`, `d_layers=50`, `d_layers=100`, `d_ff=4096`, `d_ff=20480`, `d_ff=10240`, `d_ff=102400`, `d_ff=204800`, `label_len=168`, `label_len=336`, `label_len=480`, `label_len=240`, `label_len=2400`, `label_len=4800`
- Not settable with this harness: `pred_len`, `use_amp`, `use_gpu`, `gpu`, `CUDA_VISIBLE_DEVICES`, `num_workers`, `itr`, `features`, `root_path`, `enc_in`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `d_model=64` (1.81 noise units, gap +14.1%); `batch_size=16` (1.72 noise units, gap -14.8%); `train_epochs=10` (1.42 noise units, gap -17.7%)
- Near alternatives (closest across all claims):
  - `d_model=64`: this claim +3.5%, mean |gap| 4.6% (3 runs)
  - `learning_rate=0.001`: this claim +15.8%, mean |gap| 13.7% (3 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `d_model`: d_model=64 (max I 0.49)
  - `batch_size`: batch_size=16 (max I 0.86)
  - `train_epochs`: train_epochs=10 (max I 1.03)
  - `learning_rate`: learning_rate=0.001 (max I 1.25)
  - `e_layers`: e_layers=1 (max I 1.28)
  - `dropout`: dropout=0.1 (max I 1.54)
  - `s_layers`: s_layers=2,1 (max I 1.85)
  - `d_ff`: d_ff=1024 (max I 1.96)
  - `attn`: attn=full (max I 2.03)
  - `lradj`: lradj=type2 (max I 2.08)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `__init__(..., attention_dropout=0.1)`: a default no call in the repo overrides (18 call(s)) (`models/attn.py:11`)
  - unexposed setting: `__init__(..., attention_dropout=0.1)`: a default no call in the repo overrides (18 call(s)) (`models/attn.py:39`)
  - unexposed setting: `__init__(..., max_len=5000)`: a default no call in the repo overrides (18 call(s)) (`models/embed.py:8`)
  - split fraction: `num_train` uses a fixed fraction 0.7; no flag sets it (`data/data_loader.py:233`)
  - split fraction: `num_test` uses a fixed fraction 0.2; no flag sets it (`data/data_loader.py:234`)
- Where the code differs from the paper (model-proposed, checked against the repo; literal ones were tried as patch knobs, structural ones are not tested):
  - `models/model.py:37`: paper says Informer contains a 3-layer stack and a 1-layer stack (1/4 input) in the encoder, and a 2-layer decoder.; code does Encoder layers set to 2 (e_layers=2)
  - `models/model.py:43`: paper says Informer contains a 3-layer stack and a 1-layer stack (1/4 input) in the encoder, and a 2-layer decoder.; code does Decoder layers set to 1 (d_layers=1)

Notes:
- stopped early: run budget of 28 reached (wanted 2 more run(s) of {'seq_len': '96'} for 'confirm (race)')
- closest configuration not verified: {'d_model': '64'} (gap +3.5%, 3 of 5 confirmation runs); the budget ran out first, so no attribution is made
- spec knobs no ledger assumption names (mix, inverse, distil, factor, label_len, n_heads) were screened too; no better answer
- history matching: the naive configuration is within noise of every claim
- patch round stopped early: run budget of 28 reached (wanted 1 more run(s) of {'d_model': '64', '@ast:models/attn.py:39:attention_dropout': '0.01'} for 'patch screen')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_etth2_24_mse | C_etth2_24_mae | Mean |gap| |
|---|---|---|---|---|
| `d_model=64` | 3 | +3.5% | +5.7% | 4.6% |
| `learning_rate=0.001` | 3 | +15.8% | +11.5% | 13.7% |
| naive (reproduction as run) | 5 | -31.4% | -18.0% | 24.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `batch_size=8`: other, The program did not produce any metrics when batch_size was set to 8, indicating the value was likely rejected as invalid (e.g., too small or not supported). [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `d_model=1024`, `d_model=2048`, `d_model=4096`, `d_model=8192`, `d_model=5120`, `d_model=2560`, `d_model=25600`, `d_model=51200`, `seq_len=168`, `seq_len=336`, `seq_len=720`, `seq_len=1440`, `seq_len=2880`, `seq_len=480`, `seq_len=240`, `seq_len=2400`, `seq_len=4800`, `train_epochs=20`, `train_epochs=30`, `train_epochs=50`, `train_epochs=60`, `train_epochs=300`, `train_epochs=600`, `e_layers=20`, `e_layers=10`, `e_layers=100`, `e_layers=200`, `d_layers=10`, `d_layers=5`, `d_layers=50`, `d_layers=100`, `d_ff=4096`, `d_ff=20480`, `d_ff=10240`, `d_ff=102400`, `d_ff=204800`, `label_len=168`, `label_len=336`, `label_len=480`, `label_len=240`, `label_len=2400`, `label_len=4800`

## Knob names
- Screened though no assumption named them (low prior, code-derived values): `mix`, `inverse`

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `d_model`: size (width.out_features (Linear) at models/embed.py:91)
- `dropout`: fraction (dropout.p (_DropoutNd) at models/embed.py:104)
- `e_layers`: count (range() bound at models/model.py:37)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `pred_len`, `use_amp`, `use_gpu`, `gpu`, `CUDA_VISIBLE_DEVICES`, `num_workers`, `itr`, `features`, `root_path`, `enc_in`

## Provenance
- GapFinder commit: `2af0c3af6b131fabc2f3684594cf852b93fe6830`
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `83f4c105fd9191e86c15f96142b017d6bdc6901f42fe4cd928f4dc9ab9fe70c6`
- Cost: Nemotron billed $0.0048, sandbox reported $265.6207 (total $265.6255; this search; ledger extraction is included only if it shared the search's router)
