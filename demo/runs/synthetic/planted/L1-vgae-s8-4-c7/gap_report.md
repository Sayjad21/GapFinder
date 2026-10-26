# Gap Report: planted L1-vgae-s8-4

Artifact `vgae` · generated 2026-10-26 22:52 · 135 branch runs (0 build/load setups) · sandbox $1083.0928

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Fits but unsupported | +7.8% | -2.5% | ±2.5% | `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- Tested: switching this code off moved no claim beyond noise: `gae/preprocessing.py:76` `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_cora_auc (`vgae_cora_auc`): paper 79.62, as run 85.83, without it 86.48 (difference 95% CI [-0.351, +1.66])
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 82.19, as run 87.9, without it 88.45 (difference 95% CI [-0.515, +1.36])
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 84.39, as run 87.95, without it 87.94 (difference 95% CI [-0.253, +1.7])
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 86.61, as run 89.86, without it 89.97 (difference 95% CI [-0.246, +1.41])
  - C_gae_cora_auc (`gae_cora_auc`): paper 79.8, as run 86.61, without it 86.39 (difference 95% CI [-2, +0.198])
  - C_gae_cora_ap (`gae_cora_ap`): paper 82.93, as run 88.55, without it 88.33 (difference 95% CI [-1.6, +0.103])
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:79` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_gae_cora_auc (`gae_cora_auc`): paper 79.8, as run 86.61, without it 85.74 (difference 95% CI [-2.78, -0.457])
  - C_gae_cora_ap (`gae_cora_ap`): paper 82.93, as run 88.55, without it 88.15 (difference 95% CI [-2.42, -0.079])
- Tested: switching this code off moved no claim beyond noise: `gae/preprocessing.py:106` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_cora_auc (`vgae_cora_auc`): paper 79.62, as run 85.83, without it 86.31 (difference 95% CI [-0.901, +1.43])
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 82.19, as run 87.9, without it 88.12 (difference 95% CI [-0.721, +1.02])
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 84.39, as run 87.95, without it 87.26 (difference 95% CI [-1.41, +1.17])
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 86.61, as run 89.86, without it 89.24 (difference 95% CI [-1.11, +0.812])
  - C_gae_cora_auc (`gae_cora_auc`): paper 79.8, as run 86.61, without it 85.95 (difference 95% CI [-1.72, +0.0379])
  - C_gae_cora_ap (`gae_cora_ap`): paper 82.93, as run 88.55, without it 88.24 (difference 95% CI [-1.06, +0.0506])
- **Held-out claims outside noise:**
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 82.19, measured 87.9 (+7.0%, band ±1.4%)
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 84.39, measured 87.95 (+4.2%, band ±1.3%)
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 86.61, measured 89.86 (+3.8%, band ±1.4%)
  - C_gae_cora_auc (`gae_cora_auc`): paper 79.8, measured 86.61 (+8.5%, band ±1.9%)
  - C_gae_cora_ap (`gae_cora_ap`): paper 82.93, measured 88.55 (+6.8%, band ±1.2%)
  - C_gae_citeseer_auc (`gae_citeseer_auc`): paper 81.7, measured 86.71 (+6.1%, band ±1.3%)
  - C_gae_citeseer_ap (`gae_citeseer_ap`): paper 82.85, measured 87.98 (+6.2%, band ±1.7%)

## C_vgae_cora_auc: vgae_cora_auc (paper 79.62)
**Fits but unsupported** · gap +7.8% → -2.5% · 48 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0060`, `B0124`, `B0125` (3 run(s) of the same config)
- Config: `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk` naive `0`, changed to `1`
- Command:

  Replay: fork checkpoint `b87946e7-74f5-4d81-bf4d-f55f3eafc206` and run
  ```
  @ast:gae/preprocessing.py:32:test_percent=30.0 @ast:gae/preprocessing.py:32:val_percent=40 @ast:gae/preprocessing.py:76:replace=True @ast:gae/preprocessing.py:40:@mut.11.Call.red.mean=0 @ast:gae/preprocessing.py:43:@mut.36.Compare.cmpflip=0 @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=0 @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=0 @ast:gae/preprocessing.py:74:@mut.10.Compare.cmpflip=0 @ast:gae/preprocessing.py:85:@mut.23.Compare.cmpflip=0 RUN_TAG=7fe9656e8f17 export PYTHONPATH="${WORK:-$PWD}/.gf_patch${PYTHONPATH:+${GF_PATHSEP:-:}$PYTHONPATH}"; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=2; mkdir -p out; A="--learning_rate 0.01 --epochs 200 --hidden1 32 --hidden2 16 --weight_decay 0.0 --dropout 0.0 --features 1"; cd gae; for ds in cora citeseer; do PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_vae --dataset $ds $A > ../out/vgae_$ds.log 2>&1 & PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_ae --dataset $ds $A > ../out/gae_$ds.log 2>&1 & wait; done; cd ..; bash gf_harness/emit.sh
  ```
- Output: `vgae_cora_auc` 77.61, 75.7, 78.19; gap after -2.5%; result checkpoint `1baeced8-6888-41dd-9675-ff3d14ec78d3`
- Effect: candidate 77.61 minus naive 85.83 = -8.216, 95% bootstrap interval [-10.94, -6.777] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 79.62.

### What did we measure?
- Naive median 85.83 over 5 runs; repeats: 87.19, 86.84, 84.35, 84.99, 85.83
- Spread: range 84.35 to 87.19, noise band ±2.028 (2 x MAD), CV 1.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +7.8% (noise band ±2.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `@ast:gae/preprocessing.py:32:val_percent` the gap is +7.8% (it comes back)
- PASS · Held-out claim: C_vgae_cora_ap: +7.0% to +1.3% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_auc: +4.2% to +0.2% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_ap: +3.8% to +0.1% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_auc: +8.5% to +0.9% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_ap: +6.8% to +0.4% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_auc: +6.1% to +0.6% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_ap: +6.2% to +1.4% (not worse beyond noise)
- FAIL · Evidence: `@ast:gae/preprocessing.py:32:val_percent=None`: no assumption record for this knob, so no evidence
- PASS · Effect vs noise: candidate minus naive is -8.216 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=1500` (2.97 noise units, gap +0.2%); `hidden2=3` (2.89 noise units, gap +0.4%); `hidden1=6` (2.58 noise units, gap +1.2%); `epochs=1000` (2.29 noise units, gap +2.0%); `hidden1=3200` (2.29 noise units, gap +1.9%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `@ast:gae/preprocessing.py:32:val_percent=40`: this claim +0.9%, mean |gap| 0.7% (3 runs)
  - `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1`: this claim +2.8%, mean |gap| 1.6% (3 runs)
  - `hidden2=3`: this claim +0.8%, mean |gap| 1.8% (4 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `hidden2=3` (reported)
- `epochs=20`
- `hidden1=3200, hidden2=3`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a code change: @ast:gae/preprocessing.py:32:val_percent=40 | code | 92% | 0.9 sigma (fits every claim) | run with @ast:gae/preprocessing.py:32:val_percent=40 (an in-memory code patch) |
| 2 | a code change: @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 | code | 7% | 1.4 sigma (fits every claim) | run with @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 (an in-memory code patch) |
| 3 | a code change: @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 | code | 1% | 1.8 sigma (fits every claim) | run with @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 (an in-memory code patch) |

### History matching (every measured configuration, all claims together)
- 8 of 62 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `@ast:gae/preprocessing.py:32:val_percent`: @ast:gae/preprocessing.py:32:val_percent=40 (max I 0.95)
  - `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk`: @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 (max I 1.21)
  - `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk`: @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 (max I 1.76)
  - `hidden2`: hidden2=3 (max I 2.46)
  - `hidden1`: hidden1=3200 (max I 2.8)
  - `@ast:gae/preprocessing.py:32:test_percent`: @ast:gae/preprocessing.py:32:test_percent=60 (max I 2.8)
  - `epochs`: epochs=1000 (max I 2.9)
  - `hidden1, hidden2`: hidden1=3200, hidden2=3 (max I 2.96)
- 6 separate islands (no single-knob move joins them): hidden2=3; hidden1=3200; hidden1=3200, hidden2=3 | @ast:gae/preprocessing.py:32:val_percent=40 | @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 | @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1
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
- configurations the target claim can't tell apart from the answer: hidden2=3; epochs=20; hidden1=3200, hidden2=3
- explained with a code patch (tested in memory, no file edited): gae/preprocessing.py line 32: val_percent = 20.0 -> 40
- mutation round: 1 equivalent code change(s) fit every claim (worst 1.4 sigma): gae/preprocessing.py:57: `np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0)` -> `(lambda _v: _v[:max(1, len(_v) * 1 // 2)])(np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0))`
- explained with a code change (tested in memory, no file edited): gae/preprocessing.py:57: `np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0)` -> `(lambda _v: _v[:max(1, len(_v) * 1 // 2)])(np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0))`; a code lead, not a confirmed cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `@ast:gae/preprocessing.py:32:val_percent=40` | 3 | +0.9% | +1.3% | +0.2% | +0.1% | +0.9% | +0.4% | +0.6% | +1.4% | 0.7% |
| `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1` | 3 | -2.5% | -1.7% | -2.7% | -2.3% | -0.3% | -0.2% | +0.6% | +0.0% | 1.3% |
| `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1` | 3 | +2.8% | +3.1% | +0.2% | -0.1% | +1.3% | +1.5% | +1.1% | +2.9% | 1.6% |
| `hidden2=3` | 4 | +0.8% | -0.6% | -2.2% | -3.9% | +1.2% | -1.0% | +2.8% | +1.8% | 1.8% |
| `hidden2=3`, `hidden1=3200` | 3 | +1.3% | -0.4% | -2.9% | -4.9% | +1.6% | -0.5% | -1.5% | -1.3% | 1.8% |

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
- Cost: Nemotron billed $0.0000, sandbox reported $1083.0928 (total $1083.0928; this search; ledger extraction is included only if it shared the search's router)
