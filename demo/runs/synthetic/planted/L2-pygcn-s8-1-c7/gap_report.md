# Gap Report: planted L2-pygcn-s8-1

Artifact `pygcn` · generated 2026-10-26 11:10 · 133 branch runs (0 build/load setups) · sandbox $37.1490

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_cora (cora_acc) | Paper-artifact inconsistency | +5.0% | +0.2% | ±1.0% | `hidden=8` |

## C_cora: cora_acc (paper 79.27)
**Paper-artifact inconsistency** · gap +5.0% → +0.2% · 66 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0024`, `B0059`, `B0060`, `B0076` (4 run(s) of the same config)
- Config: `hidden` naive `16`, changed to `8`
- Command:

  Replay: fork checkpoint `69abd25a-45ee-4e12-8b94-2cfde545816c` and run
  ```
  @ast:pygcn/train.py:17:default=False @ast:pygcn/train.py:19:default=False RUN_TAG=5460659eaf96 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; mkdir -p out; S=$(( $(printf %s "$RUN_TAG" | cksum | cut -d" " -f1) % 100000 )); cd pygcn && PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --no-cuda --seed $S --epochs 200 --lr 0.01 --weight_decay 0.001 --hidden 16 --dropout 0.5 > ../out/run.log 2>&1; cd ..; bash gf_harness/emit.sh
  ```
- Output: `cora_acc` 79.6, 80.3, 72, 79.3; gap after +0.2%; result checkpoint `3ac6b6ef-94c7-4725-815c-bb8959b9a1d5`
- Effect: candidate 79.45 minus naive 83.2 = -3.75, 95% bootstrap interval [-11.7, -2.8] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `cora_acc` = 79.27.

### What did we measure?
- Naive median 83.2 over 5 runs; repeats: 83.2, 83.3, 82.9, 84.4, 83
- Spread: range 82.9 to 84.4, noise band ±0.832 (2 x MAD), CV 0.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +5.0% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `weight_decay` the gap is +5.0% (it comes back)
- PASS · Held-out claim: C_cora@hidden=8 at hidden=4: n/a to +14.1% (not worse beyond noise)
- PASS · Held-out claim: C_cora@hidden=32 at hidden=16: n/a to -0.7% (not worse beyond noise)
- FAIL · Evidence: `weight_decay=None`: no evidence mentions '0.001'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -3.75 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `dropout=0.75` (4.04 noise units, gap -0.7%); `weight_decay=0.0` (3.32 noise units, gap -1.5%); `weight_decay=0.001` (3.25 noise units, gap +1.6%); `weight_decay=1e-05` (3 noise units, gap +1.8%); `lr=0.1` (2.16 noise units, gap +2.7%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `weight_decay=0.0`, `hidden=1600`: this claim +0.0%, mean |gap| 0.0% (4 runs)
  - `weight_decay=0.0`, `lr=0.1`: this claim +0.3%, mean |gap| 0.3% (4 runs)
  - `dropout=0.75`: this claim +0.4%, mean |gap| 0.4% (4 runs)

### Equally good configurations
The target claim can't tell these 10 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `weight_decay=0.001` (reported)
- `dropout=0.75`
- `weight_decay=0.0`
- `epochs=100`
- `hidden=8`
- `hidden=1600, weight_decay=0.0`
- `lr=0.1, weight_decay=0.0`
- `dropout=0.75, weight_decay=0.001`
- `epochs=100, weight_decay=0.0`
- `dropout=0.75, lr=0.1`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting dropout=0.75, weight_decay=0.001 | settings | 32% | 1.3 sigma (fits every claim) | run with dropout=0.75, weight_decay=0.001 |
| 2 | the setting epochs=100 | settings | 26% | 1.3 sigma (fits every claim) | run with epochs=100 |
| 3 | the code's hidden is 0.5 x the paper's (a unit or convention differs between paper and code) | code | 20% | 0.8 sigma (fits every claim) | find where hidden enters the computation and compare its unit with the paper's |

### History matching (every measured configuration, all claims together)
- 8 of 75 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `dropout, weight_decay`: dropout=0.75, weight_decay=0.001 (max I 1.56)
  - `dropout, hidden, weight_decay`: dropout=0.75, hidden=32, weight_decay=0.001 (max I 2.26)
  - `dropout, lr`: dropout=0.75, lr=0.1 (max I 2.38); dropout=0.75, lr=0.05 (max I 2.52)
  - `weight_decay`: weight_decay=1e-05 (max I 2.46); weight_decay=5e-05 (max I 2.86)
  - `lr`: lr=0.5 (max I 2.72)
  - `dropout`: dropout=0.1 (max I 2.86)
- 5 separate islands (no single-knob move joins them): dropout=0.75, weight_decay=0.001; dropout=0.75, hidden=32, weight_decay=0.001 | dropout=0.75, lr=0.1; dropout=0.75, lr=0.05 | weight_decay=1e-05; weight_decay=5e-05 | lr=0.5
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:17`)
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:19`)
- Equally good values: `weight_decay` in {0.0, 0.001}

Notes:
- configurations the target claim can't tell apart from the answer: weight_decay=0.001; dropout=0.75; weight_decay=0.0; epochs=100; hidden=8; hidden=1600, weight_decay=0.0; lr=0.1, weight_decay=0.0; dropout=0.75, weight_decay=0.001; epochs=100, weight_decay=0.0; dropout=0.75, lr=0.1
- equally good values within one noise band (measured): weight_decay in {0.0, 0.001}
- {'weight_decay': '0.001'} fit the target but not C_cora@hidden=8 (claims at fixed settings, I > 3); {'dropout': '0.75', 'weight_decay': '0.001'} fits every claim, those included, so it is the answer (history matching)
- discrimination: the paper's other conditions (C_cora@hidden=8, C_cora@hidden=32) don't yet tell the equally good fits apart: epochs=100 62%; dropout=0.75, weight_decay=0.001 31%; weight_decay=0.001 5%
- scale probe: the code's hidden as 0.5 x the paper's fits every swept claim after 11 runs at g(v) (C_cora at hidden=8, C_cora@hidden=8 at hidden=4, C_cora@hidden=32 at hidden=16)
- labelled Paper-artifact inconsistency: one factor (0.5 x the paper's) makes every one of the 3 swept claims fit; it replaces {'weight_decay': '0.001'}
- mutation round: no room left in the run budget
- hidden: values from 6 to 8 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- not identifiable from the paper's numbers: 9 configuration(s) of other knobs fit every claim as well as the answer (hidden=8: dropout=0.75; dropout=0.75, lr=0.1; dropout=0.75, weight_decay=0.001; epochs=100; epochs=100, weight_decay=0.0; hidden=1600, weight_decay=0.0), and the paper's other conditions (C_cora@hidden=8, C_cora@hidden=32) don't separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_cora | Mean |gap| |
|---|---|---|---|
| `weight_decay=0.0`, `hidden=1600` | 4 | +0.0% | 0.0% |
| `hidden=8` | 4 | +0.2% | 0.2% |
| `weight_decay=0.0`, `lr=0.1` | 4 | +0.3% | 0.3% |
| `dropout=0.75` | 4 | +0.4% | 0.4% |
| `weight_decay=0.0` | 4 | +0.8% | 0.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `dropout=2.5`: other, The dropout parameter must be a probability in the range [0,1]; the provided value 2.5 is outside this range, causing the program to reject it. [not taken as invalid_value: the log shows no rejection]
- `dropout=5`: other, The dropout parameter expects a float in the range [0,1]; setting it to 5 is outside this range, causing the program to reject the value and produce no metrics. [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `dropout`: fraction (dropout.p (torch.nn.functional.dropout) at pygcn/models.py:16)
- `epochs`: count (range() bound at pygcn/train.py:100)
- `lr`: rate (optimizer.lr (Adam) at pygcn/train.py:49)
- `weight_decay`: rate0 (optimizer.weight_decay (Adam) at pygcn/train.py:49)

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `dbbcc15f384db7a3ca32fa8292dfa06643946a56da69654de5843c4c0d96b244`
- Cost: Nemotron billed $0.0011, sandbox reported $37.1490 (total $37.1501; this search; ledger extraction is included only if it shared the search's router)
