# Gap Report: planted L1-b3c-s3-1

Artifact `b3c` · generated 2026-10-22 02:23 · 141 branch runs (0 build/load setups) · sandbox $588.2457

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_h2_336 (etth2_336_mse) | Fits but unsupported | +1.9% | -0.2% | ±1.0% | `batch_size=512` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Found, but the test failed**: `data_provider/data_factory.py:19` `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size; with it switched off the program didn't finish (protocol test | no metrics parsed from output: ''). The code may assume it.
- **Held-out claims outside noise:**
  - C_h2_96 (`etth2_96_mse`): paper 0.268, measured 0.2778 (+3.7%, band ±1.0%)
  - C_h2_192 (`etth2_192_mse`): paper 0.32, measured 0.3152 (-1.5%, band ±1.0%)

## C_h2_336: etth2_336_mse (paper 0.305)
**Fits but unsupported** · gap +1.9% → -0.2% · 66 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0037`, `B0083`, `B0084`, `B0085` (4 run(s) of the same config)
- Config: `batch_size` naive `256`, changed to `512`
- Command:

  Replay: fork checkpoint `73fbaf23-9abd-4621-a4b7-f0c0d970300a` and run
  ```
  @ast:layers/AutoCorrelation.py:18:attention_dropout=0.1 @ast:layers/Autoformer_EncDec.py:76:moving_avg=25 @ast:layers/Autoformer_EncDec.py:76:dropout=0.1 RUN_TAG=e4356582fa91 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out logs; export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1; n=0; for d in ETTh1 ETTh2; do if [ $d = ETTh1 ]; then LR=0.02; else LR=0.03; fi; for p in 96 192 336 720; do python -u run_longExp.py --is_training 1 --root_path ./dataset/ --data_path $d.csv --model_id ${d}_720_$p --model SparseTSF --data $d --features M --seq_len 720 --pred_len $p --label_len 48 --period_len 24 --enc_in 7 --train_epochs 30 --patience 5 --itr 1 --batch_size 512 --learning_rate $LR --lradj type3 --pct_start 0.3 --loss mse --embed learned --num_workers 0 > out/${d}_$p.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; done; wait; bash gf_harness/emit.sh
  ```
- Output: `etth2_336_mse` 0.3045, 0.3045, 0.3045, 0.3045; gap after -0.2%; result checkpoint `ae41279b-75fc-4195-9010-04dff7f33dd5`
- Effect: candidate 0.3045 minus naive 0.3107 = -0.006148, 95% bootstrap interval [-0.006148, -0.006148] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `etth2_336_mse` = 0.305.

### What did we measure?
- Naive median 0.3107 over 5 runs; repeats: 0.3107, 0.3107, 0.3107, 0.3107, 0.3107
- Spread: range 0.3107 to 0.3107, noise band ±0.003107 (2 x MAD), CV 0.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +1.9% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `batch_size` the gap is +1.9% (it comes back)
- PASS · Held-out claim: C_h2_96: +3.7% to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_h2_192: -1.5% to +0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h2_720: +0.2% to +0.3% (not worse beyond noise)
- PASS · Held-out claim: C_h1_96: -0.3% to +0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h1_192: -0.3% to -0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h1_336: +0.5% to -0.1% (not worse beyond noise)
- PASS · Held-out claim: C_h1_720: -0.1% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `batch_size=512`: no evidence mentions '512'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -0.006148 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `train_epochs=150`, `train_epochs=300`, `train_epochs=120`, `train_epochs=240`, `train_epochs=480`, `train_epochs=1500`, `train_epochs=3000`, `itr=100`, `itr=50`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `patience=25` (1.06 noise units, gap +0.8%); `patience=50` (1.06 noise units, gap +0.8%); `patience=250` (1.06 noise units, gap +0.8%)
- Near alternatives (closest across all claims):
  - `batch_size=512`, `@ast:layers/AutoCorrelation.py:18:attention_dropout=0.01`: this claim -0.2%, mean |gap| 0.1% (3 runs)
  - `patience=25`: this claim +0.8%, mean |gap| 0.7% (4 runs)
  - `patience=50`: this claim +0.8%, mean |gap| 0.7% (4 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `patience=25` (reported)
- `batch_size=512`
- `patience=50`
- `patience=250`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting batch_size=512 | settings | 51% | 0.2 sigma (fits every claim) | run with batch_size=512 |
| 2 | a code change: @ast:layers/AutoCorrelation.py:18:attention_dropout=0.01, batch_size=512 | code | 15% | 0.2 sigma (fits every claim) | run with @ast:layers/AutoCorrelation.py:18:attention_dropout=0.01, batch_size=512 (an in-memory code patch) |
| 3 | a code change: @ast:layers/Autoformer_EncDec.py:76:moving_avg=3, batch_size=512 | code | 5% | 0.2 sigma (fits every claim) | run with @ast:layers/Autoformer_EncDec.py:76:moving_avg=3, batch_size=512 (an in-memory code patch) |

### History matching (every measured configuration, all claims together)
- 34 of 94 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size`: batch_size=512 (max I 0.32)
  - `@ast:layers/AutoCorrelation.py:18:attention_dropout, batch_size`: @ast:layers/AutoCorrelation.py:18:attention_dropout=0.01, batch_size=512 (max I 0.32); @ast:layers/AutoCorrelation.py:18:attention_dropout=0.91, batch_size=512 (max I 0.32); @ast:layers/AutoCorrelation.py:18:attention_dropout=0.0, batch_size=512 (max I 0.32)
  - `@ast:layers/Autoformer_EncDec.py:76:moving_avg, batch_size`: @ast:layers/Autoformer_EncDec.py:76:moving_avg=3, batch_size=512 (max I 0.32); @ast:layers/Autoformer_EncDec.py:76:moving_avg=250, batch_size=512 (max I 0.32); @ast:layers/Autoformer_EncDec.py:76:moving_avg=1, batch_size=512 (max I 0.32)
  - `@ast:layers/Autoformer_EncDec.py:76:dropout, batch_size`: @ast:layers/Autoformer_EncDec.py:76:dropout=0.01, batch_size=512 (max I 0.32); @ast:layers/Autoformer_EncDec.py:76:dropout=0.91, batch_size=512 (max I 0.32); @ast:layers/Autoformer_EncDec.py:76:dropout=0.0, batch_size=512 (max I 0.32)
- 5 separate islands (no single-knob move joins them): batch_size=512; @ast:layers/AutoCorrelation.py:18:attention_dropout=0.01, batch_size=512; @ast:layers/Autoformer_EncDec.py:76:moving_avg=3, batch_size=512 | patience=25; patience=50; patience=250 | etth2_learning_rate=0.006; etth2_learning_rate=0.06; etth2_learning_rate=0.015 | lradj=constant; lradj=3; lradj=4
- Leads outside the settings (static code checks, nothing run; check these first):
  - eval switch: `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size (`data_provider/data_factory.py:19`)
  - unexposed setting: `__init__(..., attention_dropout=0.1)`: a default no call in the repo overrides (59 call(s)) (`layers/AutoCorrelation.py:18`)
  - unexposed setting: `__init__(..., moving_avg=25)`: a default no call in the repo overrides (59 call(s)) (`layers/Autoformer_EncDec.py:76`)
  - unexposed setting: `__init__(..., dropout=0.1)`: a default no call in the repo overrides (59 call(s)) (`layers/Autoformer_EncDec.py:76`)
  - unexposed setting: `__init__(..., moving_avg=25)`: a default no call in the repo overrides (59 call(s)) (`layers/Autoformer_EncDec.py:135`)
  - unexposed setting: `__init__(..., dropout=0.1)`: a default no call in the repo overrides (59 call(s)) (`layers/Autoformer_EncDec.py:135`)
  - unexposed setting: `__init__(..., max_len=5000)`: a default no call in the repo overrides (59 call(s)) (`layers/Embed.py:9`)
  - unexposed setting: `__init__(..., dropout=0.1)`: a default no call in the repo overrides (59 call(s)) (`layers/Embed.py:106`)
- Equally good values: `patience` in {25, 50, 250}

Notes:
- configurations the target claim can't tell apart from the answer: patience=25; batch_size=512; patience=50; patience=250
- equally good values within one noise band (measured): patience in {25, 50, 250}
- explained with a code patch (tested in memory, no file edited): layers/AutoCorrelation.py line 18: attention_dropout = 0.1 -> 0.01
- mutation round: none of 12 mutants moved C_h2_336 toward the paper

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_h2_336 | C_h2_96 | C_h2_192 | C_h2_720 | C_h1_96 | C_h1_192 | C_h1_336 | C_h1_720 | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `batch_size=512` | 4 | -0.2% | +0.0% | +0.1% | +0.3% | +0.1% | -0.1% | -0.1% | +0.0% | 0.1% |
| `batch_size=512`, `@ast:layers/AutoCorrelation.py:18:attention_dropout=0.01` | 3 | -0.2% | +0.0% | +0.1% | +0.3% | +0.1% | -0.1% | -0.1% | +0.0% | 0.1% |
| `patience=25` | 4 | +0.8% | -1.1% | -1.5% | -0.7% | -0.5% | -0.5% | +0.5% | -0.1% | 0.7% |
| `patience=50` | 4 | +0.8% | -1.1% | -1.5% | -0.7% | -0.5% | -0.5% | +0.5% | -0.1% | 0.7% |
| `patience=250` | 4 | +0.8% | -1.1% | -1.5% | -0.7% | -0.5% | -0.5% | +0.5% | -0.1% | 0.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `seq_len=7200`: other, The script failed to parse metrics when seq_len was set to 7200, indicating the value is not accepted by the program (likely exceeds supported sequence length). [not taken as invalid_value: the log shows no rejection]
- `period_len=5`: other, The program produced no metrics when period_len was set to 5, indicating the value is not accepted (likely outside allowed range or causes degenerate behavior). [not taken as invalid_value: the log shows no rejection]
- `batch_size=2560`: other, The batch size of 2560 was not accepted by the training script, likely exceeding allowed memory or causing no output, resulting in no metrics parsed. [not taken as invalid_value: the log shows no rejection]
- `pct_start=1.5`: other, The pct_start parameter expects a fraction between 0 and 1 (inclusive). The value 1.5 is outside this range, causing the program to reject it and produce no metrics. [not taken as invalid_value: the log shows no rejection]
- `pct_start=3`: other, The pct_start parameter expects a float between 0 and 1 representing the fraction of total steps used for learning rate warmup; supplying the integer 3 is outside this valid range, causing the program to reject the value and produce no metrics. [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `train_epochs=150`, `train_epochs=300`, `train_epochs=120`, `train_epochs=240`, `train_epochs=480`, `train_epochs=1500`, `train_epochs=3000`, `itr=100`, `itr=50`

## Knob names
- Code defaults read from the code instead of the ledger: `seq_len` 96 at run_longExp.py:27 (ledger said 720), `train_epochs` 100 at run_longExp.py:72 (ledger said 30), `patience` 100 at run_longExp.py:74 (ledger said 5), `itr` 2 at run_longExp.py:71 (ledger said 1), `batch_size` 128 at run_longExp.py:73 (ledger said 256), `lradj` 'type3' at run_longExp.py:78 (ledger said type3), `loss` 'mse' at run_longExp.py:77 (ledger said mse), `embed` 'learned' at run_longExp.py:63 (ledger said learned)

## Runtime trace (one dry run)
9 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `train_epochs`: size (width.out_features (Linear) at models/SparseTSF.py:21)

## Provenance
- GapFinder commit: `ca4a5e297839f0c50559b58914404255594c81fb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `b48637ad08a836c02cace081286298518699a9ae429e34af3532973636e129ee`
- Cost: Nemotron billed $0.0024, sandbox reported $588.2457 (total $588.2481; this search; ledger extraction is included only if it shared the search's router)
