# Gap Report: planted L1-pygcn-s6-1

Artifact `pygcn` · generated 2026-10-23 17:55 · 150 branch runs (0 build/load setups) · sandbox $19.1798

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_cora (cora_acc) | Fits but unsupported | +166.3% | +0.0% | ±2.7% | `dropout=1` |

## C_cora: cora_acc (paper 30.9)
**Fits but unsupported** · gap +166.3% → +0.0% · 69 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0031`, `B0057`, `B0058`, `B0078` (4 run(s) of the same config)
- Config: `dropout` naive `0.5`, changed to `1`
- Command:

  Replay: fork checkpoint `69abd25a-45ee-4e12-8b94-2cfde545816c` and run
  ```
  RUN_TAG=c43e70068fb8 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; mkdir -p out; S=$(( $(printf %s "$RUN_TAG" | cksum | cut -d" " -f1) % 100000 )); cd pygcn && PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --no-cuda --seed $S --epochs 200 --lr 0.01 --weight_decay 5e-4 --hidden 16 --dropout 1 > ../out/run.log 2>&1; cd ..; bash gf_harness/emit.sh
  ```
- Output: `cora_acc` 30.9, 30.9, 30.9, 30.9; gap after +0.0%; result checkpoint `093f0986-76e4-4ac6-9402-632361dbe470`
- Effect: candidate 30.9 minus naive 82.3 = -51.4, 95% bootstrap interval [-52.52, -51.16] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `cora_acc` = 30.9.

### What did we measure?
- Naive median 82.3 over 5 runs; repeats: 82.3, 82, 82.7, 82.2, 83.6
- Spread: range 82 to 83.6, noise band ±0.823 (2 x MAD), CV 0.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +166.3% (noise band ±2.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `dropout` the gap is +166.3% (it comes back)
- PASS · Held-out claim: C_cora@lr=0.005 at lr=0.005: +144.3% to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_cora@lr=0.02 at lr=0.02: +166.7% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `dropout=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -51.4 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=20` (62.45 noise units, gap +0.0%); `lr=0.001` (62.45 noise units, gap +0.0%); `epochs=1` (62.45 noise units, gap +0.0%); `lr=0.0001` (62.45 noise units, gap +0.0%); `weight_decay=0.025` (62.45 noise units, gap +0.0%) (and 16 more in the JSON)
- Near alternatives (closest across all claims):
  - `epochs=20`: this claim +0.0%, mean |gap| 0.0% (4 runs)
  - `lr=0.001`: this claim +0.0%, mean |gap| 0.0% (4 runs)
  - `weight_decay=0.025`: this claim +0.0%, mean |gap| 0.0% (4 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `dropout=1` (reported)
- `weight_decay=0.025`
- `epochs=20, weight_decay=0.005`
- `lr=0.001`
- `lr=0.001, weight_decay=0.005`
- `lr=0.001, weight_decay=0.025`
- `dropout=1, weight_decay=0.005`
- `dropout=1, weight_decay=0.025`
- `dropout=0.95, weight_decay=0.025`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting dropout=1 | settings | 100% | 0.0 sigma (fits every claim) | run with dropout=1 |
| 2 | a cause outside every class tested | outside | 0% |  | look for code, data or evaluation differences the classes don't cover |
| 3 | no difference in reporting: the numbers as printed at the end of the run | settings | 0% | 78.2 sigma | the settings search and the other classes |

### History matching (every measured configuration, all claims together)
- 13 of 69 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `dropout`: dropout=1 (max I 0)
  - `weight_decay`: weight_decay=0.025 (max I 0)
  - `dropout, weight_decay`: dropout=1, weight_decay=0.025 (max I 0); dropout=1, weight_decay=0.005 (max I 0); dropout=0.95, weight_decay=0.025 (max I 0)
  - `lr, weight_decay`: lr=0.001, weight_decay=0.025 (max I 0); lr=0.001, weight_decay=0.005 (max I 0)
  - `epochs, weight_decay`: epochs=20, weight_decay=0.005 (max I 0)
  - `dropout, epochs`: dropout=0.95, epochs=20 (max I 0)
  - `dropout, lr`: dropout=1, lr=0.005 (max I 0)
- 2 separate islands (no single-knob move joins them): dropout=1; weight_decay=0.025; dropout=1, weight_decay=0.025 | epochs=20, weight_decay=0.005; dropout=0.95, epochs=20; epochs=20
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:17`)
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:19`)

Notes:
- configurations the target claim can't tell apart from the answer: dropout=1; weight_decay=0.025; lr=0.001; lr=0.001, weight_decay=0.005; lr=0.001, weight_decay=0.025; dropout=1, weight_decay=0.005; dropout=1, weight_decay=0.025; epochs=20, weight_decay=0.005; dropout=0.95, weight_decay=0.025
- early code screen stopped: run budget of 150 reached (wanted 1 more run(s) of {'@ast:pygcn/train.py:17:default': 'True'} for 'patch screen (early)')
- discrimination: the paper's other conditions favour dropout=1 (posterior 100% after 0 run(s) chosen by expected information)
- patch round stopped early: run budget of 150 reached (wanted 1 more run(s) of {'dropout': '1', '@ast:pygcn/train.py:17:default': 'True'} for 'patch screen')
- value interval stopped early: run budget of 150 reached (wanted 1 more run(s) of {'dropout': '10'} for 'interval dropout=10')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_cora | Mean |gap| |
|---|---|---|---|
| `epochs=20` | 4 | +0.0% | 0.0% |
| `lr=0.001` | 4 | +0.0% | 0.0% |
| `dropout=1` | 4 | +0.0% | 0.0% |
| `weight_decay=0.025` | 4 | +0.0% | 0.0% |
| `dropout=1`, `weight_decay=0.025` | 4 | +0.0% | 0.0% |

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
- Cost: Nemotron billed $0.0000, sandbox reported $19.1798 (total $19.1798; this search; ledger extraction is included only if it shared the search's router)
