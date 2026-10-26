# Gap Report: planted L1-vgae-s8-2

Artifact `vgae` · generated 2026-10-26 20:21 · 130 branch runs (0 build/load setups) · sandbox $711.3502

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Fits but unsupported | +13.3% | +2.6% | ±1.1% | `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:76` `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 78.66, as run 87.91, without it 88.01 (difference 95% CI [+0.0012, +0.621])
- Tested: switching this code off moved no claim beyond noise: `gae/preprocessing.py:79` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_cora_auc (`vgae_cora_auc`): paper 75.8, as run 85.88, without it 86.65 (difference 95% CI [-0.742, +1.6])
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 78.66, as run 87.91, without it 88.44 (difference 95% CI [-0.553, +1.08])
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 80.93, as run 87.44, without it 87.14 (difference 95% CI [-1.4, +0.385])
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 83.7, as run 89.18, without it 88.8 (difference 95% CI [-1.73, +0.339])
  - C_gae_cora_auc (`gae_cora_auc`): paper 76.28, as run 85.95, without it 85.75 (difference 95% CI [-1.08, +0.308])
  - C_gae_cora_ap (`gae_cora_ap`): paper 79.68, as run 88.48, without it 88.02 (difference 95% CI [-0.938, +0.558])
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:106` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_gae_citeseer_auc (`gae_citeseer_auc`): paper 82.98, as run 85.01, without it 87.55 (difference 95% CI [+1.45, +3.83])
  - C_gae_citeseer_ap (`gae_citeseer_ap`): paper 84.93, as run 86.19, without it 89.1 (difference 95% CI [+1.08, +4.03])
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: gae_citeseer_auc 82.98 > vgae_citeseer_auc 80.93; measured: gae_citeseer_auc 85.01 < vgae_citeseer_auc 87.44 (margin -2.44, noise 1.22)
  - paper: gae_citeseer_ap 84.93 > vgae_citeseer_ap 83.7; measured: gae_citeseer_ap 86.19 < vgae_citeseer_ap 89.18 (margin -2.99, noise 1.63)
  - paper: gae_citeseer_ap 84.93 > gae_cora_ap 79.68; measured: gae_citeseer_ap 86.19 < gae_cora_ap 88.48 (margin -2.29, noise 1.94)
- **Held-out claims outside noise:**
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 78.66, measured 87.91 (+11.8%, band ±1.1%)
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 80.93, measured 87.44 (+8.0%, band ±1.1%)
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 83.7, measured 89.18 (+6.6%, band ±1.1%)
  - C_gae_cora_auc (`gae_cora_auc`): paper 76.28, measured 85.95 (+12.7%, band ±1.7%)
  - C_gae_cora_ap (`gae_cora_ap`): paper 79.68, measured 88.48 (+11.0%, band ±1.7%)
  - C_gae_citeseer_auc (`gae_citeseer_auc`): paper 82.98, measured 85.01 (+2.4%, band ±1.0%)

## C_vgae_cora_auc: vgae_cora_auc (paper 75.8)
**Fits but unsupported** · gap +13.3% → +2.6% · 46 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0062`, `B0119`, `B0120` (3 run(s) of the same config)
- Config: `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk` naive `0`, changed to `1`
- Command:

  Replay: fork checkpoint `b87946e7-74f5-4d81-bf4d-f55f3eafc206` and run
  ```
  @ast:gae/preprocessing.py:32:test_percent=60 @ast:gae/preprocessing.py:32:val_percent=20.0 @ast:gae/preprocessing.py:76:replace=True @ast:gae/preprocessing.py:40:@mut.11.Call.red.mean=0 @ast:gae/preprocessing.py:43:@mut.36.Compare.cmpflip=0 @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=0 @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=0 @ast:gae/preprocessing.py:74:@mut.10.Compare.cmpflip=0 @ast:gae/preprocessing.py:85:@mut.23.Compare.cmpflip=0 RUN_TAG=31b7ffdd0088 export PYTHONPATH="${WORK:-$PWD}/.gf_patch${PYTHONPATH:+${GF_PATHSEP:-:}$PYTHONPATH}"; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=2; mkdir -p out; A="--learning_rate 0.01 --epochs 200 --hidden1 32 --hidden2 16 --weight_decay 0.0 --dropout 0.0 --features 1"; cd gae; for ds in cora citeseer; do PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_vae --dataset $ds $A > ../out/vgae_$ds.log 2>&1 & PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_ae --dataset $ds $A > ../out/gae_$ds.log 2>&1 & wait; done; cd ..; bash gf_harness/emit.sh
  ```
- Output: `vgae_cora_auc` 77.24, 80.34, 77.73; gap after +2.6%; result checkpoint `6b486cc4-1810-4c78-b08e-8874a718c78b`
- Effect: candidate 77.73 minus naive 85.88 = -8.145, 95% bootstrap interval [-8.85, -4.813] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 75.8.

### What did we measure?
- Naive median 85.88 over 5 runs; repeats: 84.62, 85.88, 86.3, 85.98, 85.11
- Spread: range 84.62 to 86.3, noise band ±0.8588 (2 x MAD), CV 0.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +13.3% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `@ast:gae/preprocessing.py:32:test_percent` the gap is +13.3% (it comes back)
- PASS · Held-out claim: C_vgae_cora_ap: +11.8% to -1.8% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_auc: +8.0% to +1.7% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_ap: +6.6% to +1.5% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_auc: +12.7% to +1.0% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_ap: +11.0% to +0.7% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_auc: +2.4% to -1.8% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_ap: +1.5% to -2.1% (not worse beyond noise)
- FAIL · Evidence: `@ast:gae/preprocessing.py:32:test_percent=None`: no assumption record for this knob, so no evidence
- PASS · Effect vs noise: candidate minus naive is -8.145 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `hidden2=2` (11.51 noise units, gap +0.3%); `epochs=10` (10.55 noise units, gap -1.3%); `learning_rate=0.06` (10.1 noise units, gap -1.8%); `epochs=2000` (9.47 noise units, gap +2.6%); `learning_rate=0.1` (9.07 noise units, gap -3.0%) (and 16 more in the JSON)
- Near alternatives (closest across all claims):
  - `@ast:gae/preprocessing.py:32:test_percent=60`: this claim -2.3%, mean |gap| 1.6% (3 runs)
  - `hidden2=2`: this claim +0.0%, mean |gap| 2.4% (4 runs)
  - `epochs=2000`: this claim +2.5%, mean |gap| 3.0% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a code change: @ast:gae/preprocessing.py:32:test_percent=60 | code | 78% | 1.4 sigma (fits every claim) | run with @ast:gae/preprocessing.py:32:test_percent=60 (an in-memory code patch) |
| 2 | a code change: @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 | code | 21% | 1.4 sigma (fits every claim) | run with @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 (an in-memory code patch) |
| 3 | the setting hidden2=2 | settings | 0% | 2.6 sigma (fits every claim) | run with hidden2=2 |

### History matching (every measured configuration, all claims together)
- 3 of 60 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `@ast:gae/preprocessing.py:32:test_percent`: @ast:gae/preprocessing.py:32:test_percent=60 (max I 1.49)
  - `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk`: @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 (max I 1.76)
  - `hidden2`: hidden2=2 (max I 2.78)
- 3 separate islands (no single-knob move joins them): @ast:gae/preprocessing.py:32:test_percent=60 | @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 | hidden2=2
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
- {'hidden2': '2'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'hidden2': '2'} (gap +0.0%); it did not pass verification
- history matching: 3 of 60 tested configurations fit every claim within 3 sigma
- explained with a code patch (tested in memory, no file edited): gae/preprocessing.py line 32: test_percent = 30.0 -> 60
- mutation round: 1 equivalent code change(s) fit every claim (worst 1.4 sigma): gae/preprocessing.py:57: `np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0)` -> `(lambda _v: _v[:max(1, len(_v) * 1 // 2)])(np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0))`
- explained with a code change (tested in memory, no file edited): gae/preprocessing.py:57: `np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0)` -> `(lambda _v: _v[:max(1, len(_v) * 1 // 2)])(np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0))`; a code lead, not a confirmed cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1` | 3 | +2.6% | +2.7% | +0.2% | +0.2% | +0.9% | +0.6% | -0.9% | -1.3% | 1.2% |
| `@ast:gae/preprocessing.py:32:test_percent=60` | 3 | -2.3% | -1.8% | +1.7% | +1.5% | +1.0% | +0.7% | -1.8% | -2.1% | 1.6% |
| `hidden2=2` | 4 | +0.0% | -1.6% | -1.7% | -3.7% | +2.1% | -1.5% | -3.3% | -5.2% | 2.4% |
| `epochs=2000` | 4 | +2.5% | +4.9% | -2.4% | -0.7% | +0.3% | +2.9% | -6.2% | -3.7% | 3.0% |
| `epochs=1000` | 3 | +9.0% | +8.7% | -2.6% | -1.0% | -0.4% | +1.3% | -5.1% | -1.7% | 3.7% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at gae/train.py:142)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at gae/optimizer.py:37)

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `41556bc7eda9f2817206b268674a8bc520c20341ff90d2115cde92982a821c4d`
- Cost: Nemotron billed $0.0000, sandbox reported $711.3502 (total $711.3502; this search; ledger extraction is included only if it shared the search's router)
