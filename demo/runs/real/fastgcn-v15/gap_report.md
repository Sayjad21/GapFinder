# Gap Report: FastGCN (post-hoc v1.5 inputs)

Artifact `fastgcn` · generated 2026-10-26 09:12 · 160 branch runs (0 build/load setups) · sandbox $47.3980

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_trans_cora_f1 (trans_cora_acc) | Explained | -2.7% | -0.9% | ±1.0% | `learning_rate=0.001` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: ind_cora_acc 0.723 > ind_pubmed_acc 0.721; measured: ind_cora_acc 0.706 < ind_pubmed_acc 0.72 (margin -0.014, noise 0.0108)
- **Held-out claims outside noise:**
  - C_ind_cora_f1 (`ind_cora_acc`): paper 0.723, measured 0.706 (-2.4%, band ±1.1%) (tuned separately in the paper)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `rank1 (sample size top layer)`: "The sample sizes for FastGCN are 400, 100, and 400, respectively for the three data sets." (p.8)
  - `batchsize (iterate_minibatches_listinputs)`: "Training time is in seconds, per-epoch (batch size 1024)." (p.8)
  - `precompute AH(0) (bottom layer precomputation)`: "Hence, all the experiments that follow use precomputation." (p.8)
  - `GraphSAGE implementation (TensorFlow vs PyTorch)`: "The new implementation is in PyTorch whereas the rest are in TensorFlow." (p.9)
  - `Number of GCN layers (1 vs 2)`: "All networks (including those under comparison) contain two layers as usual." (p.7)
  - `TensorFlow version / GraphSAGE version compatibility`: "The codes of GraphSAGE and GCN are downloaded from the accompany websites" (p.7)

## C_trans_cora_f1: trans_cora_acc (paper 0.818)
**Explained** · gap -2.7% → -0.9% · 69 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0056`, `B0107`, `B0108`, `B0118` (4 run(s) of the same config)
- Config: `learning_rate` naive `0.01`, changed to `0.001`
- Command:

  Replay: fork checkpoint `e6a5358e-5cb8-4cb3-afcb-7190e86cebb7` and run
  ```
  @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.add1=0 @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.div2=0 @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.mul2=0 @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.sub1=0 @ast:pubmed-original_inductive_FastGCN.py:144:@mut.35.Call.red.mean=0 @ast:pubmed-original_inductive_FastGCN.py:151:@mut.77.num.add1=0 RUN_TAG=5a323d956443 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; export GF_SEED_FROM_RUN_TAG=1 OMP_NUM_THREADS=1 TF_CPP_MIN_LOG_LEVEL=2; mkdir -p out; A="--model gcn_mix --learning_rate 0.001 --epochs 100 --hidden1 16 --dropout 0.0 --weight_decay 5e-4 --early_stopping 10 --max_degree 3"; python pubmed-original_transductive_FastGCN.py --dataset cora $A > out/trans_cora.log 2>&1 & python pubmed-original_transductive_FastGCN.py --dataset pubmed $A > out/trans_pubmed.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset cora $A > out/ind_cora.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset pubmed $A > out/ind_pubmed.log 2>&1 & wait; bash gf_harness/emit.sh
  ```
- Output: `trans_cora_acc` 0.81, 0.807, 0.819, 0.811; gap after -0.9%; result checkpoint `62b36714-8582-46bd-8fac-e5659b7a5637`
- Effect: candidate 0.8105 minus naive 0.796 = +0.0145, 95% bootstrap interval [+0.0072, +0.0244] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `trans_cora_acc` = 0.818.

### What did we measure?
- Naive median 0.796 over 5 runs; repeats: 0.801, 0.793, 0.801, 0.796, 0.795
- Spread: range 0.793 to 0.801, noise band ±0.00796 (2 x MAD), CV 0.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.7% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `learning_rate` the gap is -2.7% (it comes back)
- PASS · Held-out claim: C_trans_pubmed_f1: +0.5% to -0.7% (not worse beyond noise)
- NOTE · Held-out claim, tuned separately: C_ind_cora_f1: -2.4% to -8.9% (worse beyond noise; reported, not a constraint)
- NOTE · Held-out claim, tuned separately: C_ind_pubmed_f1: -0.1% to -12.7% (worse beyond noise; reported, not a constraint)
- PASS · Evidence: `learning_rate=0.001`: paper evidence at paper text: 'We swept learning rate in the set {0.01, 0.001, 0.0001}.'
- PASS · Effect vs noise: candidate minus naive is +0.0145 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=5000`, `epochs=10000`
- Not settable with this harness: `rank1 (sample size top layer)`, `Hardware (CPU/GPU, memory)`, `batchsize (iterate_minibatches_listinputs)`, `precompute AH(0) (bottom layer precomputation)`, `GraphSAGE implementation (TensorFlow vs PyTorch)`, `Number of GCN layers (1 vs 2)`, `TensorFlow version / GraphSAGE version compatibility`, `Micro F1 score computation (metrics.py)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=10` (2.64 noise units, gap -0.1%); `epochs=20` (2.26 noise units, gap -0.5%); `weight_decay=0.025` (2.26 noise units, gap -0.5%); `early_stopping=1` (2.14 noise units, gap -0.6%); `learning_rate=0.002` (1.88 noise units, gap -0.9%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `early_stopping=1`: this claim -1.9%, mean |gap| 1.0% (4 runs)
  - `learning_rate=0.005`: this claim -1.3%, mean |gap| 1.1% (4 runs)
  - `hidden1=32`: this claim -2.6%, mean |gap| 1.2% (4 runs)

### Equally good configurations
The target claim can't tell these 10 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `learning_rate=0.001` (reported)
- `learning_rate=0.002`
- `epochs=20`
- `weight_decay=5e-05`
- `weight_decay=1e-05`
- `learning_rate=0.005`
- `weight_decay=0.0001`
- `early_stopping=1, learning_rate=0.002`
- `early_stopping=1, epochs=20`
- `epochs=10, weight_decay=0.0001`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting learning_rate=0.001 | settings | 29% | 0.5 sigma (fits every claim) | run with learning_rate=0.001 |
| 2 | no difference in reporting: the numbers as printed at the end of the run | settings | 16% | 1.7 sigma (fits every claim) | the settings search and the other classes |
| 3 | the setting early_stopping=1, learning_rate=0.002 | settings | 12% | 0.1 sigma (fits every claim) | run with early_stopping=1, learning_rate=0.002 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `early_stopping, learning_rate`: early_stopping=1, learning_rate=0.002 (max I 0.19)
  - `early_stopping, epochs`: early_stopping=1, epochs=20 (max I 0.66)
  - `learning_rate`: learning_rate=0.001 (max I 0.68); learning_rate=0.002 (max I 1); learning_rate=0.005 (max I 1.26)
  - `epochs`: epochs=20 (max I 0.99); epochs=10 (max I 1.23)
  - `epochs, weight_decay`: epochs=10, weight_decay=0.0001 (max I 1.02)
  - `weight_decay`: weight_decay=5e-05 (max I 1.12); weight_decay=0.0001 (max I 1.34)
- Equally good values: `learning_rate` in {0.001, 0.002, 0.005}

Notes:
- C_ind_cora_f1 (tuned separately) moves from -2.4% to -8.9% under {'learning_rate': '0.001'}: reported, not a rejection
- C_ind_pubmed_f1 (tuned separately) moves from -0.1% to -12.7% under {'learning_rate': '0.001'}: reported, not a rejection
- configurations the target claim can't tell apart from the answer: learning_rate=0.001; learning_rate=0.002; epochs=20; weight_decay=5e-05; weight_decay=1e-05; learning_rate=0.005; weight_decay=0.0001; early_stopping=1, learning_rate=0.002; early_stopping=1, epochs=20; epochs=10, weight_decay=0.0001
- equally good values within one noise band (measured): learning_rate in {0.001, 0.002, 0.005}
- found after adding spec knobs no ledger assumption names (learning_rate, epochs, weight_decay, early_stopping, max_degree)
- learning_rate: values from 0.0004472 to 0.002515 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- not identifiable from the paper's numbers: 9 configuration(s) of other knobs fit every claim as well as the answer (learning_rate=0.001: early_stopping=1, epochs=20; early_stopping=1, learning_rate=0.002; epochs=10, weight_decay=0.0001; epochs=20; learning_rate=0.002; learning_rate=0.005), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_trans_cora_f1 | C_trans_pubmed_f1 | C_ind_cora_f1 | C_ind_pubmed_f1 | Mean |gap| |
|---|---|---|---|---|---|---|
| `early_stopping=1` | 4 | -1.9% | -0.1% | -2.0% | +0.0% | 1.0% |
| `learning_rate=0.005` | 4 | -1.3% | -0.5% | -2.2% | -0.5% | 1.1% |
| `hidden1=32` | 4 | -2.6% | +0.3% | -1.7% | +0.4% | 1.2% |
| naive (reproduction as run) | 5 | -2.7% | +0.5% | -2.4% | -0.1% | 1.4% |
| `hidden1=80` | 4 | -3.2% | +0.8% | -1.7% | +0.6% | 1.6% |

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
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `b8cf68d00dd75fff65da1c503b577fd3da1679380c6d8f45518e9bad52530c3d`
- Cost: Nemotron billed $0.0012, sandbox reported $47.3980 (total $47.3992; this search; ledger extraction is included only if it shared the search's router)
