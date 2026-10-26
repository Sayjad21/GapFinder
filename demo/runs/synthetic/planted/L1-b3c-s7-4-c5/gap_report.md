# Gap Report: planted L1-b3c-s7-4

Artifact `b3c` · generated 2026-10-24 09:54 · 146 branch runs (0 build/load setups) · sandbox $485.0106

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_h2_336 (etth2_336_mse) | Fits but unsupported | -4.7% | +0.1% | ±1.0% | `seq_len=1440` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **How the code computes the reported number** (test-score selection, label-based edits, switches fixed for evaluation):
  - `data_provider/data_factory.py:19`: `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: etth2_336_mse 0.326 > etth2_192_mse 0.313; measured: etth2_336_mse 0.3107 < etth2_192_mse 0.3152 (margin -0.00455, noise 0.00443)
  - paper: etth1_336_mse 0.432 > etth1_720_mse 0.418; measured: etth1_336_mse 0.4051 < etth1_720_mse 0.4177 (margin -0.0126, noise 0.00582)
- **Held-out claims outside noise:**
  - C_h2_96 (`etth2_96_mse`): paper 0.263, measured 0.2778 (+5.6%, band ±1.1%)
  - C_h2_720 (`etth2_720_mse`): paper 0.4, measured 0.3708 (-7.3%, band ±0.9%)
  - C_h1_96 (`etth1_96_mse`): paper 0.36, measured 0.3539 (-1.7%, band ±1.0%)
  - C_h1_192 (`etth1_192_mse`): paper 0.402, measured 0.3978 (-1.0%, band ±1.0%)
  - C_h1_336 (`etth1_336_mse`): paper 0.432, measured 0.4051 (-6.2%, band ±0.9%)

## C_h2_336: etth2_336_mse (paper 0.326)
**Fits but unsupported** · gap -4.7% → +0.1% · 68 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0104`, `B0105`, `B0120` (4 run(s) of the same config)
- Config: `seq_len` naive `720`, changed to `1440`
- Command:

  Replay: fork checkpoint `73fbaf23-9abd-4621-a4b7-f0c0d970300a` and run
  ```
  @ast:layers/AutoCorrelation.py:18:attention_dropout=0.1 @ast:layers/Autoformer_EncDec.py:76:moving_avg=25 @ast:layers/Autoformer_EncDec.py:76:dropout=0.1 @ast:models/SparseTSF.py:15:@mut.25.BinOp.xdiv2=0 @ast:models/SparseTSF.py:15:@mut.25.BinOp.xmul2=0 @ast:models/SparseTSF.py:15:@mut.41.Attribute.xdiv2=0 @ast:models/SparseTSF.py:15:@mut.41.Attribute.xmul2=0 @ast:layers/Embed.py:9:@mut.40.num.add1=0 @ast:layers/Embed.py:9:@mut.40.num.div2=0 RUN_TAG=c2109f87751e export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out logs; export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1; n=0; for d in ETTh1 ETTh2; do if [ $d = ETTh1 ]; then LR=0.02; else LR=0.03; fi; for p in 96 192 336 720; do python -u run_longExp.py --is_training 1 --root_path ./dataset/ --data_path $d.csv --model_id ${d}_1440_$p --model SparseTSF --data $d --features M --seq_len 1440 --pred_len $p --label_len 48 --period_len 24 --enc_in 7 --train_epochs 30 --patience 5 --itr 1 --batch_size 256 --learning_rate $LR --lradj type3 --pct_start 0.3 --loss mse --embed learned --num_workers 0 > out/${d}_$p.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; done; wait; bash gf_harness/emit.sh
  ```
- Output: `etth2_336_mse` 0.3264, 0.3264, 0.3264, 0.3264; gap after +0.1%; result checkpoint `dfaf395d-5119-40ac-9e9d-1f5e205a4a7a`
- Effect: candidate 0.3264 minus naive 0.3107 = +0.01568, 95% bootstrap interval [+0.01568, +0.01568] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `etth2_336_mse` = 0.326.

### What did we measure?
- Naive median 0.3107 over 5 runs; repeats: 0.3107, 0.3107, 0.3107, 0.3107, 0.3107
- Spread: range 0.3107 to 0.3107, noise band ±0.003107 (2 x MAD), CV 0.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -4.7% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `seq_len` the gap is -4.7% (it comes back)
- PASS · Held-out claim: C_h2_96: +5.6% to -0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h2_192: +0.7% to -0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h2_720: -7.3% to -1.2% (not worse beyond noise)
- PASS · Held-out claim: C_h1_96: -1.7% to +0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h1_192: -1.0% to -0.0% (not worse beyond noise)
- PASS · Held-out claim: C_h1_336: -6.2% to -0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h1_720: -0.1% to -0.0% (not worse beyond noise)
- PASS · Held-out claim: C_h2_336@seq_len=360 at seq_len=360: +3.6% to +3.6% (not worse beyond noise)
- PASS · Held-out claim: C_h2_336@seq_len=1440 at seq_len=1440: -20.3% to -20.3% (not worse beyond noise)
- FAIL · Evidence: `seq_len=1440`: no evidence mentions '1440'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.01568 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `train_epochs=150`, `train_epochs=300`, `train_epochs=120`, `train_epochs=240`, `train_epochs=480`, `train_epochs=1500`, `train_epochs=3000`, `itr=100`, `itr=50`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `batch_size=150` (4.78 noise units, gap +0.1%); `loss=mae` (4.69 noise units, gap +0.2%); `batch_size=128` (4.39 noise units, gap +0.5%); `train_epochs=3` (4 noise units, gap -0.9%); `lradj=type1` (3.65 noise units, gap -1.2%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `etth2_learning_rate=0.3`: this claim -3.3%, mean |gap| 2.6% (3 runs)
  - `loss=mae`: this claim +0.2%, mean |gap| 2.7% (4 runs)
  - `batch_size=150`: this claim +0.1%, mean |gap| 3.1% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 100% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | the code's seq_len is 2 x the paper's (a unit or convention differs between paper and code) | code | 0% | 11.8 sigma | find where seq_len enters the computation and compare its unit with the paper's |
| 3 | the setting seq_len=1440 | settings | 0% | 13.6 sigma | run with seq_len=1440 |

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C_h2_336@seq_len=360, C_h2_336@seq_len=1440, among 80 tested
- Fit C_h2_336 alone (9; worst claim's implausibility in brackets, lowest is the least inconsistent): loss=mae (4.95); lradj=type1 (6.73); batch_size=128 (9.19); train_epochs=3 (13.64); seq_len=1440 (20.34); seq_len=360 (20.34)
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
- {'seq_len': '1440'} doesn't fit C_h2_336@seq_len=1440, C_h2_336@seq_len=360 (claims at fixed settings); no other tested configuration fits every claim
- scale probe: the code's seq_len as 2 x the paper's does not fit every swept claim after 9 runs at g(v) (C_h2_336 at seq_len=1440, C_h2_336@seq_len=360 at seq_len=720, C_h2_336@seq_len=1440 at seq_len=2880)
- patch round: none of 19 code-patch configurations fits every claim
- mutation round stopped early: run budget of 150 reached (wanted 1 more run(s) of {'@ast:models/SparseTSF.py:15:@mut.25.BinOp.xdiv2': '1'} for 'mutation screen')
- value interval stopped early: run budget of 150 reached (wanted 1 more run(s) of {'seq_len': '720'} for 'interval seq_len=720')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_h2_336 | C_h2_96 | C_h2_192 | C_h2_720 | C_h1_96 | C_h1_192 | C_h1_336 | C_h1_720 | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `seq_len=1440` | 4 | +0.1% | -0.1% | -0.1% | -1.2% | +0.1% | -0.0% | -0.1% | -0.0% | 0.2% |
| `etth2_learning_rate=0.3` | 3 | -3.3% | +1.7% | +2.4% | -4.0% | -1.7% | -1.0% | -6.2% | -0.1% | 2.6% |
| `loss=mae` | 4 | +0.2% | +4.6% | +4.9% | -5.0% | +0.3% | +1.3% | -4.1% | -1.0% | 2.7% |
| `batch_size=150` | 4 | +0.1% | +10.7% | -1.2% | -6.6% | -0.2% | -1.9% | -3.7% | +0.4% | 3.1% |
| `etth2_learning_rate=0.003` | 3 | -3.2% | +4.0% | +3.4% | -6.7% | -1.7% | -1.0% | -6.2% | -0.1% | 3.3% |

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
- Harness spec sha256: `2c8e56cf50113d20ca11cab3433c692c3494c7c3b4c15289d305fcef4fb5a9f7`
- Cost: Nemotron billed $0.0000, sandbox reported $485.0106 (total $485.0106; this search; ledger extraction is included only if it shared the search's router)
