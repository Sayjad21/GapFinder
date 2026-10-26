# Gap Report: VGAE (devset)

Artifact `vgae` · generated 2026-10-26 17:00 · 168 branch runs (0 build/load setups) · sandbox $858.3932

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Fits but unsupported | -6.0% | -2.9% | ±0.9% | `dropout=0.5` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:76` `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_gae_cora_ap (`gae_cora_ap`): paper 92, as run 88.28, without it 87.38 (difference 95% CI [-1.77, -0.375])
- **How the code computes the reported number** (test-score selection, label-based edits, switches fixed for evaluation):
  - `gae/preprocessing.py:79`: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed
  - `gae/preprocessing.py:106`: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: vgae_cora_auc 91.4 > vgae_citeseer_auc 90.8; measured: vgae_cora_auc 85.95 < vgae_citeseer_auc 87.35 (margin -1.39, noise 1.23)
- **Held-out claims outside noise:**
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 92.6, measured 88.17 (-4.8%, band ±1.0%)
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 90.8, measured 87.35 (-3.8%, band ±1.0%)
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 92, measured 88.97 (-3.3%, band ±1.3%)
  - C_gae_cora_auc (`gae_cora_auc`): paper 91, measured 85.81 (-5.7%, band ±1.8%)
  - C_gae_cora_ap (`gae_cora_ap`): paper 92, measured 88.28 (-4.0%, band ±1.0%)
  - C_gae_citeseer_auc (`gae_citeseer_auc`): paper 89.5, measured 85.26 (-4.7%, band ±1.0%)
  - C_gae_citeseer_ap (`gae_citeseer_ap`): paper 89.9, measured 86.36 (-3.9%, band ±1.0%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `mask_test_edges_split`: "The validation and test sets contain 5% and 10% of citation links, respectively." (p.2)
  - `negative_sampling`: "We form validation and test sets from previously removed edges and the same number of randomly sampled pairs of unconnected nodes (non-edges)." (p.2)
  - `positive_edge_reweighting`: "For very sparse A, it can be beneficial to re-weight terms with Aij = 1 in L or alternatively sub-sample terms with Aij = 0. We choose the former for the following experiments." (p.2)
  - `full_batch_training`: "We perform full-batch gradient descent and make use of the reparameterization trick [2] for training." (p.2)
  - `weight_initialization`: "For VGAE and GAE, we initialize weights as described in [9]." (p.2)
  - `adjacency_diagonal`: "we assume diagonal elements set to 1, i.e. every node is connected to itself" (p.1)

## C_vgae_cora_auc: vgae_cora_auc (paper 91.4)
**Fits but unsupported** · gap -6.0% → -2.9% · 102 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0008`, `B0016`, `B0017`, `B0018` (4 run(s) of the same config)
- Config: `dropout` naive `0.0`, changed to `0.5`
- Command:

  Replay: fork checkpoint `b87946e7-74f5-4d81-bf4d-f55f3eafc206` and run
  ```
  @ast:gae/layers.py:79:@mut.12.Call.xdiv2=0 @ast:gae/layers.py:79:@mut.12.Call.xmul2=0 @ast:gae/layers.py:79:@mut.29.num.add1=0 @ast:gae/layers.py:79:@mut.29.num.div2=0 @ast:gae/layers.py:79:@mut.29.num.mul2=0 @ast:gae/layers.py:79:@mut.29.num.sub1=0 RUN_TAG=a0e69363ff57 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=2; mkdir -p out; A="--learning_rate 0.01 --epochs 200 --hidden1 32 --hidden2 16 --weight_decay 0.0 --dropout 0.5 --features 1"; cd gae; for ds in cora citeseer; do PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_vae --dataset $ds $A > ../out/vgae_$ds.log 2>&1 & PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_ae --dataset $ds $A > ../out/gae_$ds.log 2>&1 & wait; done; cd ..; bash gf_harness/emit.sh
  ```
- Output: `vgae_cora_auc` 88.36, 89.29, 87.81, 89.1; gap after -2.9%; result checkpoint `67b3efbe-6e34-4b0f-8eea-3dc3f9d9f1df`
- Effect: candidate 88.73 minus naive 85.95 = +2.775, 95% bootstrap interval [+1.71, +3.409] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 91.4.

### What did we measure?
- Naive median 85.95 over 5 runs; repeats: 85.95, 86.16, 85.81, 85.8, 86.21
- Spread: range 85.8 to 86.21, noise band ±0.8596 (2 x MAD), CV 0.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -6.0% (noise band ±0.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `dropout` the gap is -6.0% (it comes back)
- PASS · Held-out claim: C_vgae_cora_ap: -4.8% to -3.1% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_auc: -3.8% to -4.6% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_ap: -3.3% to -4.1% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_auc: -5.7% to -3.5% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_ap: -4.0% to -2.9% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_auc: -4.7% to -2.5% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_ap: -3.9% to -1.6% (not worse beyond noise)
- FAIL · Evidence: `dropout=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +2.775 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: `CUDA_VISIBLE_DEVICES`, `random_seed`, `mask_test_edges_split`, `negative_sampling`, `positive_edge_reweighting`, `full_batch_training`, `weight_initialization`, `adjacency_diagonal`, `features_handling`, `model`, `dataset`, `sc_embedding_dim`, `dw_embedding_dim`, `dw_random_walks_per_node`, `dw_random_walk_length`, `dw_context_size`, `dw_epochs`, `num_runs_for_error_bars`, `validation_set_usage`, `adam_beta1`, `gaussian_prior`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `learning_rate=0.001`, `hidden1=160`: this claim -1.9%, mean |gap| 1.6% (2 runs)
  - `learning_rate=0.001`, `hidden1=320`: this claim -3.1%, mean |gap| 1.9% (2 runs)
  - `dropout=0.5`, `hidden1=1600`: this claim -2.0%, mean |gap| 1.9% (2 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `dropout=0.5` (reported)
- `dropout=0.5, weight_decay=5e-4`
- `dropout=0.5, weight_decay=1e-3`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting hidden1=160, learning_rate=0.001 | settings | 63% | 1.7 sigma (fits every claim) | run with hidden1=160, learning_rate=0.001 |
| 2 | the setting dropout=0.5, hidden1=1600 | settings | 34% | 1.6 sigma (fits every claim) | run with dropout=0.5, hidden1=1600 |
| 3 | the setting hidden2=800, learning_rate=0.001 | settings | 3% | 2.3 sigma (fits every claim) | run with hidden2=800, learning_rate=0.001 |

### History matching (every measured configuration, all claims together)
- 6 of 107 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `hidden1, learning_rate`: hidden1=160, learning_rate=0.001 (max I 1.86); hidden1=320, learning_rate=0.001 (max I 3)
  - `dropout, hidden1`: dropout=0.5, hidden1=1600 (max I 2.21); dropout=0.5, hidden1=3200 (max I 2.86)
  - `hidden2, learning_rate`: hidden2=800, learning_rate=0.001 (max I 2.94)
  - `dropout, hidden2`: dropout=0.5, hidden2=80 (max I 2.96)
- 4 separate islands (no single-knob move joins them): hidden1=160, learning_rate=0.001; hidden1=320, learning_rate=0.001 | dropout=0.5, hidden1=1600; dropout=0.5, hidden1=3200 | hidden2=800, learning_rate=0.001 | dropout=0.5, hidden2=80
- Leads outside the settings (static code checks, nothing run; check these first):
  - eval switch: `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed (`gae/preprocessing.py:76`)
  - eval switch: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed (`gae/preprocessing.py:79`)
  - eval switch: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed (`gae/preprocessing.py:106`)
  - unexposed setting: `mask_test_edges(..., test_percent=30)`: a default no call in the repo overrides (1 call(s)) (`gae/preprocessing.py:32`)
  - unexposed setting: `mask_test_edges(..., val_percent=20)`: a default no call in the repo overrides (1 call(s)) (`gae/preprocessing.py:32`)
  - unexposed setting: `choice(..., replace=True)`: a switch fixed in the call; no flag sets it (`gae/preprocessing.py:76`)
  - unexposed setting: `in1d(..., assume_unique=True)`: a switch fixed in the call; no flag sets it (`gae/preprocessing.py:78`)
  - unexposed setting: `in1d(..., assume_unique=True)`: a switch fixed in the call; no flag sets it (`gae/preprocessing.py:79`)
- Where the code differs from the paper (model-proposed, checked against the repo; literal ones were tried as patch knobs, structural ones are not tested):
  - `gae/preprocessing.py:32`: paper says The validation and test sets contain 5% and 10% of citation links, respectively.; code does test_percent = 30.0
  - `gae/preprocessing.py:32`: paper says The validation and test sets contain 5% and 10% of citation links, respectively.; code does val_percent = 20.0

Notes:
- configurations the target claim can't tell apart from the answer: dropout=0.5; dropout=0.5, weight_decay=5e-4; dropout=0.5, weight_decay=1e-3
- spec knobs no ledger assumption names (epochs, hidden1, hidden2, learning_rate) were screened too; no better answer
- patch round: none of 2 code-patch configurations fits every claim
- value interval stopped early: run budget of 200 reached (wanted 1 more run(s) of {'dropout': '0.3162'} for 'interval dropout=0.3162')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `learning_rate=0.001`, `hidden1=160` | 2 | -1.9% | -1.9% | -0.4% | -0.2% | -2.9% | -1.9% | +1.2% | +2.6% | 1.6% |
| `learning_rate=0.001`, `hidden1=320` | 2 | -3.1% | -2.4% | +0.1% | -0.1% | -3.8% | -2.5% | +1.0% | +2.1% | 1.9% |
| `dropout=0.5`, `hidden1=1600` | 2 | -2.0% | -2.1% | -1.2% | -1.4% | -3.4% | -3.1% | -1.1% | -0.9% | 1.9% |
| `hidden2=800`, `learning_rate=0.001` | 2 | -2.3% | -3.1% | +1.3% | +0.9% | -3.8% | -2.2% | +0.2% | +2.1% | 2.0% |
| `hidden2=800`, `learning_rate=0.002` | 4 | -0.6% | -0.8% | -2.0% | -1.5% | -5.9% | -3.4% | -0.8% | +1.5% | 2.1% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at gae/train.py:142)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at gae/optimizer.py:37)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CUDA_VISIBLE_DEVICES`, `random_seed`, `mask_test_edges_split`, `negative_sampling`, `positive_edge_reweighting`, `full_batch_training`, `weight_initialization`, `adjacency_diagonal`, `features_handling`, `model`, `dataset`, `sc_embedding_dim`, `dw_embedding_dim`, `dw_random_walks_per_node`, `dw_random_walk_length`, `dw_context_size`, `dw_epochs`, `num_runs_for_error_bars`, `validation_set_usage`, `adam_beta1`, `gaussian_prior`

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fb36007ca37611d5ecd0748fc83a1fc262056fe82025f7713ccd84ae65e7c72d`
- Cost: Nemotron billed $0.0070, sandbox reported $858.3932 (total $858.4002; this search; ledger extraction is included only if it shared the search's router)
