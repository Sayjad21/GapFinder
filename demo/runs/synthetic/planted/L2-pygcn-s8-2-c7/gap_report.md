# Gap Report: planted L2-pygcn-s8-2

Artifact `pygcn` · generated 2026-10-26 23:47 · 150 branch runs (0 build/load setups) · sandbox $80.1496

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_cora (cora_acc) | Inconclusive | +1.3% | +1.3% | ±1.0% | — |

## C_cora: cora_acc (paper 81.9)
**Inconclusive** · naive gap +1.3% is inside the noise band ±1.0%, but the band is too wide to call it a reproduction.

### Which experiment changed it?
- None could be tested: the noise band is too wide to tell values apart.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `cora_acc` = 81.9.

### What did we measure?
- Naive median 83 over 5 runs; repeats: 83, 83, 83.9, 83.6, 82.7
- Spread: range 82.7 to 83.9, noise band ±0.83 (2 x MAD), CV 0.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +1.3% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.02` (1.2 noise units, gap -0.1%); `lr=0.05` (1.08 noise units, gap +0.2%)
- Near alternatives (closest across all claims):
  - `hidden=1600`, `weight_decay=1e-05`: this claim -0.2%, mean |gap| 0.2% (4 runs)
  - `lr=0.05`, `hidden=800`: this claim -0.2%, mean |gap| 0.2% (4 runs)
  - `weight_decay=1e-05`, `hidden=800`: this claim -0.2%, mean |gap| 0.2% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | no difference in reporting: the numbers as printed at the end of the run | settings | 25% | 1.1 sigma (fits every claim) | the settings search and the other classes |
| 2 | the setting hidden=800, lr=0.05 | settings | 23% | 0.6 sigma (fits every claim) | run with hidden=800, lr=0.05 |
| 3 | the setting dropout=0.1, weight_decay=5e-05 | settings | 9% | 0.1 sigma (fits every claim) | run with dropout=0.1, weight_decay=5e-05 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `hidden, lr`: hidden=800, lr=0.05 (max I 0.08)
  - `dropout, weight_decay`: dropout=0.1, weight_decay=5e-05 (max I 0.18)
  - `hidden, weight_decay`: hidden=1600, weight_decay=5e-05 (max I 0.2); hidden=1600, weight_decay=1e-05 (max I 0.28); hidden=800, weight_decay=1e-05 (max I 0.28); hidden=800, weight_decay=5e-05 (max I 0.41)
  - `weight_decay`: weight_decay=5e-05 (max I 0.28)
  - `lr, weight_decay`: lr=0.02, weight_decay=1e-05 (max I 0.48)
  - `epochs, weight_decay`: epochs=1000, weight_decay=1e-05 (max I 0.48)
  - `epochs, lr`: epochs=1000, lr=0.05 (max I 0.56)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:17`)
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:19`)

Notes:
- stopped early: run budget of 150 reached (wanted 3 more run(s) of {'hidden': '800', 'dropout': '0.25'} for 'confirm-combo (early)')
- {'lr': '0.02'} (gap +1.3%) was verified from existing runs and rejected: did not pass verification
- {'lr': '0.05'} (gap +1.3%) was verified from existing runs and rejected: did not pass verification
- {'dropout': '0.25', 'lr': '0.02'} (gap +1.3%) was verified from existing runs and rejected: ['dropout'] dropped: each knob of {'dropout': '0.25', 'lr': '0.02'} alone gets most of the way, and {'lr': '0.02'} is within one noise band of the full set
- closest configuration not verified: {'dropout': '0.25', 'hidden': '800'} (gap -0.1%, 1 of 3 confirmation runs); the budget ran out first, so no attribution is made
- early code screen stopped: run budget of 150 reached (wanted 1 more run(s) of {'@ast:pygcn/train.py:17:default': 'True'} for 'patch screen (early)')
- the gap (+1.3%) is below the minimum detectable effect (±1.8% with 3 runs per configuration at 80% power): even a setting that closed it couldn't have been confirmed, so 'nothing explains it' can't be claimed either
- patch round: {'@ast:pygcn/train.py:19:default': 'True', 'hidden': '800', 'lr': '0.05'} fits every claim but did not pass verification

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_cora | Mean |gap| |
|---|---|---|---|
| `hidden=1600`, `weight_decay=1e-05` | 4 | -0.2% | 0.2% |
| `lr=0.05`, `hidden=800` | 4 | -0.2% | 0.2% |
| `weight_decay=1e-05`, `hidden=800` | 4 | -0.2% | 0.2% |
| `hidden=1600`, `weight_decay=5e-05` | 4 | +0.3% | 0.3% |
| `dropout=0.25`, `weight_decay=1e-05` | 4 | -0.3% | 0.3% |

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
- Cost: Nemotron billed $0.0000, sandbox reported $80.1496 (total $80.1496; this search; ledger extraction is included only if it shared the search's router)
