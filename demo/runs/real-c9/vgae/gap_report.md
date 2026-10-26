# Gap Report: VGAE (devset)

Artifact `vgae` · generated 2026-10-27 02:16 · 199 branch runs (0 build/load setups) · sandbox $1042.1724

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Paper-artifact inconsistency | -5.4% | +0.3% | ±0.9% | `@ast:gae/preprocessing.py:32:test_percent=10`, `@ast:gae/preprocessing.py:32:val_percent=5` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:76` `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_gae_cora_auc (`gae_cora_auc`): paper 91, as run 85.4, without it 86.54 (difference 95% CI [+0.0824, +1.75])
- Tested: switching this code off moved no claim beyond noise: `gae/preprocessing.py:79` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_cora_auc (`vgae_cora_auc`): paper 91.4, as run 86.44, without it 85.78 (difference 95% CI [-0.938, +0.414])
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 92.6, as run 88.82, without it 87.83 (difference 95% CI [-1.27, +0.0754])
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 90.8, as run 86.85, without it 87 (difference 95% CI [-1.56, +0.693])
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 92, as run 89.02, without it 88.68 (difference 95% CI [-1.5, +0.563])
  - C_gae_cora_auc (`gae_cora_auc`): paper 91, as run 85.4, without it 86.16 (difference 95% CI [-1.11, +1.16])
  - C_gae_cora_ap (`gae_cora_ap`): paper 92, as run 87.7, without it 88.39 (difference 95% CI [-1.13, +1.09])
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:106` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 90.8, as run 86.85, without it 88.1 (difference 95% CI [+0.0204, +2.24])
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 92, as run 89.02, without it 89.94 (difference 95% CI [+0.106, +1.95])
- **Held-out claims outside noise:**
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 92.6, measured 88.82 (-4.1%, band ±1.1%)
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 90.8, measured 86.85 (-4.3%, band ±2.7%)
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 92, measured 89.02 (-3.2%, band ±1.9%)
  - C_gae_cora_auc (`gae_cora_auc`): paper 91, measured 85.4 (-6.2%, band ±1.2%)
  - C_gae_cora_ap (`gae_cora_ap`): paper 92, measured 87.7 (-4.7%, band ±2.0%)
  - C_gae_citeseer_auc (`gae_citeseer_auc`): paper 89.5, measured 84.94 (-5.1%, band ±3.2%)
  - C_gae_citeseer_ap (`gae_citeseer_ap`): paper 89.9, measured 85.61 (-4.8%, band ±1.0%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `mask_test_edges_split`: "The validation and test sets contain 5% and 10% of citation links, respectively." (p.2)
  - `negative_sampling`: "We form validation and test sets from previously removed edges and the same number of randomly sampled pairs of unconnected nodes (non-edges)." (p.2)
  - `positive_edge_reweighting`: "For very sparse A, it can be beneficial to re-weight terms with Aij = 1 in L or alternatively sub-sample terms with Aij = 0. We choose the former for the following experiments." (p.2)
  - `full_batch_training`: "We perform full-batch gradient descent and make use of the reparameterization trick [2] for training." (p.2)
  - `weight_initialization`: "For VGAE and GAE, we initialize weights as described in [9]." (p.2)
  - `adjacency_diagonal`: "we assume diagonal elements set to 1, i.e. every node is connected to itself" (p.1)

## C_vgae_cora_auc: vgae_cora_auc (paper 91.4)
**Paper-artifact inconsistency** · gap -5.4% → +0.3% · 83 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0142`, `B0170`, `B0171` (3 run(s) of the same config)
- Config: `@ast:gae/preprocessing.py:32:test_percent` naive `30.`, changed to `10`
- Config: `@ast:gae/preprocessing.py:32:val_percent` naive `20.`, changed to `5`
- Command:

  Replay: fork checkpoint `b87946e7-74f5-4d81-bf4d-f55f3eafc206` and run
  ```
  @ast:gae/layers.py:79:@mut.12.Call.xdiv2=0 @ast:gae/layers.py:79:@mut.12.Call.xmul2=0 @ast:gae/layers.py:79:@mut.29.num.add1=0 @ast:gae/layers.py:79:@mut.29.num.div2=0 @ast:gae/layers.py:79:@mut.29.num.mul2=0 @ast:gae/layers.py:79:@mut.29.num.sub1=0 @ast:gae/preprocessing.py:32:test_percent=10 @ast:gae/preprocessing.py:32:val_percent=5 @ast:gae/preprocessing.py:76:replace=True RUN_TAG=f2055c2ae2fb export PYTHONPATH="${WORK:-$PWD}/.gf_patch${PYTHONPATH:+${GF_PATHSEP:-:}$PYTHONPATH}"; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=2; mkdir -p out; A="--learning_rate 0.01 --epochs 200 --hidden1 32 --hidden2 16 --weight_decay 0.0 --dropout 0.0 --features 1"; cd gae; for ds in cora citeseer; do PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_vae --dataset $ds $A > ../out/vgae_$ds.log 2>&1 & PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_ae --dataset $ds $A > ../out/gae_$ds.log 2>&1 & wait; done; cd ..; bash gf_harness/emit.sh
  ```
- Output: `vgae_cora_auc` 92.53, 90.45, 91.64; gap after +0.3%; result checkpoint `08050306-e648-4d19-b2a8-7c76275e07cc`
- Effect: candidate 91.64 minus naive 86.44 = +5.199, 95% bootstrap interval [+3.846, +6.764] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 91.4.

### What did we measure?
- Naive median 86.44 over 5 runs; repeats: 85.01, 86.04, 86.89, 86.44, 86.75
- Spread: range 85.01 to 86.89, noise band ±0.8644 (2 x MAD), CV 0.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -5.4% (noise band ±0.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `@ast:gae/preprocessing.py:32:test_percent` the gap is -2.7% (it comes back)
- PASS · Counterfactual (reversal test): without `@ast:gae/preprocessing.py:32:val_percent` the gap is -1.8% (it comes back)
- PASS · Held-out claim: C_vgae_cora_ap: -4.1% to +0.6% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_auc: -4.3% to -0.5% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_ap: -3.2% to +0.2% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_auc: -6.2% to -0.3% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_ap: -4.7% to -0.1% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_auc: -5.1% to +0.1% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_ap: -4.8% to +0.7% (not worse beyond noise)
- PASS · Evidence: `@ast:gae/preprocessing.py:32:test_percent=10`: paper states '10'
- PASS · Evidence: `@ast:gae/preprocessing.py:32:val_percent=5`: paper states '5'
- PASS · Effect vs noise: candidate minus naive is +5.199 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: `CUDA_VISIBLE_DEVICES`, `random_seed`, `mask_test_edges_split`, `negative_sampling`, `positive_edge_reweighting`, `full_batch_training`, `weight_initialization`, `adjacency_diagonal`, `features_handling`, `model`, `dataset`, `sc_embedding_dim`, `dw_embedding_dim`, `dw_random_walks_per_node`, `dw_random_walk_length`, `dw_context_size`, `dw_epochs`, `num_runs_for_error_bars`, `validation_set_usage`, `adam_beta1`, `gaussian_prior`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `dropout=0.5` (1.02 noise units, gap -4.5%)
- Near alternatives (closest across all claims):
  - `@ast:gae/preprocessing.py:32:test_percent=10`: this claim -1.8%, mean |gap| 1.6% (3 runs)
  - `hidden2=1600`, `learning_rate=0.002`: this claim -1.1%, mean |gap| 1.8% (4 runs)
  - `hidden1=320`, `learning_rate=0.001`: this claim -3.1%, mean |gap| 1.8% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `dropout=0.5` (reported)
- `dropout=0.5, weight_decay=5e-4`
- `dropout=0.5, weight_decay=1e-3`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a code change: @ast:gae/preprocessing.py:32:test_percent=10, @ast:gae/preprocessing.py:32:val_percent=5 | code | 79% | 0.3 sigma (fits every claim) | run with @ast:gae/preprocessing.py:32:test_percent=10, @ast:gae/preprocessing.py:32:val_percent=5 (an in-memory code patch) |
| 2 | a code change: @ast:gae/preprocessing.py:32:test_percent=3 | code | 8% | 0.7 sigma (fits every claim) | run with @ast:gae/preprocessing.py:32:test_percent=3 (an in-memory code patch) |
| 3 | a code change: @ast:gae/preprocessing.py:32:val_percent=2, dropout=0.5, hidden1=320, learning_rate=0.002 | code | 7% | 0.9 sigma (fits every claim) | run with @ast:gae/preprocessing.py:32:val_percent=2, dropout=0.5, hidden1=320, learning_rate=0.002 (an in-memory code patch) |

### History matching (every measured configuration, all claims together)
- 22 of 108 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `@ast:gae/preprocessing.py:32:test_percent, @ast:gae/preprocessing.py:32:val_percent`: @ast:gae/preprocessing.py:32:test_percent=10, @ast:gae/preprocessing.py:32:val_percent=5 (max I 0.31)
  - `@ast:gae/preprocessing.py:32:test_percent`: @ast:gae/preprocessing.py:32:test_percent=3 (max I 0.73); @ast:gae/preprocessing.py:32:test_percent=10 (max I 1.57)
  - `@ast:gae/preprocessing.py:32:val_percent, dropout, hidden1, learning_rate`: @ast:gae/preprocessing.py:32:val_percent=5, dropout=0.5, hidden1=320, learning_rate=0.002 (max I 0.82); @ast:gae/preprocessing.py:32:val_percent=2, dropout=0.5, hidden1=320, learning_rate=0.002 (max I 0.87); @ast:gae/preprocessing.py:32:val_percent=10, dropout=0.5, hidden1=320, learning_rate=0.002 (max I 1.16)
  - `@ast:gae/preprocessing.py:32:test_percent, dropout, hidden1, learning_rate`: @ast:gae/preprocessing.py:32:test_percent=3, dropout=0.5, hidden1=320, learning_rate=0.002 (max I 1); @ast:gae/preprocessing.py:32:test_percent=15, dropout=0.5, hidden1=320, learning_rate=0.002 (max I 1.2); @ast:gae/preprocessing.py:32:test_percent=10, dropout=0.5, hidden1=320, learning_rate=0.002 (max I 1.32)
  - `@ast:gae/preprocessing.py:32:test_percent, @ast:gae/preprocessing.py:32:val_percent, dropout, hidden1, learning_rate`: @ast:gae/preprocessing.py:32:test_percent=10, @ast:gae/preprocessing.py:32:val_percent=5, dropout=0.5, hidden1=320, learning_rate=0.002 (max I 1.5)
- 7 separate islands (no single-knob move joins them): @ast:gae/preprocessing.py:32:val_percent=5, dropout=0.5, hidden1=320, learning_rate=0.002; @ast:gae/preprocessing.py:32:val_percent=2, dropout=0.5, hidden1=320, learning_rate=0.002; @ast:gae/preprocessing.py:32:test_percent=3, dropout=0.5, hidden1=320, learning_rate=0.002 | @ast:gae/preprocessing.py:32:test_percent=10, @ast:gae/preprocessing.py:32:val_percent=5; @ast:gae/preprocessing.py:32:test_percent=3; @ast:gae/preprocessing.py:32:test_percent=10 | hidden1=160, learning_rate=0.002; hidden1=160, learning_rate=0.001; hidden1=320, learning_rate=0.001 | dropout=0.5, hidden1=160
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
  - `gae/preprocessing.py:32`: paper says The validation and test sets contain 5% and 10% of citation links, respectively.; code does test_percent = 30.0 (30%)
  - `gae/preprocessing.py:32`: paper says The validation and test sets contain 5% and 10% of citation links, respectively.; code does val_percent = 20.0 (20%)

Notes:
- weight_decay dropped: with repeats, {'dropout': '0.5', 'weight_decay': '5e-4'} fits {'dropout': '0.5'}'s gap by less than one noise band, so it is not needed
- configurations the target claim can't tell apart from the answer: dropout=0.5; dropout=0.5, weight_decay=5e-4; dropout=0.5, weight_decay=1e-3
- spec knobs no ledger assumption names (epochs, hidden1, hidden2, learning_rate) were screened too; no better answer
- explained with a code patch (tested in memory, no file edited): gae/preprocessing.py line 32: test_percent = 30. -> 10; gae/preprocessing.py line 32: val_percent = 20. -> 5
- @ast:gae/preprocessing.py:32:test_percent: values from 10 to 10 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- @ast:gae/preprocessing.py:32:val_percent: values from 5 to 9 fit every claim (a bisection, 3 runs a side, one run a value: approximate)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `@ast:gae/preprocessing.py:32:test_percent=10`, `@ast:gae/preprocessing.py:32:val_percent=5` | 3 | +0.3% | +0.6% | -0.5% | +0.2% | -0.3% | -0.1% | +0.1% | +0.7% | 0.4% |
| `@ast:gae/preprocessing.py:32:test_percent=10` | 3 | -1.8% | -2.2% | -1.2% | -0.6% | -2.4% | -1.4% | -2.1% | -0.9% | 1.6% |
| `hidden2=1600`, `learning_rate=0.002` | 4 | -1.1% | -1.2% | -0.3% | +0.0% | -6.0% | -3.7% | -0.8% | +1.1% | 1.8% |
| `hidden1=320`, `learning_rate=0.001` | 3 | -3.1% | -2.3% | -0.2% | -0.1% | -4.0% | -2.7% | +0.3% | +2.1% | 1.8% |
| `hidden1=160`, `learning_rate=0.001` | 3 | -2.5% | -2.7% | -0.4% | -0.2% | -3.9% | -2.5% | +0.6% | +2.2% | 1.9% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at gae/train.py:142)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at gae/optimizer.py:37)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CUDA_VISIBLE_DEVICES`, `random_seed`, `mask_test_edges_split`, `negative_sampling`, `positive_edge_reweighting`, `full_batch_training`, `weight_initialization`, `adjacency_diagonal`, `features_handling`, `model`, `dataset`, `sc_embedding_dim`, `dw_embedding_dim`, `dw_random_walks_per_node`, `dw_random_walk_length`, `dw_context_size`, `dw_epochs`, `num_runs_for_error_bars`, `validation_set_usage`, `adam_beta1`, `gaussian_prior`

## Provenance
- GapFinder commit: `f90b212a502334f9d48b56cb5c3d25e25859b4f0` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `dbcbd2dbf2e2187e56c76686bdacdc905e41f32b38b5baa501b118d0fb3b91ff`
- Cost: Nemotron billed $0.0066, sandbox reported $1042.1724 (total $1042.1790; this search; ledger extraction is included only if it shared the search's router)
