# Gap Report: planted L1-vgae-s7-2

Artifact `vgae` · generated 2026-10-24 12:40 · 148 branch runs (0 build/load setups) · sandbox $1456.9130

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Fits but unsupported | +12.5% | +3.2% | ±1.1% | `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:76` `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_gae_citeseer_ap (`gae_citeseer_ap`): paper 82.14, as run 86.43, without it 87.95 (difference 95% CI [+0.247, +3.64])
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:79` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_gae_citeseer_ap (`gae_citeseer_ap`): paper 82.14, as run 86.43, without it 87.44 (difference 95% CI [+0.0464, +3.63])
- **How the code computes the reported number** (test-score selection, label-based edits, switches fixed for evaluation):
  - `gae/preprocessing.py:106`: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: gae_citeseer_ap 82.14 > gae_cora_ap 79.25; measured: gae_citeseer_ap 86.43 < gae_cora_ap 88.21 (margin -1.78, noise 1.36)
- **Held-out claims outside noise:**
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 78.93, measured 87.93 (+11.4%, band ±1.5%)
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 80.76, measured 87.25 (+8.0%, band ±1.1%)
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 83.15, measured 89.13 (+7.2%, band ±1.1%)
  - C_gae_cora_auc (`gae_cora_auc`): paper 76.15, measured 86.08 (+13.0%, band ±1.4%)
  - C_gae_cora_ap (`gae_cora_ap`): paper 79.25, measured 88.21 (+11.3%, band ±1.2%)
  - C_gae_citeseer_auc (`gae_citeseer_auc`): paper 79.83, measured 84.87 (+6.3%, band ±1.1%)
  - C_gae_citeseer_ap (`gae_citeseer_ap`): paper 82.14, measured 86.43 (+5.2%, band ±1.2%)

## C_vgae_cora_auc: vgae_cora_auc (paper 76.15)
**Fits but unsupported** · gap +12.5% → +3.2% · 51 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0060`, `B0140`, `B0141` (3 run(s) of the same config)
- Config: `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk` naive `0`, changed to `1`
- Command:

  Replay: fork checkpoint `b87946e7-74f5-4d81-bf4d-f55f3eafc206` and run
  ```
  @ast:gae/preprocessing.py:32:test_percent=30.0 @ast:gae/preprocessing.py:32:val_percent=20.0 @ast:gae/preprocessing.py:76:replace=True @ast:gae/preprocessing.py:40:@mut.11.Call.red.mean=0 @ast:gae/preprocessing.py:43:@mut.36.Compare.cmpflip=0 @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=0 @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=0 @ast:gae/preprocessing.py:74:@mut.10.Compare.cmpflip=0 @ast:gae/preprocessing.py:85:@mut.23.Compare.cmpflip=0 RUN_TAG=422c9ecf9a6f export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=2; mkdir -p out; A="--learning_rate 0.01 --epochs 2000 --hidden1 32 --hidden2 3 --weight_decay 0.0 --dropout 0.0 --features 1"; cd gae; for ds in cora citeseer; do PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_vae --dataset $ds $A > ../out/vgae_$ds.log 2>&1 & PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_ae --dataset $ds $A > ../out/gae_$ds.log 2>&1 & wait; done; cd ..; bash gf_harness/emit.sh
  ```
- Output: `vgae_cora_auc` 78.62, 79.85, 76.84; gap after +3.2%; result checkpoint `0260eb9e-dd95-46e0-ace7-6e46f59cff8a`
- Effect: candidate 78.62 minus naive 85.69 = -7.061, 95% bootstrap interval [-10.39, -5.681] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 76.15.

### What did we measure?
- Naive median 85.69 over 5 runs; repeats: 85.48, 88.19, 85.69, 87.14, 85.49
- Spread: range 85.48 to 88.19, noise band ±0.8569 (2 x MAD), CV 1.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +12.5% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is +6.3% (it comes back)
- PASS · Counterfactual (reversal test): without `hidden2` the gap is +2.3% (it comes back)
- PASS · Held-out claim: C_vgae_cora_ap: +11.4% to -0.0% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_auc: +8.0% to -2.8% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_ap: +7.2% to -2.9% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_auc: +13.0% to +2.3% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_ap: +11.3% to +1.4% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_auc: +6.3% to +1.5% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_ap: +5.2% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `epochs=None`: no evidence mentions '2000'; it fits, but nothing says the authors used it
- FAIL · Evidence: `hidden2=None`: no evidence mentions '3'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -7.061 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=2000` (11.1 noise units, gap -0.0%); `learning_rate=0.05` (10.6 noise units, gap +0.6%); `hidden2=2` (10.05 noise units, gap +1.2%); `epochs=20` (6.51 noise units, gap +5.2%); `hidden1=6` (6.38 noise units, gap -5.3%) (and 15 more in the JSON)
- Near alternatives (closest across all claims):
  - `hidden2=3`, `epochs=2000`: this claim +0.8%, mean |gap| 1.5% (4 runs)
  - `hidden2=2`: this claim +2.0%, mean |gap| 1.8% (4 runs)
  - `@ast:gae/preprocessing.py:32:test_percent=60`: this claim -2.4%, mean |gap| 1.9% (3 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=2000, hidden2=3` (reported)
- `epochs=2000`
- `hidden2=2`
- `hidden1=6`
- `hidden1=7`
- `hidden2=3`
- `epochs=20, hidden2=2`
- `epochs=2000, hidden2=2`
- `@ast:gae/preprocessing.py:32:test_percent=60`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a code change: @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 | code | 65% | 1.4 sigma (fits every claim) | run with @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 (an in-memory code patch) |
| 2 | the setting epochs=2000, hidden2=3 | settings | 30% | 1.7 sigma (fits every claim) | run with epochs=2000, hidden2=3 |
| 3 | the setting epochs=2000 | settings | 3% | 2.3 sigma (fits every claim) | run with epochs=2000 |

### History matching (every measured configuration, all claims together)
- 6 of 65 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `@ast:gae/preprocessing.py:32:test_percent`: @ast:gae/preprocessing.py:32:test_percent=60 (max I 1.25)
  - `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk`: @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 (max I 1.35)
  - `epochs, hidden2`: epochs=2000, hidden2=3 (max I 2.04)
  - `epochs`: epochs=2000 (max I 2.29)
  - `hidden2`: hidden2=2 (max I 2.82)
  - `@ast:gae/preprocessing.py:32:val_percent`: @ast:gae/preprocessing.py:32:val_percent=40 (max I 2.84)
- 5 separate islands (no single-knob move joins them): epochs=2000, hidden2=3; epochs=2000 | @ast:gae/preprocessing.py:32:test_percent=60 | @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 | hidden2=2
- Leads outside the settings (static code checks, nothing run; check these first):
  - eval switch: `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed (`gae/preprocessing.py:76`)
  - eval switch: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed (`gae/preprocessing.py:79`)
  - eval switch: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed (`gae/preprocessing.py:106`)
  - unexposed setting: `mask_test_edges(..., test_percent=30)`: a default no call in the repo overrides (1 call(s)) (`gae/preprocessing.py:32`)
  - unexposed setting: `mask_test_edges(..., val_percent=20)`: a default no call in the repo overrides (1 call(s)) (`gae/preprocessing.py:32`)
  - unexposed setting: `choice(..., replace=True)`: a switch fixed in the call; no flag sets it (`gae/preprocessing.py:76`)
  - unexposed setting: `in1d(..., assume_unique=True)`: a switch fixed in the call; no flag sets it (`gae/preprocessing.py:78`)
  - unexposed setting: `in1d(..., assume_unique=True)`: a switch fixed in the call; no flag sets it (`gae/preprocessing.py:79`)

Notes:
- configurations the target claim can't tell apart from the answer: epochs=2000, hidden2=3; epochs=2000; hidden2=2; hidden1=6; hidden1=7; hidden2=3; epochs=20, hidden2=2; epochs=2000, hidden2=2
- patch round: {'@ast:gae/preprocessing.py:32:test_percent': '60'} also fits every claim (Fits but unsupported), but doesn't beat {'epochs': '2000', 'hidden2': '3'}
- patch round: {'@ast:gae/preprocessing.py:32:test_percent': '60'} fits every claim as well as the answer; the claims can't tell them apart
- mutation round: 1 equivalent code change(s) fit every claim (worst 1.4 sigma): gae/preprocessing.py:57: `np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0)` -> `(lambda _v: _v[:max(1, len(_v) * 1 // 2)])(np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0))`
- explained with a code change (tested in memory, no file edited): gae/preprocessing.py:57: `np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0)` -> `(lambda _v: _v[:max(1, len(_v) * 1 // 2)])(np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0))`; a code lead, not a confirmed cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `hidden2=3`, `epochs=2000` | 4 | +0.8% | -0.0% | -2.8% | -2.9% | +2.3% | +1.4% | +1.5% | +0.0% | 1.5% |
| `hidden2=2` | 4 | +2.0% | +0.1% | -3.0% | -4.1% | +1.1% | -1.2% | -0.3% | -2.5% | 1.8% |
| `@ast:gae/preprocessing.py:32:test_percent=60` | 3 | -2.4% | -2.0% | +1.8% | +2.1% | +0.7% | +0.1% | +2.9% | +2.9% | 1.9% |
| `epochs=2000` | 4 | +2.3% | +4.4% | -3.1% | -0.7% | +0.3% | +2.7% | -2.5% | -0.3% | 2.1% |
| `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1` | 3 | +3.2% | +3.1% | +1.0% | +1.3% | +3.6% | +2.8% | +1.2% | +1.0% | 2.2% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at gae/train.py:142)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at gae/optimizer.py:37)

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `a4940396afa9ae1a64d6378c18ad65fd08cf221b7658e61e54ddedc4a7a46ef8`
- Cost: Nemotron billed $0.0000, sandbox reported $1456.9130 (total $1456.9130; this search; ledger extraction is included only if it shared the search's router)
