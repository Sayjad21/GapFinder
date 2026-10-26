# Gap Report: planted L1-pygcn-s8-4

Artifact `pygcn` · generated 2026-10-26 18:14 · 140 branch runs (0 build/load setups) · sandbox $18.5106

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_cora (cora_acc) | Fits but unsupported | +169.3% | +0.0% | ±3.9% | `dropout=1` |

## C_cora: cora_acc (paper 30.9)
**Fits but unsupported** · gap +169.3% → +0.0% · 63 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0031`, `B0055`, `B0056`, `B0078` (4 run(s) of the same config)
- Config: `dropout` naive `0.5`, changed to `1`
- Command:

  Replay: fork checkpoint `69abd25a-45ee-4e12-8b94-2cfde545816c` and run
  ```
  @ast:pygcn/train.py:17:default=False @ast:pygcn/train.py:19:default=False RUN_TAG=3e35d2f37ac5 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; mkdir -p out; S=$(( $(printf %s "$RUN_TAG" | cksum | cut -d" " -f1) % 100000 )); cd pygcn && PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --no-cuda --seed $S --epochs 200 --lr 0.01 --weight_decay 5e-4 --hidden 16 --dropout 1 > ../out/run.log 2>&1; cd ..; bash gf_harness/emit.sh
  ```
- Output: `cora_acc` 30.9, 30.9, 30.9, 30.9; gap after +0.0%; result checkpoint `840ab9ab-3c94-4345-be65-20ce2da8cd48`
- Effect: candidate 30.9 minus naive 83.2 = -52.3, 95% bootstrap interval [-52.84, -51.48] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `cora_acc` = 30.9.

### What did we measure?
- Naive median 83.2 over 5 runs; repeats: 83.2, 83.8, 83.5, 82.3, 82.5
- Spread: range 82.3 to 83.8, noise band ±1.2 (2 x MAD), CV 0.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +169.3% (noise band ±3.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `dropout` the gap is +169.3% (it comes back)
- PASS · Held-out claim: C_cora@lr=0.005 at lr=0.005: +146.3% to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_cora@lr=0.02 at lr=0.02: +169.6% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `dropout=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -52.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=20` (43.58 noise units, gap +0.0%); `epochs=4` (43.58 noise units, gap +0.0%); `lr=0.0001` (43.58 noise units, gap +0.0%); `weight_decay=0.025` (43.58 noise units, gap +0.0%); `lr=0.001` (42.58 noise units, gap +3.9%) (and 18 more in the JSON)
- Near alternatives (closest across all claims):
  - `epochs=20`: this claim +0.0%, mean |gap| 0.0% (4 runs)
  - `weight_decay=0.025`: this claim +0.0%, mean |gap| 0.0% (4 runs)
  - `dropout=1`, `weight_decay=0.025`: this claim +0.0%, mean |gap| 0.0% (4 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `dropout=1` (reported)
- `weight_decay=0.025`
- `epochs=20`
- `lr=0.001, weight_decay=0.025`
- `dropout=1, weight_decay=0.005`
- `dropout=1, weight_decay=0.025`
- `epochs=20, weight_decay=0.005`
- `epochs=20, weight_decay=0.025`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting dropout=1 | settings | 43% | 0.0 sigma (fits every claim) | run with dropout=1 |
| 2 | the setting weight_decay=0.025 | settings | 14% | 0.0 sigma (fits every claim) | run with weight_decay=0.025 |
| 3 | the setting lr=0.001, weight_decay=0.025 | settings | 14% | 0.0 sigma (fits every claim) | run with lr=0.001, weight_decay=0.025 |

### History matching (every measured configuration, all claims together)
- 17 of 75 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `dropout`: dropout=1 (max I 0)
  - `weight_decay`: weight_decay=0.025 (max I 0)
  - `dropout, weight_decay`: dropout=1, weight_decay=0.025 (max I 0); dropout=1, weight_decay=0.005 (max I 0)
  - `epochs, weight_decay`: epochs=20, weight_decay=0.025 (max I 0); epochs=20, weight_decay=0.005 (max I 0)
  - `lr, weight_decay`: lr=0.001, weight_decay=0.025 (max I 0); lr=0.005, weight_decay=0.025 (max I 0)
  - `dropout, lr`: dropout=1, lr=0.005 (max I 0); dropout=1, lr=0.02 (max I 0)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:17`)
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:19`)

Notes:
- its runs spread 0.3x the naive run's noise band (reported, not used to judge)
- configurations the target claim can't tell apart from the answer: dropout=1; weight_decay=0.025; epochs=20; lr=0.001, weight_decay=0.025; dropout=1, weight_decay=0.005; dropout=1, weight_decay=0.025; epochs=20, weight_decay=0.005; epochs=20, weight_decay=0.025
- discrimination: the paper's other conditions (C_cora@lr=0.005, C_cora@lr=0.02) don't yet tell the equally good fits apart: dropout=1 50%; weight_decay=0.025 50%; epochs=20 0%
- its runs spread 0.3x the naive run's noise band (reported, not used to judge)
- explained with a code patch (tested in memory, no file edited): pygcn/train.py line 17: default = False -> True
- dropout: values from 1 to 1 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- not identifiable from the paper's numbers: 5 configuration(s) of other knobs fit every claim as well as the answer (dropout=1: epochs=20; epochs=20, weight_decay=0.005; epochs=20, weight_decay=0.025; lr=0.001, weight_decay=0.025; weight_decay=0.025), and the paper's other conditions (C_cora@lr=0.005, C_cora@lr=0.02) don't separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_cora | Mean |gap| |
|---|---|---|---|
| `epochs=20` | 4 | +0.0% | 0.0% |
| `dropout=1` | 4 | +0.0% | 0.0% |
| `weight_decay=0.025` | 4 | +0.0% | 0.0% |
| `dropout=1`, `weight_decay=0.025` | 4 | +0.0% | 0.0% |
| `epochs=20`, `weight_decay=0.025` | 4 | +0.0% | 0.0% |

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
- Cost: Nemotron billed $0.0000, sandbox reported $18.5106 (total $18.5106; this search; ledger extraction is included only if it shared the search's router)
