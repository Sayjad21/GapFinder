# Gap Report: planted L1-b3c-s7-3

Artifact `b3c` · generated 2026-10-24 08:58 · 150 branch runs (0 build/load setups) · sandbox $518.4713

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_h2_336 (etth2_336_mse) | Fits but unsupported | -11.0% | -0.1% | ±0.9% | `lradj=type2` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Found, but the test failed**: `data_provider/data_factory.py:19` `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size; with it switched off the program didn't finish (protocol test | no metrics parsed from output: ''). The code may assume it.
- **Held-out claims outside noise:**
  - C_h2_96 (`etth2_96_mse`): paper 0.335, measured 0.2778 (-17.1%, band ±0.8%)
  - C_h2_192 (`etth2_192_mse`): paper 0.361, measured 0.3152 (-12.7%, band ±0.9%)
  - C_h2_720 (`etth2_720_mse`): paper 0.41, measured 0.3708 (-9.6%, band ±0.9%)
  - C_h1_96 (`etth1_96_mse`): paper 0.458, measured 0.3539 (-22.7%, band ±0.8%)
  - C_h1_192 (`etth1_192_mse`): paper 0.48, measured 0.3978 (-17.1%, band ±0.8%)
  - C_h1_336 (`etth1_336_mse`): paper 0.493, measured 0.4051 (-17.8%, band ±0.8%)
  - C_h1_720 (`etth1_720_mse`): paper 0.527, measured 0.4177 (-20.7%, band ±0.8%)

## C_h2_336: etth2_336_mse (paper 0.349)
**Fits but unsupported** · gap -11.0% → -0.1% · 66 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0055`, `B0077`, `B0078`, `B0101` (4 run(s) of the same config)
- Config: `lradj` naive `type3`, changed to `type2`
- Command:

  Replay: fork checkpoint `73fbaf23-9abd-4621-a4b7-f0c0d970300a` and run
  ```
  @ast:layers/AutoCorrelation.py:18:attention_dropout=0.1 @ast:layers/Autoformer_EncDec.py:76:moving_avg=25 @ast:layers/Autoformer_EncDec.py:76:dropout=0.1 RUN_TAG=c6c6630bd965 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out logs; export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1; n=0; for d in ETTh1 ETTh2; do if [ $d = ETTh1 ]; then LR=0.02; else LR=0.03; fi; for p in 96 192 336 720; do python -u run_longExp.py --is_training 1 --root_path ./dataset/ --data_path $d.csv --model_id ${d}_720_$p --model SparseTSF --data $d --features M --seq_len 720 --pred_len $p --label_len 48 --period_len 24 --enc_in 7 --train_epochs 30 --patience 5 --itr 1 --batch_size 256 --learning_rate $LR --lradj type2 --pct_start 0.3 --loss mse --embed learned --num_workers 0 > out/${d}_$p.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; done; wait; bash gf_harness/emit.sh
  ```
- Output: `etth2_336_mse` 0.3485, 0.3485, 0.3485, 0.3485; gap after -0.1%; result checkpoint `89de8cd7-35bf-417d-aa48-f862c73d6e0d`
- Effect: candidate 0.3485 minus naive 0.3107 = +0.03788, 95% bootstrap interval [+0.03788, +0.03788] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `etth2_336_mse` = 0.349.

### What did we measure?
- Naive median 0.3107 over 5 runs; repeats: 0.3107, 0.3107, 0.3107, 0.3107, 0.3107
- Spread: range 0.3107 to 0.3107, noise band ±0.003107 (2 x MAD), CV 0.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -11.0% (noise band ±0.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lradj` the gap is -11.0% (it comes back)
- PASS · Held-out claim: C_h2_96: -17.1% to -0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h2_192: -12.7% to +0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h2_720: -9.6% to -0.6% (not worse beyond noise)
- PASS · Held-out claim: C_h1_96: -22.7% to -0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h1_192: -17.1% to -0.0% (not worse beyond noise)
- PASS · Held-out claim: C_h1_336: -17.8% to +0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h1_720: -20.7% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `lradj=type2`: no evidence mentions 'type2'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.03788 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `train_epochs=150`, `train_epochs=300`, `train_epochs=120`, `train_epochs=240`, `train_epochs=480`, `train_epochs=1500`, `train_epochs=3000`, `itr=100`, `itr=50`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `seq_len=144` (11.75 noise units, gap +0.5%); `batch_size=26` (8.69 noise units, gap +3.2%); `batch_size=51` (7.5 noise units, gap +4.3%); `train_epochs=1` (6.57 noise units, gap +5.1%); `batch_size=128` (5.48 noise units, gap -6.1%) (and 8 more in the JSON)
- Near alternatives (closest across all claims):
  - `lradj=type2`, `@ast:layers/AutoCorrelation.py:18:attention_dropout=0.01`: this claim -0.1%, mean |gap| 0.1% (3 runs)
  - `seq_len=144`: this claim +0.5%, mean |gap| 8.8% (4 runs)
  - `train_epochs=3`: this claim -7.4%, mean |gap| 9.7% (3 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lradj=type2` (reported)
- `seq_len=144`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting lradj=type2 | settings | 55% | 0.4 sigma (fits every claim) | run with lradj=type2 |
| 2 | a code change: @ast:layers/AutoCorrelation.py:18:attention_dropout=0.01, lradj=type2 | code | 16% | 0.4 sigma (fits every claim) | run with @ast:layers/AutoCorrelation.py:18:attention_dropout=0.01, lradj=type2 (an in-memory code patch) |
| 3 | a code change: @ast:layers/Autoformer_EncDec.py:76:moving_avg=3, lradj=type2 | code | 6% | 0.3 sigma (fits every claim) | run with @ast:layers/Autoformer_EncDec.py:76:moving_avg=3, lradj=type2 (an in-memory code patch) |

### History matching (every measured configuration, all claims together)
- 19 of 93 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lradj`: lradj=type2 (max I 0.56)
  - `@ast:layers/AutoCorrelation.py:18:attention_dropout, lradj`: @ast:layers/AutoCorrelation.py:18:attention_dropout=0.01, lradj=type2 (max I 0.56); @ast:layers/AutoCorrelation.py:18:attention_dropout=0.91, lradj=type2 (max I 0.56); @ast:layers/AutoCorrelation.py:18:attention_dropout=0.0, lradj=type2 (max I 0.56)
  - `@ast:layers/Autoformer_EncDec.py:76:moving_avg, lradj`: @ast:layers/Autoformer_EncDec.py:76:moving_avg=3, lradj=type2 (max I 0.56); @ast:layers/Autoformer_EncDec.py:76:moving_avg=250, lradj=type2 (max I 0.56); @ast:layers/Autoformer_EncDec.py:76:moving_avg=1, lradj=type2 (max I 0.56)
  - `@ast:layers/Autoformer_EncDec.py:76:dropout, lradj`: @ast:layers/Autoformer_EncDec.py:76:dropout=0.01, lradj=type2 (max I 0.56); @ast:layers/Autoformer_EncDec.py:76:dropout=0.91, lradj=type2 (max I 0.56); @ast:layers/Autoformer_EncDec.py:76:dropout=0.0, lradj=type2 (max I 0.56)
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
- configurations the target claim can't tell apart from the answer: lradj=type2; seq_len=144
- explained with a code patch (tested in memory, no file edited): layers/AutoCorrelation.py line 18: attention_dropout = 0.1 -> 0.01

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_h2_336 | C_h2_96 | C_h2_192 | C_h2_720 | C_h1_96 | C_h1_192 | C_h1_336 | C_h1_720 | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `lradj=type2` | 4 | -0.1% | -0.1% | +0.1% | -0.6% | -0.1% | -0.0% | +0.1% | +0.0% | 0.1% |
| `lradj=type2`, `@ast:layers/AutoCorrelation.py:18:attention_dropout=0.01` | 3 | -0.1% | -0.1% | +0.1% | -0.6% | -0.1% | -0.0% | +0.1% | +0.0% | 0.1% |
| `seq_len=144` | 4 | +0.5% | -14.6% | -1.9% | -2.8% | -12.4% | -7.8% | -12.2% | -17.9% | 8.8% |
| `train_epochs=3` | 3 | -7.4% | -14.8% | -8.7% | -6.9% | -14.9% | -4.8% | -7.8% | -11.9% | 9.7% |
| `train_epochs=1` | 4 | +5.1% | +1.9% | +4.0% | +3.9% | +15.3% | +20.1% | +25.6% | +20.5% | 12.1% |

## Failed hypotheses (triaged by Nemotron 3 Super)
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
- Cost: Nemotron billed $0.0000, sandbox reported $518.4713 (total $518.4713; this search; ledger extraction is included only if it shared the search's router)
