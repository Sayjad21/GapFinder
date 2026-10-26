# Gap Report: planted L2-pygcn-s2-2

Artifact `pygcn` · generated 2026-10-21 23:45 · 128 branch runs (0 build/load setups) · sandbox $45.8127

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_cora (cora_acc) | Paper-artifact inconsistency | +3.4% | -0.2% | ±1.2% | `weight_decay=0.001` |

## C_cora: cora_acc (paper 80.33)
**Paper-artifact inconsistency** · gap +3.4% → -0.2% · 85 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0019`, `B0053`, `B0054`, `B0055` (4 run(s) of the same config)
- Config: `weight_decay` naive `5e-4`, changed to `0.001`
- Command:

  Replay: fork checkpoint `69abd25a-45ee-4e12-8b94-2cfde545816c` and run
  ```
  RUN_TAG=c766e16b8960 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; mkdir -p out; S=$(( $(printf %s "$RUN_TAG" | cksum | cut -d" " -f1) % 100000 )); cd pygcn && PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --no-cuda --seed $S --epochs 200 --lr 0.01 --weight_decay 0.001 --hidden 16 --dropout 0.5 > ../out/run.log 2>&1; cd ..; bash gf_harness/emit.sh
  ```
- Output: `cora_acc` 79.8, 80.2, 80.2, 80.3; gap after -0.2%; result checkpoint `2d22186f-72b9-4c9a-bbcf-414291a03721`
- Effect: candidate 80.2 minus naive 83.1 = -2.9, 95% bootstrap interval [-3.553, -2.173] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `cora_acc` = 80.33.

### What did we measure?
- Naive median 83.1 over 5 runs; repeats: 83.1, 84, 82.1, 83.6, 82.8
- Spread: range 82.1 to 84, noise band ±1 (2 x MAD), CV 0.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +3.4% (noise band ±1.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `weight_decay` the gap is +3.4% (it comes back)
- PASS · Held-out claim: C_cora@weight_decay=0.00025 at weight_decay=5e-4: n/a to -0.8% (not worse beyond noise)
- PASS · Held-out claim: C_cora@weight_decay=0.001 at weight_decay=0.002: n/a to -1.2% (not worse beyond noise)
- FAIL · Evidence: `weight_decay=0.001`: no evidence mentions '0.001'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -2.9 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `dropout=0.75` (1.8 noise units, gap +1.2%); `weight_decay=1e-05` (1.6 noise units, gap +1.5%); `weight_decay=0.0` (1.04 noise units, gap -2.2%)
- Near alternatives (closest across all claims):
  - `weight_decay=0.0`: this claim -0.2%, mean |gap| 0.2% (4 runs)
  - `dropout=0.75`: this claim +0.3%, mean |gap| 0.3% (4 runs)
  - `dropout=0.1`, `lr=0.005`: this claim +0.4%, mean |gap| 0.4% (4 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `weight_decay=0.001` (reported)
- `dropout=0.75`
- `weight_decay=0.0`
- `weight_decay=1e-05`
- `lr=0.005, weight_decay=1e-05`
- `hidden=800, weight_decay=1e-05`
- `dropout=0.1, weight_decay=1e-05`
- `dropout=0.1, lr=0.005`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the code's weight_decay is 2 x the paper's (a unit or convention differs between paper and code) | code | 64% | 0.7 sigma (fits every claim) | find where weight_decay enters the computation and compare its unit with the paper's |
| 2 | the setting dropout=0.75 | settings | 22% | 1.3 sigma (fits every claim) | run with dropout=0.75 |
| 3 | the setting dropout=0.1, lr=0.005 | settings | 5% | 1.5 sigma (fits every claim) | run with dropout=0.1, lr=0.005 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `dropout`: dropout=0.75 (max I 1.32)
  - `dropout, weight_decay`: dropout=0.75, weight_decay=0.001 (max I 1.4); dropout=0.75, weight_decay=1e-05 (max I 1.58)
  - `dropout, hidden`: dropout=0.75, hidden=800 (max I 1.58); dropout=0.1, hidden=80 (max I 1.58)
  - `hidden, lr`: hidden=80, lr=0.02 (max I 1.58)
  - `epochs, lr`: epochs=400, lr=0.005 (max I 1.58)
  - `dropout, lr`: dropout=0.1, lr=0.005 (max I 1.63)
  - `dropout, epochs`: dropout=0.1, epochs=2000 (max I 1.63)
  - `dropout, lr, weight_decay`: dropout=0.1, lr=0.005, weight_decay=0.00025 (max I 1.63)
- 2 separate islands (no single-knob move joins them): dropout=0.75; dropout=0.75, weight_decay=0.001; dropout=0.75, weight_decay=1e-05 | epochs=2000, hidden=800; epochs=400, hidden=80; epochs=2000, hidden=80
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:17`)
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:19`)
- Equally good values: `weight_decay` in {0.0, 0.001}

Notes:
- configurations the target claim can't tell apart from the answer: weight_decay=0.001; dropout=0.75; weight_decay=0.0; weight_decay=1e-05; lr=0.005, weight_decay=1e-05; hidden=800, weight_decay=1e-05; dropout=0.1, weight_decay=1e-05; dropout=0.1, lr=0.005
- equally good values within one noise band (measured): weight_decay in {0.0, 0.001}
- discrimination: the paper's other conditions (C_cora@weight_decay=0.00025, C_cora@weight_decay=0.001) don't yet tell the equally good fits apart: dropout=0.75 63%; dropout=0.1, lr=0.005 21%; lr=0.005, weight_decay=1e-05 4%
- scale probe: the code's weight_decay as 2 x the paper's fits every swept claim after 11 runs at g(v) (C_cora at weight_decay=0.001, C_cora@weight_decay=0.00025 at weight_decay=5e-4, C_cora@weight_decay=0.001 at weight_decay=0.002)
- labelled Paper-artifact inconsistency: one factor (2 x the paper's) makes every one of the 3 swept claims fit
- mutation round: no room left in the run budget

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_cora | Mean |gap| |
|---|---|---|---|
| `weight_decay=0.001` | 4 | -0.2% | 0.2% |
| `weight_decay=0.0` | 4 | -0.2% | 0.2% |
| `dropout=0.75` | 4 | +0.3% | 0.3% |
| `dropout=0.1`, `lr=0.005` | 4 | +0.4% | 0.4% |
| `weight_decay=1e-05`, `hidden=800` | 3 | +1.3% | 1.3% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `dropout=2.5`: other, Dropout rate must be a probability in [0,1]; value 2.5 is outside this range, causing the program to reject it. [not taken as invalid_value: the log shows no rejection]
- `dropout=5`: other, The dropout parameter expects a probability between 0 and 1; value '5' is out of range, causing the program to reject it. [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `dropout`: fraction (dropout.p (torch.nn.functional.dropout) at pygcn/models.py:16)
- `epochs`: count (range() bound at pygcn/train.py:100)
- `lr`: rate (optimizer.lr (Adam) at pygcn/train.py:49)
- `weight_decay`: rate0 (optimizer.weight_decay (Adam) at pygcn/train.py:49)

## Provenance
- GapFinder commit: `1c8f0f8b4a997137c12c0ee6716ab6adeed88fc3`
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `8142ea3e751e0b113ef55c227c8642b84177f98ff01eb9ec545b910efe081eb3`
- Cost: Nemotron billed $0.0000, sandbox reported $45.8127 (total $45.8127; this search; ledger extraction is included only if it shared the search's router)
