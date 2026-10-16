# Gap Report: FastGCN (ICLR 2018), post-hoc

Artifact `fastgcn` · generated 2026-10-16 06:56 · 45 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_trans_cora_f1 (trans_cora_acc) | Explained | -2.3% | -0.2% | ±1.0% | `learning_rate=0.001` |

## C_trans_cora_f1: trans_cora_acc (paper 0.818)
**Explained** · gap -2.3% → -0.2% · 10 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0017`, `B0016`, `B0037` (4 run(s) of the same config)
- Config: `learning_rate` naive `0.01`, changed to `0.001`
- Command:

  Replay: fork checkpoint `e6a5358e-5cb8-4cb3-afcb-7190e86cebb7` and run
  ```
  RUN_TAG=029cacfa3012 export GF_SEED_FROM_RUN_TAG=1 OMP_NUM_THREADS=1 TF_CPP_MIN_LOG_LEVEL=2; mkdir -p out; A="--model gcn_mix --learning_rate 0.001 --epochs 100 --hidden1 16 --dropout 0.0 --weight_decay 5e-4 --early_stopping 10 --max_degree 3"; python pubmed-original_transductive_FastGCN.py --dataset cora $A > out/trans_cora.log 2>&1 & python pubmed-original_transductive_FastGCN.py --dataset pubmed $A > out/trans_pubmed.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset cora $A > out/ind_cora.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset pubmed $A > out/ind_pubmed.log 2>&1 & wait; bash gf_harness/emit.sh
  ```
- Output: `trans_cora_acc` 0.809, 0.817, 0.816, 0.82; gap after -0.2%; result checkpoint `3e22a8c2-3bb0-4e63-ae65-d8d9e62f7640`
- Effect: candidate 0.8165 minus naive 0.799 = +0.0175, 95% bootstrap interval [+0.01133, +0.022] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `trans_cora_acc` = 0.818.

### What did we measure?
- Naive median 0.799 over 5 runs; repeats: 0.805, 0.805, 0.798, 0.799, 0.797
- Spread: range 0.797 to 0.805, noise band ±0.00799 (2 x MAD), CV 0.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.3% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `learning_rate` the gap is -2.3% (it comes back)
- PASS · Held-out claim: C_trans_pubmed_f1: -0.5% to -0.8% (not worse beyond noise)
- PASS · Evidence: `learning_rate=0.001`: paper states 'selected from {0.01, 0.001, 0.0001} via hyperparameter selection'
- PASS · Effect vs noise: candidate minus naive is +0.0175 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `sample_size_layer1`, `sampling_method`, `cpu_model`, `hidden_dim`, `graphsage_sample_size_1`, `graphsage_sample_size_2`, `precompute_AH0`, `dataset_split`, `framework`, `sample_size_layer2`, `dropout_rate`, `graphsage_aggregator`, `gcn_batched`, `graphsage_new_implementation`, `graphsage_hidden_dim`, `num_epochs`, `ram_size`, `weight_initialization`, `feature_normalization`, `validation_test_indices`, `optimizer`, `random_seed`, `early_stopping_patience`, `activation_function`, `gradient_clipping`, `num_layers`, `loss_function`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `learning_rate=0.002` (1.94 noise units, gap -0.4%); `learning_rate=0.005` (1.25 noise units, gap -1.1%)
- Near alternatives (closest across all claims):
  - `learning_rate=0.005`: this claim -1.1%, mean |gap| 0.9% (4 runs)
  - `learning_rate=0.002`: this claim -0.4%, mean |gap| 0.9% (4 runs)
  - `learning_rate=0.02`: this claim -9.5%, mean |gap| 5.0% (4 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `learning_rate=0.001` (reported)
- `learning_rate=0.002`
- `learning_rate=0.005`

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `learning_rate`: learning_rate=0.001 (max I 0.17); learning_rate=0.002 (max I 0.2); learning_rate=0.005 (max I 0.22); learning_rate=0.05 (max I 2.38); +2 more
- Equally good values: `learning_rate` in {0.001, 0.002, 0.005}

Notes:
- configurations the target claim can't tell apart from the answer: learning_rate=0.001; learning_rate=0.002; learning_rate=0.005
- equally good values within one noise band (measured): learning_rate in {0.001, 0.002, 0.005}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_trans_cora_f1 | C_trans_pubmed_f1 | Mean |gap| |
|---|---|---|---|---|
| `learning_rate=0.001` | 4 | -0.2% | -0.8% | 0.5% |
| `learning_rate=0.005` | 4 | -1.1% | -0.6% | 0.9% |
| `learning_rate=0.002` | 4 | -0.4% | -1.4% | 0.9% |
| naive (reproduction as run) | 5 | -2.3% | -0.5% | 1.4% |
| `learning_rate=0.02` | 4 | -9.5% | -0.5% | 5.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `sample_size_layer1`, `sampling_method`, `cpu_model`, `hidden_dim`, `graphsage_sample_size_1`, `graphsage_sample_size_2`, `precompute_AH0`, `dataset_split`, `framework`, `sample_size_layer2`, `dropout_rate`, `graphsage_aggregator`, `gcn_batched`, `graphsage_new_implementation`, `graphsage_hidden_dim`, `num_epochs`, `ram_size`, `weight_initialization`, `feature_normalization`, `validation_test_indices`, `optimizer`, `random_seed`, `early_stopping_patience`, `activation_function`, `gradient_clipping`, `num_layers`, `loss_function`

## Provenance
- GapFinder commit: `270a7170323f45eb66c63be1e32ceb3fa5c12a56` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `4d3799ddae0a330bf539ca061f485232f4dfb3a8433e533746d248417f200a09`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
