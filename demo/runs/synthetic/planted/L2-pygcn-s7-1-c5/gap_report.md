# Gap Report: planted L2-pygcn-s7-1

Artifact `pygcn` · generated 2026-10-24 14:21 · 150 branch runs (0 build/load setups) · sandbox $50.0137

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_cora (cora_acc) | Fits but unsupported | +1.3% | -0.0% | ±1.0% | `weight_decay=1e-05` |

## C_cora: cora_acc (paper 82.17)
**Fits but unsupported** · gap +1.3% → -0.0% · 45 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0046`, `B0056`, `B0057`, `B0058` (4 run(s) of the same config)
- Config: `weight_decay` naive `5e-4`, changed to `1e-05`
- Command:

  Replay: fork checkpoint `69abd25a-45ee-4e12-8b94-2cfde545816c` and run
  ```
  RUN_TAG=2b3196ee2bda export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; mkdir -p out; S=$(( $(printf %s "$RUN_TAG" | cksum | cut -d" " -f1) % 100000 )); cd pygcn && PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --no-cuda --seed $S --epochs 200 --lr 0.01 --weight_decay 1e-05 --hidden 16 --dropout 0.5 > ../out/run.log 2>&1; cd ..; bash gf_harness/emit.sh
  ```
- Output: `cora_acc` 82.2, 82.6, 82.1, 81.1; gap after -0.0%; result checkpoint `dd6bf54d-3b23-44dc-be43-f8534440d97f`
- Effect: candidate 82.15 minus naive 83.2 = -1.05, 95% bootstrap interval [-2.1, -0.3267] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `cora_acc` = 82.17.

### What did we measure?
- Naive median 83.2 over 5 runs; repeats: 83.2, 83.3, 82.9, 83.5, 82.4
- Spread: range 82.4 to 83.5, noise band ±0.832 (2 x MAD), CV 0.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +1.3% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `weight_decay` the gap is +1.3% (it comes back)
- PASS · Held-out claim: C_cora@weight_decay=0.00025 at weight_decay=0.00025: -0.4% to -0.4% (not worse beyond noise)
- PASS · Held-out claim: C_cora@weight_decay=0.001 at weight_decay=0.001: +1.6% to +1.6% (not worse beyond noise)
- FAIL · Evidence: `weight_decay=1e-05`: no evidence mentions '1e-05'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -1.05 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `weight_decay=0.0001` (1.2 noise units, gap +0.0%)
- Near alternatives (closest across all claims):
  - `hidden=800`, `epochs=400`: this claim -0.1%, mean |gap| 0.1% (4 runs)
  - `weight_decay=1e-05`, `lr=0.05`: this claim -0.1%, mean |gap| 0.1% (4 runs)
  - `weight_decay=1e-05`, `hidden=160`: this claim -0.1%, mean |gap| 0.1% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | no difference in reporting: the numbers as printed at the end of the run | settings | 32% | 0.9 sigma (fits every claim) | the settings search and the other classes |
| 2 | the setting weight_decay=1e-05 | settings | 21% | 0.9 sigma (fits every claim) | run with weight_decay=1e-05 |
| 3 | the setting hidden=160, weight_decay=1e-05 | settings | 7% | 0.9 sigma (fits every claim) | run with hidden=160, weight_decay=1e-05 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `hidden, weight_decay`: hidden=160, weight_decay=1e-05 (max I 0.02); hidden=800, weight_decay=0.0001 (max I 0.11)
  - `lr, weight_decay`: lr=0.05, weight_decay=1e-05 (max I 0.07); lr=0.05, weight_decay=0.0001 (max I 0.34)
  - `epochs, hidden`: epochs=400, hidden=800 (max I 0.14)
  - `dropout, lr`: dropout=0.25, lr=0.1 (max I 0.24)
  - `dropout, epochs`: dropout=0.25, epochs=400 (max I 0.27)
  - `lr`: lr=0.1 (max I 0.32)
  - `dropout, hidden`: dropout=0.25, hidden=800 (max I 0.32); dropout=0.05, hidden=800 (max I 0.35)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:17`)
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:19`)

Notes:
- stopped early: run budget of 150 reached (wanted 1 more run(s) of {'lr': '0.05', 'hidden': '800'} for 'combine')
- verified from runs already made, after the budget ran out
- early code screen stopped: run budget of 150 reached (wanted 1 more run(s) of {'@ast:pygcn/train.py:17:default': 'True'} for 'patch screen (early)')
- patch round stopped early: run budget of 150 reached (wanted 1 more run(s) of {'hidden': '160', 'weight_decay': '1e-05', '@ast:pygcn/train.py:17:default': 'True'} for 'patch screen')
- value interval stopped early: run budget of 150 reached (wanted 1 more run(s) of {'weight_decay': '5e-06'} for 'interval weight_decay=5e-06')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_cora | Mean |gap| |
|---|---|---|---|
| `weight_decay=1e-05` | 4 | -0.0% | 0.0% |
| `hidden=800`, `epochs=400` | 4 | -0.1% | 0.1% |
| `weight_decay=1e-05`, `lr=0.05` | 4 | -0.1% | 0.1% |
| `weight_decay=1e-05`, `hidden=160` | 4 | -0.1% | 0.1% |
| `weight_decay=0.0001`, `hidden=800` | 4 | +0.2% | 0.2% |

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
- Cost: Nemotron billed $0.0000, sandbox reported $50.0137 (total $50.0137; this search; ledger extraction is included only if it shared the search's router)
