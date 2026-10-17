# Gap Report: VGAE (Kipf & Welling 2016), devset

Artifact `vgae` · generated 2026-10-17 19:15 · 120 branch runs (0 build/load setups) · sandbox $425.6390

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Fits but unsupported | -5.8% | -1.6% | ±0.9% | `hidden1=320`, `dropout=0.5`, `learning_rate=0.002` |

## C_vgae_cora_auc: vgae_cora_auc (paper 91.4)
**Fits but unsupported** · gap -5.8% → -1.6% · 66 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0053`, `B0091`, `B0115` (3 run(s) of the same config)
- Config: `hidden1` naive `32`, changed to `320`
- Config: `dropout` naive `0.0`, changed to `0.5`
- Config: `learning_rate` naive `0.01`, changed to `0.002`
- Command:

  Replay: fork checkpoint `b87946e7-74f5-4d81-bf4d-f55f3eafc206` and run
  ```
  RUN_TAG=8088e64b9e02 export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=2; mkdir -p out; A="--learning_rate 0.002 --epochs 200 --hidden1 320 --hidden2 16 --weight_decay 0.0 --dropout 0.5 --features 1"; cd gae; for ds in cora citeseer; do PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_vae --dataset $ds $A > ../out/vgae_$ds.log 2>&1 & PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_ae --dataset $ds $A > ../out/gae_$ds.log 2>&1 & wait; done; cd ..; bash gf_harness/emit.sh
  ```
- Output: `vgae_cora_auc` 90.33, 89.49, 89.93; gap after -1.6%; result checkpoint `67c43b27-ff3a-49fb-a4d8-40219bed7914`
- Effect: candidate 89.93 minus naive 86.06 = +3.869, 95% bootstrap interval [+3.164, +4.529] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 91.4.

### What did we measure?
- Naive median 86.06 over 5 runs; repeats: 86.06, 86.31, 85.49, 85.8, 86.6
- Spread: range 85.49 to 86.6, noise band ±0.8607 (2 x MAD), CV 0.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -5.8% (noise band ±0.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `hidden1` the gap is -6.2% (it comes back)
- PASS · Counterfactual (reversal test): without `dropout` the gap is -6.0% (it comes back)
- PASS · Counterfactual (reversal test): without `learning_rate` the gap is -3.9% (it comes back)
- PASS · Held-out claim: C_vgae_cora_ap: -4.7% to -1.8% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_auc: -3.9% to -3.0% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_citeseer_ap: -3.2% to -2.8% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_auc: -6.2% to -2.8% (not worse beyond noise)
- PASS · Held-out claim: C_gae_cora_ap: -4.9% to -2.2% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_auc: -5.6% to -2.4% (not worse beyond noise)
- PASS · Held-out claim: C_gae_citeseer_ap: -4.0% to -1.2% (not worse beyond noise)
- FAIL · Evidence: `hidden1=320`: no evidence mentions '320'; it fits, but nothing says the authors used it
- FAIL · Evidence: `dropout=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- FAIL · Evidence: `learning_rate=0.002`: no evidence mentions '0.002'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +3.869 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: `CUDA_VISIBLE_DEVICES`, `random_seed`, `mask_test_edges_split`, `negative_sampling`, `positive_edge_reweighting`, `full_batch_training`, `weight_initialization`, `adjacency_diagonal`, `features_handling`, `model`, `dataset`, `sc_embedding_dim`, `dw_embedding_dim`, `dw_random_walks_per_node`, `dw_random_walk_length`, `dw_context_size`, `dw_epochs`, `num_runs_for_error_bars`, `validation_set_usage`, `adam_beta1`, `gaussian_prior`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `learning_rate=0.001` (2.52 noise units, gap -3.5%); `dropout=0.2` (1.27 noise units, gap -4.6%); `epochs=100` (1.15 noise units, gap -4.8%); `learning_rate=0.005` (1.09 noise units, gap -4.8%)
- Near alternatives (closest across all claims):
  - `hidden1=320`, `learning_rate=0.001`: this claim -3.7%, mean |gap| 1.9% (2 runs)
  - `learning_rate=0.001`, `hidden1=64`: this claim -3.9%, mean |gap| 2.0% (2 runs)
  - `learning_rate=0.002`, `hidden1=64`: this claim -3.6%, mean |gap| 2.3% (3 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `dropout, hidden1, learning_rate`: dropout=0.5, hidden1=320, learning_rate=0.002 (max I 0.58)
  - `epochs, hidden1`: epochs=100, hidden1=320 (max I 0.68)
  - `hidden1, learning_rate`: hidden1=64, learning_rate=0.001 (max I 0.78); hidden1=320, learning_rate=0.001 (max I 0.81)
  - `dropout, hidden1`: dropout=0.5, hidden1=320 (max I 0.79); dropout=0.5, hidden1=64 (max I 0.85)
  - `dropout, learning_rate`: dropout=0.2, learning_rate=0.002 (max I 0.8)
  - `learning_rate`: learning_rate=0.002 (max I 0.81)
  - `learning_rate, weight_decay`: learning_rate=0.002, weight_decay=1e-3 (max I 0.83)
  - `dropout`: dropout=0.5 (max I 0.85)

Notes:
- stopped early: run budget of 120 reached (wanted 1 more run(s) of {'learning_rate': '0.001', 'hidden1': '320'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `hidden1=320`, `learning_rate=0.001` | 2 | -3.7% | -2.8% | -0.1% | +0.2% | -4.1% | -2.5% | +0.5% | +1.7% | 1.9% |
| `learning_rate=0.001`, `hidden1=64` | 2 | -3.9% | -3.9% | -0.9% | -1.2% | -2.7% | -1.7% | +0.2% | +1.3% | 2.0% |
| `hidden1=320`, `dropout=0.5`, `learning_rate=0.002` | 3 | -1.6% | -1.8% | -3.0% | -2.8% | -2.8% | -2.2% | -2.4% | -1.2% | 2.2% |
| `learning_rate=0.002`, `hidden1=64` | 3 | -3.6% | -3.3% | -1.0% | -0.6% | -4.4% | -3.4% | +0.3% | +1.6% | 2.3% |
| `hidden1=320`, `epochs=100` | 3 | -3.8% | -2.8% | -2.2% | -1.8% | -3.2% | -2.1% | +0.9% | +1.8% | 2.3% |

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
- Harness spec sha256: `524bd1c6d64bb45d4387789d865ca4ef736f9a737727e6da5c053592ce0b44d5`
- Cost: Nemotron billed $0.0000, sandbox reported $425.6390 (total $425.6390; this search; ledger extraction is included only if it shared the search's router)
