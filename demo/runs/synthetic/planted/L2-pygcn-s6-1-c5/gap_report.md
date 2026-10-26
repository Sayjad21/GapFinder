# Gap Report: planted L2-pygcn-s6-1

Artifact `pygcn` · generated 2026-10-23 17:58 · 150 branch runs (0 build/load setups) · sandbox $39.5752

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_cora (cora_acc) | Fits but unsupported | +5.2% | +0.2% | ±2.3% | `hidden=8` |

## C_cora: cora_acc (paper 78.17)
**Fits but unsupported** · gap +5.2% → +0.2% · 78 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0024`, `B0057`, `B0058`, `B0065` (4 run(s) of the same config)
- Config: `hidden` naive `16`, changed to `8`
- Command:

  Replay: fork checkpoint `69abd25a-45ee-4e12-8b94-2cfde545816c` and run
  ```
  RUN_TAG=865c0f695c30 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; mkdir -p out; S=$(( $(printf %s "$RUN_TAG" | cksum | cut -d" " -f1) % 100000 )); cd pygcn && PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --no-cuda --seed $S --epochs 200 --lr 0.01 --weight_decay 5e-4 --hidden 8 --dropout 0.5 > ../out/run.log 2>&1; cd ..; bash gf_harness/emit.sh
  ```
- Output: `cora_acc` 79.6, 78.7, 77.9, 78; gap after +0.2%; result checkpoint `7d72b484-c1f6-4bc0-9278-40e289631aa2`
- Effect: candidate 78.35 minus naive 82.2 = -3.85, 95% bootstrap interval [-5.207, -2.94] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `cora_acc` = 78.17.

### What did we measure?
- Naive median 82.2 over 5 runs; repeats: 82.2, 83.3, 83.1, 82.1, 80.9
- Spread: range 80.9 to 83.3, noise band ±1.8 (2 x MAD), CV 1.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +5.2% (noise band ±2.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `hidden` the gap is +5.2% (it comes back)
- PASS · Held-out claim: C_cora@hidden=8 at hidden=8: -0.9% to -0.9% (not worse beyond noise)
- PASS · Held-out claim: C_cora@hidden=32 at hidden=32: -1.3% to -1.3% (not worse beyond noise)
- FAIL · Evidence: `hidden=8`: no evidence mentions '8'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -3.85 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.005` (2.17 noise units, gap +0.2%); `lr=0.5` (1.2 noise units, gap -2.4%); `weight_decay=0.001` (1.17 noise units, gap +2.5%); `weight_decay=0.0` (1.17 noise units, gap +2.5%); `dropout=0.75` (1.11 noise units, gap +2.6%)
- Near alternatives (closest across all claims):
  - `epochs=100`, `dropout=0.1`: this claim +0.0%, mean |gap| 0.0% (4 runs)
  - `weight_decay=0.0`, `lr=0.005`: this claim -0.2%, mean |gap| 0.2% (4 runs)
  - `weight_decay=0.001`, `hidden=8`: this claim -0.3%, mean |gap| 0.3% (4 runs)

### Equally good configurations
The target claim can't tell these 11 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `hidden=8` (reported)
- `weight_decay=0.001`
- `dropout=0.75`
- `lr=0.005`
- `dropout=0.75, weight_decay=0.001`
- `hidden=1600, weight_decay=0.0`
- `dropout=0.1, epochs=100`
- `hidden=8, weight_decay=0.001`
- `dropout=0.1, lr=0.005`
- `lr=0.005, weight_decay=0.0`
- `hidden=8, lr=0.5`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting hidden=8 | settings | 81% | 0.7 sigma (fits every claim) | run with hidden=8 |
| 2 | the setting weight_decay=0.001 | settings | 8% | 0.7 sigma (fits every claim) | run with weight_decay=0.001 |
| 3 | the setting hidden=8, weight_decay=0.001 | settings | 7% | 0.7 sigma (fits every claim) | run with hidden=8, weight_decay=0.001 |

### History matching (every measured configuration, all claims together)
- 32 of 86 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `hidden`: hidden=8 (max I 0.69)
  - `dropout, lr`: dropout=0.1, lr=0.005 (max I 1.1); dropout=0.75, lr=0.005 (max I 1.58); dropout=0.1, lr=0.5 (max I 2.1)
  - `weight_decay`: weight_decay=0.001 (max I 1.3); weight_decay=1e-05 (max I 2.13)
  - `hidden, weight_decay`: hidden=8, weight_decay=0.001 (max I 1.3)
  - `epochs, weight_decay`: epochs=100, weight_decay=0.0 (max I 1.39)
  - `epochs, lr`: epochs=100, lr=0.5 (max I 1.78)
  - `dropout, hidden`: dropout=0.1, hidden=8 (max I 2.14)
- 7 separate islands (no single-knob move joins them): hidden=8; dropout=0.1, lr=0.005; weight_decay=0.001 | lr=0.05; lr=0.1 | epochs=100, weight_decay=0.0 | epochs=100, lr=0.5
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:17`)
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:19`)

Notes:
- configurations the target claim can't tell apart from the answer: hidden=8; weight_decay=0.001; dropout=0.75; lr=0.005; dropout=0.75, weight_decay=0.001; hidden=1600, weight_decay=0.0; dropout=0.1, epochs=100; hidden=8, weight_decay=0.001; dropout=0.1, lr=0.005; lr=0.005, weight_decay=0.0; hidden=8, lr=0.5
- discrimination: the paper's other conditions (C_cora@hidden=8, C_cora@hidden=32) don't yet tell the equally good fits apart: hidden=8 77%; weight_decay=0.001 20%; dropout=0.1, epochs=100 2%
- patch round stopped early: run budget of 150 reached (wanted 2 more run(s) of {'@ast:pygcn/train.py:19:default': 'True', 'hidden': '8'} for 'patch confirm')
- value interval stopped early: run budget of 150 reached (wanted 1 more run(s) of {'hidden': '5'} for 'interval hidden=5')
- not identifiable from the paper's numbers: 8 configuration(s) of other knobs fit every claim as well as the answer (hidden=8: dropout=0.1, epochs=100; dropout=0.1, lr=0.005; dropout=0.75; dropout=0.75, weight_decay=0.001; hidden=1600, weight_decay=0.0; lr=0.005), and the paper's other conditions (C_cora@hidden=8, C_cora@hidden=32) don't separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_cora | Mean |gap| |
|---|---|---|---|
| `epochs=100`, `dropout=0.1` | 4 | +0.0% | 0.0% |
| `weight_decay=0.0`, `lr=0.005` | 4 | -0.2% | 0.2% |
| `hidden=8` | 4 | +0.2% | 0.2% |
| `weight_decay=0.001`, `hidden=8` | 4 | -0.3% | 0.3% |
| `weight_decay=0.001`, `dropout=0.75` | 4 | +1.1% | 1.1% |

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
- Cost: Nemotron billed $0.0011, sandbox reported $39.5752 (total $39.5763; this search; ledger extraction is included only if it shared the search's router)
