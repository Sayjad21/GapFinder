# Gap Report: planted L1-b4a-s4-1

Artifact `b4a` · generated 2026-10-22 16:41 · 114 branch runs (0 build/load setups) · sandbox $118.3160

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_book_auc (book_auc) | Fits but unsupported | -95.8% | -0.3% | ±0.1% | `@ast:src/train.py:58:@mut.17.Call.red.sum=1` |

## C_book_auc: book_auc (paper 15.426)
**Fits but unsupported** · gap -95.8% → -0.3% · 60 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0054`, `B0023`, `B0024` (3 run(s) of the same config)
- Config: `@ast:src/train.py:58:@mut.17.Call.red.sum` naive `0`, changed to `1`
- Command:

  Replay: fork checkpoint `ac13dc48-a859-4a2f-adcc-acdc56bf4780` and run
  ```
  @ast:src/data_loader.py:37:replace=False @ast:src/data_loader.py:39:replace=False @ast:src/main.py:20:default=True @ast:src/train.py:58:@mut.17.Call.red.sum=1 @ast:src/train.py:58:@mut.43.Call.red.sum=0 @ast:src/model.py:166:@mut.14.Call.red.sum=0 @ast:src/model.py:165:@mut.28.Compare.cmpflip=0 @ast:src/train.py:23:@mut.26.Call.xdiv2=0 @ast:src/train.py:23:@mut.26.Call.xmul2=0 RUN_TAG=b3f346556e5f export PYTHONPATH="${WORK:-$PWD}/.gf_patch${PYTHONPATH:+${GF_PATHSEP:-:}$PYTHONPATH}"; cd /work; mkdir -p out; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=1 TF_NUM_INTRAOP_THREADS=1 TF_NUM_INTEROP_THREADS=1; cd src; n=0; for r in 1 2 3 4 5; do python main.py --dataset book --dim 4 --n_hop 2 --kge_weight 0.01 --l2_weight 1e-7 --lr 0.02 --batch_size 1024 --n_epoch 10 --n_memory 32 --item_update_mode plus_transform > ../out/run$r.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; wait; cd ..; bash gf_harness/emit.sh
  ```
- Output: `book_auc` 15.38, 15.53, 15.35; gap after -0.3%; result checkpoint `41ec5343-14bc-4b4d-8b51-95565ecd2874`
- Effect: candidate 15.38 minus naive 0.6484 = +14.73, 95% bootstrap interval [+14.7, +14.89] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `book_auc` = 15.426.

### What did we measure?
- Naive median 0.6484 over 5 runs; repeats: 0.6529, 0.6501, 0.6484, 0.637, 0.6427
- Spread: range 0.637 to 0.6529, noise band ±0.009 (2 x MAD), CV 1.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -95.8% (noise band ±0.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `@ast:src/train.py:58:@mut.17.Call.red.sum` the gap is -95.8% (it comes back)
- PASS · Held-out claim: C_book_acc: +0.8% to -0.1% (not worse beyond noise)
- FAIL · Evidence: `@ast:src/train.py:58:@mut.17.Call.red.sum=1`: no assumption record for this knob, so no evidence
- PASS · Effect vs noise: candidate minus naive is +14.73 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `dim=200`, `dim=400`, `n_hop=10`, `n_hop=20`, `n_hop=100`, `n_hop=200`, `n_epoch=100`, `n_epoch=500`, `n_epoch=1000`, `n_memory=160`, `n_memory=320`, `n_memory=1600`, `n_memory=3200`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n_epoch=2` (4.47 noise units, gap -95.5%); `lr=0.002` (3.86 noise units, gap -95.6%); `lr=0.004` (2.35 noise units, gap -95.7%)
- Near alternatives (closest across all claims):
  - `lr=0.002`, `dim=1`: this claim -95.7%, mean |gap| 47.9% (3 runs)
  - `n_epoch=5`: this claim -95.8%, mean |gap| 48.0% (3 runs)
  - `n_epoch=1`: this claim -95.7%, mean |gap| 48.5% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a code change: @ast:src/train.py:58:@mut.17.Call.red.sum=1 | code | 100% | 0.1 sigma (fits every claim) | run with @ast:src/train.py:58:@mut.17.Call.red.sum=1 (an in-memory code patch) |
| 2 | a cause outside every class tested | outside | 0% |  | look for code, data or evaluation differences the classes don't cover |
| 3 | no difference in reporting: the numbers as printed at the end of the run | settings | 0% | 64.6 sigma | the settings search and the other classes |

### History matching (every measured configuration, all claims together)
- 1 of 74 tested configurations fit every claim within 3 sigma
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:37`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:39`)
  - fixed seed: random seed fixed to 555 (`src/main.py:6`)
  - unexposed setting: `add_argument(..., default=True)`: a switch fixed in the call; no flag sets it (`src/main.py:20`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/preprocess.py:68`)
  - fixed seed: random seed fixed to 555 (`src/preprocess.py:119`)

Notes:
- {'lr': '0.002'} closes this claim but makes held-out claims worse; rejected
- dim dropped: with repeats, {'lr': '0.002', 'dim': '1'} fits {'lr': '0.002'}'s gap by less than one noise band, so it is not needed
- closest configuration tried: {'lr': '0.002'} (gap -95.6%); it did not pass verification
- history matching: 1 of 74 tested configurations fit every claim within 3 sigma
- explained with a code patch (tested in memory, no file edited): src/train.py line 58: @mut.17.Call.red.sum = 0 -> 1

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_book_auc | C_book_acc | Mean |gap| |
|---|---|---|---|---|
| `@ast:src/train.py:58:@mut.17.Call.red.sum=1` | 3 | -0.3% | -0.1% | 0.2% |
| `lr=0.002`, `dim=1` | 3 | -95.7% | +0.2% | 47.9% |
| `n_epoch=5` | 3 | -95.8% | +0.1% | 48.0% |
| naive (reproduction as run) | 5 | -95.8% | +0.8% | 48.3% |
| `n_epoch=1` | 4 | -95.7% | -1.2% | 48.5% |

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
- Harness spec sha256: `3a4093a8d019b352cba3ee0655169290de3f427cc1db0b0667a1cef1c73adccc`
- Cost: Nemotron billed $0.0000, sandbox reported $118.3160 (total $118.3160; this search; ledger extraction is included only if it shared the search's router)
