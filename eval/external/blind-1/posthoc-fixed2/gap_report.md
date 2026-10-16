# Gap Report: FastGCN (ICLR 2018), post-hoc with the blind-1 fixes

Artifact `fastgcn` · generated 2026-10-16 13:35 · 161 branch runs (0 build/load setups) · sandbox $16.1874

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_trans_cora_f1 (trans_cora_acc) | Explained | -2.4% | +0.3% | ±1.0% | `learning_rate=0.001` |

## C_trans_cora_f1: trans_cora_acc (paper 0.818)
**Explained** · gap -2.4% → +0.3% · 76 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0042`, `B0051`, `B0052`, `B0053` (4 run(s) of the same config)
- Config: `learning_rate` naive `0.01`, changed to `0.001`
- Command:

  Replay: fork checkpoint `e6a5358e-5cb8-4cb3-afcb-7190e86cebb7` and run
  ```
  RUN_TAG=645973539fb4 export GF_SEED_FROM_RUN_TAG=1 OMP_NUM_THREADS=1 TF_CPP_MIN_LOG_LEVEL=2; mkdir -p out; A="--model gcn_mix --learning_rate 0.001 --epochs 100 --hidden1 16 --dropout 0.0 --weight_decay 5e-4 --early_stopping 10 --max_degree 3"; python pubmed-original_transductive_FastGCN.py --dataset cora $A > out/trans_cora.log 2>&1 & python pubmed-original_transductive_FastGCN.py --dataset pubmed $A > out/trans_pubmed.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset cora $A > out/ind_cora.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset pubmed $A > out/ind_pubmed.log 2>&1 & wait; bash gf_harness/emit.sh
  ```
- Output: `trans_cora_acc` 0.82, 0.823, 0.814, 0.821; gap after +0.3%; result checkpoint `c2d3a9a4-ecc9-4420-95be-bb0f40705c38`
- Effect: candidate 0.8205 minus naive 0.798 = +0.0225, 95% bootstrap interval [+0.0122, +0.0254] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `trans_cora_acc` = 0.818.

### What did we measure?
- Naive median 0.798 over 5 runs; repeats: 0.798, 0.804, 0.802, 0.798, 0.797
- Spread: range 0.797 to 0.804, noise band ±0.00798 (2 x MAD), CV 0.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.4% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `learning_rate` the gap is -2.4% (it comes back)
- PASS · Held-out claim: C_trans_pubmed_f1: -0.4% to -0.7% (not worse beyond noise)
- NOTE · Held-out claim, tuned separately: C_ind_cora_f1: -3.0% to -10.5% (worse beyond noise; reported, not a constraint)
- NOTE · Held-out claim, tuned separately: C_ind_pubmed_f1: +0.4% to -8.7% (worse beyond noise; reported, not a constraint)
- PASS · Evidence: `learning_rate=0.001`: paper evidence at paper text: 'We swept learning rate in the set {0.01, 0.001, 0.0001}.'
- PASS · Effect vs noise: candidate minus naive is +0.0225 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=5000`, `epochs=10000`
- Not settable with this harness: `rank1 (sample size top layer)`, `Hardware (CPU/GPU, memory)`, `batchsize (iterate_minibatches_listinputs)`, `precompute AH(0) (bottom layer precomputation)`, `GraphSAGE implementation (TensorFlow vs PyTorch)`, `Number of GCN layers (1 vs 2)`, `TensorFlow version / GraphSAGE version compatibility`, `Micro F1 score computation (metrics.py)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `learning_rate=0.002` (2.51 noise units, gap +0.0%); `epochs=10` (2.19 noise units, gap -0.3%); `epochs=20` (1.63 noise units, gap -0.9%); `epochs=50` (1.07 noise units, gap -1.4%); `early_stopping=2` (1 noise units, gap -1.5%)
- Near alternatives (closest across all claims):
  - `learning_rate=0.002`, `early_stopping=1000`: this claim +0.4%, mean |gap| 1.2% (3 runs)
  - `epochs=50`: this claim -1.4%, mean |gap| 1.3% (4 runs)
  - `hidden1=32`: this claim -3.5%, mean |gap| 1.5% (4 runs)

### Equally good configurations
The target claim can't tell these 11 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `learning_rate=0.001` (reported)
- `learning_rate=0.002`
- `epochs=10`
- `epochs=20`
- `epochs=50`
- `early_stopping=1000, learning_rate=0.002`
- `early_stopping=2, learning_rate=0.001`
- `early_stopping=1000, epochs=20`
- `learning_rate=0.002, weight_decay=0.0001`
- `epochs=20, weight_decay=0.0001`
- `learning_rate=0.002, weight_decay=5e-06`

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `learning_rate`: learning_rate=0.001 (max I 0.11); learning_rate=0.002 (max I 0.18)
  - `early_stopping, learning_rate`: early_stopping=2, learning_rate=0.001 (max I 0.14); early_stopping=1000, learning_rate=0.002 (max I 0.22)
  - `epochs`: epochs=20 (max I 0.15); epochs=10 (max I 0.23)
  - `early_stopping, epochs`: early_stopping=1000, epochs=20 (max I 0.15); early_stopping=2, epochs=20 (max I 0.24)
  - `learning_rate, weight_decay`: learning_rate=0.002, weight_decay=0.0001 (max I 0.19); learning_rate=0.002, weight_decay=5e-06 (max I 0.24)
- Equally good values: `learning_rate` in {0.001, 0.002}

Notes:
- C_ind_cora_f1 (tuned separately) moves from -3.0% to -10.5% under {'learning_rate': '0.001'}: reported, not a rejection
- C_ind_pubmed_f1 (tuned separately) moves from +0.4% to -8.7% under {'learning_rate': '0.001'}: reported, not a rejection
- configurations the target claim can't tell apart from the answer: learning_rate=0.001; learning_rate=0.002; epochs=10; epochs=20; epochs=50; early_stopping=1000, learning_rate=0.002; early_stopping=2, learning_rate=0.001; early_stopping=1000, epochs=20; learning_rate=0.002, weight_decay=0.0001; epochs=20, weight_decay=0.0001; learning_rate=0.002, weight_decay=5e-06
- equally good values within one noise band (measured): learning_rate in {0.001, 0.002}
- found after adding spec knobs no ledger assumption names (learning_rate, epochs, weight_decay, early_stopping, max_degree)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_trans_cora_f1 | C_trans_pubmed_f1 | C_ind_cora_f1 | C_ind_pubmed_f1 | Mean |gap| |
|---|---|---|---|---|---|---|
| `learning_rate=0.002`, `early_stopping=1000` | 3 | +0.4% | -1.2% | -2.9% | +0.3% | 1.2% |
| `epochs=50` | 4 | -1.4% | -0.4% | -2.4% | -1.0% | 1.3% |
| `hidden1=32` | 4 | -3.5% | +0.3% | -1.2% | +1.0% | 1.5% |
| naive (reproduction as run) | 5 | -2.4% | -0.4% | -3.0% | +0.4% | 1.6% |
| `early_stopping=2` | 4 | -2.3% | -0.3% | -2.9% | -1.1% | 1.6% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=5000`, `epochs=10000`

## Knob names
- Ledger names mapped to spec knobs: `FLAGS.hidden1` → `hidden1`
- Screened though no assumption named them (low prior, code-derived values): `learning_rate`, `epochs`, `weight_decay`, `early_stopping`, `max_degree`
- Code defaults read from the code instead of the ledger: `hidden1` 16 at pubmed-original_inductive_FastGCN.py:24 (ledger said 16 (train.py:22), 128 (train_batch_multiRank_inductive_reddit_Mixlayers_sampleA.py:26))

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `rank1 (sample size top layer)`, `Hardware (CPU/GPU, memory)`, `batchsize (iterate_minibatches_listinputs)`, `precompute AH(0) (bottom layer precomputation)`, `GraphSAGE implementation (TensorFlow vs PyTorch)`, `Number of GCN layers (1 vs 2)`, `TensorFlow version / GraphSAGE version compatibility`, `Micro F1 score computation (metrics.py)`

## Provenance
- GapFinder commit: `4f763df19a8f0b1418afcb674d220cc6d05c0856` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `4d3799ddae0a330bf539ca061f485232f4dfb3a8433e533746d248417f200a09`
- Cost: Nemotron billed $0.0000, sandbox reported $16.1874 (total $16.1874; this search; ledger extraction is included only if it shared the search's router)
