# Gap Report: planted L2-pygcn-s4-1

Artifact `pygcn` · generated 2026-10-22 13:31 · 150 branch runs (0 build/load setups) · sandbox $144.9866

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_cora (cora_acc) | Fits but unsupported | +3.2% | -0.4% | ±2.0% | `weight_decay=0.001` |

## C_cora: cora_acc (paper 80)
**Fits but unsupported** · gap +3.2% → -0.4% · 81 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0019`, `B0053`, `B0054`, `B0055` (4 run(s) of the same config)
- Config: `weight_decay` naive `5e-4`, changed to `0.001`
- Command:

  Replay: fork checkpoint `69abd25a-45ee-4e12-8b94-2cfde545816c` and run
  ```
  RUN_TAG=f34a94910353 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; mkdir -p out; S=$(( $(printf %s "$RUN_TAG" | cksum | cut -d" " -f1) % 100000 )); cd pygcn && PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --no-cuda --seed $S --epochs 200 --lr 0.01 --weight_decay 0.001 --hidden 16 --dropout 0.5 > ../out/run.log 2>&1; cd ..; bash gf_harness/emit.sh
  ```
- Output: `cora_acc` 79.6, 79, 79.7, 80.7; gap after -0.4%; result checkpoint `0ef3db05-de05-499c-81fa-553ada42c8d4`
- Effect: candidate 79.65 minus naive 82.6 = -2.95, 95% bootstrap interval [-3.92, -1.193] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `cora_acc` = 80.

### What did we measure?
- Naive median 82.6 over 5 runs; repeats: 83.4, 81.3, 81.3, 82.6, 83.2
- Spread: range 81.3 to 83.4, noise band ±1.6 (2 x MAD), CV 1.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +3.2% (noise band ±2.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `weight_decay` the gap is +3.2% (it comes back)
- PASS · Held-out claim: C_cora@weight_decay=0.00025 at weight_decay=0.00025: -0.2% to -0.2% (not worse beyond noise)
- PASS · Held-out claim: C_cora@weight_decay=0.001 at weight_decay=0.001: +5.0% to +5.0% (not worse beyond noise)
- FAIL · Evidence: `weight_decay=0.001`: no evidence mentions '0.001'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -2.95 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `dropout=0.75` (1.44 noise units, gap +0.4%); `weight_decay=0.0` (1.25 noise units, gap +0.7%); `hidden=8` (1.06 noise units, gap -1.1%)
- Near alternatives (closest across all claims):
  - `epochs=1000`, `weight_decay=0.0`: this claim +0.0%, mean |gap| 0.0% (4 runs)
  - `dropout=0.75`: this claim -0.3%, mean |gap| 0.3% (4 runs)
  - `weight_decay=0.0`, `dropout=0.0`: this claim -0.7%, mean |gap| 0.7% (4 runs)

### Equally good configurations
The target claim can't tell these 7 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `weight_decay=0.001` (reported)
- `dropout=0.75`
- `hidden=8`
- `epochs=1000, weight_decay=0.0`
- `dropout=0.0, weight_decay=0.0`
- `hidden=1600, weight_decay=0.0`
- `lr=0.05, weight_decay=0.0`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting hidden=8 | settings | 42% | 1.6 sigma (fits every claim) | run with hidden=8 |
| 2 | the setting dropout=0.0, lr=0.005 | settings | 24% | 1.4 sigma (fits every claim) | run with dropout=0.0, lr=0.005 |
| 3 | the code's weight_decay is 1.5 x the paper's (a unit or convention differs between paper and code) | code | 16% | 2.3 sigma (fits every claim) | find where weight_decay enters the computation and compare its unit with the paper's |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `dropout, lr`: dropout=0.0, lr=0.005 (max I 1.21)
  - `dropout, lr, weight_decay`: dropout=0.0, lr=0.005, weight_decay=0.00025 (max I 1.21); dropout=0.0, lr=0.005, weight_decay=0.001 (max I 1.34)
  - `hidden`: hidden=8 (max I 1.35); hidden=800 (max I 1.4)
  - `hidden, weight_decay`: hidden=8, weight_decay=0.00025 (max I 1.35)
  - `@ast:pygcn/train.py:17:default`: @ast:pygcn/train.py:17:default=True (max I 1.4)
  - `dropout, epochs`: dropout=0.0, epochs=2000 (max I 1.46)
  - `lr`: lr=0.1 (max I 1.53)
  - `hidden, lr`: hidden=1600, lr=0.005 (max I 1.53)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:17`)
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:19`)
- Equally good values: `weight_decay` in {0.0, 0.001}

Notes:
- configurations the target claim can't tell apart from the answer: weight_decay=0.001; dropout=0.75; hidden=8; epochs=1000, weight_decay=0.0; dropout=0.0, weight_decay=0.0; hidden=1600, weight_decay=0.0; lr=0.05, weight_decay=0.0
- equally good values within one noise band (measured): weight_decay in {0.0, 0.001}
- discrimination: the paper's other conditions (C_cora@weight_decay=0.00025, C_cora@weight_decay=0.001) don't yet tell the equally good fits apart: hidden=8 86%; dropout=0.75 11%; weight_decay=0.001 3%
- scale probe: the code's weight_decay as 1.5 x the paper's does not fit every swept claim after 6 runs at g(v) (C_cora at weight_decay=0.00075, C_cora@weight_decay=0.00025 at weight_decay=0.000375, C_cora@weight_decay=0.001 at weight_decay=0.0015)
- patch round: {'@ast:pygcn/train.py:17:default': 'True', 'dropout': '0.0', 'lr': '0.005'} fits every claim but did not pass verification
- value interval stopped early: run budget of 150 reached (wanted 1 more run(s) of {'weight_decay': '0.0006307'} for 'interval weight_decay=0.0006307')
- not identifiable from the paper's numbers: 7 configurations of different knobs fit every claim as well as the answer (dropout=0.0, weight_decay=0.0; dropout=0.75; epochs=1000, weight_decay=0.0; hidden=1600, weight_decay=0.0; hidden=8; lr=0.05, weight_decay=0.0), and the paper's other conditions (C_cora@weight_decay=0.00025, C_cora@weight_decay=0.001) don't separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_cora | Mean |gap| |
|---|---|---|---|
| `epochs=1000`, `weight_decay=0.0` | 4 | +0.0% | 0.0% |
| `dropout=0.75` | 4 | -0.3% | 0.3% |
| `weight_decay=0.001` | 4 | -0.4% | 0.4% |
| `weight_decay=0.0`, `dropout=0.0` | 4 | -0.7% | 0.7% |
| `hidden=8` | 4 | -0.8% | 0.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `dropout=2.5`: other, The dropout parameter expects a probability in the range [0, 1]. The provided value '2.5' is outside this range, causing the program to reject it as an invalid value. [not taken as invalid_value: the log shows no rejection]
- `dropout=5`: other, The dropout parameter expects a probability value between 0 and 1; setting it to 5 is outside this range, causing the program to reject the input. [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `dropout`: fraction (dropout.p (torch.nn.functional.dropout) at pygcn/models.py:16)
- `epochs`: count (range() bound at pygcn/train.py:100)
- `lr`: rate (optimizer.lr (Adam) at pygcn/train.py:49)
- `weight_decay`: rate0 (optimizer.weight_decay (Adam) at pygcn/train.py:49)

## Provenance
- GapFinder commit: `96f43d9d872690442737d0ad342eeb7d86352416` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `dbbcc15f384db7a3ca32fa8292dfa06643946a56da69654de5843c4c0d96b244`
- Cost: Nemotron billed $0.0000, sandbox reported $144.9866 (total $144.9866; this search; ledger extraction is included only if it shared the search's router)
