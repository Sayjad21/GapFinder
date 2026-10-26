# Gap Report: planted L1-b3c-s8-2

Artifact `b3c` · generated 2026-10-26 14:19 · 150 branch runs (0 build/load setups) · sandbox $1008.1301

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
**Fits but unsupported** · gap +1.9% → -0.2% · 75 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0037`, `B0083`, `B0084`, `B0085` (4 run(s) of the same config)
- Config: `batch_size` naive `256`, changed to `512`
- Command:

  Replay: fork checkpoint `73fbaf23-9abd-4621-a4b7-f0c0d970300a` and run
  ```
  @ast:data_provider/data_factory.py:29:shuffle_flag=True @ast:data_provider/data_factory.py:30:drop_last=True @ast:models/SparseTSF.py:18:bias=False RUN_TAG=919e64494bb0 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out logs; export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1; n=0; for d in ETTh1 ETTh2; do if [ $d = ETTh1 ]; then LR=0.02; else LR=0.03; fi; for p in 96 192 336 720; do python -u run_longExp.py --is_training 1 --root_path ./dataset/ --data_path $d.csv --model_id ${d}_720_$p --model SparseTSF --data $d --features M --seq_len 720 --pred_len $p --label_len 48 --period_len 24 --enc_in 7 --train_epochs 30 --patience 5 --itr 1 --batch_size 512 --learning_rate $LR --lradj type3 --pct_start 0.3 --loss mse --embed learned --num_workers 0 > out/${d}_$p.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; done; wait; bash gf_harness/emit.sh
  ```
- Output: `etth2_336_mse` 0.3045, 0.3045, 0.3045, 0.3045; gap after -0.2%; result checkpoint `c004ca9d-8bc8-4780-a97c-a308e45f9982`
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
- PASS · Held-out claim: C_h2_336@batch_size=128 at batch_size=128: +5.5% to +5.5% (not worse beyond noise)
- PASS · Held-out claim: C_h2_336@batch_size=512 at batch_size=512: -2.4% to -2.4% (not worse beyond noise)
- FAIL · Evidence: `batch_size=512`: no evidence mentions '512'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -0.006148 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `train_epochs=150`, `train_epochs=300`, `train_epochs=120`, `train_epochs=240`, `train_epochs=480`, `train_epochs=1500`, `train_epochs=3000`, `itr=100`, `itr=50`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `patience=25` (1.06 noise units, gap +0.8%); `patience=50` (1.06 noise units, gap +0.8%); `patience=250` (1.06 noise units, gap +0.8%)
- Near alternatives (closest across all claims):
  - `batch_size=512`, `embed=timeF`: this claim -0.2%, mean |gap| 0.1% (4 runs)
  - `embed=fixed`, `batch_size=512`: this claim -0.2%, mean |gap| 0.1% (4 runs)
  - `itr=2`, `batch_size=512`: this claim -0.2%, mean |gap| 0.3% (4 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `patience=25` (reported)
- `batch_size=512`
- `patience=50`
- `patience=250`
- `batch_size=512, embed=fixed`
- `batch_size=512, embed=timeF`
- `batch_size=512, itr=2`
- `itr=2, patience=25`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting batch_size=512 | settings | 38% | 3.2 sigma | run with batch_size=512 |
| 2 | the setting itr=2, patience=25 | settings | 18% | 2.6 sigma (fits every claim) | run with itr=2, patience=25 |
| 3 | the setting batch_size=512, embed=fixed | settings | 13% | 3.2 sigma | run with batch_size=512, embed=fixed |

### History matching (every measured configuration, all claims together)
- 14 of 83 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `itr`: itr=10 (max I 2.02); itr=5 (max I 2.12); itr=2 (max I 2.37)
  - `etth2_learning_rate`: etth2_learning_rate=0.06 (max I 2.28); etth2_learning_rate=0.015 (max I 2.57); etth2_learning_rate=0.15 (max I 2.66)
  - `batch_size, itr`: batch_size=512, itr=2 (max I 2.37)
  - `batch_size, embed`: batch_size=512, embed=timeF (max I 2.37); batch_size=512, embed=fixed (max I 2.37)
  - `@ast:data_provider/data_factory.py:30:drop_last, batch_size, itr`: @ast:data_provider/data_factory.py:30:drop_last=False, batch_size=512, itr=2 (max I 2.56)
- 4 separate islands (no single-knob move joins them): itr=10; itr=5; itr=2 | lradj=constant; lradj=3; lradj=4 | etth2_learning_rate=0.06; etth2_learning_rate=0.015; etth2_learning_rate=0.15 | batch_size=512, embed=timeF; batch_size=512, embed=fixed
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `shuffle_flag = True` is a switch passed on to a call; no flag sets it (`data_provider/data_factory.py:29`)
  - unexposed setting: `drop_last = True` is a switch passed on to a call; no flag sets it (`data_provider/data_factory.py:30`)
  - unexposed setting: `Conv1d(..., bias=False)`: a switch fixed in the call; no flag sets it (`models/SparseTSF.py:18`)
  - unexposed setting: `Linear(..., bias=False)`: a switch fixed in the call; no flag sets it (`models/SparseTSF.py:21`)
  - unexposed setting: `add_argument(..., required=True)`: a switch fixed in the call; no flag sets it (`run_longExp.py:11`)
  - unexposed setting: `add_argument(..., required=True)`: a switch fixed in the call; no flag sets it (`run_longExp.py:12`)
  - unexposed setting: `add_argument(..., required=True)`: a switch fixed in the call; no flag sets it (`run_longExp.py:13`)
  - unexposed setting: `add_argument(..., required=True)`: a switch fixed in the call; no flag sets it (`run_longExp.py:16`)
- Equally good values: `patience` in {25, 50, 250}

Notes:
- configurations the target claim can't tell apart from the answer: patience=25; batch_size=512; patience=50; patience=250; batch_size=512, embed=fixed; batch_size=512, embed=timeF; batch_size=512, itr=2; itr=2, patience=25
- equally good values within one noise band (measured): patience in {25, 50, 250}
- {'patience': '25'} doesn't fit C_h2_336@batch_size=128 (claims at fixed settings); no other tested configuration fits every claim
- discrimination: the paper's other conditions (C_h2_336@batch_size=128, C_h2_336@batch_size=512) don't yet tell the equally good fits apart: batch_size=512 62%; patience=250 15%; patience=25 12%
- explained with a code patch (tested in memory, no file edited): data_provider/data_factory.py line 30: drop_last = True -> False
- batch_size: values from 512 to 512 fit every claim (a bisection, 3 runs a side, one run a value: approximate)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_h2_336 | C_h2_96 | C_h2_192 | C_h2_720 | C_h1_96 | C_h1_192 | C_h1_336 | C_h1_720 | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `batch_size=512` | 4 | -0.2% | +0.0% | +0.1% | +0.3% | +0.1% | -0.1% | -0.1% | +0.0% | 0.1% |
| `batch_size=512`, `embed=timeF` | 4 | -0.2% | +0.0% | +0.1% | +0.3% | +0.1% | -0.1% | -0.1% | +0.0% | 0.1% |
| `embed=fixed`, `batch_size=512` | 4 | -0.2% | +0.0% | +0.1% | +0.3% | +0.1% | -0.1% | -0.1% | +0.0% | 0.1% |
| `itr=2`, `batch_size=512` | 4 | -0.2% | +0.2% | -0.1% | +0.3% | -0.0% | +0.2% | -1.5% | +0.1% | 0.3% |
| `batch_size=512`, `patience=25` | 4 | -0.4% | -0.1% | +0.1% | +0.3% | -0.1% | -0.1% | -3.0% | +0.0% | 0.5% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `seq_len=7200`: other, The seq_len value of 7200 exceeds the model's supported sequence length, causing the run to produce no metrics; a smaller but still increased length like 1440 retains the intent of using a longer sequence while staying within valid bounds. [not taken as invalid_value: the log shows no rejection]
- `period_len=5`: other, The value 5 for period_len is not accepted by the model (likely because period_len must be a divisor of seq_len or meet a minimum threshold), causing no metrics to be parsed. [not taken as invalid_value: the log shows no rejection]
- `pct_start=1.5`: other, The pct_start parameter expects a fraction of total training steps for the learning rate warm‑up phase and must be in the range [0, 1]. Supplying 1.5 is outside this range, so the program rejected it as an invalid value. [not taken as invalid_value: the log shows no rejection]
- `pct_start=3`: other, The pct_start parameter expects a float between 0 and 1 representing the fraction of training steps used for the learning rate warm‑up. Supplying '3' is outside this range, so the program rejected the value. [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `train_epochs=150`, `train_epochs=300`, `train_epochs=120`, `train_epochs=240`, `train_epochs=480`, `train_epochs=1500`, `train_epochs=3000`, `itr=100`, `itr=50`

## Knob names
- Code defaults read from the code instead of the ledger: `seq_len` 96 at run_longExp.py:27 (ledger said 720), `train_epochs` 100 at run_longExp.py:72 (ledger said 30), `patience` 100 at run_longExp.py:74 (ledger said 5), `itr` 2 at run_longExp.py:71 (ledger said 1), `batch_size` 128 at run_longExp.py:73 (ledger said 256), `lradj` 'type3' at run_longExp.py:78 (ledger said type3), `loss` 'mse' at run_longExp.py:77 (ledger said mse), `embed` 'learned' at run_longExp.py:63 (ledger said learned)

## Runtime trace (one dry run)
9 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `train_epochs`: size (width.out_features (Linear) at models/SparseTSF.py:21)

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `081d3eaa79ac40569b9517197a2d35fee50c5098e977e06df5a46393518ecbe2`
- Cost: Nemotron billed $0.0025, sandbox reported $1008.1301 (total $1008.1327; this search; ledger extraction is included only if it shared the search's router)
