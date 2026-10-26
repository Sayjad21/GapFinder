# Gap Report: planted L1-b4a-s7-3

Artifact `b4a` · generated 2026-10-24 09:20 · 146 branch runs (0 build/load setups) · sandbox $770.5928

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_book_auc (book_auc) | Fits but unsupported | +6.4% | +1.2% | ±1.1% | `@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_book_acc (`book_acc`): paper 0.577, measured 0.614 (+6.4%, band ±1.6%)

## C_book_auc: book_auc (paper 0.603)
**Fits but unsupported** · gap +6.4% → +1.2% · 68 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0057`, `B0142`, `B0143` (3 run(s) of the same config)
- Config: `@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk` naive `0`, changed to `1`
- Command:

  Replay: fork checkpoint `ac13dc48-a859-4a2f-adcc-acdc56bf4780` and run
  ```
  @ast:src/data_loader.py:37:replace=False @ast:src/data_loader.py:39:replace=False @ast:src/main.py:20:default=True @ast:src/train.py:58:@mut.17.Call.red.sum=0 @ast:src/train.py:58:@mut.43.Call.red.sum=0 @ast:src/model.py:166:@mut.14.Call.red.sum=0 @ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=0 @ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=0 @ast:src/data_loader.py:54:@mut.20.ListComp.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKFtpIGZvciBpIGluIHRyYWluX2luZGljZXMgaWYgcmF0aW5nX25wW2ldWzBdIGluIHVzZXJfaGlzdG9yeV9kaWN0XSk=0 RUN_TAG=e4c466a339d4 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=1 TF_NUM_INTRAOP_THREADS=1 TF_NUM_INTEROP_THREADS=1; cd src; n=0; for r in 1 2 3 4 5; do python main.py --dataset book --dim 4 --n_hop 2 --kge_weight 0.01 --l2_weight 1e-7 --lr 0.02 --batch_size 1024 --n_epoch 10 --n_memory 1 --item_update_mode plus_transform > ../out/run$r.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; wait; cd ..; bash gf_harness/emit.sh
  ```
- Output: `book_auc` 0.6072, 0.6223, 0.61; gap after +1.2%; result checkpoint `8d96e047-0d67-4a7b-aca3-7c53ae0b3b01`
- Effect: candidate 0.61 minus naive 0.6418 = -0.0318, 95% bootstrap interval [-0.03996, -0.01866] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `book_auc` = 0.603.

### What did we measure?
- Naive median 0.6418 over 5 runs; repeats: 0.6453, 0.6504, 0.6393, 0.6392, 0.6418
- Spread: range 0.6392 to 0.6504, noise band ±0.006418 (2 x MAD), CV 0.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +6.4% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n_memory` the gap is +6.4% (it comes back)
- PASS · Held-out claim: C_book_acc: +6.4% to +1.8% (not worse beyond noise)
- FAIL · Evidence: `n_memory=None`: no evidence mentions '1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -0.0318 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `dim=200`, `dim=400`, `n_hop=10`, `n_hop=20`, `n_hop=100`, `n_hop=200`, `n_epoch=100`, `n_epoch=500`, `n_epoch=1000`, `n_memory=160`, `n_memory=320`, `n_memory=1600`, `n_memory=3200`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n_memory=1` (4.19 noise units, gap +2.0%); `batch_size=102` (3.55 noise units, gap +2.7%); `n_memory=6` (2.94 noise units, gap +3.3%); `n_memory=3` (2.21 noise units, gap +4.1%); `lr=0.1` (2.17 noise units, gap +4.1%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `n_memory=6`, `batch_size=102`: this claim -0.0%, mean |gap| 0.4% (4 runs)
  - `batch_size=205`, `item_update_mode=plus`: this claim -0.4%, mean |gap| 0.4% (4 runs)
  - `lr=0.1`, `n_memory=1`: this claim -1.2%, mean |gap| 0.6% (3 runs)

### Equally good configurations
The target claim can't tell these 16 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n_memory=1` (reported)
- `batch_size=102`
- `item_update_mode=plus, n_memory=6`
- `item_update_mode=plus, n_memory=1`
- `batch_size=205, item_update_mode=plus`
- `batch_size=102, n_memory=6`
- `item_update_mode=plus, lr=0.1`
- `lr=0.1, n_memory=6`
- `batch_size=102, lr=0.04`
- `batch_size=205, n_memory=6`
- `lr=0.04, n_memory=1`
- `lr=0.1, n_memory=1`
- `dim=2, n_memory=1`
- `lr=0.04, n_memory=6`
- `batch_size=205, lr=0.04`
- `@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a code change: @ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1 | code | 23% | 0.9 sigma (fits every claim) | run with @ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1 (an in-memory code patch) |
| 2 | the setting batch_size=102, n_memory=6 | settings | 21% | 0.3 sigma (fits every claim) | run with batch_size=102, n_memory=6 |
| 3 | the setting batch_size=205, item_update_mode=plus | settings | 21% | 0.4 sigma (fits every claim) | run with batch_size=205, item_update_mode=plus |

### History matching (every measured configuration, all claims together)
- 21 of 76 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, n_memory`: batch_size=102, n_memory=6 (max I 0.36); batch_size=205, n_memory=6 (max I 1.28)
  - `@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk`: @ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1 (max I 0.47)
  - `batch_size, item_update_mode`: batch_size=205, item_update_mode=plus (max I 0.47)
  - `lr, n_memory`: lr=0.1, n_memory=1 (max I 0.54); lr=0.1, n_memory=6 (max I 1.1); lr=0.04, n_memory=1 (max I 1.67); lr=0.04, n_memory=6 (max I 1.73)
  - `item_update_mode, lr`: item_update_mode=plus, lr=0.1 (max I 0.93)
  - `n_memory`: n_memory=1 (max I 1.38)
- 4 separate islands (no single-knob move joins them): batch_size=102, n_memory=6; batch_size=205, item_update_mode=plus; lr=0.1, n_memory=1 | @ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1 | item_update_mode=plus, lr=0.1 | @ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:37`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:39`)
  - fixed seed: random seed fixed to 555 (`src/main.py:6`)
  - unexposed setting: `add_argument(..., default=True)`: a switch fixed in the call; no flag sets it (`src/main.py:20`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/preprocess.py:68`)
  - fixed seed: random seed fixed to 555 (`src/preprocess.py:119`)

Notes:
- configurations the target claim can't tell apart from the answer: n_memory=1; batch_size=102; item_update_mode=plus, n_memory=6; item_update_mode=plus, n_memory=1; batch_size=205, item_update_mode=plus; batch_size=102, n_memory=6; item_update_mode=plus, lr=0.1; lr=0.1, n_memory=6; batch_size=102, lr=0.04; batch_size=205, n_memory=6; lr=0.04, n_memory=1; lr=0.1, n_memory=1; dim=2, n_memory=1; lr=0.04, n_memory=6; batch_size=205, lr=0.04
- patch round: {'@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk': '1'} also fits every claim (Fits but unsupported), but doesn't beat {'n_memory': '1'}
- patch round: {'@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk': '1'} fits every claim as well as the answer; the claims can't tell them apart
- mutation round: 1 equivalent code change(s) fit every claim (worst 0.9 sigma): src/data_loader.py:40: `list(left - set(test_indices))` -> `(lambda _v: _v[:max(1, len(_v) * 1 // 2)])(list(left - set(test_indices)))`
- explained with a code change (tested in memory, no file edited): src/data_loader.py:40: `list(left - set(test_indices))` -> `(lambda _v: _v[:max(1, len(_v) * 1 // 2)])(list(left - set(test_indices)))`; a code lead, not a confirmed cause
- not identifiable from the paper's numbers: 12 configuration(s) of other knobs fit every claim as well as the answer (@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1: batch_size=102, lr=0.04; batch_size=102, n_memory=6; batch_size=205, item_update_mode=plus; batch_size=205, n_memory=6; item_update_mode=plus, lr=0.1; item_update_mode=plus, n_memory=1), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_book_auc | C_book_acc | Mean |gap| |
|---|---|---|---|---|
| `n_memory=6`, `batch_size=102` | 4 | -0.0% | +0.7% | 0.4% |
| `batch_size=205`, `item_update_mode=plus` | 4 | -0.4% | -0.5% | 0.4% |
| `lr=0.1`, `n_memory=1` | 3 | -1.2% | +0.1% | 0.6% |
| `lr=0.1`, `item_update_mode=plus` | 3 | -1.1% | +0.5% | 0.8% |
| `lr=0.1`, `n_memory=6` | 4 | -1.5% | -0.5% | 1.0% |

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
- Harness spec sha256: `09593a622eba95b8b8c865658ff1c8c1fee4128ae7907257c96f6a46161d7b3d`
- Cost: Nemotron billed $0.0000, sandbox reported $770.5928 (total $770.5928; this search; ledger extraction is included only if it shared the search's router)
