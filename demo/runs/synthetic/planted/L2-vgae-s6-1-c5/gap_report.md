# Gap Report: planted L2-vgae-s6-1

Artifact `vgae` · generated 2026-10-23 22:54 · 149 branch runs (0 build/load setups) · sandbox $695.4140

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Inconclusive | +1.3% | +1.3% | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:76` `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 89.21, as run 88.35, without it 89.85 (difference 95% CI [+0.406, +2])
- Tested: switching this code off moved no claim beyond noise: `gae/preprocessing.py:79` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_cora_auc (`vgae_cora_auc`): paper 84.48, as run 85.57, without it 85.96 (difference 95% CI [-1.12, +0.549])
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 86.93, as run 87.86, without it 88.14 (difference 95% CI [-0.851, +0.712])
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 87.42, as run 86.56, without it 87.75 (difference 95% CI [-0.299, +2.12])
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 89.21, as run 88.35, without it 89.2 (difference 95% CI [-0.249, +1.86])
  - C_gae_cora_auc (`gae_cora_auc`): paper 86.31, as run 86.01, without it 85.71 (difference 95% CI [-1.19, +0.806])
  - C_gae_cora_ap (`gae_cora_ap`): paper 88.81, as run 88.07, without it 88.25 (difference 95% CI [-1.06, +0.787])
- **How the code computes the reported number** (test-score selection, label-based edits, switches fixed for evaluation):
  - `gae/preprocessing.py:106`: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed
- **Held-out claims outside noise:**
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 86.93, measured 87.86 (+1.1%, band ±1.0%)
  - C_gae_citeseer_auc (`gae_citeseer_auc`): paper 84.69, measured 86.59 (+2.2%, band ±1.0%)
  - C_gae_citeseer_ap (`gae_citeseer_ap`): paper 86.23, measured 88.23 (+2.3%, band ±1.1%)

## C_vgae_cora_auc: vgae_cora_auc (paper 84.48)
**Inconclusive** · naive gap +1.3% is inside the noise band ±1.0%, but the band is too wide to call it a reproduction.

### Which experiment changed it?
- None could be tested: the noise band is too wide to tell values apart.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 84.48.

### What did we measure?
- Naive median 85.57 over 5 runs; repeats: 85.46, 85.39, 87.87, 85.57, 85.57
- Spread: range 85.39 to 87.87, noise band ±0.8557 (2 x MAD), CV 1.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +1.3% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `learning_rate=0.02` (1.24 noise units, gap +0.0%); `hidden1=15` (1.23 noise units, gap -0.0%); `hidden2=4` (1.11 noise units, gap +0.2%); `epochs=400` (1.1 noise units, gap -0.2%)
- Near alternatives (closest across all claims):
  - `@ast:gae/preprocessing.py:40:@mut.11.Call.red.mean=1`: this claim +1.5%, mean |gap| 0.6% (3 runs)
  - `@ast:gae/preprocessing.py:76:replace=False`: this claim +1.4%, mean |gap| 1.1% (3 runs)
  - `@ast:gae/preprocessing.py:79:assume_unique=False`: this claim +1.8%, mean |gap| 1.1% (3 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting hidden2=32 | settings | 38% | 0.9 sigma (fits every claim) | run with hidden2=32 |
| 2 | no difference in reporting: the numbers as printed at the end of the run | settings | 17% | 1.7 sigma (fits every claim) | the settings search and the other classes |
| 3 | the setting hidden2=8 | settings | 17% | 1.0 sigma (fits every claim) | run with hidden2=8 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `hidden2`: hidden2=32 (max I 0.94); hidden2=8 (max I 1.04)
  - `@ast:gae/preprocessing.py:40:@mut.11.Call.red.mean`: @ast:gae/preprocessing.py:40:@mut.11.Call.red.mean=1 (max I 1.04)
  - `@ast:gae/preprocessing.py:76:replace`: @ast:gae/preprocessing.py:76:replace=False (max I 1.14)
  - `hidden1, hidden2`: hidden1=64, hidden2=32 (max I 1.2)
  - `hidden1`: hidden1=1600 (max I 1.39)
  - `@ast:gae/optimizer.py:16:@mut.26.Call.xmul2`: @ast:gae/optimizer.py:16:@mut.26.Call.xmul2=1 (max I 1.55)
  - `epochs`: epochs=100 (max I 1.77)
  - `@ast:gae/preprocessing.py:32:val_percent`: @ast:gae/preprocessing.py:32:val_percent=4 (max I 1.93)
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
- {'hidden1': '15'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'hidden1': '15'} (gap +0.0%); it did not pass verification
- the gap (+1.3%) is below the minimum detectable effect (±3.8% with 3 runs per configuration at 80% power): even a setting that closed it couldn't have been confirmed, so 'nothing explains it' can't be claimed either
- patch round: {'@ast:gae/preprocessing.py:40:@mut.11.Call.red.mean': '1'} fits every claim but did not pass verification
- mutation round: none of 12 mutants moved C_vgae_cora_auc toward the paper

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `@ast:gae/preprocessing.py:40:@mut.11.Call.red.mean=1` | 3 | +1.5% | +1.2% | -0.1% | -0.3% | -0.2% | -0.5% | -0.3% | -0.8% | 0.6% |
| `@ast:gae/preprocessing.py:76:replace=False` | 3 | +1.4% | +1.4% | +0.3% | +0.7% | -0.2% | -0.7% | +2.2% | +1.6% | 1.1% |
| `@ast:gae/preprocessing.py:79:assume_unique=False` | 3 | +1.8% | +1.4% | +0.4% | -0.0% | -0.7% | -0.6% | +1.9% | +1.8% | 1.1% |
| naive (reproduction as run) | 5 | +1.3% | +1.1% | -1.0% | -1.0% | -0.3% | -0.8% | +2.2% | +2.3% | 1.3% |
| `epochs=400` | 4 | +0.3% | +0.5% | -2.1% | -2.1% | -3.3% | -2.7% | -2.3% | -1.8% | 1.9% |

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
- Harness spec sha256: `7baecaa1585101ed2ace707caf2a5e2ca21e777c058d76fcd8ddffe0329c89c0`
- Cost: Nemotron billed $0.0047, sandbox reported $695.4140 (total $695.4187; this search; ledger extraction is included only if it shared the search's router)
