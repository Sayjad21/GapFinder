# Gap Report: VGAE (Kipf & Welling 2016), devset

Artifact `vgae` · generated 2026-10-17 19:57 · 165 branch runs (0 build/load setups) · sandbox $381.3639

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Fits but unsupported | -5.8% | -1.5% | ±0.9% | `hidden2=1600`, `learning_rate=0.002` |

## C_vgae_cora_auc: vgae_cora_auc (paper 91.4)
**Fits but unsupported** · gap -5.8% → -1.5% · 71 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0027`, `B0031`, `B0039` (3 run(s) of the same config)
- Config: `hidden2` naive `16`, changed to `1600`
- Config: `learning_rate` naive `0.01`, changed to `0.002`
- Command:

  Replay: fork checkpoint `b87946e7-74f5-4d81-bf4d-f55f3eafc206` and run
  ```
  RUN_TAG=43ae2a1f1ef8 export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=2; mkdir -p out; A="--learning_rate 0.002 --epochs 200 --hidden1 32 --hidden2 1600 --weight_decay 0.0 --dropout 0.0 --features 1"; cd gae; for ds in cora citeseer; do PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_vae --dataset $ds $A > ../out/vgae_$ds.log 2>&1 & PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_ae --dataset $ds $A > ../out/gae_$ds.log 2>&1 & wait; done; cd ..; bash gf_harness/emit.sh
  ```
- Output: `vgae_cora_auc` 90.05, 91.29, 89.72; gap after -1.5%; result checkpoint `ecfe950a-9441-4634-9993-92d31fc39025`
- Effect: candidate 90.05 minus naive 86.06 = +3.989, 95% bootstrap interval [+3.351, +5.461] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 91.4.

### What did we measure?
- Naive median 86.06 over 5 runs; repeats: 85.8, 86.31, 85.49, 86.6, 86.06
- Spread: range 85.49 to 86.6, noise band ±0.8607 (2 x MAD), CV 0.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -5.8% (noise band ±0.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `hidden2` the gap is -3.8% (it comes back)
- PASS · Counterfactual (reversal test): without `learning_rate` the gap is -4.1% (it comes back)
- PASS · Held-out claim: C_vgae_cora_ap: -4.7% to -1.6% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_auc: -3.9% to -1.5% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_ap: -3.2% to -0.8% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_auc: -6.2% to -6.5% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_ap: -4.9% to -4.4% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_auc: -5.6% to -1.6% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_ap: -4.0% to +0.8% (not worse beyond noise)
- FAIL · Evidence: `hidden2=1600`: no evidence mentions '1600'; it fits, but nothing says the authors used it
- FAIL · Evidence: `learning_rate=0.002`: no evidence mentions '0.002'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +3.989 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: `CUDA_VISIBLE_DEVICES`, `random_seed`, `mask_test_edges_split`, `negative_sampling`, `positive_edge_reweighting`, `full_batch_training`, `weight_initialization`, `adjacency_diagonal`, `features_handling`, `model`, `dataset`, `sc_embedding_dim`, `dw_embedding_dim`, `dw_random_walks_per_node`, `dw_random_walk_length`, `dw_context_size`, `dw_epochs`, `num_runs_for_error_bars`, `validation_set_usage`, `adam_beta1`, `gaussian_prior`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `dropout=0.5` (3.17 noise units, gap -2.9%); `hidden2=800` (2.3 noise units, gap -3.7%); `learning_rate=0.001` (1.76 noise units, gap -4.2%); `hidden1=320` (1.13 noise units, gap -4.8%)
- Near alternatives (closest across all claims):
  - `learning_rate=0.001`, `hidden2=800`: this claim -1.8%, mean |gap| 1.8% (3 runs)
  - `hidden1=320`, `learning_rate=0.001`: this claim -2.5%, mean |gap| 1.8% (3 runs)
  - `hidden1=64`, `learning_rate=0.001`: this claim -3.9%, mean |gap| 2.0% (2 runs)

### Equally good configurations
The target claim can't tell these 7 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `hidden2=1600, learning_rate=0.002` (reported)
- `dropout=0.5`
- `hidden2=800, learning_rate=0.002`
- `hidden2=800, learning_rate=0.001`
- `dropout=0.5, hidden2=800`
- `hidden1=320, learning_rate=0.001`
- `dropout=0.5, hidden2=1600`

### History matching (every measured configuration, all claims together)
- 2 of 89 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 2 configurations
  - `dropout, hidden1, learning_rate`: dropout=0.5, hidden1=320, learning_rate=0.002 (max I 2.48)
  - `epochs, hidden1`: epochs=100, hidden1=320 (max I 2.98)
- 2 separate islands (no single-knob move joins them): dropout=0.5, hidden1=320, learning_rate=0.002 | epochs=100, hidden1=320
- Equally good values: `hidden2` in {800, 1600}

Notes:
- configurations the target claim can't tell apart from the answer: hidden2=1600, learning_rate=0.002; dropout=0.5; hidden2=800, learning_rate=0.002; hidden2=800, learning_rate=0.001; dropout=0.5, hidden2=800; hidden1=320, learning_rate=0.001; dropout=0.5, hidden2=1600
- equally good values within one noise band (measured): hidden2 in {800, 1600}
- found after adding spec knobs no ledger assumption names (epochs, hidden1, hidden2, learning_rate)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `learning_rate=0.001`, `hidden2=800` | 3 | -1.8% | -2.8% | +0.3% | +0.3% | -4.4% | -2.6% | -0.3% | +1.8% | 1.8% |
| `hidden1=320`, `learning_rate=0.001` | 3 | -2.5% | -1.8% | -0.2% | -0.1% | -4.2% | -3.1% | +0.9% | +2.0% | 1.8% |
| `hidden1=64`, `learning_rate=0.001` | 2 | -3.9% | -3.9% | -0.9% | -1.2% | -2.7% | -1.7% | +0.2% | +1.3% | 2.0% |
| `dropout=0.5`, `hidden1=320`, `learning_rate=0.002` | 3 | -1.6% | -1.8% | -3.0% | -2.8% | -2.8% | -2.2% | -2.4% | -1.2% | 2.2% |
| `hidden1=64`, `learning_rate=0.002` | 3 | -3.6% | -3.3% | -1.0% | -0.6% | -4.4% | -3.4% | +0.3% | +1.6% | 2.3% |

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
- Harness spec sha256: `15f7c737773fb5129b275e6b7100f9bf5d82d644e623da0f49326611b9d2b1c6`
- Cost: Nemotron billed $0.0000, sandbox reported $381.3639 (total $381.3639; this search; ledger extraction is included only if it shared the search's router)
