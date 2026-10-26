# Gap Report: FastGCN (post-hoc v1.5 inputs)

Artifact `fastgcn` · generated 2026-10-26 18:00 · 163 branch runs (0 build/load setups) · sandbox $47.4354

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_trans_cora_f1 (trans_cora_acc) | Explained | -2.8% | -0.1% | ±1.0% | `learning_rate=0.001` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: ind_cora_acc 0.723 > ind_pubmed_acc 0.721; measured: ind_cora_acc 0.7 < ind_pubmed_acc 0.724 (margin -0.024, noise 0.014)
- **Held-out claims outside noise:**
  - C_ind_cora_f1 (`ind_cora_acc`): paper 0.723, measured 0.7 (-3.2%, band ±1.7%) (tuned separately in the paper)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `rank1 (sample size top layer)`: "The sample sizes for FastGCN are 400, 100, and 400, respectively for the three data sets." (p.8)
  - `batchsize (iterate_minibatches_listinputs)`: "Training time is in seconds, per-epoch (batch size 1024)." (p.8)
  - `precompute AH(0) (bottom layer precomputation)`: "Hence, all the experiments that follow use precomputation." (p.8)
  - `GraphSAGE implementation (TensorFlow vs PyTorch)`: "The new implementation is in PyTorch whereas the rest are in TensorFlow." (p.9)
  - `Number of GCN layers (1 vs 2)`: "All networks (including those under comparison) contain two layers as usual." (p.7)
  - `TensorFlow version / GraphSAGE version compatibility`: "The codes of GraphSAGE and GCN are downloaded from the accompany websites" (p.7)

## C_trans_cora_f1: trans_cora_acc (paper 0.818)
**Explained** · gap -2.8% → -0.1% · 66 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0056`, `B0105`, `B0106`, `B0119` (4 run(s) of the same config)
- Config: `learning_rate` naive `0.01`, changed to `0.001`
- Command:

  Replay: fork checkpoint `e6a5358e-5cb8-4cb3-afcb-7190e86cebb7` and run
  ```
  @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.add1=0 @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.div2=0 @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.mul2=0 @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.sub1=0 @ast:pubmed-original_inductive_FastGCN.py:144:@mut.35.Call.red.mean=0 @ast:pubmed-original_inductive_FastGCN.py:151:@mut.77.num.add1=0 RUN_TAG=e7ef1f5f97b3 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; export GF_SEED_FROM_RUN_TAG=1 OMP_NUM_THREADS=1 TF_CPP_MIN_LOG_LEVEL=2; mkdir -p out; A="--model gcn_mix --learning_rate 0.001 --epochs 100 --hidden1 16 --dropout 0.0 --weight_decay 5e-4 --early_stopping 10 --max_degree 3"; python pubmed-original_transductive_FastGCN.py --dataset cora $A > out/trans_cora.log 2>&1 & python pubmed-original_transductive_FastGCN.py --dataset pubmed $A > out/trans_pubmed.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset cora $A > out/ind_cora.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset pubmed $A > out/ind_pubmed.log 2>&1 & wait; bash gf_harness/emit.sh
  ```
- Output: `trans_cora_acc` 0.819, 0.805, 0.816, 0.82; gap after -0.1%; result checkpoint `fea37a29-eaaa-4b44-9d14-02131eb209f2`
- Effect: candidate 0.8175 minus naive 0.795 = +0.0225, 95% bootstrap interval [+0.0072, +0.0262] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `trans_cora_acc` = 0.818.

### What did we measure?
- Naive median 0.795 over 5 runs; repeats: 0.799, 0.798, 0.794, 0.795, 0.793
- Spread: range 0.793 to 0.799, noise band ±0.00795 (2 x MAD), CV 0.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.8% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `learning_rate` the gap is -2.8% (it comes back)
- PASS · Held-out claim: C_trans_pubmed_f1: -0.3% to -0.4% (not worse beyond noise)
- NOTE · Held-out claim, tuned separately: C_ind_cora_f1: -3.2% to -14.9% (worse beyond noise; reported, not a constraint)
- NOTE · Held-out claim, tuned separately: C_ind_pubmed_f1: +0.4% to -7.2% (worse beyond noise; reported, not a constraint)
- PASS · Evidence: `learning_rate=0.001`: paper evidence at paper text: 'We swept learning rate in the set {0.01, 0.001, 0.0001}.'
- PASS · Effect vs noise: candidate minus naive is +0.0225 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=5000`, `epochs=10000`
- Not settable with this harness: `rank1 (sample size top layer)`, `Hardware (CPU/GPU, memory)`, `batchsize (iterate_minibatches_listinputs)`, `precompute AH(0) (bottom layer precomputation)`, `GraphSAGE implementation (TensorFlow vs PyTorch)`, `Number of GCN layers (1 vs 2)`, `TensorFlow version / GraphSAGE version compatibility`, `Micro F1 score computation (metrics.py)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `learning_rate=0.002` (2.77 noise units, gap +0.1%); `epochs=10` (2.39 noise units, gap -0.5%); `weight_decay=5e-05` (2.14 noise units, gap -0.7%); `weight_decay=0.005` (1.76 noise units, gap -1.1%); `early_stopping=2` (1.64 noise units, gap -1.2%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `early_stopping=5`: this claim -2.2%, mean |gap| 1.1% (4 runs)
  - `epochs=50`: this claim -1.2%, mean |gap| 1.2% (4 runs)
  - `max_degree=15`: this claim -2.5%, mean |gap| 1.2% (4 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `learning_rate=0.001` (reported)
- `learning_rate=0.002`
- `epochs=20`
- `epochs=50`
- `weight_decay=5e-05`
- `epochs=50, learning_rate=0.002`
- `epochs=10, weight_decay=5e-05`
- `early_stopping=2, learning_rate=0.002`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting learning_rate=0.001 | settings | 28% | 0.4 sigma (fits every claim) | run with learning_rate=0.001 |
| 2 | no difference in reporting: the numbers as printed at the end of the run | settings | 13% | 1.8 sigma (fits every claim) | the settings search and the other classes |
| 3 | the setting epochs=50, learning_rate=0.002 | settings | 10% | 0.6 sigma (fits every claim) | run with epochs=50, learning_rate=0.002 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `learning_rate`: learning_rate=0.001 (max I 0.54); learning_rate=0.002 (max I 0.69)
  - `early_stopping, learning_rate`: early_stopping=2, learning_rate=0.002 (max I 0.66); early_stopping=2, learning_rate=0.001 (max I 1.24)
  - `epochs, learning_rate`: epochs=50, learning_rate=0.002 (max I 0.69)
  - `epochs`: epochs=20 (max I 0.75); epochs=50 (max I 1.18); epochs=10 (max I 1.21)
  - `epochs, weight_decay`: epochs=10, weight_decay=5e-05 (max I 0.75)
  - `weight_decay`: weight_decay=5e-05 (max I 1.21)
- Equally good values: `learning_rate` in {0.001, 0.002}

Notes:
- C_ind_cora_f1 (tuned separately) moves from -3.2% to -14.9% under {'learning_rate': '0.001'}: reported, not a rejection
- C_ind_pubmed_f1 (tuned separately) moves from +0.4% to -7.2% under {'learning_rate': '0.001'}: reported, not a rejection
- configurations the target claim can't tell apart from the answer: learning_rate=0.001; learning_rate=0.002; epochs=20; epochs=50; weight_decay=5e-05; epochs=50, learning_rate=0.002; epochs=10, weight_decay=5e-05; early_stopping=2, learning_rate=0.002
- equally good values within one noise band (measured): learning_rate in {0.001, 0.002}
- found after adding spec knobs no ledger assumption names (learning_rate, epochs, weight_decay, early_stopping, max_degree)
- learning_rate: values from 0.001 to 0.003162 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- not identifiable from the paper's numbers: 7 configuration(s) of other knobs fit every claim as well as the answer (learning_rate=0.001: early_stopping=2, learning_rate=0.002; epochs=10, weight_decay=5e-05; epochs=20; epochs=50; epochs=50, learning_rate=0.002; learning_rate=0.002), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_trans_cora_f1 | C_trans_pubmed_f1 | C_ind_cora_f1 | C_ind_pubmed_f1 | Mean |gap| |
|---|---|---|---|---|---|---|
| `early_stopping=5` | 4 | -2.2% | +0.1% | -1.5% | +0.5% | 1.1% |
| `epochs=50` | 4 | -1.2% | +0.3% | -2.3% | -0.9% | 1.2% |
| `max_degree=15` | 4 | -2.5% | +0.2% | -1.8% | +0.2% | 1.2% |
| `max_degree=6` | 4 | -2.4% | +0.1% | -2.3% | +0.2% | 1.2% |
| `early_stopping=2` | 4 | -1.8% | -0.3% | -2.3% | -0.8% | 1.3% |

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
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `b8cf68d00dd75fff65da1c503b577fd3da1679380c6d8f45518e9bad52530c3d`
- Cost: Nemotron billed $0.0012, sandbox reported $47.4354 (total $47.4365; this search; ledger extraction is included only if it shared the search's router)
