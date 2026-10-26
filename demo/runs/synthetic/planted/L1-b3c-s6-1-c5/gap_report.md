# Gap Report: planted L1-b3c-s6-1

Artifact `b3c` · generated 2026-10-23 18:49 · 150 branch runs (0 build/load setups) · sandbox $567.5723

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_h2_336 (etth2_336_mse) | Fits but unsupported | -5.0% | -0.1% | ±1.0% | `loss=mae` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **How the code computes the reported number** (test-score selection, label-based edits, switches fixed for evaluation):
  - `data_provider/data_factory.py:19`: `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size
- **Held-out claims outside noise:**
  - C_h2_96 (`etth2_96_mse`): paper 0.275, measured 0.2778 (+1.0%, band ±1.0%)
  - C_h2_192 (`etth2_192_mse`): paper 0.328, measured 0.3152 (-3.9%, band ±1.0%)
  - C_h2_720 (`etth2_720_mse`): paper 0.38, measured 0.3708 (-2.4%, band ±1.0%)
  - C_h1_96 (`etth1_96_mse`): paper 0.361, measured 0.3539 (-2.0%, band ±1.0%)
  - C_h1_192 (`etth1_192_mse`): paper 0.407, measured 0.3978 (-2.3%, band ±1.0%)
  - C_h1_336 (`etth1_336_mse`): paper 0.414, measured 0.4051 (-2.1%, band ±1.0%)

## C_h2_336: etth2_336_mse (paper 0.327)
**Fits but unsupported** · gap -5.0% → -0.1% · 74 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0066`, `B0091`, `B0092`, `B0093` (4 run(s) of the same config)
- Config: `loss` naive `mse`, changed to `mae`
- Command:

  Replay: fork checkpoint `73fbaf23-9abd-4621-a4b7-f0c0d970300a` and run
  ```
  RUN_TAG=ba7faeba069d export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out logs; export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1; n=0; for d in ETTh1 ETTh2; do if [ $d = ETTh1 ]; then LR=0.02; else LR=0.03; fi; for p in 96 192 336 720; do python -u run_longExp.py --is_training 1 --root_path ./dataset/ --data_path $d.csv --model_id ${d}_720_$p --model SparseTSF --data $d --features M --seq_len 720 --pred_len $p --label_len 48 --period_len 24 --enc_in 7 --train_epochs 30 --patience 5 --itr 1 --batch_size 256 --learning_rate $LR --lradj type3 --pct_start 0.3 --loss mae --embed learned --num_workers 0 > out/${d}_$p.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; done; wait; bash gf_harness/emit.sh
  ```
- Output: `etth2_336_mse` 0.3268, 0.3268, 0.3268, 0.3268; gap after -0.1%; result checkpoint `34f732ce-1eba-417c-8545-1cb448802c74`
- Effect: candidate 0.3268 minus naive 0.3107 = +0.0161, 95% bootstrap interval [+0.0161, +0.0161] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `etth2_336_mse` = 0.327.

### What did we measure?
- Naive median 0.3107 over 5 runs; repeats: 0.3107, 0.3107, 0.3107, 0.3107, 0.3107
- Spread: range 0.3107 to 0.3107, noise band ±0.003107 (2 x MAD), CV 0.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -5.0% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `loss` the gap is -5.0% (it comes back)
- PASS · Held-out claim: C_h2_96: +1.0% to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_h2_192: -3.9% to +0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h2_720: -2.4% to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_h1_96: -2.0% to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_h1_192: -2.3% to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_h1_336: -2.1% to +0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h1_720: +0.9% to -0.0% (not worse beyond noise)
- FAIL · Evidence: `loss=mae`: no evidence mentions 'mae'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.0161 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `train_epochs=150`, `train_epochs=300`, `train_epochs=120`, `train_epochs=240`, `train_epochs=480`, `train_epochs=1500`, `train_epochs=3000`, `itr=100`, `itr=50`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `seq_len=1440` (5.05 noise units, gap -0.2%); `batch_size=128` (5.04 noise units, gap +0.2%); `train_epochs=3` (4 noise units, gap -1.2%); `lradj=type1` (3.65 noise units, gap -1.5%); `seq_len=360` (3.62 noise units, gap -1.6%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `loss=mae`, `seq_len=1440`: this claim +1.8%, mean |gap| 1.0% (3 runs)
  - `lradj=type1`: this claim -1.5%, mean |gap| 1.2% (4 runs)
  - `batch_size=128`, `seq_len=1440`: this claim -0.4%, mean |gap| 1.3% (4 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `loss=mae` (reported)
- `batch_size=128, seq_len=1440`
- `loss=mae, seq_len=1440`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting loss=mae | settings | 96% | 0.1 sigma (fits every claim) | run with loss=mae |
| 2 | the setting loss=mae, seq_len=1440 | settings | 2% | 1.5 sigma (fits every claim) | run with loss=mae, seq_len=1440 |
| 3 | the setting lradj=type1 | settings | 2% | 1.4 sigma (fits every claim) | run with lradj=type1 |

### History matching (every measured configuration, all claims together)
- 3 of 84 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `loss`: loss=mae (max I 0.14)
  - `lradj`: lradj=type1 (max I 2.07)
  - `loss, seq_len`: loss=mae, seq_len=1440 (max I 2.35)
- 2 separate islands (no single-knob move joins them): loss=mae; loss=mae, seq_len=1440 | lradj=type1
- Leads outside the settings (static code checks, nothing run; check these first):
  - eval switch: `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size (`data_provider/data_factory.py:19`)
  - unexposed setting: `__init__(..., attention_dropout=0.1)`: a default no call in the repo overrides (59 call(s)) (`layers/AutoCorrelation.py:18`)
  - unexposed setting: `__init__(..., moving_avg=25)`: a default no call in the repo overrides (59 call(s)) (`layers/Autoformer_EncDec.py:76`)
  - unexposed setting: `__init__(..., dropout=0.1)`: a default no call in the repo overrides (59 call(s)) (`layers/Autoformer_EncDec.py:76`)
  - unexposed setting: `__init__(..., moving_avg=25)`: a default no call in the repo overrides (59 call(s)) (`layers/Autoformer_EncDec.py:135`)
  - unexposed setting: `__init__(..., dropout=0.1)`: a default no call in the repo overrides (59 call(s)) (`layers/Autoformer_EncDec.py:135`)
  - unexposed setting: `__init__(..., max_len=5000)`: a default no call in the repo overrides (59 call(s)) (`layers/Embed.py:9`)
  - unexposed setting: `__init__(..., dropout=0.1)`: a default no call in the repo overrides (59 call(s)) (`layers/Embed.py:106`)

Notes:
- configurations the target claim can't tell apart from the answer: loss=mae; batch_size=128, seq_len=1440; loss=mae, seq_len=1440
- patch round stopped early: run budget of 150 reached (wanted 1 more run(s) of {'loss': 'mae', '@ast:layers/Autoformer_EncDec.py:76:moving_avg': '5'} for 'patch screen')
- value interval stopped early: run budget of 150 reached (wanted 1 more run(s) of {'loss': 'mse'} for 'interval loss=mse')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_h2_336 | C_h2_96 | C_h2_192 | C_h2_720 | C_h1_96 | C_h1_192 | C_h1_336 | C_h1_720 | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `loss=mae` | 4 | -0.1% | +0.0% | +0.1% | +0.0% | +0.0% | +0.0% | +0.1% | -0.0% | 0.1% |
| `loss=mae`, `seq_len=1440` | 3 | +1.8% | -0.4% | -0.1% | +2.4% | +0.2% | +0.7% | -1.1% | -1.0% | 1.0% |
| `lradj=type1` | 4 | -1.5% | +2.1% | +0.4% | -1.1% | +1.1% | +0.6% | -0.6% | +2.0% | 1.2% |
| `batch_size=128`, `seq_len=1440` | 4 | -0.4% | +0.2% | +2.1% | +1.4% | +1.8% | +0.5% | +3.0% | +1.0% | 1.3% |
| `etth2_learning_rate=0.003` | 3 | -3.5% | -0.5% | -1.3% | -1.8% | -2.0% | -2.3% | -2.1% | +0.9% | 1.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `seq_len=7200`: other, The program did not produce any metrics when seq_len=7200, indicating the value is likely outside the accepted range (too large for the model's sequence length capacity). A shorter but still longer-than-default value such as 1440 preserves the intent of using a longer sequence while being within supported limits. [not taken as invalid_value: the log shows no rejection]
- `period_len=5`: other, The program failed to parse metrics when period_len=5, indicating the value is not accepted (likely because period_len must be a divisor of seq_len or within a valid range). [not taken as invalid_value: the log shows no rejection]
- `batch_size=2560`: other, The batch_size value of 2560 caused the program to produce no metrics, indicating it was rejected (likely due to exceeding allowed limits or causing resource exhaustion). A smaller batch size is needed to keep the same intent of using a larger batch while staying within valid bounds. [not taken as invalid_value: the log shows no rejection]
- `pct_start=1.5`: other, The program likely interprets pct_start as a warm‑up fraction that must lie in the interval (0, 1]; supplying 1.5 is outside this range, causing the run to produce no parsable metrics.', "suggestion": 1.0}]} [not taken as invalid_value: the log shows no rejection]
- `pct_start=3`: other, The program expects pct_start to be a fraction between 0 and 1 (e.g., 0.3 for 30%). Supplying '3' is outside this range, causing the value to be rejected. [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `train_epochs=150`, `train_epochs=300`, `train_epochs=120`, `train_epochs=240`, `train_epochs=480`, `train_epochs=1500`, `train_epochs=3000`, `itr=100`, `itr=50`

## Knob names
- Code defaults read from the code instead of the ledger: `seq_len` 96 at run_longExp.py:27 (ledger said 720), `train_epochs` 100 at run_longExp.py:72 (ledger said 30), `patience` 100 at run_longExp.py:74 (ledger said 5), `itr` 2 at run_longExp.py:71 (ledger said 1), `batch_size` 128 at run_longExp.py:73 (ledger said 256), `lradj` 'type3' at run_longExp.py:78 (ledger said type3), `loss` 'mse' at run_longExp.py:77 (ledger said mse), `embed` 'learned' at run_longExp.py:63 (ledger said learned)

## Runtime trace (one dry run)
9 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `train_epochs`: size (width.out_features (Linear) at models/SparseTSF.py:21)

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `9b5258df049e4705704c935491b76349936d4572735a8b6faa34becf3c7c813c`
- Cost: Nemotron billed $0.0029, sandbox reported $567.5723 (total $567.5752; this search; ledger extraction is included only if it shared the search's router)
