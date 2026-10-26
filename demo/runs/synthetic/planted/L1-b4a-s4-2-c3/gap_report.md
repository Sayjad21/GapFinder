# Gap Report: planted L1-b4a-s4-2

Artifact `b4a` · generated 2026-10-22 16:30 · 131 branch runs (0 build/load setups) · sandbox $198.8014

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_book_auc (book_auc) | Fits but unsupported | +68.8% | +1.2% | ±1.7% | `item_update_mode=replace_transform` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: book_acc 0.433 > book_auc 0.381; measured: book_acc 0.615 < book_auc 0.6431 (margin -0.0281, noise 0.0089)
- **Held-out claims outside noise:**
  - C_book_acc (`book_acc`): paper 0.433, measured 0.615 (+42.0%, band ±1.4%)

## C_book_auc: book_auc (paper 0.381)
**Fits but unsupported** · gap +68.8% → +1.2% · 66 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0048`, `B0051`, `B0052`, `B0075` (4 run(s) of the same config)
- Config: `item_update_mode` naive `plus_transform`, changed to `replace_transform`
- Command:

  Replay: fork checkpoint `ac13dc48-a859-4a2f-adcc-acdc56bf4780` and run
  ```
  RUN_TAG=41aaf3caeeeb export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=1 TF_NUM_INTRAOP_THREADS=1 TF_NUM_INTEROP_THREADS=1; cd src; n=0; for r in 1 2 3 4 5; do python main.py --dataset book --dim 4 --n_hop 2 --kge_weight 0.01 --l2_weight 1e-7 --lr 0.02 --batch_size 1024 --n_epoch 10 --n_memory 32 --item_update_mode replace_transform > ../out/run$r.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; wait; cd ..; bash gf_harness/emit.sh
  ```
- Output: `book_auc` 0.3854, 0.3788, 0.3855, 0.3888; gap after +1.2%; result checkpoint `4e8690eb-9652-4cae-8a7c-9e0ce9eb351d`
- Effect: candidate 0.3855 minus naive 0.6431 = -0.2576, 95% bootstrap interval [-0.2673, -0.2502] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `book_auc` = 0.381.

### What did we measure?
- Naive median 0.6431 over 5 runs; repeats: 0.635, 0.6503, 0.6414, 0.6431, 0.6443
- Spread: range 0.635 to 0.6503, noise band ±0.006431 (2 x MAD), CV 0.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +68.8% (noise band ±1.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `item_update_mode` the gap is +68.8% (it comes back)
- PASS · Held-out claim: C_book_acc: +42.0% to +0.4% (not worse beyond noise)
- FAIL · Evidence: `item_update_mode=replace_transform`: no evidence mentions 'replace_transform'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -0.2576 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `dim=200`, `dim=400`, `n_hop=10`, `n_hop=20`, `n_hop=100`, `n_hop=200`, `n_epoch=100`, `n_epoch=500`, `n_epoch=1000`, `n_memory=160`, `n_memory=320`, `n_memory=1600`, `n_memory=3200`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `item_update_mode=replace` (38.57 noise units, gap -3.7%); `lr=0.2` (6.81 noise units, gap +57.3%); `n_memory=1` (4.24 noise units, gap +61.6%); `batch_size=102` (4.09 noise units, gap +61.9%); `lr=0.1` (3.15 noise units, gap +63.5%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `dim=1`, `item_update_mode=replace`: this claim -1.2%, mean |gap| 0.7% (4 runs)
  - `item_update_mode=replace_transform`, `dim=1`: this claim -1.2%, mean |gap| 0.7% (4 runs)
  - `item_update_mode=replace_transform`, `dim=2`: this claim -1.1%, mean |gap| 0.7% (4 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `item_update_mode=replace_transform` (reported)
- `item_update_mode=replace, n_memory=1`
- `dim=2, item_update_mode=replace_transform`
- `dim=1, item_update_mode=replace_transform`
- `dim=1, item_update_mode=replace`
- `@ast:src/data_loader.py:37:replace=True, dim=2, item_update_mode=replace_transform`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting item_update_mode=replace_transform | settings | 39% | 0.5 sigma (fits every claim) | run with item_update_mode=replace_transform |
| 2 | the setting dim=2, item_update_mode=replace_transform | settings | 14% | 0.4 sigma (fits every claim) | run with dim=2, item_update_mode=replace_transform |
| 3 | the setting dim=1, item_update_mode=replace_transform | settings | 13% | 0.6 sigma (fits every claim) | run with dim=1, item_update_mode=replace_transform |

### History matching (every measured configuration, all claims together)
- 8 of 69 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `dim, item_update_mode`: dim=2, item_update_mode=replace_transform (max I 0.42); dim=1, item_update_mode=replace_transform (max I 0.62); dim=1, item_update_mode=replace (max I 0.65); dim=2, item_update_mode=replace (max I 1.78)
  - `item_update_mode`: item_update_mode=replace_transform (max I 0.5); item_update_mode=replace (max I 1.94)
  - `item_update_mode, n_memory`: item_update_mode=replace, n_memory=1 (max I 0.86); item_update_mode=replace_transform, n_memory=1 (max I 2.73)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:37`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:39`)
  - fixed seed: random seed fixed to 555 (`src/main.py:6`)
  - unexposed setting: `add_argument(..., default=True)`: a switch fixed in the call; no flag sets it (`src/main.py:20`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/preprocess.py:68`)
  - fixed seed: random seed fixed to 555 (`src/preprocess.py:119`)

Notes:
- configurations the target claim can't tell apart from the answer: item_update_mode=replace_transform; item_update_mode=replace, n_memory=1; dim=2, item_update_mode=replace_transform; dim=1, item_update_mode=replace_transform; dim=1, item_update_mode=replace
- patch round: {'@ast:src/data_loader.py:37:replace': 'True', 'dim': '2', 'item_update_mode': 'replace_transform'} also fits every claim (Fits but unsupported), but doesn't beat {'item_update_mode': 'replace_transform'}
- patch round: {'@ast:src/data_loader.py:37:replace': 'True', 'dim': '2', 'item_update_mode': 'replace_transform'} fits every claim as well as the answer; the claims can't tell them apart
- not identifiable from the paper's numbers: 6 configurations of different knobs fit every claim as well as the answer (@ast:src/data_loader.py:37:replace=True, dim=2, item_update_mode=replace_transform; dim=1, item_update_mode=replace; dim=1, item_update_mode=replace_transform; dim=2, item_update_mode=replace_transform; item_update_mode=replace, n_memory=1; item_update_mode=replace_transform), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_book_auc | C_book_acc | Mean |gap| |
|---|---|---|---|---|
| `dim=1`, `item_update_mode=replace` | 4 | -1.2% | -0.1% | 0.7% |
| `item_update_mode=replace_transform`, `dim=1` | 4 | -1.2% | -0.1% | 0.7% |
| `item_update_mode=replace_transform`, `dim=2` | 4 | -1.1% | -0.4% | 0.7% |
| `item_update_mode=replace_transform` | 4 | +1.2% | +0.4% | 0.8% |
| `item_update_mode=replace`, `n_memory=1` | 4 | +0.7% | -1.4% | 1.0% |

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
- GapFinder commit: `96f43d9d872690442737d0ad342eeb7d86352416` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `b0a86388de10df975d6b49504363e8370f7c208830d460725975bdd7bfefe4de`
- Cost: Nemotron billed $0.0000, sandbox reported $198.8014 (total $198.8014; this search; ledger extraction is included only if it shared the search's router)
