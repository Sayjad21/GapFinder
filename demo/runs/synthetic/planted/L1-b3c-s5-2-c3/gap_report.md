# Gap Report: planted L1-b3c-s5-2

Artifact `b3c` · generated 2026-10-23 02:32 · 149 branch runs (0 build/load setups) · sandbox $500.3755

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_h2_336 (etth2_336_mse) | Fits but unsupported | -3.5% | -0.0% | ±1.0% | `seq_len=360` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **How the code computes the reported number** (test-score selection, label-based edits, switches fixed for evaluation):
  - `data_provider/data_factory.py:19`: `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: etth1_96_mse 0.391 > etth1_336_mse 0.389; measured: etth1_96_mse 0.3539 < etth1_336_mse 0.4051 (margin -0.0512, noise 0.00538)
  - paper: etth1_192_mse 0.415 > etth1_336_mse 0.389; measured: etth1_192_mse 0.3978 < etth1_336_mse 0.4051 (margin -0.00731, noise 0.00568)
  - paper: etth1_192_mse 0.415 > etth1_720_mse 0.412; measured: etth1_192_mse 0.3978 < etth1_720_mse 0.4177 (margin -0.0199, noise 0.00577)
- **Held-out claims outside noise:**
  - C_h2_96 (`etth2_96_mse`): paper 0.272, measured 0.2778 (+2.1%, band ±1.0%)
  - C_h2_192 (`etth2_192_mse`): paper 0.324, measured 0.3152 (-2.7%, band ±1.0%)
  - C_h2_720 (`etth2_720_mse`): paper 0.38, measured 0.3708 (-2.4%, band ±1.0%)
  - C_h1_96 (`etth1_96_mse`): paper 0.391, measured 0.3539 (-9.5%, band ±0.9%)
  - C_h1_192 (`etth1_192_mse`): paper 0.415, measured 0.3978 (-4.1%, band ±1.0%)
  - C_h1_336 (`etth1_336_mse`): paper 0.389, measured 0.4051 (+4.1%, band ±1.0%)
  - C_h1_720 (`etth1_720_mse`): paper 0.412, measured 0.4177 (+1.4%, band ±1.0%)

## C_h2_336: etth2_336_mse (paper 0.322)
**Fits but unsupported** · gap -3.5% → -0.0% · 71 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0078`, `B0079`, `B0095` (4 run(s) of the same config)
- Config: `seq_len` naive `720`, changed to `360`
- Command:

  Replay: fork checkpoint `73fbaf23-9abd-4621-a4b7-f0c0d970300a` and run
  ```
  @ast:layers/AutoCorrelation.py:18:attention_dropout=0.1 @ast:layers/Autoformer_EncDec.py:76:moving_avg=25 @ast:layers/Autoformer_EncDec.py:76:dropout=0.1 @ast:models/SparseTSF.py:15:@mut.25.BinOp.xdiv2=0 @ast:models/SparseTSF.py:15:@mut.25.BinOp.xmul2=0 @ast:models/SparseTSF.py:15:@mut.41.Attribute.xdiv2=0 @ast:models/SparseTSF.py:15:@mut.41.Attribute.xmul2=0 @ast:layers/Embed.py:9:@mut.40.num.add1=0 @ast:layers/Embed.py:9:@mut.40.num.div2=0 RUN_TAG=0e7fea66b86d export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out logs; export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1; n=0; for d in ETTh1 ETTh2; do if [ $d = ETTh1 ]; then LR=0.02; else LR=0.03; fi; for p in 96 192 336 720; do python -u run_longExp.py --is_training 1 --root_path ./dataset/ --data_path $d.csv --model_id ${d}_360_$p --model SparseTSF --data $d --features M --seq_len 360 --pred_len $p --label_len 48 --period_len 24 --enc_in 7 --train_epochs 30 --patience 5 --itr 1 --batch_size 256 --learning_rate $LR --lradj type3 --pct_start 0.3 --loss mse --embed learned --num_workers 0 > out/${d}_$p.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; done; wait; bash gf_harness/emit.sh
  ```
- Output: `etth2_336_mse` 0.3219, 0.3219, 0.3219, 0.3219; gap after -0.0%; result checkpoint `e045315b-a305-4182-838e-dc899536acf9`
- Effect: candidate 0.3219 minus naive 0.3107 = +0.01124, 95% bootstrap interval [+0.01124, +0.01124] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `etth2_336_mse` = 0.322.

### What did we measure?
- Naive median 0.3107 over 5 runs; repeats: 0.3107, 0.3107, 0.3107, 0.3107, 0.3107
- Spread: range 0.3107 to 0.3107, noise band ±0.003107 (2 x MAD), CV 0.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -3.5% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `seq_len` the gap is -3.5% (it comes back)
- PASS · Held-out claim: C_h2_96: +2.1% to +0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h2_192: -2.7% to -0.0% (not worse beyond noise)
- PASS · Held-out claim: C_h2_720: -2.4% to -0.8% (not worse beyond noise)
- PASS · Held-out claim: C_h1_96: -9.5% to +0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h1_192: -4.1% to -0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h1_336: +4.1% to -0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h1_720: +1.4% to +0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h2_336@seq_len=1440 at seq_len=1440: +5.0% to +5.0% (not worse beyond noise)
- FAIL · Evidence: `seq_len=360`: no evidence mentions '360'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.01124 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `train_epochs=150`, `train_epochs=300`, `train_epochs=120`, `train_epochs=240`, `train_epochs=480`, `train_epochs=1500`, `train_epochs=3000`, `itr=100`, `itr=50`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lradj=type1` (3.65 noise units, gap +0.0%); `train_epochs=3` (3.29 noise units, gap +0.3%); `seq_len=1440` (2.25 noise units, gap +1.4%); `loss=mae` (2.11 noise units, gap +1.5%); `batch_size=128` (1.82 noise units, gap +1.8%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `@ast:layers/AutoCorrelation.py:18:attention_dropout=0.01`, `seq_len=360`: this claim -0.0%, mean |gap| 0.2% (3 runs)
  - `lradj=type1`, `seq_len=360`: this claim -1.7%, mean |gap| 1.4% (3 runs)
  - `loss=mae`: this claim +1.5%, mean |gap| 2.6% (4 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `seq_len=360` (reported)
- `etth2_learning_rate=0.003`
- `etth2_learning_rate=0.3`
- `lradj=type1, seq_len=360`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a code change: @ast:layers/AutoCorrelation.py:18:attention_dropout=0.01, seq_len=360 | code | 32% | 2.9 sigma (fits every claim) | run with @ast:layers/AutoCorrelation.py:18:attention_dropout=0.01, seq_len=360 (an in-memory code patch) |
| 2 | the setting seq_len=360 | settings | 31% | 3.4 sigma | run with seq_len=360 |
| 3 | a code change: @ast:layers/Autoformer_EncDec.py:76:moving_avg=3, seq_len=360 | code | 12% | 2.9 sigma (fits every claim) | run with @ast:layers/Autoformer_EncDec.py:76:moving_avg=3, seq_len=360 (an in-memory code patch) |

### History matching (every measured configuration, all claims together)
- 18 of 99 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `@ast:layers/AutoCorrelation.py:18:attention_dropout, seq_len`: @ast:layers/AutoCorrelation.py:18:attention_dropout=0.01, seq_len=360 (max I 0.83); @ast:layers/AutoCorrelation.py:18:attention_dropout=0.91, seq_len=360 (max I 0.83); @ast:layers/AutoCorrelation.py:18:attention_dropout=0.0, seq_len=360 (max I 0.83); @ast:layers/AutoCorrelation.py:18:attention_dropout=0.05, seq_len=360 (max I 0.83)
  - `@ast:layers/Autoformer_EncDec.py:76:moving_avg, seq_len`: @ast:layers/Autoformer_EncDec.py:76:moving_avg=3, seq_len=360 (max I 0.83); @ast:layers/Autoformer_EncDec.py:76:moving_avg=250, seq_len=360 (max I 0.83); @ast:layers/Autoformer_EncDec.py:76:moving_avg=1, seq_len=360 (max I 0.83)
  - `@ast:layers/Autoformer_EncDec.py:76:dropout, seq_len`: @ast:layers/Autoformer_EncDec.py:76:dropout=0.01, seq_len=360 (max I 0.83); @ast:layers/Autoformer_EncDec.py:76:dropout=0.91, seq_len=360 (max I 0.83); @ast:layers/Autoformer_EncDec.py:76:dropout=0.0, seq_len=360 (max I 0.83)
- 3 separate islands (no single-knob move joins them): @ast:layers/AutoCorrelation.py:18:attention_dropout=0.01, seq_len=360; @ast:layers/AutoCorrelation.py:18:attention_dropout=0.91, seq_len=360; @ast:layers/AutoCorrelation.py:18:attention_dropout=0.0, seq_len=360 | @ast:layers/Autoformer_EncDec.py:76:moving_avg=3, seq_len=360; @ast:layers/Autoformer_EncDec.py:76:moving_avg=250, seq_len=360; @ast:layers/Autoformer_EncDec.py:76:moving_avg=1, seq_len=360 | @ast:layers/Autoformer_EncDec.py:76:dropout=0.01, seq_len=360; @ast:layers/Autoformer_EncDec.py:76:dropout=0.91, seq_len=360; @ast:layers/Autoformer_EncDec.py:76:dropout=0.0, seq_len=360
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
- configurations the target claim can't tell apart from the answer: seq_len=360; etth2_learning_rate=0.003; etth2_learning_rate=0.3; lradj=type1, seq_len=360
- early code screen stopped: run budget of 150 reached (wanted 1 more run(s) of {'@ast:models/SparseTSF.py:15:@mut.25.BinOp.xdiv2': '1'} for 'mutation screen (early)')
- {'seq_len': '360'} doesn't fit C_h2_336@seq_len=1440 (claims at fixed settings); no other tested configuration fits every claim
- discrimination: the paper's other conditions favour seq_len=360 (posterior 100% after 0 run(s) chosen by expected information)
- explained with a code patch (tested in memory, no file edited): layers/AutoCorrelation.py line 18: attention_dropout = 0.1 -> 0.01
- value interval stopped early: run budget of 150 reached (wanted 1 more run(s) of {'seq_len': '228'} for 'interval seq_len=228')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_h2_336 | C_h2_96 | C_h2_192 | C_h2_720 | C_h1_96 | C_h1_192 | C_h1_336 | C_h1_720 | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `seq_len=360` | 4 | -0.0% | +0.1% | -0.0% | -0.8% | +0.1% | -0.1% | -0.1% | +0.1% | 0.2% |
| `@ast:layers/AutoCorrelation.py:18:attention_dropout=0.01`, `seq_len=360` | 3 | -0.0% | +0.1% | -0.0% | -0.8% | +0.1% | -0.1% | -0.1% | +0.1% | 0.2% |
| `lradj=type1`, `seq_len=360` | 3 | -1.7% | +2.7% | +0.0% | -0.9% | +2.8% | +1.7% | +0.2% | +1.5% | 1.4% |
| `loss=mae` | 4 | +1.5% | +1.1% | +1.4% | +0.0% | -7.7% | -1.9% | +6.5% | +0.4% | 2.6% |
| `lradj=type1` | 4 | +0.0% | +3.2% | +1.6% | -1.1% | -6.7% | -1.4% | +5.8% | +2.5% | 2.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `seq_len=7200`: other, The program failed to parse metrics when seq_len=7200, indicating the value is outside the accepted range; a shorter sequence length is needed. [not taken as invalid_value: the log shows no rejection]
- `period_len=5`: other, The value 5 for period_len likely does not divide the sequence length (720) or produce valid seasonal decomposition, causing the model to produce no output metrics. A nearby valid divisor is 6. [not taken as invalid_value: the log shows no rejection]
- `batch_size=2560`: other, The value 2560 likely exceeds the maximum supported batch size (or causes memory issues), leading to no metrics being parsed. A valid batch size such as 1024 keeps the intent of using a larger batch while staying within limits. [not taken as invalid_value: the log shows no rejection]
- `pct_start=1.5`: other, The program expects pct_start to be a fraction between 0 and 1 (inclusive). The value 1.5 is outside this range, causing the program to reject it and produce no metrics output. [not taken as invalid_value: the log shows no rejection]
- `pct_start=3`: other, The pct_start parameter expects a float between 0 and 1 representing the fraction of training steps used for learning rate warm‑up. Supplying the integer '3' is outside this valid range, causing the program to reject the value. [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `train_epochs=150`, `train_epochs=300`, `train_epochs=120`, `train_epochs=240`, `train_epochs=480`, `train_epochs=1500`, `train_epochs=3000`, `itr=100`, `itr=50`

## Knob names
- Code defaults read from the code instead of the ledger: `seq_len` 96 at run_longExp.py:27 (ledger said 720), `train_epochs` 100 at run_longExp.py:72 (ledger said 30), `patience` 100 at run_longExp.py:74 (ledger said 5), `itr` 2 at run_longExp.py:71 (ledger said 1), `batch_size` 128 at run_longExp.py:73 (ledger said 256), `lradj` 'type3' at run_longExp.py:78 (ledger said type3), `loss` 'mse' at run_longExp.py:77 (ledger said mse), `embed` 'learned' at run_longExp.py:63 (ledger said learned)

## Runtime trace (one dry run)
9 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `train_epochs`: size (width.out_features (Linear) at models/SparseTSF.py:21)

## Provenance
- GapFinder commit: `96f43d9d872690442737d0ad342eeb7d86352416` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `2c8e56cf50113d20ca11cab3433c692c3494c7c3b4c15289d305fcef4fb5a9f7`
- Cost: Nemotron billed $0.0007, sandbox reported $500.3755 (total $500.3761; this search; ledger extraction is included only if it shared the search's router)
