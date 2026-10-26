# Gap Report: planted L2-b4a-s3-1

Artifact `b4a` · generated 2026-10-22 02:52 · 150 branch runs (0 build/load setups) · sandbox $850.6341

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_book_auc (book_auc) | Fits but unsupported | -4.7% | -1.1% | ±1.0% | `n_epoch=2` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_book_acc (`book_acc`): paper 0.627, measured 0.6129 (-2.2%, band ±1.0%)

## C_book_auc: book_auc (paper 0.675)
**Fits but unsupported** · gap -4.7% → -1.1% · 73 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0039`, `B0052`, `B0053`, `B0075` (4 run(s) of the same config)
- Config: `n_epoch` naive `10`, changed to `2`
- Command:

  Replay: fork checkpoint `ac13dc48-a859-4a2f-adcc-acdc56bf4780` and run
  ```
  RUN_TAG=f787f9119cfb export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=1 TF_NUM_INTRAOP_THREADS=1 TF_NUM_INTEROP_THREADS=1; cd src; n=0; for r in 1 2 3 4 5; do python main.py --dataset book --dim 4 --n_hop 2 --kge_weight 0.01 --l2_weight 1e-7 --lr 0.02 --batch_size 1024 --n_epoch 2 --n_memory 32 --item_update_mode plus_transform > ../out/run$r.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; wait; cd ..; bash gf_harness/emit.sh
  ```
- Output: `book_auc` 0.6692, 0.6652, 0.6657, 0.6817; gap after -1.1%; result checkpoint `cb2bbb3e-1a2e-43b9-aa35-759f4984dd5e`
- Effect: candidate 0.6674 minus naive 0.6432 = +0.02425, 95% bootstrap interval [+0.02169, +0.04306] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `book_auc` = 0.675.

### What did we measure?
- Naive median 0.6432 over 5 runs; repeats: 0.6435, 0.6432, 0.6368, 0.6438, 0.6379
- Spread: range 0.6368 to 0.6438, noise band ±0.006432 (2 x MAD), CV 0.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -4.7% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n_epoch` the gap is -4.7% (it comes back)
- PASS · Held-out claim: C_book_acc: -2.2% to -1.1% (not worse beyond noise)
- FAIL · Evidence: `n_epoch=2`: no evidence mentions '2'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.02425 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `dim=200`, `dim=400`, `n_hop=10`, `n_hop=20`, `n_hop=100`, `n_hop=200`, `n_epoch=100`, `n_epoch=500`, `n_epoch=1000`, `n_memory=160`, `n_memory=320`, `n_memory=1600`, `n_memory=3200`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.004` (4.77 noise units, gap -0.2%); `lr=0.002` (4.06 noise units, gap -0.8%); `n_epoch=1` (3.5 noise units, gap +1.4%); `dim=20` (3.23 noise units, gap -1.6%); `dim=1` (3.05 noise units, gap -1.8%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `n_epoch=1`, `n_memory=64`: this claim +0.8%, mean |gap| 0.4% (3 runs)
  - `lr=0.004`, `batch_size=5120`: this claim +0.6%, mean |gap| 0.6% (3 runs)
  - `lr=0.004`: this claim -0.5%, mean |gap| 0.8% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting n_epoch=2 | settings | 38% | 0.4 sigma (fits every claim) | run with n_epoch=2 |
| 2 | the setting dim=20, lr=0.002 | settings | 11% | 0.7 sigma (fits every claim) | run with dim=20, lr=0.002 |
| 3 | the setting dim=20, n_epoch=2 | settings | 11% | 0.8 sigma (fits every claim) | run with dim=20, n_epoch=2 |

### History matching (every measured configuration, all claims together)
- 26 of 72 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, lr`: batch_size=5120, lr=0.004 (max I 0.27); batch_size=10240, lr=0.004 (max I 1.13)
  - `lr, n_memory`: lr=0.002, n_memory=64 (max I 0.47)
  - `n_epoch`: n_epoch=2 (max I 0.59); n_epoch=1 (max I 1.11)
  - `dim, lr`: dim=20, lr=0.002 (max I 0.9)
  - `lr, n_epoch`: lr=0.004, n_epoch=2 (max I 1.08)
  - `dim, n_epoch`: dim=20, n_epoch=2 (max I 1.11)
  - `lr`: lr=0.004 (max I 1.12)
  - `n_epoch, n_memory`: n_epoch=1, n_memory=64 (max I 1.2)
- 3 separate islands (no single-knob move joins them): batch_size=5120, lr=0.004; lr=0.002, n_memory=64; n_epoch=2 | n_hop=1 | l2_weight=1e-5, lr=1e-3, n_hop=3
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:37`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:39`)
  - fixed seed: random seed fixed to 555 (`src/main.py:6`)
  - unexposed setting: `add_argument(..., default=True)`: a switch fixed in the call; no flag sets it (`src/main.py:20`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/preprocess.py:68`)
  - fixed seed: random seed fixed to 555 (`src/preprocess.py:119`)

Notes:
- stopped early: run budget of 150 reached (wanted 1 more run(s) of {'lr': '0.002', 'batch_size': '5120'} for 'confirm-combo')
- verified from runs already made, after the budget ran out
- patch round stopped early: run budget of 150 reached (wanted 1 more run(s) of {'batch_size': '5120', 'lr': '0.004', '@ast:src/data_loader.py:37:replace': 'True'} for 'patch screen')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_book_auc | C_book_acc | Mean |gap| |
|---|---|---|---|---|
| `n_epoch=1`, `n_memory=64` | 3 | +0.8% | +0.1% | 0.4% |
| `lr=0.004`, `batch_size=5120` | 3 | +0.6% | +0.7% | 0.6% |
| `lr=0.004` | 4 | -0.5% | +1.1% | 0.8% |
| `n_epoch=1` | 4 | +1.2% | +0.5% | 0.8% |
| `n_epoch=2`, `dim=20` | 4 | +0.4% | +1.3% | 0.8% |

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
- Cost: Nemotron billed $0.0000, sandbox reported $850.6341 (total $850.6341; this search; ledger extraction is included only if it shared the search's router)
