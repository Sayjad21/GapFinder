# Gap Report: VGAE (devset)

Artifact `vgae` · generated 2026-10-27 11:23 · 199 branch runs (0 build/load setups) · sandbox $1474.6109

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Fits but unsupported | -7.0% | -2.8% | ±0.9% | `dropout=0.5`, `weight_decay=1e-3` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:76` `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_cora_auc (`vgae_cora_auc`): paper 91.4, as run 84.98, without it 86.25 (difference 95% CI [+0.967, +1.95])
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 92.6, as run 87.14, without it 88.49 (difference 95% CI [+0.83, +1.85])
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:79` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 92.6, as run 87.14, without it 88.27 (difference 95% CI [+0.0836, +1.7])
  - C_gae_cora_auc (`gae_cora_auc`): paper 91, as run 85.69, without it 86.35 (difference 95% CI [+0.338, +1.64])
  - C_gae_cora_ap (`gae_cora_ap`): paper 92, as run 88.15, without it 88.85 (difference 95% CI [+0.114, +1.65])
- **How the code computes the reported number** (test-score selection, label-based edits, switches fixed for evaluation):
  - `gae/preprocessing.py:106`: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: vgae_cora_auc 91.4 > vgae_citeseer_auc 90.8; measured: vgae_cora_auc 84.98 < vgae_citeseer_auc 87.26 (margin -2.28, noise 1.45)
  - paper: vgae_cora_ap 92.6 > vgae_citeseer_ap 92; measured: vgae_cora_ap 87.14 < vgae_citeseer_ap 89.27 (margin -2.12, noise 1.25)
- **Held-out claims outside noise:**
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 92.6, measured 87.14 (-5.9%, band ±0.9%)
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 90.8, measured 87.26 (-3.9%, band ±1.3%)
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 92, measured 89.27 (-3.0%, band ±1.0%)
  - C_gae_cora_auc (`gae_cora_auc`): paper 91, measured 85.69 (-5.8%, band ±1.2%)
  - C_gae_cora_ap (`gae_cora_ap`): paper 92, measured 88.15 (-4.2%, band ±1.0%)
  - C_gae_citeseer_auc (`gae_citeseer_auc`): paper 89.5, measured 86.86 (-3.0%, band ±2.2%)
  - C_gae_citeseer_ap (`gae_citeseer_ap`): paper 89.9, measured 88.11 (-2.0%, band ±1.5%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `mask_test_edges_split`: "The validation and test sets contain 5% and 10% of citation links, respectively." (p.2)
  - `negative_sampling`: "We form validation and test sets from previously removed edges and the same number of randomly sampled pairs of unconnected nodes (non-edges)." (p.2)
  - `positive_edge_reweighting`: "For very sparse A, it can be beneficial to re-weight terms with Aij = 1 in L or alternatively sub-sample terms with Aij = 0. We choose the former for the following experiments." (p.2)
  - `full_batch_training`: "We perform full-batch gradient descent and make use of the reparameterization trick [2] for training." (p.2)
  - `weight_initialization`: "For VGAE and GAE, we initialize weights as described in [9]." (p.2)
  - `adjacency_diagonal`: "we assume diagonal elements set to 1, i.e. every node is connected to itself" (p.1)

## C_vgae_cora_auc: vgae_cora_auc (paper 91.4)
**Fits but unsupported** · gap -7.0% → -2.8% · 89 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0026`, `B0031`, `B0032` (3 run(s) of the same config)
- Config: `dropout` naive `0.0`, changed to `0.5`
- Config: `weight_decay` naive `0.0`, changed to `1e-3`
- Command:

  Replay: fork checkpoint `b87946e7-74f5-4d81-bf4d-f55f3eafc206` and run
  ```
  @ast:gae/layers.py:79:@mut.12.Call.xdiv2=0 @ast:gae/layers.py:79:@mut.12.Call.xmul2=0 @ast:gae/layers.py:79:@mut.29.num.add1=0 @ast:gae/layers.py:79:@mut.29.num.div2=0 @ast:gae/layers.py:79:@mut.29.num.mul2=0 @ast:gae/layers.py:79:@mut.29.num.sub1=0 RUN_TAG=90adb88f0c88 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=2; mkdir -p out; A="--learning_rate 0.01 --epochs 200 --hidden1 32 --hidden2 16 --weight_decay 1e-3 --dropout 0.5 --features 1"; cd gae; for ds in cora citeseer; do PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_vae --dataset $ds $A > ../out/vgae_$ds.log 2>&1 & PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_ae --dataset $ds $A > ../out/gae_$ds.log 2>&1 & wait; done; cd ..; bash gf_harness/emit.sh
  ```
- Output: `vgae_cora_auc` 88.56, 88.81, 88.99; gap after -2.8%; result checkpoint `2810f456-b0fc-47d6-8010-8c81b2e2b2d7`
- Effect: candidate 88.81 minus naive 84.98 = +3.83, 95% bootstrap interval [+3.492, +4.589] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 91.4.

### What did we measure?
- Naive median 84.98 over 5 runs; repeats: 85.05, 84.98, 84.4, 84.2, 85.17
- Spread: range 84.2 to 85.17, noise band ±0.8498 (2 x MAD), CV 0.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -7.0% (noise band ±0.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `dropout` the gap is -6.3% (it comes back)
- PASS · Counterfactual (reversal test): without `weight_decay` the gap is -4.1% (it comes back)
- PASS · Held-out claim: C_vgae_cora_ap: -5.9% to -2.8% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_auc: -3.9% to -3.7% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_ap: -3.0% to -3.6% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_auc: -5.8% to -3.9% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_ap: -4.2% to -2.7% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_auc: -3.0% to -2.9% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_ap: -2.0% to -1.6% (not worse beyond noise)
- FAIL · Evidence: `dropout=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- FAIL · Evidence: `weight_decay=1e-3`: no evidence mentions '1e-3'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +3.83 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: `CUDA_VISIBLE_DEVICES`, `random_seed`, `mask_test_edges_split`, `negative_sampling`, `positive_edge_reweighting`, `full_batch_training`, `weight_initialization`, `adjacency_diagonal`, `features_handling`, `model`, `dataset`, `sc_embedding_dim`, `dw_embedding_dim`, `dw_random_walks_per_node`, `dw_random_walk_length`, `dw_context_size`, `dw_epochs`, `num_runs_for_error_bars`, `validation_set_usage`, `adam_beta1`, `gaussian_prior`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `dropout=0.2` (2.31 noise units, gap -4.9%); `weight_decay=5e-4` (1.43 noise units, gap -5.7%)
- Near alternatives (closest across all claims):
  - `@ast:gae/preprocessing.py:32:test_percent=10.0`, `@ast:gae/preprocessing.py:32:val_percent=5.0`: this claim -1.3%, mean |gap| 1.4% (3 runs)
  - `learning_rate=0.001`, `hidden1=160`: this claim -2.5%, mean |gap| 1.7% (2 runs)
  - `hidden2=1600`, `learning_rate=0.001`: this claim -2.1%, mean |gap| 1.8% (2 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `dropout=0.5, weight_decay=1e-3` (reported)
- `@ast:gae/preprocessing.py:32:test_percent=10.0, @ast:gae/preprocessing.py:32:val_percent=5.0`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a code change: @ast:gae/preprocessing.py:32:test_percent=10.0, @ast:gae/preprocessing.py:32:val_percent=5.0 | code | 94% | 1.4 sigma (fits every claim) | run with @ast:gae/preprocessing.py:32:test_percent=10.0, @ast:gae/preprocessing.py:32:val_percent=5.0 (an in-memory code patch) |
| 2 | the setting hidden1=160, learning_rate=0.001 | settings | 5% | 1.7 sigma (fits every claim) | run with hidden1=160, learning_rate=0.001 |
| 3 | the setting hidden2=800, learning_rate=0.001 | settings | 1% | 2.6 sigma (fits every claim) | run with hidden2=800, learning_rate=0.001 |

### History matching (every measured configuration, all claims together)
- 2 of 94 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 2 configurations
  - `hidden1, learning_rate`: hidden1=160, learning_rate=0.001 (max I 2.28)
  - `hidden2, learning_rate`: hidden2=800, learning_rate=0.001 (max I 2.83)
- 2 separate islands (no single-knob move joins them): hidden1=160, learning_rate=0.001 | hidden2=800, learning_rate=0.001
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
  - `gae/preprocessing.py:32`: paper says The validation and test sets contain 5% and 10% of citation links, respectively.; code does Uses val_percent=20.0 (default)
  - `gae/preprocessing.py:32`: paper says The validation and test sets contain 5% and 10% of citation links, respectively.; code does Uses test_percent=30.0 (default)

Notes:
- spec knobs no ledger assumption names (epochs, hidden1, hidden2, learning_rate) were screened too; no better answer
- patch round: {'@ast:gae/preprocessing.py:32:test_percent': '10.0', '@ast:gae/preprocessing.py:32:val_percent': '5.0'} also fits every claim (Partially explained), but doesn't beat {'dropout': '0.5', 'weight_decay': '1e-3'}
- patch round: {'@ast:gae/preprocessing.py:32:test_percent': '10.0', '@ast:gae/preprocessing.py:32:val_percent': '5.0'} fits every claim as well as the answer; the claims can't tell them apart
- value interval stopped early: run budget of 200 reached (wanted 1 more run(s) of {'dropout': '0.3162', 'weight_decay': '1e-3'} for 'interval dropout=0.3162')
- not identifiable from the paper's numbers: 1 configuration(s) of other knobs fit every claim as well as the answer (dropout=0.5, weight_decay=1e-3: @ast:gae/preprocessing.py:32:test_percent=10.0, @ast:gae/preprocessing.py:32:val_percent=5.0), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `@ast:gae/preprocessing.py:32:test_percent=10.0`, `@ast:gae/preprocessing.py:32:val_percent=5.0` | 3 | -1.3% | -0.7% | +1.1% | +1.2% | +0.5% | +1.4% | -2.4% | -2.5% | 1.4% |
| `learning_rate=0.001`, `hidden1=160` | 2 | -2.5% | -2.3% | -0.1% | -0.1% | -3.4% | -2.4% | +0.8% | +2.2% | 1.7% |
| `hidden2=1600`, `learning_rate=0.001` | 2 | -2.1% | -3.6% | +0.5% | +0.4% | -3.8% | -2.2% | -0.2% | +1.7% | 1.8% |
| `learning_rate=0.001`, `hidden2=800` | 2 | -1.7% | -2.3% | +0.6% | +0.5% | -4.2% | -2.5% | +0.6% | +2.4% | 1.8% |
| `hidden2=1600`, `learning_rate=0.002` | 4 | -1.1% | -1.4% | -0.7% | -0.4% | -6.3% | -4.0% | -1.3% | +0.8% | 2.0% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at gae/train.py:142)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at gae/optimizer.py:37)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CUDA_VISIBLE_DEVICES`, `random_seed`, `mask_test_edges_split`, `negative_sampling`, `positive_edge_reweighting`, `full_batch_training`, `weight_initialization`, `adjacency_diagonal`, `features_handling`, `model`, `dataset`, `sc_embedding_dim`, `dw_embedding_dim`, `dw_random_walks_per_node`, `dw_random_walk_length`, `dw_context_size`, `dw_epochs`, `num_runs_for_error_bars`, `validation_set_usage`, `adam_beta1`, `gaussian_prior`

## Provenance
- GapFinder commit: `7e3568335cda944b166665fca73315f0b4a5e13a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `dbcbd2dbf2e2187e56c76686bdacdc905e41f32b38b5baa501b118d0fb3b91ff`
- Cost: Nemotron billed $0.0062, sandbox reported $1474.6109 (total $1474.6171; this search; ledger extraction is included only if it shared the search's router)
