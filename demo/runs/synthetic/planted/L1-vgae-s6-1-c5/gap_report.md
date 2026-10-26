# Gap Report: planted L1-vgae-s6-1

Artifact `vgae` · generated 2026-10-23 21:06 · 150 branch runs (0 build/load setups) · sandbox $1182.9183

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Fits but unsupported | +7.7% | -2.9% | ±1.4% | `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:76` `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 82.06, as run 87.28, without it 86.32 (difference 95% CI [-1.38, -0.491])
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 84.65, as run 89.21, without it 88.69 (difference 95% CI [-0.995, -0.243])
- Tested: switching this code off moved no claim beyond noise: `gae/preprocessing.py:79` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_cora_auc (`vgae_cora_auc`): paper 79.22, as run 85.32, without it 86.66 (difference 95% CI [-0.336, +1.6])
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 81.93, as run 87.57, without it 88.72 (difference 95% CI [-0.386, +1.41])
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 82.06, as run 87.28, without it 87.87 (difference 95% CI [-0.0498, +1.94])
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 84.65, as run 89.21, without it 89.87 (difference 95% CI [-0.0858, +1.84])
  - C_gae_cora_auc (`gae_cora_auc`): paper 80.01, as run 86.74, without it 86 (difference 95% CI [-1.04, +0.697])
  - C_gae_cora_ap (`gae_cora_ap`): paper 83.05, as run 89.3, without it 88.35 (difference 95% CI [-1.19, +0.597])
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:106` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_gae_cora_ap (`gae_cora_ap`): paper 83.05, as run 89.3, without it 87.9 (difference 95% CI [-1.67, -0.249])
- **Held-out claims outside noise:**
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 81.93, measured 87.57 (+6.9%, band ±1.1%)
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 82.06, measured 87.28 (+6.4%, band ±1.1%)
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 84.65, measured 89.21 (+5.4%, band ±1.1%)
  - C_gae_cora_auc (`gae_cora_auc`): paper 80.01, measured 86.74 (+8.4%, band ±1.1%)
  - C_gae_cora_ap (`gae_cora_ap`): paper 83.05, measured 89.3 (+7.5%, band ±1.1%)

## C_vgae_cora_auc: vgae_cora_auc (paper 79.22)
**Fits but unsupported** · gap +7.7% → -2.9% · 52 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0134`, `B0139`, `B0140` (3 run(s) of the same config)
- Config: `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk` naive `0`, changed to `1`
- Command: not recorded
- Output: `vgae_cora_auc` 78.69, 76.94, 75.67; gap after -2.9%
- Effect: candidate 76.94 minus naive 85.32 = -8.375, 95% bootstrap interval [-10.47, -6.443] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 79.22.

### What did we measure?
- Naive median 85.32 over 5 runs; repeats: 85.32, 85.13, 86.68, 86.23, 84.77
- Spread: range 84.77 to 86.68, noise band ±1.106 (2 x MAD), CV 0.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +7.7% (noise band ±1.4% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -8.375 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `learning_rate=0.05` (5.32 noise units, gap +0.3%); `epochs=1500` (5.08 noise units, gap +0.6%); `hidden2=3` (4.86 noise units, gap +0.9%); `hidden1=10` (4.58 noise units, gap +1.3%); `epochs=2000` (3.25 noise units, gap -3.2%) (and 8 more in the JSON)
- Near alternatives (closest across all claims):
  - `hidden2=3`: this claim +3.1%, mean |gap| 1.9% (4 runs)
  - `hidden2=3`, `hidden1=10`: this claim +2.2%, mean |gap| 2.5% (3 runs)
  - `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1`: this claim +3.3%, mean |gap| 2.8% (3 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting hidden2=3 | settings | 83% | 1.6 sigma (fits every claim) | run with hidden2=3 |
| 2 | a code change: @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 | code | 17% | 2.0 sigma (fits every claim) | run with @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 (an in-memory code patch) |
| 3 | a code change: gae/preprocessing.py:57: `np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0)` -> `(lambda _v: _v[:max(1, len(_v) * 3 // 4)])(np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0))` | code | 0% | 2.4 sigma (fits every claim) | run with @ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1 (an in-memory code patch) |

### History matching (every measured configuration, all claims together)
- 1 of 63 tested configurations fit every claim within 3 sigma
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
- {'hidden2': '3'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'hidden2': '3'} (gap +3.1%); it did not pass verification
- history matching: 1 of 63 tested configurations fit every claim within 3 sigma
- patch round: none of 13 code-patch configurations fits every claim
- mutation round: 1 equivalent code change(s) fit every claim (worst 2.0 sigma): gae/preprocessing.py:57: `np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0)` -> `(lambda _v: _v[:max(1, len(_v) * 1 // 2)])(np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0))`
- explained with a code change (tested in memory, no file edited): gae/preprocessing.py:57: `np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0)` -> `(lambda _v: _v[:max(1, len(_v) * 1 // 2)])(np.delete(edges_positive, np.hstack([test_edge_idx, val_edge_idx]), axis=0))`; a code lead, not a confirmed cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `hidden2=3` | 4 | +3.1% | +1.0% | +0.8% | -1.2% | +3.1% | +0.4% | -2.5% | -3.4% | 1.9% |
| `hidden2=3`, `hidden1=10` | 3 | +2.2% | +0.2% | -5.5% | -6.5% | +2.0% | +0.1% | -0.7% | -2.5% | 2.5% |
| `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1` | 3 | -2.9% | -3.0% | -0.1% | -0.6% | -1.2% | -1.1% | -5.8% | -6.2% | 2.6% |
| `@ast:gae/preprocessing.py:57:@mut.18.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLmRlbGV0ZShlZGdlc19wb3NpdGl2ZSwgbnAuaHN0YWNrKFt0ZXN0X2VkZ2VfaWR4LCB2YWxfZWRnZV9pZHhdKSwgYXhpcz0wKSk=1` | 3 | +3.3% | +3.8% | +3.6% | +3.0% | +4.0% | +3.5% | -0.7% | +0.4% | 2.8% |
| `hidden1=10` | 4 | +3.0% | +1.2% | -3.6% | -3.8% | +4.8% | +2.9% | -2.3% | -4.0% | 3.2% |

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
- Harness spec sha256: `fddb1012c68c36eba4cb4b134add3a69078b48ad80239cca120416848467a9cc`
- Cost: Nemotron billed $0.0000, sandbox reported $1182.9183 (total $1182.9183; this search; ledger extraction is included only if it shared the search's router)
