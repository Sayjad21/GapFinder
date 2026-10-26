# Gap Report: planted L1-b4a-s7-4

Artifact `b4a` · generated 2026-10-24 14:01 · 147 branch runs (0 build/load setups) · sandbox $1328.0105

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_book_auc (book_auc) | Fits but unsupported | -2.1% | -0.6% | ±1.3% | `lr=0.01` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_book_acc (`book_acc`): paper 0.627, measured 0.6133 (-2.2%, band ±1.0%)

## C_book_auc: book_auc (paper 0.657)
**Fits but unsupported** · gap -2.1% → -0.6% · 69 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0025`, `B0055`, `B0056`, `B0064` (4 run(s) of the same config)
- Config: `lr` naive `0.02`, changed to `0.01`
- Command:

  Replay: fork checkpoint `ac13dc48-a859-4a2f-adcc-acdc56bf4780` and run
  ```
  RUN_TAG=8c3a2c1cd671 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=1 TF_NUM_INTRAOP_THREADS=1 TF_NUM_INTEROP_THREADS=1; cd src; n=0; for r in 1 2 3 4 5; do python main.py --dataset book --dim 4 --n_hop 2 --kge_weight 0.01 --l2_weight 1e-7 --lr 0.01 --batch_size 1024 --n_epoch 10 --n_memory 32 --item_update_mode plus_transform > ../out/run$r.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; wait; cd ..; bash gf_harness/emit.sh
  ```
- Output: `book_auc` 0.6529, 0.6529, 0.6536, 0.6521; gap after -0.6%; result checkpoint `b1c7738c-a626-46e3-b815-0f4345d79f81`
- Effect: candidate 0.6529 minus naive 0.6434 = +0.0095, 95% bootstrap interval [+0.0026, +0.01284] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `book_auc` = 0.657.

### What did we measure?
- Naive median 0.6434 over 5 runs; repeats: 0.6485, 0.6418, 0.6434, 0.639, 0.6515
- Spread: range 0.639 to 0.6515, noise band ±0.0088 (2 x MAD), CV 0.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.1% (noise band ±1.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is -2.1% (it comes back)
- PASS · Held-out claim: C_book_auc@lr=0.01 at lr=0.005: n/a to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_book_auc@lr=0.04 at lr=0.02: n/a to -0.4% (not worse beyond noise)
- FAIL · Evidence: `lr=0.01`: no evidence mentions '0.01'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.0095 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `dim=200`, `dim=400`, `n_hop=10`, `n_hop=20`, `n_hop=100`, `n_hop=200`, `n_epoch=100`, `n_epoch=500`, `n_epoch=1000`, `n_memory=160`, `n_memory=320`, `n_memory=1600`, `n_memory=3200`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n_hop=1` (1.48 noise units, gap -0.1%); `batch_size=10240` (1.32 noise units, gap -0.3%); `lr=0.004` (1.18 noise units, gap -0.5%); `dim=20` (1.05 noise units, gap -0.7%); `n_epoch=5` (1 noise units, gap -0.7%)
- Near alternatives (closest across all claims):
  - `n_hop=1`, `dim=8`, `@ast:src/main.py:20:default=False`: this claim +0.0%, mean |gap| 0.2% (3 runs)
  - `batch_size=10240`: this claim -0.3%, mean |gap| 0.2% (4 runs)
  - `n_hop=1`, `dim=8`: this claim +0.1%, mean |gap| 0.2% (4 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=0.01` (reported)
- `n_hop=1`
- `dim=8, n_hop=1`
- `batch_size=10240, dim=8`
- `@ast:src/main.py:20:default=False, dim=8, n_hop=1`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the code's lr is 0.5 x the paper's (a unit or convention differs between paper and code) | code | 15% | 1.0 sigma (fits every claim) | find where lr enters the computation and compare its unit with the paper's |
| 2 | the setting dim=8, n_hop=1 | settings | 14% | 0.4 sigma (fits every claim) | run with dim=8, n_hop=1 |
| 3 | the setting batch_size=10240, dim=8 | settings | 13% | 0.5 sigma (fits every claim) | run with batch_size=10240, dim=8 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `dim, n_hop`: dim=8, n_hop=1 (max I 0.46)
  - `batch_size, dim`: batch_size=10240, dim=8 (max I 0.55)
  - `dim, lr`: dim=20, lr=0.01 (max I 0.71); dim=20, lr=0.004 (max I 0.73)
  - `dim, lr, n_hop`: dim=8, lr=0.01, n_hop=1 (max I 0.79); dim=8, lr=0.04, n_hop=1 (max I 0.83)
  - `@ast:src/data_loader.py:37:replace`: @ast:src/data_loader.py:37:replace=True (max I 0.86)
  - `batch_size`: batch_size=10240 (max I 0.9)
  - `@ast:src/main.py:20:default`: @ast:src/main.py:20:default=False (max I 0.98)
  - `dim`: dim=2 (max I 1)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:37`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:39`)
  - fixed seed: random seed fixed to 555 (`src/main.py:6`)
  - unexposed setting: `add_argument(..., default=True)`: a switch fixed in the call; no flag sets it (`src/main.py:20`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/preprocess.py:68`)
  - fixed seed: random seed fixed to 555 (`src/preprocess.py:119`)
- Equally good values: `lr` in {0.004, 0.01}

Notes:
- configurations the target claim can't tell apart from the answer: lr=0.01; n_hop=1; dim=8, n_hop=1; batch_size=10240, dim=8
- equally good values within one noise band (measured): lr in {0.004, 0.01}
- discrimination: the paper's other conditions (C_book_auc@lr=0.01, C_book_auc@lr=0.04) don't yet tell the equally good fits apart: n_hop=1 49%; lr=0.01 28%; batch_size=10240, dim=8 23%
- scale probe: the code's lr as 0.5 x the paper's fits every swept claim after 11 runs at g(v) (C_book_auc at lr=0.01, C_book_auc@lr=0.01 at lr=0.005, C_book_auc@lr=0.04 at lr=0.02)
- scale probe: only 1 of the 3 swept claims were off as run, so the factor is at most an unsupported fit
- labelled Fits but unsupported: one factor (0.5 x the paper's) makes every one of the 3 swept claims fit
- patch round: {'@ast:src/main.py:20:default': 'False', 'dim': '8', 'n_hop': '1'} also fits every claim (Fits but unsupported), but doesn't beat {'lr': '0.01'}
- patch round: {'@ast:src/main.py:20:default': 'False', 'dim': '8', 'n_hop': '1'} fits every claim as well as the answer; the claims can't tell them apart
- mutation round: no room left in the run budget
- lr: values from 0.01 to 0.01 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- not identifiable from the paper's numbers: 4 configuration(s) of other knobs fit every claim as well as the answer (lr=0.01: @ast:src/main.py:20:default=False, dim=8, n_hop=1; batch_size=10240, dim=8; dim=8, n_hop=1; n_hop=1), and the paper's other conditions (C_book_auc@lr=0.01, C_book_auc@lr=0.04) don't separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_book_auc | C_book_acc | Mean |gap| |
|---|---|---|---|---|
| `n_hop=1`, `dim=8`, `@ast:src/main.py:20:default=False` | 3 | +0.0% | -0.4% | 0.2% |
| `batch_size=10240` | 4 | -0.3% | +0.2% | 0.2% |
| `n_hop=1`, `dim=8` | 4 | +0.1% | -0.4% | 0.2% |
| `n_hop=1` | 4 | -0.2% | -0.3% | 0.2% |
| `dim=8`, `batch_size=10240` | 4 | +0.0% | +0.6% | 0.3% |

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
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `b0a86388de10df975d6b49504363e8370f7c208830d460725975bdd7bfefe4de`
- Cost: Nemotron billed $0.0000, sandbox reported $1328.0105 (total $1328.0105; this search; ledger extraction is included only if it shared the search's router)
