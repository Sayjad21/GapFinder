# Gap Report: planted L1-b3c-s3-2

Artifact `b3c` · generated 2026-10-22 02:23 · 117 branch runs (0 build/load setups) · sandbox $452.9984

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_h2_336 (etth2_336_mse) | Paper-artifact inconsistency | -4.7% | +0.1% | ±1.0% | `seq_len=1440` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Found, but the test failed**: `data_provider/data_factory.py:19` `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size; with it switched off the program didn't finish (protocol test | no metrics parsed from output: ''). The code may assume it.
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
**Paper-artifact inconsistency** · gap -4.7% → +0.1% · 44 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0019`, `B0058`, `B0059`, `B0062` (4 run(s) of the same config)
- Config: `seq_len` naive `720`, changed to `1440`
- Command:

  Replay: fork checkpoint `73fbaf23-9abd-4621-a4b7-f0c0d970300a` and run
  ```
  RUN_TAG=e8378c928309 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out logs; export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1; n=0; for d in ETTh1 ETTh2; do if [ $d = ETTh1 ]; then LR=0.02; else LR=0.03; fi; for p in 96 192 336 720; do python -u run_longExp.py --is_training 1 --root_path ./dataset/ --data_path $d.csv --model_id ${d}_1440_$p --model SparseTSF --data $d --features M --seq_len 1440 --pred_len $p --label_len 48 --period_len 24 --enc_in 7 --train_epochs 30 --patience 5 --itr 1 --batch_size 256 --learning_rate $LR --lradj type3 --pct_start 0.3 --loss mse --embed learned --num_workers 0 > out/${d}_$p.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; done; wait; bash gf_harness/emit.sh
  ```
- Output: `etth2_336_mse` 0.3264, 0.3264, 0.3264, 0.3264; gap after +0.1%; result checkpoint `280434b0-aeed-4918-a44d-ce88a2e1ec12`
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
- PASS · Held-out claim: C_h2_336@seq_len=360 at seq_len=720: n/a to -0.0% (not worse beyond noise)
- PASS · Held-out claim: C_h2_336@seq_len=1440 at seq_len=2880: n/a to +0.0% (not worse beyond noise)
- FAIL · Evidence: `seq_len=1440`: no evidence mentions '1440'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.01568 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `train_epochs=150`, `train_epochs=300`, `train_epochs=120`, `train_epochs=240`, `train_epochs=480`, `train_epochs=1500`, `train_epochs=3000`, `itr=100`, `itr=50`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `loss=mae` (4.69 noise units, gap +0.2%); `batch_size=128` (4.39 noise units, gap +0.5%); `train_epochs=3` (4 noise units, gap -0.9%); `lradj=type1` (3.65 noise units, gap -1.2%); `seq_len=360` (3.62 noise units, gap -1.3%)
- Near alternatives (closest across all claims):
  - `loss=mae`: this claim +0.2%, mean |gap| 2.7% (4 runs)
  - `lradj=type1`: this claim -1.2%, mean |gap| 3.5% (4 runs)
  - `batch_size=128`: this claim +0.5%, mean |gap| 3.7% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 92% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | the code's seq_len is 2 x the paper's (a unit or convention differs between paper and code) | code | 8% | 4.2 sigma | find where seq_len enters the computation and compare its unit with the paper's |
| 3 | the setting seq_len=1440 | settings | 0% | 13.6 sigma | run with seq_len=1440 |

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C_h2_336@seq_len=360, C_h2_336@seq_len=1440, among 41 tested
- Fit C_h2_336 alone (8; worst claim's implausibility in brackets, lowest is the least inconsistent): loss=mae (4.95); lradj=type1 (6.73); train_epochs=3 (13.64); seq_len=1440 (20.34); seq_len=360 (20.34); batch_size=128, seq_len=1440 (20.53)
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
- scale probe: the code's seq_len as 2 x the paper's fits every swept claim after 11 runs at g(v) (C_h2_336 at seq_len=1440, C_h2_336@seq_len=360 at seq_len=720, C_h2_336@seq_len=1440 at seq_len=2880)
- labelled Paper-artifact inconsistency: one factor (2 x the paper's) makes every one of the 3 swept claims fit
- patch round: none of 36 code-patch configurations fits every claim
- mutation round: none of 7 mutants ran

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_h2_336 | C_h2_96 | C_h2_192 | C_h2_720 | C_h1_96 | C_h1_192 | C_h1_336 | C_h1_720 | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `seq_len=1440` | 4 | +0.1% | -0.1% | -0.1% | -1.2% | +0.1% | -0.0% | -0.1% | -0.0% | 0.2% |
| `loss=mae` | 4 | +0.2% | +4.6% | +4.9% | -5.0% | +0.3% | +1.3% | -4.1% | -1.0% | 2.7% |
| naive (reproduction as run) | 5 | -4.7% | +5.6% | +0.7% | -7.3% | -1.7% | -1.0% | -6.2% | -0.1% | 3.4% |
| `lradj=type1` | 4 | -1.2% | +6.7% | +5.2% | -6.0% | +1.4% | +1.8% | -4.8% | +1.0% | 3.5% |
| `batch_size=128` | 4 | +0.5% | +8.0% | +9.2% | -8.0% | -0.4% | -0.3% | -3.2% | -0.2% | 3.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `period_len=5`: other, The program produced no metrics when period_len was set to 5, indicating the value is not accepted (likely outside allowed range or causes degenerate behavior). [not taken as invalid_value: the log shows no rejection]
- `batch_size=1280`: other, The batch size of 1280 likely exceeds allowable limits (e.g., GPU memory) and caused the program to produce no metrics; a nearby valid batch size such as 1024 preserves the intended larger batch size while being acceptable. [not taken as invalid_value: the log shows no rejection]

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
- Harness spec sha256: `4cee855740c8e27436c3d8d3f33501cd78c56eb97f3d35766fba27494598973d`
- Cost: Nemotron billed $0.0012, sandbox reported $452.9984 (total $452.9995; this search; ledger extraction is included only if it shared the search's router)
