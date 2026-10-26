# Gap Report: planted L1-b4a-s8-2

Artifact `b4a` · generated 2026-10-26 17:41 · 141 branch runs (0 build/load setups) · sandbox $965.8740

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_book_auc (book_auc) | Fits but unsupported | +7.3% | +1.5% | ±1.1% | `@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_book_acc (`book_acc`): paper 0.573, measured 0.6124 (+6.9%, band ±1.1%)

## C_book_auc: book_auc (paper 0.598)
**Fits but unsupported** · gap +7.3% → +1.5% · 64 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0057`, `B0125`, `B0126` (3 run(s) of the same config)
- Config: `@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk` naive `0`, changed to `1`
- Command:

  Replay: fork checkpoint `ac13dc48-a859-4a2f-adcc-acdc56bf4780` and run
  ```
  @ast:src/data_loader.py:37:replace=False @ast:src/data_loader.py:39:replace=False @ast:src/main.py:20:default=True @ast:src/train.py:58:@mut.17.Call.red.sum=0 @ast:src/train.py:58:@mut.43.Call.red.sum=0 @ast:src/model.py:166:@mut.14.Call.red.sum=0 @ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=0 @ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=0 @ast:src/data_loader.py:54:@mut.20.ListComp.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKFtpIGZvciBpIGluIHRyYWluX2luZGljZXMgaWYgcmF0aW5nX25wW2ldWzBdIGluIHVzZXJfaGlzdG9yeV9kaWN0XSk=0 RUN_TAG=1fda200b8df2 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=1 TF_NUM_INTRAOP_THREADS=1 TF_NUM_INTEROP_THREADS=1; cd src; n=0; for r in 1 2 3 4 5; do python main.py --dataset book --dim 4 --n_hop 2 --kge_weight 0.01 --l2_weight 1e-7 --lr 0.2 --batch_size 1024 --n_epoch 10 --n_memory 32 --item_update_mode plus_transform > ../out/run$r.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; wait; cd ..; bash gf_harness/emit.sh
  ```
- Output: `book_auc` 0.586, 0.6124, 0.6069; gap after +1.5%; result checkpoint `8e4c4e34-3408-4e52-a444-87009ad8333e`
- Effect: candidate 0.6069 minus naive 0.6419 = -0.035, 95% bootstrap interval [-0.05916, -0.02565] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `book_auc` = 0.598.

### What did we measure?
- Naive median 0.6419 over 5 runs; repeats: 0.6424, 0.6348, 0.6503, 0.6401, 0.6419
- Spread: range 0.6348 to 0.6503, noise band ±0.006419 (2 x MAD), CV 0.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +7.3% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +7.3% (it comes back)
- PASS · Held-out claim: C_book_acc: +6.9% to +1.3% (not worse beyond noise)
- FAIL · Evidence: `lr=None`: no evidence mentions '0.2'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -0.035 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `dim=200`, `dim=400`, `n_hop=10`, `n_hop=20`, `n_hop=100`, `n_hop=200`, `n_epoch=100`, `n_epoch=500`, `n_epoch=1000`, `n_memory=160`, `n_memory=320`, `n_memory=1600`, `n_memory=3200`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n_memory=1` (4.22 noise units, gap +2.8%); `lr=0.2` (3.96 noise units, gap +3.1%); `lr=0.1` (3.55 noise units, gap +3.5%); `batch_size=102` (2.87 noise units, gap +4.3%); `n_memory=3` (2.31 noise units, gap +4.9%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=0.2`: this claim +1.3%, mean |gap| 1.3% (4 runs)
  - `n_memory=3`, `batch_size=102`: this claim +1.4%, mean |gap| 1.4% (3 runs)
  - `n_memory=1`, `n_epoch=50`: this claim +1.6%, mean |gap| 1.5% (3 runs)

### Equally good configurations
The target claim can't tell these 13 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=0.2` (reported)
- `n_memory=1`
- `n_memory=3`
- `n_memory=6`
- `batch_size=102, n_memory=3`
- `n_epoch=50, n_memory=1`
- `n_epoch=20, n_memory=1`
- `batch_size=102, n_epoch=50`
- `lr=0.1, n_memory=1`
- `lr=0.2, n_epoch=50`
- `lr=0.1, n_memory=3`
- `n_epoch=50, n_memory=3`
- `@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a code change: @ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1 | code | 44% | 0.2 sigma (fits every claim) | run with @ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1 (an in-memory code patch) |
| 2 | the setting batch_size=102, n_memory=3 | settings | 21% | 1.0 sigma (fits every claim) | run with batch_size=102, n_memory=3 |
| 3 | the setting n_epoch=50, n_memory=1 | settings | 11% | 1.2 sigma (fits every claim) | run with n_epoch=50, n_memory=1 |

### History matching (every measured configuration, all claims together)
- 12 of 72 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr`: lr=0.2 (max I 0.39)
  - `batch_size, n_memory`: batch_size=102, n_memory=3 (max I 1.18)
  - `@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk`: @ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1 (max I 1.23)
  - `n_epoch, n_memory`: n_epoch=50, n_memory=1 (max I 1.43); n_epoch=20, n_memory=1 (max I 1.85); n_epoch=50, n_memory=3 (max I 2.54)
  - `n_memory`: n_memory=1 (max I 1.58); n_memory=3 (max I 2.42)
  - `lr, n_memory`: lr=0.1, n_memory=3 (max I 2.29)
  - `batch_size, n_epoch`: batch_size=102, n_epoch=50 (max I 2.71)
- 5 separate islands (no single-knob move joins them): batch_size=102, n_memory=3; n_epoch=50, n_memory=1; n_memory=1 | lr=0.2 | @ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1 | batch_size=102, n_epoch=50
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:37`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:39`)
  - fixed seed: random seed fixed to 555 (`src/main.py:6`)
  - unexposed setting: `add_argument(..., default=True)`: a switch fixed in the call; no flag sets it (`src/main.py:20`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/preprocess.py:68`)
  - fixed seed: random seed fixed to 555 (`src/preprocess.py:119`)

Notes:
- configurations the target claim can't tell apart from the answer: lr=0.2; n_memory=1; n_memory=3; n_memory=6; batch_size=102, n_memory=3; n_epoch=50, n_memory=1; n_epoch=20, n_memory=1; batch_size=102, n_epoch=50; lr=0.1, n_memory=1; lr=0.2, n_epoch=50; lr=0.1, n_memory=3; n_epoch=50, n_memory=3
- patch round: {'@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk': '1'} also fits every claim (Fits but unsupported), but doesn't beat {'lr': '0.2'}
- patch round: {'@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk': '1'} fits every claim as well as the answer; the claims can't tell them apart
- mutation round: 1 equivalent code change(s) fit every claim (worst 0.2 sigma): src/data_loader.py:40: `list(left - set(test_indices))` -> `(lambda _v: _v[:max(1, len(_v) * 1 // 2)])(list(left - set(test_indices)))`
- explained with a code change (tested in memory, no file edited): src/data_loader.py:40: `list(left - set(test_indices))` -> `(lambda _v: _v[:max(1, len(_v) * 1 // 2)])(list(left - set(test_indices)))`; a code lead, not a confirmed cause
- not identifiable from the paper's numbers: 7 configuration(s) of other knobs fit every claim as well as the answer (@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1: batch_size=102, n_memory=3; lr=0.1, n_memory=3; lr=0.2; lr=0.2, n_epoch=50; n_epoch=20, n_memory=1; n_epoch=50, n_memory=1), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_book_auc | C_book_acc | Mean |gap| |
|---|---|---|---|---|
| `lr=0.2` | 4 | +1.3% | +1.3% | 1.3% |
| `@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKGxpc3QobGVmdCAtIHNldCh0ZXN0X2luZGljZXMpKSk=1` | 3 | +1.5% | +1.3% | 1.4% |
| `n_memory=3`, `batch_size=102` | 3 | +1.4% | +1.5% | 1.4% |
| `n_memory=1`, `n_epoch=50` | 3 | +1.6% | +1.5% | 1.5% |
| `n_memory=1`, `n_epoch=20` | 3 | +2.1% | +2.4% | 2.2% |

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
- Harness spec sha256: `f901be4c7959bb6e83feb9cc4e12d11ba5c4c696e5442944ccbc5ff8d7d7df51`
- Cost: Nemotron billed $0.0000, sandbox reported $965.8740 (total $965.8740; this search; ledger extraction is included only if it shared the search's router)
