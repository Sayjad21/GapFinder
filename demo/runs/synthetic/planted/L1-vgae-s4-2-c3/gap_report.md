# Gap Report: planted L1-vgae-s4-2

Artifact `vgae` · generated 2026-10-22 16:36 · 150 branch runs (0 build/load setups) · sandbox $418.7298

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Fits but unsupported | +30.2% | +0.2% | ±1.3% | `learning_rate=0.0001` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **How the code computes the reported number** (test-score selection, label-based edits, switches fixed for evaluation):
  - `gae/preprocessing.py:76`: `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed
  - `gae/preprocessing.py:79`: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed
  - `gae/preprocessing.py:106`: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: gae_cora_auc 81.56 > gae_cora_ap 81.34; measured: gae_cora_auc 85.41 < gae_cora_ap 87.77 (margin -2.36, noise 1.28)
  - paper: gae_citeseer_auc 87.32 > vgae_citeseer_auc 67.81; measured: gae_citeseer_auc 86.3 < vgae_citeseer_auc 87.91 (margin -1.61, noise 1.44)
  - paper: gae_citeseer_ap 87.48 > vgae_citeseer_ap 72.21; measured: gae_citeseer_ap 87.68 < vgae_citeseer_ap 89.75 (margin -2.07, noise 1.68)
- **Held-out claims outside noise:**
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 68.7, measured 87.74 (+27.7%, band ±2.2%)
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 67.81, measured 87.91 (+29.6%, band ±1.7%)
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 72.21, measured 89.75 (+24.3%, band ±2.0%)
  - C_gae_cora_auc (`gae_cora_auc`): paper 81.56, measured 85.41 (+4.7%, band ±1.0%)
  - C_gae_cora_ap (`gae_cora_ap`): paper 81.34, measured 87.77 (+7.9%, band ±1.2%)
  - C_gae_citeseer_auc (`gae_citeseer_auc`): paper 87.32, measured 86.3 (-1.2%, band ±1.0%)

## C_vgae_cora_auc: vgae_cora_auc (paper 66.17)
**Fits but unsupported** · gap +30.2% → +0.2% · 62 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0032`, `B0043`, `B0044`, `B0067` (4 run(s) of the same config)
- Config: `learning_rate` naive `0.01`, changed to `0.0001`
- Command:

  Replay: fork checkpoint `b87946e7-74f5-4d81-bf4d-f55f3eafc206` and run
  ```
  RUN_TAG=44380c8970f2 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=2; mkdir -p out; A="--learning_rate 0.0001 --epochs 200 --hidden1 32 --hidden2 16 --weight_decay 0.0 --dropout 0.0 --features 1"; cd gae; for ds in cora citeseer; do PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_vae --dataset $ds $A > ../out/vgae_$ds.log 2>&1 & PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_ae --dataset $ds $A > ../out/gae_$ds.log 2>&1 & wait; done; cd ..; bash gf_harness/emit.sh
  ```
- Output: `vgae_cora_auc` 66.37, 66.2, 64.7, 66.47; gap after +0.2%; result checkpoint `08696fb3-bbb1-401b-9a9a-71e2aadc209d`
- Effect: candidate 66.28 minus naive 86.16 = -19.87, 95% bootstrap interval [-21.57, -18.34] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 66.17.

### What did we measure?
- Naive median 86.16 over 5 runs; repeats: 84.36, 86.52, 86.23, 84.7, 86.16
- Spread: range 84.36 to 86.52, noise band ±0.8616 (2 x MAD), CV 1.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +30.2% (noise band ±1.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `learning_rate` the gap is +30.2% (it comes back)
- PASS · Held-out claim: C_vgae_cora_ap: +27.7% to +0.7% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_auc: +29.6% to -0.0% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_ap: +24.3% to +0.2% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_auc: +4.7% to +1.5% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_ap: +7.9% to +1.7% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_auc: -1.2% to +0.4% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_ap: +0.2% to +0.7% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_cora_auc@learning_rate=0.005 at learning_rate=0.005: +28.9% to +28.9% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_cora_auc@learning_rate=0.02 at learning_rate=0.02: +20.9% to +20.9% (not worse beyond noise)
- FAIL · Evidence: `learning_rate=0.0001`: no evidence mentions '0.0001'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -19.87 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `learning_rate=0.0002` (22.59 noise units, gap +0.8%); `epochs=4` (22.37 noise units, gap +1.1%); `epochs=2` (21.84 noise units, gap -1.8%); `hidden2=1` (21.57 noise units, gap -2.1%); `hidden1=3` (21.04 noise units, gap -2.8%) (and 18 more in the JSON)
- Near alternatives (closest across all claims):
  - `hidden1=3`: this claim -3.3%, mean |gap| 4.4% (3 runs)
  - `learning_rate=0.0002`, `hidden1=6`: this claim -3.8%, mean |gap| 5.0% (3 runs)
  - `hidden2=2`, `learning_rate=0.0001`: this claim -3.8%, mean |gap| 6.3% (3 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 100% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | the setting learning_rate=0.0001 | settings | 0% | 16.7 sigma | run with learning_rate=0.0001 |
| 3 | the code's learning_rate is 0.01 x the paper's (a unit or convention differs between paper and code) | code | 0% | 17.0 sigma | find where learning_rate enters the computation and compare its unit with the paper's |

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C_vgae_cora_auc@learning_rate=0.005, C_vgae_cora_auc@learning_rate=0.02, among 68 tested
- Fit C_vgae_cora_auc alone (10; worst claim's implausibility in brackets, lowest is the least inconsistent): learning_rate=0.0001 (12.54); hidden2=1, learning_rate=0.0002 (14.65); hidden2=1 (15.98); hidden1=6, hidden2=1 (16.36); epochs=2 (17.96); epochs=4 (18.33)
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
- early code screen stopped: run budget of 150 reached (wanted 1 more run(s) of {'@ast:gae/preprocessing.py:32:val_percent': '40'} for 'patch screen (early)')
- {'learning_rate': '0.0001'} doesn't fit C_vgae_cora_auc@learning_rate=0.005, C_vgae_cora_auc@learning_rate=0.02 (claims at fixed settings); no other tested configuration fits every claim
- scale probe: the code's learning_rate as 0.01 x the paper's does not fit every swept claim after 8 runs at g(v) (C_vgae_cora_auc at learning_rate=0.0001, C_vgae_cora_auc@learning_rate=0.005 at learning_rate=5e-05, C_vgae_cora_auc@learning_rate=0.02 at learning_rate=0.0002)
- patch round: none of 0 code-patch configurations fits every claim
- mutation round: no room left in the run budget
- value interval stopped early: run budget of 150 reached (wanted 1 more run(s) of {'learning_rate': '1e-05'} for 'interval learning_rate=1e-05')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `learning_rate=0.0001` | 4 | +0.2% | +0.7% | -0.0% | +0.2% | +1.5% | +1.7% | +0.4% | +0.7% | 0.7% |
| `hidden1=3` | 3 | -3.3% | -3.9% | +5.0% | +2.7% | -2.8% | -1.5% | -8.2% | -8.3% | 4.4% |
| `learning_rate=0.0002`, `hidden1=6` | 3 | -3.8% | -4.0% | -3.5% | -1.8% | -7.2% | -7.0% | -6.9% | -5.8% | 5.0% |
| `hidden2=2`, `learning_rate=0.0001` | 3 | -3.8% | -6.5% | +1.3% | +0.4% | -10.4% | -8.5% | -10.3% | -9.2% | 6.3% |
| `hidden1=3`, `hidden2=2` | 2 | -7.8% | -4.7% | +0.3% | -1.1% | -10.9% | -8.6% | -9.0% | -8.3% | 6.3% |

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
- Harness spec sha256: `8aaf0eb320c51df263ea42b0eacac8c6d475265f7e353bc99fca609e56cd2a58`
- Cost: Nemotron billed $0.0000, sandbox reported $418.7298 (total $418.7298; this search; ledger extraction is included only if it shared the search's router)
