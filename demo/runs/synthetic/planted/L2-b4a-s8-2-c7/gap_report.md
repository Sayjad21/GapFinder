# Gap Report: planted L2-b4a-s8-2

Artifact `b4a` · generated 2026-10-27 02:25 · 148 branch runs (0 build/load setups) · sandbox $945.8432

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_book_auc (book_auc) | Fits but unsupported | -1.8% | +0.5% | ±1.0% | `n_epoch=5` |

## C_book_auc: book_auc (paper 0.659)
**Fits but unsupported** · gap -1.8% → +0.5% · 79 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0037`, `B0057`, `B0058`, `B0063` (4 run(s) of the same config)
- Config: `n_epoch` naive `10`, changed to `5`
- Command:

  Replay: fork checkpoint `ac13dc48-a859-4a2f-adcc-acdc56bf4780` and run
  ```
  RUN_TAG=85e05e8a3cf1 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=1 TF_NUM_INTRAOP_THREADS=1 TF_NUM_INTEROP_THREADS=1; cd src; n=0; for r in 1 2 3 4 5; do python main.py --dataset book --dim 4 --n_hop 2 --kge_weight 0.01 --l2_weight 1e-7 --lr 0.02 --batch_size 1024 --n_epoch 5 --n_memory 32 --item_update_mode plus_transform > ../out/run$r.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; wait; cd ..; bash gf_harness/emit.sh
  ```
- Output: `book_auc` 0.6608, 0.6678, 0.664, 0.6489; gap after +0.5%; result checkpoint `c16c1b61-8392-453b-aeef-694cb3d90eb7`
- Effect: candidate 0.6624 minus naive 0.647 = +0.0154, 95% bootstrap interval [+0.001, +0.02853] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `book_auc` = 0.659.

### What did we measure?
- Naive median 0.647 over 5 runs; repeats: 0.6488, 0.6443, 0.632, 0.6497, 0.647
- Spread: range 0.632 to 0.6497, noise band ±0.00647 (2 x MAD), CV 1.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -1.8% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n_epoch` the gap is -1.8% (it comes back)
- PASS · Held-out claim: C_book_auc@n_epoch=20 at n_epoch=10: n/a to +0.9% (not worse beyond noise)
- PASS · Held-out claim: C_book_auc@n_epoch=40 at n_epoch=20: n/a to -1.0% (not worse beyond noise)
- FAIL · Evidence: `n_epoch=5`: no evidence mentions '5'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.0154 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `dim=200`, `dim=400`, `n_hop=10`, `n_hop=20`, `n_hop=100`, `n_hop=200`, `n_epoch=100`, `n_epoch=500`, `n_epoch=1000`, `n_memory=160`, `n_memory=320`, `n_memory=1600`, `n_memory=3200`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n_epoch=1` (1.81 noise units, gap +0.0%); `batch_size=10240` (1.64 noise units, gap +0.2%); `n_hop=1` (1.47 noise units, gap +0.4%); `batch_size=5120` (1.05 noise units, gap -0.8%)
- Near alternatives (closest across all claims):
  - `dim=20`, `n_epoch=5`: this claim -0.3%, mean |gap| 0.3% (4 runs)
  - `n_hop=1`: this claim -0.7%, mean |gap| 0.4% (4 runs)
  - `n_hop=4`, `n_epoch=5`: this claim +0.4%, mean |gap| 0.4% (4 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n_epoch=5` (reported)
- `n_hop=1`
- `batch_size=10240`
- `n_epoch=5, n_hop=4`
- `dim=20, n_epoch=5`
- `lr=0.01, n_hop=4`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting n_epoch=5 | settings | 22% | 1.0 sigma (fits every claim) | run with n_epoch=5 |
| 2 | no difference in reporting: the numbers as printed at the end of the run | settings | 13% | 1.4 sigma (fits every claim) | the settings search and the other classes |
| 3 | the setting n_epoch=5, n_hop=4 | settings | 12% | 0.3 sigma (fits every claim) | run with n_epoch=5, n_hop=4 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n_epoch, n_hop`: n_epoch=5, n_hop=4 (max I 0.26)
  - `dim, n_epoch`: dim=20, n_epoch=5 (max I 0.37)
  - `lr`: lr=0.01 (max I 0.48)
  - `lr, n_hop`: lr=0.01, n_hop=4 (max I 0.49)
  - `kge_weight`: kge_weight=0.1 (max I 0.54)
  - `batch_size, n_hop`: batch_size=5120, n_hop=4 (max I 0.54)
  - `dim`: dim=20 (max I 0.55)
  - `dim, lr`: dim=1, lr=0.01 (max I 0.59)
  - `batch_size`: batch_size=5120 (max I 0.65)
  - `l2_weight`: l2_weight=5e-07 (max I 0.68)
- 2 separate islands (no single-knob move joins them): n_epoch=5, n_hop=4; dim=20, n_epoch=5; lr=0.01 | l2_weight=1e-5, lr=1e-3, n_hop=3
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:37`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:39`)
  - fixed seed: random seed fixed to 555 (`src/main.py:6`)
  - unexposed setting: `add_argument(..., default=True)`: a switch fixed in the call; no flag sets it (`src/main.py:20`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/preprocess.py:68`)
  - fixed seed: random seed fixed to 555 (`src/preprocess.py:119`)

Notes:
- configurations the target claim can't tell apart from the answer: n_epoch=5; n_hop=1; batch_size=10240; n_epoch=5, n_hop=4; dim=20, n_epoch=5; lr=0.01, n_hop=4
- discrimination: the paper's other conditions (C_book_auc@n_epoch=20, C_book_auc@n_epoch=40) don't yet tell the equally good fits apart: n_epoch=5 45%; n_hop=1 28%; batch_size=10240 18%
- scale probe: the code's n_epoch as 0.5 x the paper's fits every swept claim after 11 runs at g(v) (C_book_auc at n_epoch=5, C_book_auc@n_epoch=20 at n_epoch=10, C_book_auc@n_epoch=40 at n_epoch=20)
- scale probe: only 0 of the 3 swept claims were off as run, so the factor is at most an unsupported fit
- labelled Fits but unsupported: one factor (0.5 x the paper's) makes every one of the 3 swept claims fit
- patch round: {'@ast:src/main.py:20:default': 'False', 'n_epoch': '5', 'n_hop': '4'} fits every claim but did not pass verification
- mutation round: no room left in the run budget
- n_epoch: values from 4 to 6 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- not identifiable from the paper's numbers: 2 configuration(s) of other knobs fit every claim as well as the answer (n_epoch=5: lr=0.01, n_hop=4; n_hop=1), and the paper's other conditions (C_book_auc@n_epoch=20, C_book_auc@n_epoch=40) don't separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_book_auc | C_book_acc | Mean |gap| |
|---|---|---|---|---|
| `dim=20`, `n_epoch=5` | 4 | -0.3% | -0.3% | 0.3% |
| `n_hop=1` | 4 | -0.7% | -0.0% | 0.4% |
| `n_hop=4`, `n_epoch=5` | 4 | +0.4% | +0.4% | 0.4% |
| `n_hop=4`, `lr=0.01` | 4 | -0.7% | +0.2% | 0.5% |
| `n_epoch=5` | 4 | +0.5% | +0.5% | 0.5% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `dim=200`, `dim=400`, `n_hop=10`, `n_hop=20`, `n_hop=100`, `n_hop=200`, `n_epoch=100`, `n_epoch=500`, `n_epoch=1000`, `n_memory=160`, `n_memory=320`, `n_memory=1600`, `n_memory=3200`

## Knob names
- Code defaults read from the code instead of the ledger: `item_update_mode` 'plus_transform' at src/main.py:18 (ledger said plus_transform)

## Runtime trace (one dry run)
6 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `lr`: rate (optimizer.learning_rate (AdamOptimizer) at src/model.py:150)
- `n_epoch`: count (range() bound at src/train.py:18)
- `n_hop`: count (range() bound at src/data_loader.py:100)

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `b0a86388de10df975d6b49504363e8370f7c208830d460725975bdd7bfefe4de`
- Cost: Nemotron billed $0.0000, sandbox reported $945.8432 (total $945.8432; this search; ledger extraction is included only if it shared the search's router)
