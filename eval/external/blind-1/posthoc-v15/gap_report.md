# Gap Report: FastGCN (ICLR 2018), post-hoc on the current code

Artifact `fastgcn` · generated 2026-10-17 18:02 · 200 branch runs (0 build/load setups) · sandbox $53.3560

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_trans_cora_f1 (trans_cora_acc) | Fits but unsupported | -2.3% | -0.5% | ±1.0% | `learning_rate=0.001` |

## C_trans_cora_f1: trans_cora_acc (paper 0.818)
**Fits but unsupported** · gap -2.3% → -0.5% · 94 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0050`, `B0091`, `B0092`, `B0103` (4 run(s) of the same config)
- Config: `learning_rate` naive `0.01`, changed to `0.001`
- Command:

  Replay: fork checkpoint `e6a5358e-5cb8-4cb3-afcb-7190e86cebb7` and run
  ```
  RUN_TAG=c172c98035b2 export GF_SEED_FROM_RUN_TAG=1 OMP_NUM_THREADS=1 TF_CPP_MIN_LOG_LEVEL=2; mkdir -p out; A="--model gcn_mix --learning_rate 0.001 --epochs 100 --hidden1 16 --dropout 0.0 --weight_decay 5e-4 --early_stopping 10 --max_degree 3"; python pubmed-original_transductive_FastGCN.py --dataset cora $A > out/trans_cora.log 2>&1 & python pubmed-original_transductive_FastGCN.py --dataset pubmed $A > out/trans_pubmed.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset cora $A > out/ind_cora.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset pubmed $A > out/ind_pubmed.log 2>&1 & wait; bash gf_harness/emit.sh
  ```
- Output: `trans_cora_acc` 0.816, 0.816, 0.812, 0.804; gap after -0.5%; result checkpoint `c4b9bd65-629f-4f78-b52b-ce2b1f54af22`
- Effect: candidate 0.814 minus naive 0.799 = +0.015, 95% bootstrap interval [+0.0038, +0.02167] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `trans_cora_acc` = 0.818.

### What did we measure?
- Naive median 0.799 over 5 runs; repeats: 0.793, 0.799, 0.802, 0.793, 0.802
- Spread: range 0.793 to 0.802, noise band ±0.00799 (2 x MAD), CV 0.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.3% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `learning_rate` the gap is -2.3% (it comes back)
- PASS · Held-out claim: C_trans_pubmed_f1: +0.0% to -1.0% (not worse beyond noise)
- NOTE · Held-out claim, tuned separately: C_ind_cora_f1: -1.7% to -14.2% (worse beyond noise; reported, not a constraint)
- NOTE · Held-out claim, tuned separately: C_ind_pubmed_f1: +0.3% to -4.2% (worse beyond noise; reported, not a constraint)
- PASS · Evidence: `learning_rate=0.001`: paper evidence at paper text: 'We swept learning rate in the set {0.01, 0.001, 0.0001}.'
- PASS · Effect vs noise: candidate minus naive is +0.015 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=5000`, `epochs=10000`
- Not settable with this harness: `rank1 (sample size top layer)`, `Hardware (CPU/GPU, memory)`, `batchsize (iterate_minibatches_listinputs)`, `precompute AH(0) (bottom layer precomputation)`, `GraphSAGE implementation (TensorFlow vs PyTorch)`, `Number of GCN layers (1 vs 2)`, `TensorFlow version / GraphSAGE version compatibility`, `Micro F1 score computation (metrics.py)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `learning_rate=0.002` (2.13 noise units, gap -0.2%); `weight_decay=5e-05` (1.75 noise units, gap -0.6%); `epochs=50` (1.63 noise units, gap -0.7%); `epochs=10` (1.5 noise units, gap -0.9%); `epochs=20` (1.13 noise units, gap -1.2%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `epochs=50`, `early_stopping=2`: this claim -1.6%, mean |gap| 1.1% (2 runs)
  - `hidden1=32`, `learning_rate=0.002`: this claim -0.6%, mean |gap| 1.4% (3 runs)
  - `epochs=50`: this claim -1.3%, mean |gap| 1.5% (4 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `learning_rate, max_degree`: learning_rate=0.002, max_degree=300 (max I 0.06); learning_rate=0.001, max_degree=30 (max I 0.14)
  - `epochs, weight_decay`: epochs=10, weight_decay=5e-05 (max I 0.07)
  - `epochs, learning_rate`: epochs=50, learning_rate=0.001 (max I 0.1)
  - `epochs`: epochs=20 (max I 0.13)
  - `early_stopping, learning_rate`: early_stopping=1, learning_rate=0.002 (max I 0.15)
  - `epochs, max_degree`: epochs=10, max_degree=300 (max I 0.19)
  - `learning_rate`: learning_rate=0.002 (max I 0.2); learning_rate=0.001 (max I 0.2)
  - `hidden1, learning_rate`: hidden1=32, learning_rate=0.002 (max I 0.2)

Notes:
- stopped early: run budget of 200 reached (wanted 1 more run(s) of {'epochs': '50', 'early_stopping': '2'} for 'confirm-combo')
- C_ind_cora_f1 (tuned separately) moves from -1.7% to -14.2% under {'learning_rate': '0.001'}: reported, not a rejection
- C_ind_pubmed_f1 (tuned separately) moves from +0.3% to -4.2% under {'learning_rate': '0.001'}: reported, not a rejection
- verified from runs already made, after the budget ran out
- found after adding spec knobs no ledger assumption names (learning_rate, epochs, weight_decay, early_stopping, max_degree)
- capped at Fits but unsupported (was Explained): the run budget ran out before the search finished

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_trans_cora_f1 | C_trans_pubmed_f1 | C_ind_cora_f1 | C_ind_pubmed_f1 | Mean |gap| |
|---|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | -2.3% | +0.0% | -1.7% | +0.3% | 1.1% |
| `epochs=50`, `early_stopping=2` | 2 | -1.6% | -0.7% | -1.6% | -0.5% | 1.1% |
| `hidden1=32`, `learning_rate=0.002` | 3 | -0.6% | -1.0% | -1.7% | -2.2% | 1.4% |
| `epochs=50` | 4 | -1.3% | -0.6% | -3.4% | +0.6% | 1.5% |
| `hidden1=32` | 4 | -3.1% | +0.0% | -2.1% | +0.8% | 1.5% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=5000`, `epochs=10000`

## Knob names
- Ledger names mapped to spec knobs: `FLAGS.hidden1` → `hidden1`
- Screened though no assumption named them (low prior, code-derived values): `learning_rate`, `epochs`, `weight_decay`, `early_stopping`, `max_degree`
- Code defaults read from the code instead of the ledger: `hidden1` 16 at pubmed-original_inductive_FastGCN.py:24 (ledger said 16 (train.py:22), 128 (train_batch_multiRank_inductive_reddit_Mixlayers_sampleA.py:26))

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at pubmed-original_transductive_FastGCN.py:139)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at models.py:58)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `rank1 (sample size top layer)`, `Hardware (CPU/GPU, memory)`, `batchsize (iterate_minibatches_listinputs)`, `precompute AH(0) (bottom layer precomputation)`, `GraphSAGE implementation (TensorFlow vs PyTorch)`, `Number of GCN layers (1 vs 2)`, `TensorFlow version / GraphSAGE version compatibility`, `Micro F1 score computation (metrics.py)`

## Provenance
- GapFinder commit: `6365f5307de6d92dfb5d09f6eae1b52cad19914f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `c2810806b1b6e50bd7fc247355944c60e0aa6c7575426c89ef41c58ac0219c5f`
- Cost: Nemotron billed $0.0000, sandbox reported $53.3560 (total $53.3560; this search; ledger extraction is included only if it shared the search's router)
