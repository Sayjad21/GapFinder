# Gap Report: planted L1-vgae-s5-2

Artifact `vgae` · generated 2026-10-23 05:24 · 144 branch runs (0 build/load setups) · sandbox $422.4980

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Paper-artifact inconsistency | +28.7% | +0.2% | ±1.8% | `learning_rate=0.0001` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **How the code computes the reported number** (test-score selection, label-based edits, switches fixed for evaluation):
  - `gae/preprocessing.py:76`: `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed
  - `gae/preprocessing.py:79`: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed
  - `gae/preprocessing.py:106`: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: gae_cora_auc 82.64 > gae_cora_ap 81.8; measured: gae_cora_auc 86.16 < gae_cora_ap 88.8 (margin -2.63, noise 1.81)
- **Held-out claims outside noise:**
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 68.73, measured 87.9 (+27.9%, band ±2.4%)
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 70.28, measured 87.37 (+24.3%, band ±1.2%)
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 74.13, measured 89.23 (+20.4%, band ±1.2%)
  - C_gae_cora_auc (`gae_cora_auc`): paper 82.64, measured 86.16 (+4.3%, band ±1.9%)
  - C_gae_cora_ap (`gae_cora_ap`): paper 81.8, measured 88.8 (+8.6%, band ±1.1%)

## C_vgae_cora_auc: vgae_cora_auc (paper 66.26)
**Paper-artifact inconsistency** · gap +28.7% → +0.2% · 51 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0032`, `B0068`, `B0069`, `B0091` (4 run(s) of the same config)
- Config: `learning_rate` naive `0.01`, changed to `0.0001`
- Command:

  Replay: fork checkpoint `b87946e7-74f5-4d81-bf4d-f55f3eafc206` and run
  ```
  @ast:gae/preprocessing.py:32:test_percent=30.0 @ast:gae/preprocessing.py:32:val_percent=20.0 @ast:gae/preprocessing.py:76:replace=True @ast:gae/preprocessing.py:40:@mut.11.Call.red.mean=0 @ast:gae/optimizer.py:15:@mut.22.Call.xdiv2=0 @ast:gae/optimizer.py:15:@mut.22.Call.xmul2=0 @ast:gae/optimizer.py:16:@mut.26.Call.xdiv2=0 @ast:gae/optimizer.py:16:@mut.26.Call.xmul2=0 @ast:gae/optimizer.py:37:@mut.22.Call.xdiv2=0 RUN_TAG=086b7f08a2c3 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=2; mkdir -p out; A="--learning_rate 0.0001 --epochs 200 --hidden1 32 --hidden2 16 --weight_decay 0.0 --dropout 0.0 --features 1"; cd gae; for ds in cora citeseer; do PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_vae --dataset $ds $A > ../out/vgae_$ds.log 2>&1 & PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_ae --dataset $ds $A > ../out/gae_$ds.log 2>&1 & wait; done; cd ..; bash gf_harness/emit.sh
  ```
- Output: `vgae_cora_auc` 66.86, 65.56, 65.95, 68.06; gap after +0.2%; result checkpoint `51a88acc-8a4a-4195-935c-287b4c55606e`
- Effect: candidate 66.41 minus naive 85.29 = -18.88, 95% bootstrap interval [-21, -16.74] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 66.26.

### What did we measure?
- Naive median 85.29 over 5 runs; repeats: 85.29, 87.21, 85.88, 84.07, 85.29
- Spread: range 84.07 to 87.21, noise band ±1.178 (2 x MAD), CV 1.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +28.7% (noise band ±1.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `learning_rate` the gap is +28.7% (it comes back)
- PASS · Held-out claim: C_vgae_cora_auc@learning_rate=0.005 at learning_rate=5e-05: n/a to +2.9% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_cora_auc@learning_rate=0.02 at learning_rate=0.0002: n/a to -2.9% (not worse beyond noise)
- FAIL · Evidence: `learning_rate=0.0001`: no evidence mentions '0.0001'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -18.88 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=3` (15.66 noise units, gap +0.9%); `hidden2=1` (15.17 noise units, gap -1.7%); `epochs=2` (14.56 noise units, gap -2.8%); `hidden1=2` (14.51 noise units, gap +2.9%); `epochs=1` (14.46 noise units, gap -3.0%) (and 17 more in the JSON)
- Near alternatives (closest across all claims):
  - `learning_rate=0.0002`: this claim +2.2%, mean |gap| 4.0% (4 runs)
  - `hidden1=3`: this claim +1.6%, mean |gap| 4.9% (4 runs)
  - `learning_rate=5e-05`: this claim -0.3%, mean |gap| 6.0% (2 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 100% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | the code's learning_rate is 0.01 x the paper's (a unit or convention differs between paper and code) | code | 0% | 13.8 sigma | find where learning_rate enters the computation and compare its unit with the paper's |
| 3 | the setting learning_rate=0.0001 | settings | 0% | 20.9 sigma | run with learning_rate=0.0001 |

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C_vgae_cora_auc@learning_rate=0.02, among 64 tested
- Fit C_vgae_cora_auc alone (10; worst claim's implausibility in brackets, lowest is the least inconsistent): hidden1=3 (5.91); hidden2=1, learning_rate=0.005 (11.26); learning_rate=0.0001 (13.46); learning_rate=0.0002 (13.46); hidden2=1, learning_rate=0.02 (13.79); epochs=2 (14.1)
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
- {'learning_rate': '0.0001'} doesn't fit C_vgae_cora_auc@learning_rate=0.005, C_vgae_cora_auc@learning_rate=0.02 (claims at fixed settings); no other tested configuration fits every claim
- scale probe: the code's learning_rate as 0.01 x the paper's fits every swept claim after 10 runs at g(v) (C_vgae_cora_auc at learning_rate=0.0001, C_vgae_cora_auc@learning_rate=0.005 at learning_rate=5e-05, C_vgae_cora_auc@learning_rate=0.02 at learning_rate=0.0002)
- labelled Paper-artifact inconsistency: one factor (0.01 x the paper's) makes every one of the 3 swept claims fit
- patch round: none of 20 code-patch configurations fits every claim
- mutation round: none of 6 mutants moved C_vgae_cora_auc toward the paper
- value interval stopped early: run budget of 150 reached (wanted 1 more run(s) of {'learning_rate': '7.071e-05'} for 'interval learning_rate=7.071e-05')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `learning_rate=0.0001` | 4 | +0.2% | -0.2% | -1.8% | -1.3% | -0.0% | +0.5% | -1.1% | -0.8% | 0.7% |
| `learning_rate=0.0002` | 4 | +2.2% | +1.4% | +9.4% | +5.6% | +3.9% | +5.2% | +2.1% | +2.5% | 4.0% |
| `hidden1=3` | 4 | +1.6% | +1.5% | -2.4% | -3.3% | -6.6% | -4.1% | -9.6% | -9.9% | 4.9% |
| `learning_rate=5e-05` | 2 | -0.3% | -1.4% | -3.7% | -5.1% | -12.4% | -9.3% | -8.1% | -7.6% | 6.0% |
| `hidden2=1` | 4 | -2.8% | -1.2% | +0.3% | -2.5% | -14.7% | -12.5% | -18.6% | -17.6% | 8.8% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at gae/train.py:142)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at gae/optimizer.py:37)

## Provenance
- GapFinder commit: `96f43d9d872690442737d0ad342eeb7d86352416` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `c4c29fe426cb05636b2801a35a0720a28235827c742cd4be4e3cf17305e715e5`
- Cost: Nemotron billed $0.0000, sandbox reported $422.4980 (total $422.4980; this search; ledger extraction is included only if it shared the search's router)
