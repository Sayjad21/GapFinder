# Gap Report: planted L2-vgae-s3-2

Artifact `vgae` · generated 2026-10-22 08:04 · 146 branch runs (0 build/load setups) · sandbox $691.4096

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Fits but unsupported | +3.6% | -1.1% | ±1.0% | `epochs=1000` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- Tested: switching this code off moved no claim beyond noise: `gae/preprocessing.py:76` `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_cora_auc (`vgae_cora_auc`): paper 82.68, as run 85.66, without it 85.43 (difference 95% CI [-1.15, +1.19])
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 85.77, as run 88.04, without it 87.28 (difference 95% CI [-1.28, +0.728])
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 81.86, as run 88.04, without it 86.92 (difference 95% CI [-1.54, +1.73])
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 85.01, as run 90.01, without it 89.02 (difference 95% CI [-1.4, +1.73])
  - C_gae_cora_auc (`gae_cora_auc`): paper 79.02, as run 86.27, without it 87.08 (difference 95% CI [-0.179, +1.45])
  - C_gae_cora_ap (`gae_cora_ap`): paper 83.2, as run 88.31, without it 88.49 (difference 95% CI [-0.189, +1.12])
- Tested: switching this code off moved no claim beyond noise: `gae/preprocessing.py:79` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_cora_auc (`vgae_cora_auc`): paper 82.68, as run 85.66, without it 85.36 (difference 95% CI [-0.809, +0.257])
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 85.77, as run 88.04, without it 87.59 (difference 95% CI [-0.753, +0.393])
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 81.86, as run 88.04, without it 86.78 (difference 95% CI [-1.83, +1.32])
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 85.01, as run 90.01, without it 89.17 (difference 95% CI [-1.5, +1.65])
  - C_gae_cora_auc (`gae_cora_auc`): paper 79.02, as run 86.27, without it 86.91 (difference 95% CI [-3.13, +1.22])
  - C_gae_cora_ap (`gae_cora_ap`): paper 83.2, as run 88.31, without it 88.61 (difference 95% CI [-2.4, +0.927])
- Tested: switching this code off moved no claim beyond noise: `gae/preprocessing.py:106` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_cora_auc (`vgae_cora_auc`): paper 82.68, as run 85.66, without it 85.92 (difference 95% CI [-0.13, +1.4])
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 85.77, as run 88.04, without it 88.11 (difference 95% CI [-0.214, +0.859])
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 81.86, as run 88.04, without it 87.3 (difference 95% CI [-1.97, +1.68])
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 85.01, as run 90.01, without it 89.33 (difference 95% CI [-1.87, +1.67])
  - C_gae_cora_auc (`gae_cora_auc`): paper 79.02, as run 86.27, without it 86.11 (difference 95% CI [-1.15, +1.06])
  - C_gae_cora_ap (`gae_cora_ap`): paper 83.2, as run 88.31, without it 88.67 (difference 95% CI [-0.797, +0.935])
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: vgae_cora_auc 82.68 > vgae_citeseer_auc 81.86; measured: vgae_cora_auc 85.66 < vgae_citeseer_auc 88.04 (margin -2.38, noise 1.81)
  - paper: vgae_cora_ap 85.77 > vgae_citeseer_ap 85.01; measured: vgae_cora_ap 88.04 < vgae_citeseer_ap 90.01 (margin -1.97, noise 1.64)
  - paper: gae_citeseer_ap 83.61 > gae_cora_ap 83.2; measured: gae_citeseer_ap 86 < gae_cora_ap 88.31 (margin -2.31, noise 1.87)
- **Held-out claims outside noise:**
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 85.77, measured 88.04 (+2.6%, band ±1.0%)
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 81.86, measured 88.04 (+7.6%, band ±1.9%)
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 85.01, measured 90.01 (+5.9%, band ±1.6%)
  - C_gae_cora_auc (`gae_cora_auc`): paper 79.02, measured 86.27 (+9.2%, band ±1.1%)
  - C_gae_cora_ap (`gae_cora_ap`): paper 83.2, measured 88.31 (+6.1%, band ±1.3%)
  - C_gae_citeseer_auc (`gae_citeseer_auc`): paper 80, measured 85.22 (+6.5%, band ±2.9%)
  - C_gae_citeseer_ap (`gae_citeseer_ap`): paper 83.61, measured 86 (+2.9%, band ±1.8%)

## C_vgae_cora_auc: vgae_cora_auc (paper 82.68)
**Fits but unsupported** · gap +3.6% → -1.1% · 41 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0015`, `B0051`, `B0052`, `B0074` (4 run(s) of the same config)
- Config: `epochs` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `b87946e7-74f5-4d81-bf4d-f55f3eafc206` and run
  ```
  RUN_TAG=2e9efe5b1384 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=2; mkdir -p out; A="--learning_rate 0.01 --epochs 1000 --hidden1 32 --hidden2 16 --weight_decay 0.0 --dropout 0.0 --features 1"; cd gae; for ds in cora citeseer; do PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_vae --dataset $ds $A > ../out/vgae_$ds.log 2>&1 & PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_ae --dataset $ds $A > ../out/gae_$ds.log 2>&1 & wait; done; cd ..; bash gf_harness/emit.sh
  ```
- Output: `vgae_cora_auc` 82.04, 82.75, 80.33, 81.52; gap after -1.1%; result checkpoint `f257c32c-a597-492c-8575-c7dfbe14f659`
- Effect: candidate 81.78 minus naive 85.66 = -3.887, 95% bootstrap interval [-5.631, -2.61] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 82.68.

### What did we measure?
- Naive median 85.66 over 5 runs; repeats: 85.2, 85.32, 85.66, 85.96, 86.32
- Spread: range 85.2 to 86.32, noise band ±0.8566 (2 x MAD), CV 0.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +3.6% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is +3.6% (it comes back)
- PASS · Held-out claim: C_vgae_cora_ap: +2.6% to -0.9% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_auc: +7.6% to -1.7% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_ap: +5.9% to -1.3% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_auc: +9.2% to -3.0% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_ap: +6.1% to -2.0% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_auc: +6.5% to -0.8% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_ap: +2.9% to -1.0% (not worse beyond noise)
- FAIL · Evidence: `epochs=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -3.887 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=400` (2.92 noise units, gap +0.6%); `learning_rate=0.05` (2.53 noise units, gap -1.0%); `hidden1=3200` (2.39 noise units, gap +1.1%); `epochs=600` (2.11 noise units, gap +1.4%); `epochs=20` (1.91 noise units, gap +1.6%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `epochs=800`: this claim +1.1%, mean |gap| 0.9% (4 runs)
  - `epochs=600`: this claim +1.3%, mean |gap| 1.3% (4 runs)
  - `epochs=800`, `@ast:gae/preprocessing.py:76:replace=False`: this claim -0.1%, mean |gap| 1.4% (3 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=1000` (reported)
- `epochs=600`
- `epochs=800`
- `epochs=400`
- `hidden2=3`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting epochs=1000 | settings | 46% | 1.2 sigma (fits every claim) | run with epochs=1000 |
| 2 | the setting epochs=800 | settings | 27% | 0.6 sigma (fits every claim) | run with epochs=800 |
| 3 | the setting epochs=600 | settings | 24% | 0.8 sigma (fits every claim) | run with epochs=600 |

### History matching (every measured configuration, all claims together)
- 5 of 41 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `epochs`: epochs=800 (max I 0.58); epochs=600 (max I 1.44); epochs=1000 (max I 1.94)
  - `learning_rate`: learning_rate=0.02 (max I 2.23)
  - `hidden2`: hidden2=3 (max I 2.61)
- 3 separate islands (no single-knob move joins them): epochs=800; epochs=600; epochs=1000 | learning_rate=0.02 | hidden2=3
- Leads outside the settings (static code checks, nothing run; check these first):
  - eval switch: `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed (`gae/preprocessing.py:76`)
  - eval switch: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed (`gae/preprocessing.py:79`)
  - eval switch: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed (`gae/preprocessing.py:106`)
  - unexposed setting: `mask_test_edges(..., test_percent=30)`: a default no call in the repo overrides (1 call(s)) (`gae/preprocessing.py:32`)
  - unexposed setting: `mask_test_edges(..., val_percent=20)`: a default no call in the repo overrides (1 call(s)) (`gae/preprocessing.py:32`)
  - unexposed setting: `choice(..., replace=True)`: a switch fixed in the call; no flag sets it (`gae/preprocessing.py:76`)
  - unexposed setting: `in1d(..., assume_unique=True)`: a switch fixed in the call; no flag sets it (`gae/preprocessing.py:78`)
  - unexposed setting: `in1d(..., assume_unique=True)`: a switch fixed in the call; no flag sets it (`gae/preprocessing.py:79`)
- Equally good values: `epochs` in {20, 400, 600, 800, 1000}

Notes:
- configurations the target claim can't tell apart from the answer: epochs=1000; epochs=600; epochs=800; epochs=400; hidden2=3
- equally good values within one noise band (measured): epochs in {20, 400, 600, 800, 1000}
- patch round: {'@ast:gae/preprocessing.py:76:replace': 'False', 'epochs': '800'} also fits every claim (Fits but unsupported), but doesn't beat {'epochs': '1000'}
- mutation round: no mutant fits every claim (gae/train.py:138: `sp.eye(adj_train.shape[0])` -> `(sp.eye(adj_train.shape[0])) / 2`: worst 4.4 sigma; gae/train.py:66: `sparse_to_tuple(features.tocoo())` -> `(sparse_to_tuple(features.tocoo())) * 2`: worst 4.9 sigma; gae/train.py:54: `preprocess_graph(adj)` -> `(preprocess_graph(adj)) * 2`: worst 5.7 sigma)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `epochs=800` | 4 | +1.1% | +0.6% | -1.0% | -0.8% | -0.7% | -0.5% | -0.8% | -1.4% | 0.9% |
| `epochs=600` | 4 | +1.3% | +0.5% | +1.4% | +1.0% | +3.5% | +1.6% | +0.3% | -1.0% | 1.3% |
| `epochs=800`, `@ast:gae/preprocessing.py:76:replace=False` | 3 | -0.1% | -0.3% | -0.6% | -1.7% | -2.2% | -1.7% | -2.2% | -2.4% | 1.4% |
| `epochs=1000` | 4 | -1.1% | -0.9% | -1.7% | -1.3% | -3.0% | -2.0% | -0.8% | -1.0% | 1.5% |
| `hidden2=3` | 4 | -0.6% | -2.9% | +0.6% | -2.1% | +1.3% | -1.8% | +5.5% | +1.1% | 2.0% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at gae/train.py:142)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at gae/optimizer.py:37)

## Provenance
- GapFinder commit: `ca4a5e297839f0c50559b58914404255594c81fb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `72ec87d30fff45601e2692c37b41b5390eecd05efbc1e32dadcc17fdc1f4befb`
- Cost: Nemotron billed $0.0000, sandbox reported $691.4096 (total $691.4096; this search; ledger extraction is included only if it shared the search's router)
