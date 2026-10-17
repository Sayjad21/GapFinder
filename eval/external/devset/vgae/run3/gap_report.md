# Gap Report: VGAE (Kipf & Welling 2016), devset

Artifact `vgae` · generated 2026-10-17 21:19 · 168 branch runs (0 build/load setups) · sandbox $647.8417

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Paper-artifact inconsistency | -5.8% | +0.4% | ±0.9% | `@ast:gae/preprocessing.py:32:test_percent=10`, `@ast:gae/preprocessing.py:32:val_percent=5` |

## C_vgae_cora_auc: vgae_cora_auc (paper 91.4)
**Paper-artifact inconsistency** · gap -5.8% → +0.4% · 83 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0112`, `B0118`, `B0119` (3 run(s) of the same config)
- Config: `@ast:gae/preprocessing.py:32:test_percent` naive `30.`, changed to `10`
- Config: `@ast:gae/preprocessing.py:32:val_percent` naive `20.`, changed to `5`
- Command:

  Replay: fork checkpoint `b87946e7-74f5-4d81-bf4d-f55f3eafc206` and run
  ```
  @ast:gae/preprocessing.py:32:test_percent=10 @ast:gae/preprocessing.py:32:val_percent=5 RUN_TAG=82dc62d68c36 export PYTHONPATH="${WORK:-$PWD}/.gf_patch${PYTHONPATH:+:$PYTHONPATH}"; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=2; mkdir -p out; A="--learning_rate 0.01 --epochs 200 --hidden1 32 --hidden2 16 --weight_decay 0.0 --dropout 0.0 --features 1"; cd gae; for ds in cora citeseer; do PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_vae --dataset $ds $A > ../out/vgae_$ds.log 2>&1 & PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_ae --dataset $ds $A > ../out/gae_$ds.log 2>&1 & wait; done; cd ..; bash gf_harness/emit.sh
  ```
- Output: `vgae_cora_auc` 90.6, 91.74, 92.81; gap after +0.4%; result checkpoint `878dcec0-032b-4128-8b3a-8c20ee2f111d`
- Effect: candidate 91.74 minus naive 86.06 = +5.686, 95% bootstrap interval [+4.474, +7.22] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 91.4.

### What did we measure?
- Naive median 86.06 over 5 runs; repeats: 86.06, 85.91, 86.17, 86.2, 84.9
- Spread: range 84.9 to 86.2, noise band ±0.8606 (2 x MAD), CV 0.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -5.8% (noise band ±0.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `@ast:gae/preprocessing.py:32:test_percent` the gap is -3.3% (it comes back)
- PASS · Counterfactual (reversal test): without `@ast:gae/preprocessing.py:32:val_percent` the gap is -2.2% (it comes back)
- PASS · Held-out claim: C_vgae_cora_ap: -4.8% to +0.8% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_auc: -3.5% to -1.3% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_ap: -2.6% to -1.1% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_auc: -6.5% to +0.6% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_ap: -4.9% to +1.1% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_auc: -6.0% to -0.5% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_ap: -3.8% to +0.1% (not worse beyond noise)
- PASS · Evidence: `@ast:gae/preprocessing.py:32:test_percent=10`: paper states '10'
- PASS · Evidence: `@ast:gae/preprocessing.py:32:val_percent=5`: paper states '5'
- PASS · Effect vs noise: candidate minus naive is +5.686 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: `CUDA_VISIBLE_DEVICES`, `random_seed`, `mask_test_edges_split`, `negative_sampling`, `positive_edge_reweighting`, `full_batch_training`, `weight_initialization`, `adjacency_diagonal`, `features_handling`, `model`, `dataset`, `sc_embedding_dim`, `dw_embedding_dim`, `dw_random_walks_per_node`, `dw_random_walk_length`, `dw_context_size`, `dw_epochs`, `num_runs_for_error_bars`, `validation_set_usage`, `adam_beta1`, `gaussian_prior`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `dropout=0.5` (3.97 noise units, gap -2.1%); `dropout=0.2` (1.53 noise units, gap -4.4%); `weight_decay=5e-4` (1.13 noise units, gap -4.8%)
- Near alternatives (closest across all claims):
  - `learning_rate=0.002`, `hidden1=320`, `hidden2=1600`, `dropout=0.5`: this claim -0.1%, mean |gap| 1.0% (3 runs)
  - `@ast:gae/preprocessing.py:32:test_percent=10`: this claim -2.2%, mean |gap| 1.2% (3 runs)
  - `learning_rate=0.001`, `hidden2=800`: this claim -1.8%, mean |gap| 1.8% (3 runs)

### History matching (every measured configuration, all claims together)
- 10 of 93 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `@ast:gae/preprocessing.py:32:test_percent, @ast:gae/preprocessing.py:32:val_percent`: @ast:gae/preprocessing.py:32:test_percent=10, @ast:gae/preprocessing.py:32:val_percent=5 (max I 1.17)
  - `@ast:gae/preprocessing.py:32:test_percent`: @ast:gae/preprocessing.py:32:test_percent=10 (max I 1.75)
  - `dropout, hidden1, hidden2, learning_rate`: dropout=0.5, hidden1=320, hidden2=1600, learning_rate=0.002 (max I 1.97)
  - `@ast:gae/preprocessing.py:32:test_percent, dropout, hidden1, hidden2, learning_rate`: @ast:gae/preprocessing.py:32:test_percent=10, dropout=0.5, hidden1=320, hidden2=1600, learning_rate=0.002 (max I 2.01)
  - `@ast:gae/preprocessing.py:32:val_percent, dropout, hidden1, hidden2, learning_rate`: @ast:gae/preprocessing.py:32:val_percent=5, dropout=0.5, hidden1=320, hidden2=1600, learning_rate=0.002 (max I 2.41)
  - `@ast:gae/preprocessing.py:32:test_percent, @ast:gae/preprocessing.py:32:val_percent, dropout, hidden1, hidden2, learning_rate`: @ast:gae/preprocessing.py:32:test_percent=10, @ast:gae/preprocessing.py:32:val_percent=5, dropout=0.5, hidden1=320, hidden2=1600, learning_rate=0.002 (max I 2.57)
  - `learning_rate`: learning_rate=0.002 (max I 2.68)
  - `hidden1, learning_rate`: hidden1=320, learning_rate=0.001 (max I 2.76)
  - `@ast:gae/preprocessing.py:32:val_percent`: @ast:gae/preprocessing.py:32:val_percent=5 (max I 2.89)
  - `learning_rate, weight_decay`: learning_rate=0.002, weight_decay=1e-3 (max I 2.94)
- 4 separate islands (no single-knob move joins them): dropout=0.5, hidden1=320, hidden2=1600, learning_rate=0.002; @ast:gae/preprocessing.py:32:test_percent=10, dropout=0.5, hidden1=320, hidden2=1600, learning_rate=0.002; @ast:gae/preprocessing.py:32:val_percent=5, dropout=0.5, hidden1=320, hidden2=1600, learning_rate=0.002 | @ast:gae/preprocessing.py:32:test_percent=10, @ast:gae/preprocessing.py:32:val_percent=5; @ast:gae/preprocessing.py:32:test_percent=10; @ast:gae/preprocessing.py:32:val_percent=5 | learning_rate=0.002; learning_rate=0.002, weight_decay=1e-3 | hidden1=320, learning_rate=0.001
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `mask_test_edges(..., test_percent=30)`: a default no call in the repo overrides (1 call(s)) (`gae/preprocessing.py:32`)
  - unexposed setting: `mask_test_edges(..., val_percent=20)`: a default no call in the repo overrides (1 call(s)) (`gae/preprocessing.py:32`)
- Where the code differs from the paper (model-proposed, checked against the repo; literal ones were tried as patch knobs, structural ones are not tested):
  - `gae/preprocessing.py:32`: paper says The validation and test sets contain 5% and 10% of citation links, respectively.; code does test_percent = 30.0
  - `gae/preprocessing.py:32`: paper says The validation and test sets contain 5% and 10% of citation links, respectively.; code does val_percent = 20.0

Notes:
- {'dropout': '0.5'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'dropout': '0.5'} (gap -2.6%); it did not pass verification
- spec knobs no ledger assumption names (epochs, hidden1, hidden2, learning_rate) were screened too; no better answer
- history matching: 4 of 87 tested configurations fit every claim within 3 sigma
- explained with a code patch (tested in memory, no file edited): gae/preprocessing.py line 32: test_percent = 30. -> 10; gae/preprocessing.py line 32: val_percent = 20. -> 5

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `@ast:gae/preprocessing.py:32:test_percent=10`, `@ast:gae/preprocessing.py:32:val_percent=5` | 3 | +0.4% | +0.8% | -1.3% | -1.1% | +0.6% | +1.1% | -0.5% | +0.1% | 0.7% |
| `learning_rate=0.002`, `hidden1=320`, `hidden2=1600`, `dropout=0.5` | 3 | -0.1% | +0.2% | -0.4% | +0.3% | -2.9% | -1.3% | -2.8% | -0.3% | 1.0% |
| `@ast:gae/preprocessing.py:32:test_percent=10` | 3 | -2.2% | -1.9% | -0.8% | -0.3% | -2.6% | -1.7% | +0.2% | -0.4% | 1.2% |
| `learning_rate=0.001`, `hidden2=800` | 3 | -1.8% | -2.8% | +0.3% | +0.3% | -4.4% | -2.6% | -0.3% | +1.8% | 1.8% |
| `hidden1=320`, `dropout=0.2` | 2 | -4.0% | -3.3% | -0.7% | -0.4% | -3.5% | -2.4% | +1.2% | +2.2% | 2.2% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at gae/train.py:142)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at gae/optimizer.py:37)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CUDA_VISIBLE_DEVICES`, `random_seed`, `mask_test_edges_split`, `negative_sampling`, `positive_edge_reweighting`, `full_batch_training`, `weight_initialization`, `adjacency_diagonal`, `features_handling`, `model`, `dataset`, `sc_embedding_dim`, `dw_embedding_dim`, `dw_random_walks_per_node`, `dw_random_walk_length`, `dw_context_size`, `dw_epochs`, `num_runs_for_error_bars`, `validation_set_usage`, `adam_beta1`, `gaussian_prior`

## Provenance
- GapFinder commit: `cf2b9fa3e8dafec5ffeba134fce0c0bf84a72714` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `5d7b1bee707daf8d9d8eda686aff0492255f658ab841b7dba10916b8b91f86c0`
- Cost: Nemotron billed $0.0018, sandbox reported $647.8417 (total $647.8434; this search; ledger extraction is included only if it shared the search's router)
