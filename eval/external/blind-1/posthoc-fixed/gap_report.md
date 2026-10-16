# Gap Report: FastGCN (ICLR 2018), post-hoc with the blind-1 fixes

Artifact `fastgcn` · generated 2026-10-16 13:20 · 149 branch runs (0 build/load setups) · sandbox $26.0144

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_trans_cora_f1 (trans_cora_acc) | Fits but unsupported | -2.3% | -0.4% | ±1.0% | `learning_rate=0.002` |

## C_trans_cora_f1: trans_cora_acc (paper 0.818)
**Fits but unsupported** · gap -2.3% → -0.4% · 76 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0028`, `B0029`, `B0036` (4 run(s) of the same config)
- Config: `learning_rate` naive `0.01`, changed to `0.002`
- Command:

  Replay: fork checkpoint `e6a5358e-5cb8-4cb3-afcb-7190e86cebb7` and run
  ```
  RUN_TAG=8f9d5d2e6825 export GF_SEED_FROM_RUN_TAG=1 OMP_NUM_THREADS=1 TF_CPP_MIN_LOG_LEVEL=2; mkdir -p out; A="--model gcn_mix --learning_rate 0.002 --epochs 100 --hidden1 16 --dropout 0.0 --weight_decay 5e-4 --early_stopping 10 --max_degree 3"; python pubmed-original_transductive_FastGCN.py --dataset cora $A > out/trans_cora.log 2>&1 & python pubmed-original_transductive_FastGCN.py --dataset pubmed $A > out/trans_pubmed.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset cora $A > out/ind_cora.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset pubmed $A > out/ind_pubmed.log 2>&1 & wait; bash gf_harness/emit.sh
  ```
- Output: `trans_cora_acc` 0.815, 0.809, 0.819, 0.814; gap after -0.4%; result checkpoint `b5b2dc8a-6efd-4910-b8b2-6ba133b55736`
- Effect: candidate 0.8145 minus naive 0.799 = +0.0155, 95% bootstrap interval [+0.0056, +0.0202] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `trans_cora_acc` = 0.818.

### What did we measure?
- Naive median 0.799 over 5 runs; repeats: 0.805, 0.805, 0.798, 0.799, 0.797
- Spread: range 0.797 to 0.805, noise band ±0.00799 (2 x MAD), CV 0.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.3% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `learning_rate` the gap is -2.3% (it comes back)
- PASS · Held-out claim: C_trans_pubmed_f1: -0.5% to -1.4% (not worse beyond noise)
- NOTE · Held-out claim, tuned separately: C_ind_cora_f1: -1.8% to -5.2% (worse beyond noise; reported, not a constraint)
- NOTE · Held-out claim, tuned separately: C_ind_pubmed_f1: +0.7% to +0.1% (not worse beyond noise)
- FAIL · Evidence: `learning_rate=0.002`: no evidence mentions '0.002'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.0155 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=5000`, `epochs=10000`
- Not settable with this harness: `rank1 (sample size top layer)`, `Hardware (CPU/GPU, memory)`, `FLAGS.hidden1`, `batchsize (iterate_minibatches_listinputs)`, `precompute AH(0) (bottom layer precomputation)`, `GraphSAGE implementation (TensorFlow vs PyTorch)`, `Number of GCN layers (1 vs 2)`, `TensorFlow version / GraphSAGE version compatibility`, `Micro F1 score computation (metrics.py)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=20` (2.25 noise units, gap -0.1%); `learning_rate=0.001` (2.19 noise units, gap -0.2%); `epochs=10` (2.13 noise units, gap -0.2%); `learning_rate=0.005` (1.25 noise units, gap -1.1%); `epochs=50` (1 noise units, gap -1.3%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `learning_rate=0.005`: this claim -1.1%, mean |gap| 1.1% (4 runs)
  - `learning_rate=0.002`, `early_stopping=1000`: this claim +0.4%, mean |gap| 1.2% (3 runs)
  - `epochs=50`: this claim -1.4%, mean |gap| 1.3% (4 runs)

### Equally good configurations
The target claim can't tell these 12 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `learning_rate=0.002` (reported)
- `learning_rate=0.001`
- `epochs=10`
- `epochs=20`
- `learning_rate=0.005`
- `early_stopping=1000, learning_rate=0.002`
- `early_stopping=2, learning_rate=0.001`
- `learning_rate=0.001, weight_decay=0.0001`
- `early_stopping=1000, epochs=20`
- `learning_rate=0.002, weight_decay=0.0001`
- `epochs=20, weight_decay=0.0001`
- `learning_rate=0.002, weight_decay=5e-06`

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `early_stopping, learning_rate`: early_stopping=2, learning_rate=0.001 (max I 0.14); early_stopping=1000, learning_rate=0.002 (max I 0.22)
  - `epochs`: epochs=20 (max I 0.15); epochs=10 (max I 0.23)
  - `early_stopping, epochs`: early_stopping=1000, epochs=20 (max I 0.15); early_stopping=2, epochs=20 (max I 0.24)
  - `learning_rate`: learning_rate=0.001 (max I 0.17); learning_rate=0.002 (max I 0.2); learning_rate=0.005 (max I 0.22)
  - `learning_rate, weight_decay`: learning_rate=0.002, weight_decay=0.0001 (max I 0.19)
- Equally good values: `learning_rate` in {0.001, 0.002, 0.005}

Notes:
- C_ind_cora_f1 (tuned separately) moves from -1.8% to -5.2% under {'learning_rate': '0.002'}: reported, not a rejection
- configurations the target claim can't tell apart from the answer: learning_rate=0.002; learning_rate=0.001; epochs=10; epochs=20; learning_rate=0.005; early_stopping=1000, learning_rate=0.002; early_stopping=2, learning_rate=0.001; learning_rate=0.001, weight_decay=0.0001; early_stopping=1000, epochs=20; learning_rate=0.002, weight_decay=0.0001; epochs=20, weight_decay=0.0001; learning_rate=0.002, weight_decay=5e-06
- equally good values within one noise band (measured): learning_rate in {0.001, 0.002, 0.005}
- found after adding spec knobs no ledger assumption names (learning_rate, epochs, hidden1, weight_decay, early_stopping, max_degree)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_trans_cora_f1 | C_trans_pubmed_f1 | C_ind_cora_f1 | C_ind_pubmed_f1 | Mean |gap| |
|---|---|---|---|---|---|---|
| `learning_rate=0.005` | 4 | -1.1% | -0.6% | -2.2% | -0.3% | 1.1% |
| `learning_rate=0.002`, `early_stopping=1000` | 3 | +0.4% | -1.2% | -2.9% | +0.3% | 1.2% |
| `epochs=50` | 4 | -1.4% | -0.4% | -2.4% | -1.0% | 1.3% |
| naive (reproduction as run) | 5 | -2.3% | -0.5% | -1.8% | +0.7% | 1.3% |
| `learning_rate=0.002` | 4 | -0.4% | -1.4% | -5.2% | +0.1% | 1.8% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=5000`, `epochs=10000`

## Knob names
- Screened though no assumption named them (low prior, code-derived values): `learning_rate`, `epochs`, `hidden1`, `weight_decay`, `early_stopping`, `max_degree`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `rank1 (sample size top layer)`, `Hardware (CPU/GPU, memory)`, `FLAGS.hidden1`, `batchsize (iterate_minibatches_listinputs)`, `precompute AH(0) (bottom layer precomputation)`, `GraphSAGE implementation (TensorFlow vs PyTorch)`, `Number of GCN layers (1 vs 2)`, `TensorFlow version / GraphSAGE version compatibility`, `Micro F1 score computation (metrics.py)`

## Provenance
- GapFinder commit: `4f763df19a8f0b1418afcb674d220cc6d05c0856` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `4d3799ddae0a330bf539ca061f485232f4dfb3a8433e533746d248417f200a09`
- Cost: Nemotron billed $0.0000, sandbox reported $26.0144 (total $26.0144; this search; ledger extraction is included only if it shared the search's router)
