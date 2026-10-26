# Gap Report: planted L2-b4a-s2-1

Artifact `b4a` · generated 2026-10-22 00:40 · 144 branch runs (0 build/load setups) · sandbox $346.7099

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_book_auc (book_auc) | Fits but unsupported | -2.4% | +0.2% | ±1.0% | `n_epoch=5` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_book_acc (`book_acc`): paper 0.626, measured 0.6143 (-1.9%, band ±1.0%)

## C_book_auc: book_auc (paper 0.66)
**Fits but unsupported** · gap -2.4% → +0.2% · 68 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0037`, `B0063`, `B0062`, `B0065` (4 run(s) of the same config)
- Config: `n_epoch` naive `10`, changed to `5`
- Command:

  Replay: fork checkpoint `ac13dc48-a859-4a2f-adcc-acdc56bf4780` and run
  ```
  RUN_TAG=9b274c975974 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=1 TF_NUM_INTRAOP_THREADS=1 TF_NUM_INTEROP_THREADS=1; cd src; n=0; for r in 1 2 3 4 5; do python main.py --dataset book --dim 4 --n_hop 2 --kge_weight 0.01 --l2_weight 1e-7 --lr 0.02 --batch_size 1024 --n_epoch 5 --n_memory 32 --item_update_mode plus_transform > ../out/run$r.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; wait; cd ..; bash gf_harness/emit.sh
  ```
- Output: `book_auc` 0.6512, 0.6668, 0.66, 0.6623; gap after +0.2%; result checkpoint `80a2c763-52ec-4d00-9d86-809f5581a9fe`
- Effect: candidate 0.6612 minus naive 0.644 = +0.01715, 95% bootstrap interval [+0.01559, +0.02966] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `book_auc` = 0.66.

### What did we measure?
- Naive median 0.644 over 5 runs; repeats: 0.6309, 0.6457, 0.6379, 0.644, 0.6465
- Spread: range 0.6309 to 0.6465, noise band ±0.00644 (2 x MAD), CV 1.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.4% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n_epoch` the gap is -2.4% (it comes back)
- PASS · Held-out claim: C_book_acc: -1.9% to -0.0% (not worse beyond noise)
- FAIL · Evidence: `n_epoch=5`: no evidence mentions '5'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.01715 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `dim=200`, `dim=400`, `n_hop=10`, `n_hop=20`, `n_hop=100`, `n_hop=200`, `n_epoch=100`, `n_epoch=500`, `n_epoch=1000`, `n_memory=160`, `n_memory=320`, `n_memory=1600`, `n_memory=3200`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `batch_size=10240` (1.83 noise units, gap +0.6%); `lr=0.004` (1.43 noise units, gap +1.0%)
- Near alternatives (closest across all claims):
  - `batch_size=512`, `lr=0.004`: this claim +0.0%, mean |gap| 0.1% (4 runs)
  - `dim=20`, `lr=0.004`: this claim -0.1%, mean |gap| 0.3% (4 runs)
  - `dim=20`, `lr=0.01`: this claim +0.1%, mean |gap| 0.6% (3 runs)

### Equally good configurations
The target claim can't tell these 10 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n_epoch=5` (reported)
- `batch_size=10240`
- `lr=0.004`
- `dim=20, lr=0.004`
- `dim=20, lr=0.01`
- `dim=8, lr=0.004`
- `dim=20, n_epoch=5`
- `batch_size=512, lr=0.004`
- `dim=8, lr=0.01`
- `batch_size=512, n_epoch=5`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting n_epoch=5 | settings | 35% | 0.2 sigma (fits every claim) | run with n_epoch=5 |
| 2 | the setting dim=20, lr=0.004 | settings | 11% | 0.3 sigma (fits every claim) | run with dim=20, lr=0.004 |
| 3 | the setting dim=8, lr=0.004 | settings | 10% | 0.4 sigma (fits every claim) | run with dim=8, lr=0.004 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, lr`: batch_size=512, lr=0.004 (max I 0.12)
  - `n_epoch`: n_epoch=5 (max I 0.22)
  - `dim, lr`: dim=20, lr=0.004 (max I 0.3); dim=8, lr=0.004 (max I 0.46); dim=8, lr=0.01 (max I 0.78)
  - `batch_size, kge_weight`: batch_size=5120, kge_weight=0.05 (max I 0.81); batch_size=10240, kge_weight=0.05 (max I 0.87)
  - `batch_size, n_epoch`: batch_size=512, n_epoch=5 (max I 0.86)
  - `lr`: lr=0.004 (max I 0.9)
  - `kge_weight, lr`: kge_weight=0.05, lr=0.004 (max I 0.92)
- 2 separate islands (no single-knob move joins them): batch_size=512, lr=0.004; n_epoch=5; dim=20, lr=0.004 | l2_weight=1e-5, lr=1e-3, n_hop=3
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:37`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:39`)
  - fixed seed: random seed fixed to 555 (`src/main.py:6`)
  - unexposed setting: `add_argument(..., default=True)`: a switch fixed in the call; no flag sets it (`src/main.py:20`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/preprocess.py:68`)
  - fixed seed: random seed fixed to 555 (`src/preprocess.py:119`)

Notes:
- configurations the target claim can't tell apart from the answer: n_epoch=5; batch_size=10240; lr=0.004; dim=20, lr=0.004; dim=20, lr=0.01; dim=8, lr=0.004; dim=20, n_epoch=5; batch_size=512, lr=0.004; dim=8, lr=0.01; batch_size=512, n_epoch=5
- patch round: {'@ast:src/data_loader.py:37:replace': 'True', 'batch_size': '512', 'lr': '0.004'} also fits every claim (Fits but unsupported), but doesn't beat {'n_epoch': '5'}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_book_auc | C_book_acc | Mean |gap| |
|---|---|---|---|---|
| `batch_size=512`, `lr=0.004` | 4 | +0.0% | +0.1% | 0.1% |
| `n_epoch=5` | 4 | +0.2% | -0.0% | 0.1% |
| `dim=20`, `lr=0.004` | 4 | -0.1% | -0.6% | 0.3% |
| `dim=20`, `lr=0.01` | 3 | +0.1% | -1.0% | 0.6% |
| `kge_weight=0.05`, `batch_size=10240` | 4 | -1.2% | -0.1% | 0.7% |

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
- GapFinder commit: `1c8f0f8b4a997137c12c0ee6716ab6adeed88fc3`
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `b0a86388de10df975d6b49504363e8370f7c208830d460725975bdd7bfefe4de`
- Cost: Nemotron billed $0.0000, sandbox reported $346.7099 (total $346.7099; this search; ledger extraction is included only if it shared the search's router)
