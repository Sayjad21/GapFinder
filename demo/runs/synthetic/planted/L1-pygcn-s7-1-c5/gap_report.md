# Gap Report: planted L1-pygcn-s7-1

Artifact `pygcn` · generated 2026-10-24 06:33 · 150 branch runs (0 build/load setups) · sandbox $43.3541

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_cora (cora_acc) | Fits but unsupported | +3.6% | +0.3% | ±3.0% | `weight_decay=0.001` |

## C_cora: cora_acc (paper 79.67)
**Fits but unsupported** · gap +3.6% → +0.3% · 85 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0019`, `B0053`, `B0054`, `B0055` (4 run(s) of the same config)
- Config: `weight_decay` naive `5e-4`, changed to `0.001`
- Command:

  Replay: fork checkpoint `69abd25a-45ee-4e12-8b94-2cfde545816c` and run
  ```
  RUN_TAG=e42bc13fcc9e export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; mkdir -p out; S=$(( $(printf %s "$RUN_TAG" | cksum | cut -d" " -f1) % 100000 )); cd pygcn && PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --no-cuda --seed $S --epochs 200 --lr 0.01 --weight_decay 0.001 --hidden 16 --dropout 0.5 > ../out/run.log 2>&1; cd ..; bash gf_harness/emit.sh
  ```
- Output: `cora_acc` 79.8, 79.5, 80, 80.6; gap after +0.3%; result checkpoint `24bb83b9-c173-4f35-871a-3a058516e391`
- Effect: candidate 79.9 minus naive 82.5 = -2.6, 95% bootstrap interval [-3.893, -1.26] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `cora_acc` = 79.67.

### What did we measure?
- Naive median 82.5 over 5 runs; repeats: 82.4, 82.5, 80.8, 84.1, 83.7
- Spread: range 80.8 to 84.1, noise band ±2.4 (2 x MAD), CV 1.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +3.6% (noise band ±3.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `weight_decay` the gap is +3.6% (it comes back)
- PASS · Held-out claim: C_cora@hidden=8 at hidden=8: +2.1% to +0.2% (not worse beyond noise)
- PASS · Held-out claim: C_cora@hidden=32 at hidden=32: +1.5% to +0.9% (not worse beyond noise)
- FAIL · Evidence: `weight_decay=0.001`: no evidence mentions '0.001'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -2.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `hidden=8` (1.11 noise units, gap -0.2%)
- Near alternatives (closest across all claims):
  - `dropout=0.1`, `weight_decay=0.0`: this claim -0.0%, mean |gap| 0.0% (4 runs)
  - `epochs=1000`, `weight_decay=0.0`: this claim -0.3%, mean |gap| 0.3% (4 runs)
  - `weight_decay=0.0`, `hidden=800`: this claim -0.6%, mean |gap| 0.6% (4 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `weight_decay=0.001` (reported)
- `epochs=1000, weight_decay=0.0`
- `dropout=0.1, weight_decay=0.0`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting weight_decay=0.001 | settings | 39% | 0.4 sigma (fits every claim) | run with weight_decay=0.001 |
| 2 | the setting epochs=1000, weight_decay=0.0 | settings | 12% | 0.5 sigma (fits every claim) | run with epochs=1000, weight_decay=0.0 |
| 3 | no difference in reporting: the numbers as printed at the end of the run | settings | 11% | 1.9 sigma (fits every claim) | the settings search and the other classes |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `weight_decay`: weight_decay=0.001 (max I 0.38)
  - `epochs, weight_decay`: epochs=1000, weight_decay=0.0 (max I 0.47)
  - `dropout, weight_decay`: dropout=0.75, weight_decay=0.001 (max I 0.75); dropout=0.1, weight_decay=0.0 (max I 1.18)
  - `epochs, hidden, weight_decay`: epochs=1000, hidden=32, weight_decay=0.0 (max I 0.82)
  - `hidden`: hidden=8 (max I 0.87); hidden=800 (max I 0.97)
  - `dropout, epochs`: dropout=0.1, epochs=100 (max I 0.87)
  - `dropout, hidden, weight_decay`: dropout=0.1, hidden=8, weight_decay=0.0 (max I 1.18); dropout=0.1, hidden=32, weight_decay=0.0 (max I 1.18)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:17`)
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:19`)
- Equally good values: `weight_decay` in {0.0, 0.001}

Notes:
- its runs spread 0.3x the naive run's noise band (reported, not used to judge)
- configurations the target claim can't tell apart from the answer: weight_decay=0.001; epochs=1000, weight_decay=0.0; dropout=0.1, weight_decay=0.0
- equally good values within one noise band (measured): weight_decay in {0.0, 0.001}
- discrimination: the paper's other conditions (C_cora@hidden=8, C_cora@hidden=32) don't yet tell the equally good fits apart: weight_decay=0.001 60%; epochs=1000, weight_decay=0.0 28%; dropout=0.1, weight_decay=0.0 12%
- patch round stopped early: run budget of 150 reached (wanted 1 more run(s) of {'weight_decay': '0.001', '@ast:pygcn/train.py:19:default': 'True'} for 'patch screen')
- value interval stopped early: run budget of 150 reached (wanted 1 more run(s) of {'weight_decay': '0.0005'} for 'interval weight_decay=0.0005')
- not identifiable from the paper's numbers: 2 configuration(s) of other knobs fit every claim as well as the answer (weight_decay=0.001: dropout=0.1, weight_decay=0.0; epochs=1000, weight_decay=0.0), and the paper's other conditions (C_cora@hidden=8, C_cora@hidden=32) don't separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_cora | Mean |gap| |
|---|---|---|---|
| `dropout=0.1`, `weight_decay=0.0` | 4 | -0.0% | 0.0% |
| `weight_decay=0.001` | 4 | +0.3% | 0.3% |
| `epochs=1000`, `weight_decay=0.0` | 4 | -0.3% | 0.3% |
| `weight_decay=0.0`, `hidden=800` | 4 | -0.6% | 0.6% |
| `dropout=0.75`, `weight_decay=0.0` | 4 | +0.8% | 0.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `dropout=2.5`: other, Dropout must be a probability in the range [0,1]; the value 2.5 is outside this range and was rejected by the program. [not taken as invalid_value: the log shows no rejection]
- `dropout=5`: other, The training script expects dropout to be a floating-point probability in the range [0,1]. Supplying '5' is outside this range, so the program rejected the value. [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `dropout`: fraction (dropout.p (torch.nn.functional.dropout) at pygcn/models.py:16)
- `epochs`: count (range() bound at pygcn/train.py:100)
- `lr`: rate (optimizer.lr (Adam) at pygcn/train.py:49)
- `weight_decay`: rate0 (optimizer.weight_decay (Adam) at pygcn/train.py:49)

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `dbbcc15f384db7a3ca32fa8292dfa06643946a56da69654de5843c4c0d96b244`
- Cost: Nemotron billed $0.0000, sandbox reported $43.3541 (total $43.3541; this search; ledger extraction is included only if it shared the search's router)
