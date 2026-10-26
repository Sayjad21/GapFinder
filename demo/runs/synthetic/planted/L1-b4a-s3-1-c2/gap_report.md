# Gap Report: planted L1-b4a-s3-1

Artifact `b4a` · generated 2026-10-22 04:26 · 115 branch runs (0 build/load setups) · sandbox $799.1747

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_book_auc (book_auc) | Fits but unsupported | +69.1% | +1.2% | ±1.7% | `item_update_mode=replace_transform` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: book_acc 0.431 > book_auc 0.381; measured: book_acc 0.6155 < book_auc 0.6441 (margin -0.0286, noise 0.00891)
- **Held-out claims outside noise:**
  - C_book_acc (`book_acc`): paper 0.431, measured 0.6155 (+42.8%, band ±1.4%)

## C_book_auc: book_auc (paper 0.381)
**Fits but unsupported** · gap +69.1% → +1.2% · 44 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0048`, `B0050`, `B0051`, `B0074` (4 run(s) of the same config)
- Config: `item_update_mode` naive `plus_transform`, changed to `replace_transform`
- Command:

  Replay: fork checkpoint `ac13dc48-a859-4a2f-adcc-acdc56bf4780` and run
  ```
  @ast:src/data_loader.py:37:replace=False @ast:src/data_loader.py:39:replace=False @ast:src/main.py:20:default=True RUN_TAG=8e11b972726d export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=1 TF_NUM_INTRAOP_THREADS=1 TF_NUM_INTEROP_THREADS=1; cd src; n=0; for r in 1 2 3 4 5; do python main.py --dataset book --dim 4 --n_hop 2 --kge_weight 0.01 --l2_weight 1e-7 --lr 0.02 --batch_size 1024 --n_epoch 10 --n_memory 32 --item_update_mode replace_transform > ../out/run$r.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; wait; cd ..; bash gf_harness/emit.sh
  ```
- Output: `book_auc` 0.3836, 0.3899, 0.3878, 0.3801; gap after +1.2%; result checkpoint `b38345ed-3a97-4d4b-af25-7f18f23bc5b5`
- Effect: candidate 0.3857 minus naive 0.6441 = -0.2584, 95% bootstrap interval [-0.2667, -0.2535] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `book_auc` = 0.381.

### What did we measure?
- Naive median 0.6441 over 5 runs; repeats: 0.6433, 0.6463, 0.6441, 0.6486, 0.6428
- Spread: range 0.6428 to 0.6486, noise band ±0.006441 (2 x MAD), CV 0.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +69.1% (noise band ±1.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `item_update_mode` the gap is +69.1% (it comes back)
- PASS · Held-out claim: C_book_acc: +42.8% to +1.2% (not worse beyond noise)
- FAIL · Evidence: `item_update_mode=replace_transform`: no evidence mentions 'replace_transform'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -0.2584 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `dim=200`, `dim=400`, `n_hop=10`, `n_hop=20`, `n_hop=100`, `n_hop=200`, `n_epoch=100`, `n_epoch=500`, `n_epoch=1000`, `n_memory=160`, `n_memory=320`, `n_memory=1600`, `n_memory=3200`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `item_update_mode=replace` (38.67 noise units, gap -3.7%); `lr=0.2` (8.52 noise units, gap +54.6%); `n_memory=3` (3.07 noise units, gap +63.9%); `l2_weight=1e-08` (2.9 noise units, gap +64.1%); `n_memory=1` (2.81 noise units, gap +64.3%) (and 8 more in the JSON)
- Near alternatives (closest across all claims):
  - `item_update_mode=replace_transform`, `@ast:src/data_loader.py:37:replace=True`: this claim +0.1%, mean |gap| 0.3% (3 runs)
  - `item_update_mode=replace`: this claim -3.7%, mean |gap| 2.1% (4 runs)
  - `lr=0.2`: this claim +54.2%, mean |gap| 43.1% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting item_update_mode=replace_transform | settings | 56% | 0.7 sigma (fits every claim) | run with item_update_mode=replace_transform |
| 2 | a code change: @ast:src/data_loader.py:37:replace=True, item_update_mode=replace_transform | code | 30% | 0.2 sigma (fits every claim) | run with @ast:src/data_loader.py:37:replace=True, item_update_mode=replace_transform (an in-memory code patch) |
| 3 | a code change: @ast:src/data_loader.py:39:replace=True, item_update_mode=replace_transform | code | 10% | 1.0 sigma (fits every claim) | run with @ast:src/data_loader.py:39:replace=True, item_update_mode=replace_transform (an in-memory code patch) |

### History matching (every measured configuration, all claims together)
- 4 of 50 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `@ast:src/data_loader.py:37:replace, item_update_mode`: @ast:src/data_loader.py:37:replace=True, item_update_mode=replace_transform (max I 0.29)
  - `item_update_mode`: item_update_mode=replace_transform (max I 0.93)
  - `@ast:src/data_loader.py:39:replace, item_update_mode`: @ast:src/data_loader.py:39:replace=True, item_update_mode=replace_transform (max I 1.19)
  - `@ast:src/main.py:20:default, item_update_mode`: @ast:src/main.py:20:default=False, item_update_mode=replace_transform (max I 2.13)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:37`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:39`)
  - fixed seed: random seed fixed to 555 (`src/main.py:6`)
  - unexposed setting: `add_argument(..., default=True)`: a switch fixed in the call; no flag sets it (`src/main.py:20`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/preprocess.py:68`)
  - fixed seed: random seed fixed to 555 (`src/preprocess.py:119`)

Notes:
- explained with a code patch (tested in memory, no file edited): src/data_loader.py line 37: replace = False -> True
- mutation round: no mutant fits every claim (src/model.py:133: `tf.expand_dims(self.t_emb_list[hop], axis=3)` -> `(tf.expand_dims(self.t_emb_list[hop], axis=3)) / 2`: worst 30.1 sigma; src/model.py:132: `tf.expand_dims(self.h_emb_list[hop], axis=2)` -> `(tf.expand_dims(self.h_emb_list[hop], axis=2)) / 2`: worst 31.9 sigma; src/model.py:112: `o` -> `(o) * 2`: worst 38.7 sigma)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_book_auc | C_book_acc | Mean |gap| |
|---|---|---|---|---|
| `item_update_mode=replace_transform`, `@ast:src/data_loader.py:37:replace=True` | 3 | +0.1% | -0.5% | 0.3% |
| `item_update_mode=replace_transform` | 4 | +1.2% | +1.2% | 1.2% |
| `item_update_mode=replace` | 4 | -3.7% | +0.5% | 2.1% |
| `lr=0.2` | 4 | +54.2% | +31.9% | 43.1% |
| `n_memory=1` | 4 | +61.4% | +36.9% | 49.1% |

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
- GapFinder commit: `ca4a5e297839f0c50559b58914404255594c81fb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3a37607286fa5f05585001e7626eb97d0e89adc6c94367209cf7245a737cfdf8`
- Cost: Nemotron billed $0.0000, sandbox reported $799.1747 (total $799.1747; this search; ledger extraction is included only if it shared the search's router)
