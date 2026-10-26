# Gap Report: planted L1-b3c-s8-4

Artifact `b3c` · generated 2026-10-26 13:21 · 128 branch runs (0 build/load setups) · sandbox $639.3826

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_h2_336 (etth2_336_mse) | Paper-artifact inconsistency | -13.0% | +0.1% | ±0.9% | `etth2_learning_rate=0.0003` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **How the code computes the reported number** (test-score selection, label-based edits, switches fixed for evaluation):
  - `data_provider/data_factory.py:19`: `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: etth2_720_mse 0.42 > etth1_720_mse 0.418; measured: etth2_720_mse 0.3708 < etth1_720_mse 0.4177 (margin -0.0469, noise 0.00559)
- **Held-out claims outside noise:**
  - C_h2_96 (`etth2_96_mse`): paper 0.338, measured 0.2778 (-17.8%, band ±0.8%)
  - C_h2_192 (`etth2_192_mse`): paper 0.369, measured 0.3152 (-14.6%, band ±0.9%)
  - C_h2_720 (`etth2_720_mse`): paper 0.42, measured 0.3708 (-11.7%, band ±0.9%)

## C_h2_336: etth2_336_mse (paper 0.357)
**Paper-artifact inconsistency** · gap -13.0% → +0.1% · 68 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0120`, `B0121` (2 run(s) of the same config)
- Config: `etth2_learning_rate` naive `0.03`, changed to `0.0003`
- Command: not recorded
- Output: `etth2_336_mse` 0.3573, 0.3573; gap after +0.1%
- Effect: candidate 0.3573 minus naive 0.3107 = +0.04668, 95% bootstrap interval [+0.04668, +0.04668] (2 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `etth2_336_mse` = 0.357.

### What did we measure?
- Naive median 0.3107 over 5 runs; repeats: 0.3107, 0.3107, 0.3107, 0.3107, 0.3107
- Spread: range 0.3107 to 0.3107, noise band ±0.003107 (2 x MAD), CV 0.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -13.0% (noise band ±0.9% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- PASS · Held-out claim: C_h2_336@etth2_learning_rate=0.015 at etth2_learning_rate=0.00015: n/a to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_h2_336@etth2_learning_rate=0.06 at etth2_learning_rate=0.0006: n/a to +0.0% (not worse beyond noise)
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.04668 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `train_epochs=150`, `train_epochs=300`, `train_epochs=120`, `train_epochs=240`, `train_epochs=480`, `train_epochs=1500`, `train_epochs=3000`, `itr=100`, `itr=50`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `batch_size=60` (13.94 noise units, gap +0.8%); `batch_size=26` (13.84 noise units, gap +0.9%); `seq_len=144` (12.93 noise units, gap -1.7%); `batch_size=51` (12.65 noise units, gap +2.0%); `lradj=type2` (12.19 noise units, gap -2.4%) (and 10 more in the JSON)
- Near alternatives (closest across all claims):
  - `etth2_learning_rate=0.0006`: this claim -3.9%, mean |gap| 2.1% (2 runs)
  - `etth2_learning_rate=0.00015`: this claim +5.3%, mean |gap| 2.2% (2 runs)
  - `batch_size=60`: this claim +0.8%, mean |gap| 5.4% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 100% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | the setting etth2_learning_rate=0.0003 | settings | 0% | 9.7 sigma | run with etth2_learning_rate=0.0003 |
| 3 | the code's etth2_learning_rate is 0.01 x the paper's (a unit or convention differs between paper and code) | code | 0% | 10.3 sigma | find where etth2_learning_rate enters the computation and compare its unit with the paper's |

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C_h2_336@etth2_learning_rate=0.015, among 65 tested
- Fit C_h2_336 alone (7; worst claim's implausibility in brackets, lowest is the least inconsistent): batch_size=60 (13.57); batch_size=51 (15.17); seq_len=144 (15.34); batch_size=26 (15.96); lradj=type2 (29.28); etth2_learning_rate=0.06, train_epochs=1 (52.83)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `shuffle_flag = True` is a switch passed on to a call; no flag sets it (`data_provider/data_factory.py:29`)
  - unexposed setting: `drop_last = True` is a switch passed on to a call; no flag sets it (`data_provider/data_factory.py:30`)
  - unexposed setting: `Conv1d(..., bias=False)`: a switch fixed in the call; no flag sets it (`models/SparseTSF.py:18`)
  - unexposed setting: `Linear(..., bias=False)`: a switch fixed in the call; no flag sets it (`models/SparseTSF.py:21`)
  - unexposed setting: `add_argument(..., required=True)`: a switch fixed in the call; no flag sets it (`run_longExp.py:11`)
  - unexposed setting: `add_argument(..., required=True)`: a switch fixed in the call; no flag sets it (`run_longExp.py:12`)
  - unexposed setting: `add_argument(..., required=True)`: a switch fixed in the call; no flag sets it (`run_longExp.py:13`)
  - unexposed setting: `add_argument(..., required=True)`: a switch fixed in the call; no flag sets it (`run_longExp.py:16`)

Notes:
- {'train_epochs': '1'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'train_epochs': '1'} (gap +2.8%); it did not pass verification
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C_h2_336@etth2_learning_rate=0.015, among 65 tested
- scale probe: the code's etth2_learning_rate as 0.01 x the paper's fits every swept claim after 6 runs at g(v) (C_h2_336 at etth2_learning_rate=0.0003, C_h2_336@etth2_learning_rate=0.015 at etth2_learning_rate=0.00015, C_h2_336@etth2_learning_rate=0.06 at etth2_learning_rate=0.0006)
- labelled Paper-artifact inconsistency: one factor (0.01 x the paper's) makes every one of the 3 swept claims fit
- patch round: none of 6 code-patch configurations fits every claim
- mutation round stopped early: run budget of 150 reached (wanted 1 more run(s) of {'@ast:models/SparseTSF.py:15:@mut.25.BinOp.xdiv2': '1'} for 'mutation screen')
- value interval stopped early: run budget of 150 reached (wanted 1 more run(s) of {'etth2_learning_rate': '0.0002121'} for 'interval etth2_learning_rate=0.0002121')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_h2_336 | C_h2_96 | C_h2_192 | C_h2_720 | C_h1_96 | C_h1_192 | C_h1_336 | C_h1_720 | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `etth2_learning_rate=0.0003` | 2 | +0.1% | +0.0% | -0.1% | -0.8% | -0.0% | -0.0% | +0.0% | -0.1% | 0.1% |
| `etth2_learning_rate=0.0006` | 2 | -3.9% | -4.8% | -3.6% | -4.4% | -0.0% | -0.0% | +0.0% | -0.1% | 2.1% |
| `etth2_learning_rate=0.00015` | 2 | +5.3% | +3.5% | +4.4% | +4.1% | -0.0% | -0.0% | +0.0% | -0.1% | 2.2% |
| `batch_size=60` | 4 | +0.8% | -13.6% | -9.1% | -8.5% | +3.1% | +0.3% | +6.1% | +1.7% | 5.4% |
| `batch_size=26` | 4 | +0.9% | -16.0% | -4.4% | -9.2% | +3.1% | -1.5% | +4.8% | +4.4% | 5.5% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `seq_len=7200`: other, The seq_len value of 7200 exceeds the model's supported sequence length, causing the run to produce no metrics; a smaller but still increased length like 1440 retains the intent of using a longer sequence while staying within valid bounds. [not taken as invalid_value: the log shows no rejection]
- `period_len=5`: other, The value 5 for period_len is not accepted by the model (likely because period_len must be a divisor of seq_len or meet a minimum threshold), causing no metrics to be parsed. [not taken as invalid_value: the log shows no rejection]
- `batch_size=2560`: other, The batch size of 2560 exceeds the program's allowable limit (likely GPU memory), causing it to produce no output metrics. [not taken as invalid_value: the log shows no rejection]
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
- Harness spec sha256: `ca886ebf9772f94f3135b29b1ae6853724dd13577191b77614eb3836fb4bc881`
- Cost: Nemotron billed $0.0000, sandbox reported $639.3826 (total $639.3826; this search; ledger extraction is included only if it shared the search's router)
