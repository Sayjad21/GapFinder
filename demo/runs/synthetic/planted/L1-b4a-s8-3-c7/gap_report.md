# Gap Report: planted L1-b4a-s8-3

Artifact `b4a` · generated 2026-10-26 17:36 · 120 branch runs (0 build/load setups) · sandbox $729.9454

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_book_auc (book_auc) | Fits but unsupported | +74.9% | -0.1% | ±1.7% | `item_update_mode=replace` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: book_acc 0.433 > book_auc 0.367; measured: book_acc 0.6141 < book_auc 0.6419 (margin -0.0278, noise 0.00921)
- **Held-out claims outside noise:**
  - C_book_acc (`book_acc`): paper 0.433, measured 0.6141 (+41.8%, band ±1.5%)

## C_book_auc: book_auc (paper 0.367)
**Fits but unsupported** · gap +74.9% → -0.1% · 71 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0046`, `B0067`, `B0068`, `B0075` (4 run(s) of the same config)
- Config: `item_update_mode` naive `plus_transform`, changed to `replace`
- Command:

  Replay: fork checkpoint `ac13dc48-a859-4a2f-adcc-acdc56bf4780` and run
  ```
  @ast:src/data_loader.py:37:replace=False @ast:src/data_loader.py:39:replace=False @ast:src/main.py:20:default=True RUN_TAG=97cca7a3493e export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=1 TF_NUM_INTRAOP_THREADS=1 TF_NUM_INTEROP_THREADS=1; cd src; n=0; for r in 1 2 3 4 5; do python main.py --dataset book --dim 4 --n_hop 2 --kge_weight 0.01 --l2_weight 1e-7 --lr 0.02 --batch_size 1024 --n_epoch 10 --n_memory 32 --item_update_mode replace > ../out/run$r.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; wait; cd ..; bash gf_harness/emit.sh
  ```
- Output: `book_auc` 0.3657, 0.3663, 0.3666, 0.3669; gap after -0.1%; result checkpoint `219d680c-102d-4e65-884d-9ff3b46dc1b8`
- Effect: candidate 0.3664 minus naive 0.6419 = -0.2755, 95% bootstrap interval [-0.2771, -0.2701] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `book_auc` = 0.367.

### What did we measure?
- Naive median 0.6419 over 5 runs; repeats: 0.6442, 0.6421, 0.6419, 0.6378, 0.6361
- Spread: range 0.6361 to 0.6442, noise band ±0.006419 (2 x MAD), CV 0.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +74.9% (noise band ±1.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `item_update_mode` the gap is +74.9% (it comes back)
- PASS · Held-out claim: C_book_acc: +41.8% to -0.1% (not worse beyond noise)
- FAIL · Evidence: `item_update_mode=replace`: no evidence mentions 'replace'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -0.2755 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `dim=200`, `dim=400`, `n_hop=10`, `n_hop=20`, `n_hop=100`, `n_hop=200`, `n_epoch=100`, `n_epoch=500`, `n_epoch=1000`, `n_memory=160`, `n_memory=320`, `n_memory=1600`, `n_memory=3200`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `item_update_mode=replace_transform` (40.32 noise units, gap +4.4%); `lr=0.2` (4.72 noise units, gap +66.6%); `lr=0.1` (4.05 noise units, gap +67.8%); `n_memory=1` (3.86 noise units, gap +68.1%); `n_memory=3` (3.1 noise units, gap +69.5%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `item_update_mode=replace`, `@ast:src/data_loader.py:37:replace=True`: this claim -0.3%, mean |gap| 0.2% (3 runs)
  - `dim=2`, `item_update_mode=replace`: this claim +0.4%, mean |gap| 0.4% (4 runs)
  - `item_update_mode=replace_transform`, `dim=2`: this claim +2.6%, mean |gap| 1.7% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `item_update_mode=replace` (reported)
- `dim=2, item_update_mode=replace`
- `dim=2, item_update_mode=replace_transform`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting item_update_mode=replace | settings | 54% | 0.1 sigma (fits every claim) | run with item_update_mode=replace |
| 2 | a code change: @ast:src/data_loader.py:37:replace=True, item_update_mode=replace | code | 17% | 0.2 sigma (fits every claim) | run with @ast:src/data_loader.py:37:replace=True, item_update_mode=replace (an in-memory code patch) |
| 3 | the setting dim=2, item_update_mode=replace | settings | 17% | 0.3 sigma (fits every claim) | run with dim=2, item_update_mode=replace |

### History matching (every measured configuration, all claims together)
- 6 of 77 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `item_update_mode`: item_update_mode=replace (max I 0.12)
  - `@ast:src/data_loader.py:37:replace, item_update_mode`: @ast:src/data_loader.py:37:replace=True, item_update_mode=replace (max I 0.18)
  - `dim, item_update_mode`: dim=2, item_update_mode=replace (max I 0.33); dim=2, item_update_mode=replace_transform (max I 1.69)
  - `@ast:src/data_loader.py:39:replace, item_update_mode`: @ast:src/data_loader.py:39:replace=True, item_update_mode=replace (max I 1.02)
  - `item_update_mode, n_memory`: item_update_mode=replace, n_memory=1 (max I 2.85)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:37`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:39`)
  - fixed seed: random seed fixed to 555 (`src/main.py:6`)
  - unexposed setting: `add_argument(..., default=True)`: a switch fixed in the call; no flag sets it (`src/main.py:20`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/preprocess.py:68`)
  - fixed seed: random seed fixed to 555 (`src/preprocess.py:119`)

Notes:
- configurations the target claim can't tell apart from the answer: item_update_mode=replace; dim=2, item_update_mode=replace; dim=2, item_update_mode=replace_transform
- explained with a code patch (tested in memory, no file edited): src/data_loader.py line 37: replace = False -> True
- not identifiable from the paper's numbers: 1 configuration(s) of other knobs fit every claim as well as the answer (item_update_mode=replace: dim=2, item_update_mode=replace_transform), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_book_auc | C_book_acc | Mean |gap| |
|---|---|---|---|---|
| `item_update_mode=replace` | 4 | -0.1% | -0.1% | 0.1% |
| `item_update_mode=replace`, `@ast:src/data_loader.py:37:replace=True` | 3 | -0.3% | -0.2% | 0.2% |
| `dim=2`, `item_update_mode=replace` | 4 | +0.4% | -0.5% | 0.4% |
| `item_update_mode=replace_transform`, `dim=2` | 3 | +2.6% | -0.8% | 1.7% |
| `item_update_mode=replace_transform` | 4 | +4.4% | +0.0% | 2.2% |

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
- Cost: Nemotron billed $0.0000, sandbox reported $729.9454 (total $729.9454; this search; ledger extraction is included only if it shared the search's router)
