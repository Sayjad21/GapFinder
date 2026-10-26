# Gap Report: FastGCN (blind inputs)

Artifact `fastgcn` · generated 2026-10-27 00:17 · 200 branch runs (0 build/load setups) · sandbox $52.2238

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_trans_cora_f1 (trans_cora_acc) | Fits but unsupported | -2.6% | -1.2% | ±1.0% | `epochs=50` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: ind_cora_acc 0.723 > ind_pubmed_acc 0.721; measured: ind_cora_acc 0.706 < ind_pubmed_acc 0.724 (margin -0.018, noise 0.0176)
- **Held-out claims outside noise:**
  - C_ind_cora_f1 (`ind_cora_acc`): paper 0.723, measured 0.706 (-2.4%, band ±2.2%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `sample_size_layer1`: "The sample sizes for FastGCN are 400, 100, and 400, respectively for the three data sets." (p.8)
  - `sampling_method`: "Hence, later experiments will apply importance sampling." (p.8)
  - `cpu_model`: "Hardware: Running time is compared on a single machine with 4-core 2.5 GHz Intel Core i7, and 16G RAM." (p.13)
  - `graphsage_sample_size_1`: "Following the setting of Hamilton et al. (2017), we use two layers with neighborhood sample sizes S1 = 25 and S2 = 10." (p.12)
  - `graphsage_sample_size_2`: "Following the setting of Hamilton et al. (2017), we use two layers with neighborhood sample sizes S1 = 25 and S2 = 10." (p.12)
  - `precompute_AH0`: "Hence, one may precompute the product rather than sampling this layer to gain efficiency. The compared results are listed on the right part of Table 2 (columns under "Precompute"). One sees that the t" (p.8)

## C_trans_cora_f1: trans_cora_acc (paper 0.818)
**Fits but unsupported** · gap -2.6% → -1.2% · 44 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0039`, `B0080`, `B0081`, `B0133` (4 run(s) of the same config)
- Config: `epochs` naive `100`, changed to `50`
- Command:

  Replay: fork checkpoint `e6a5358e-5cb8-4cb3-afcb-7190e86cebb7` and run
  ```
  @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.add1=0 @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.div2=0 @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.mul2=0 @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.sub1=0 @ast:pubmed-original_inductive_FastGCN.py:144:@mut.35.Call.red.mean=0 @ast:pubmed-original_inductive_FastGCN.py:151:@mut.77.num.add1=0 RUN_TAG=d485f7447501 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; export GF_SEED_FROM_RUN_TAG=1 OMP_NUM_THREADS=1 TF_CPP_MIN_LOG_LEVEL=2; mkdir -p out; A="--model gcn_mix --learning_rate 0.01 --epochs 50 --hidden1 16 --dropout 0.0 --weight_decay 5e-4 --early_stopping 10 --max_degree 3"; python pubmed-original_transductive_FastGCN.py --dataset cora $A > out/trans_cora.log 2>&1 & python pubmed-original_transductive_FastGCN.py --dataset pubmed $A > out/trans_pubmed.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset cora $A > out/ind_cora.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset pubmed $A > out/ind_pubmed.log 2>&1 & wait; bash gf_harness/emit.sh
  ```
- Output: `trans_cora_acc` 0.808, 0.807, 0.81, 0.808; gap after -1.2%; result checkpoint `94ca1a90-7776-448f-9e40-c1868c89853e`
- Effect: candidate 0.808 minus naive 0.797 = +0.011, 95% bootstrap interval [+0.005533, +0.01647] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `trans_cora_acc` = 0.818.

### What did we measure?
- Naive median 0.797 over 5 runs; repeats: 0.791, 0.802, 0.801, 0.796, 0.797
- Spread: range 0.791 to 0.802, noise band ±0.008 (2 x MAD), CV 0.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.6% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is -2.6% (it comes back)
- PASS · Held-out claim: C_trans_pubmed_f1: -0.3% to -0.6% (not worse beyond noise)
- PASS · Held-out claim: C_ind_cora_f1: -2.4% to -2.0% (not worse beyond noise)
- PASS · Held-out claim: C_ind_pubmed_f1: +0.4% to -0.8% (not worse beyond noise)
- FAIL · Evidence: `epochs=50`: no evidence mentions '50'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.011 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=5000`, `epochs=10000`
- Not settable with this harness: `sample_size_layer1`, `sampling_method`, `cpu_model`, `graphsage_sample_size_1`, `graphsage_sample_size_2`, `precompute_AH0`, `dataset_split`, `framework`, `sample_size_layer2`, `graphsage_aggregator`, `gcn_batched`, `graphsage_new_implementation`, `graphsage_hidden_dim`, `ram_size`, `weight_initialization`, `feature_normalization`, `validation_test_indices`, `optimizer`, `random_seed`, `activation_function`, `gradient_clipping`, `num_layers`, `loss_function`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `learning_rate=0.002` (2.56 noise units, gap +0.1%); `epochs=10` (2.44 noise units, gap -0.2%); `epochs=20` (2.38 noise units, gap -0.2%); `learning_rate=0.001` (2.06 noise units, gap -0.6%); `learning_rate=0.005` (1.19 noise units, gap -1.4%)
- Near alternatives (closest across all claims):
  - `learning_rate=0.0025`: this claim -0.4%, mean |gap| 1.0% (4 runs)
  - `@ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.mul2=1`: this claim -2.1%, mean |gap| 1.1% (3 runs)
  - `learning_rate=0.005`: this claim -1.4%, mean |gap| 1.2% (4 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=50` (reported)
- `learning_rate=0.005`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting epochs=50 | settings | 26% | 1.1 sigma (fits every claim) | run with epochs=50 |
| 2 | no difference in reporting: the numbers as printed at the end of the run | settings | 17% | 1.7 sigma (fits every claim) | the settings search and the other classes |
| 3 | the setting learning_rate=0.005 | settings | 12% | 1.2 sigma (fits every claim) | run with learning_rate=0.005 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `@ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.mul2`: @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.mul2=1 (max I 0.88)
  - `learning_rate`: learning_rate=0.005 (max I 1.2); learning_rate=0.0025 (max I 1.33)
  - `early_stopping`: early_stopping=500 (max I 1.36); early_stopping=2 (max I 1.48); early_stopping=1 (max I 1.56); early_stopping=20 (max I 1.65); +1 more
  - `epochs`: epochs=50 (max I 1.49)
  - `@ast:pubmed-original_inductive_FastGCN.py:151:@mut.77.num.add1`: @ast:pubmed-original_inductive_FastGCN.py:151:@mut.77.num.add1=1 (max I 1.56)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `dot(..., sparse=True)`: a switch fixed in the call; no flag sets it (`layers.py:192`)
  - unexposed setting: `Dense(..., sparse_inputs=False)`: a switch fixed in the call; no flag sets it (`models.py:258`)
  - unexposed setting: `model_func(..., logging=True)`: a switch fixed in the call; no flag sets it (`pubmed-original_inductive_FastGCN.py:106`)
  - unexposed setting: `iterate_minibatches_listinputs(..., shuffle=True)`: a switch fixed in the call; no flag sets it (`pubmed-original_inductive_FastGCN.py:137`)
  - unexposed setting: `model_func(..., logging=True)`: a switch fixed in the call; no flag sets it (`pubmed-original_transductive_FastGCN.py:112`)
  - unexposed setting: `iterate_minibatches_listinputs(..., shuffle=True)`: a switch fixed in the call; no flag sets it (`pubmed-original_transductive_FastGCN.py:143`)
  - unexposed setting: `__init__(..., rank=100)`: a default no call in the repo overrides (8 call(s)) (`layers.py:203`)
  - unexposed setting: `dot(..., sparse=True)`: a switch fixed in the call; no flag sets it (`layers.py:243`)

Notes:
- configurations the target claim can't tell apart from the answer: epochs=50; learning_rate=0.005
- found after adding spec knobs no ledger assumption names (weight_decay, max_degree)
- patch round: {'@ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.mul2': '1'} fits every claim but did not pass verification
- mutation round: none of 21 mutants moved C_trans_cora_f1 toward the paper
- value interval stopped early: run budget of 200 reached (wanted 1 more run(s) of {'epochs': '35'} for 'interval epochs=35')
- not identifiable from the paper's numbers: 1 configuration(s) of other knobs fit every claim as well as the answer (epochs=50: learning_rate=0.005), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_trans_cora_f1 | C_trans_pubmed_f1 | C_ind_cora_f1 | C_ind_pubmed_f1 | Mean |gap| |
|---|---|---|---|---|---|---|
| `learning_rate=0.0025` | 4 | -0.4% | -0.5% | -1.7% | -1.5% | 1.0% |
| `@ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.mul2=1` | 3 | -2.1% | +0.0% | -1.9% | +0.4% | 1.1% |
| `learning_rate=0.005` | 4 | -1.4% | -0.3% | -2.3% | -0.6% | 1.2% |
| `epochs=50` | 4 | -1.2% | -0.6% | -2.0% | -0.8% | 1.2% |
| `epochs=500` | 4 | -2.9% | +0.5% | -1.7% | +0.0% | 1.3% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `early_stopping=None`: other, The program expected an integer value for early_stopping but received the string 'None', which caused it to fail to parse metrics from the output. [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=5000`, `epochs=10000`

## Knob names
- Ledger names mapped to spec knobs: `hidden_dim` → `hidden1`, `dropout_rate` → `dropout`, `num_epochs` → `epochs`, `early_stopping_patience` → `early_stopping`
- Screened though no assumption named them (low prior, code-derived values): `weight_decay`, `max_degree`
- Code defaults read from the code instead of the ledger: `learning_rate` 0.01 at pubmed-original_inductive_FastGCN.py:22 (ledger said 0.001), `hidden1` 16 at pubmed-original_inductive_FastGCN.py:24 (ledger said 128), `dropout` 0.0 at pubmed-original_inductive_FastGCN.py:25 (ledger said 0.5), `epochs` 100 at pubmed-original_inductive_FastGCN.py:23 (ledger said 200)

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at pubmed-original_transductive_FastGCN.py:139)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at models.py:58)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `sample_size_layer1`, `sampling_method`, `cpu_model`, `graphsage_sample_size_1`, `graphsage_sample_size_2`, `precompute_AH0`, `dataset_split`, `framework`, `sample_size_layer2`, `graphsage_aggregator`, `gcn_batched`, `graphsage_new_implementation`, `graphsage_hidden_dim`, `ram_size`, `weight_initialization`, `feature_normalization`, `validation_test_indices`, `optimizer`, `random_seed`, `activation_function`, `gradient_clipping`, `num_layers`, `loss_function`

## Provenance
- GapFinder commit: `f90b212a502334f9d48b56cb5c3d25e25859b4f0` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d3fcc3a19f6d28ed7c16c947a8c612e865980d766b13bef9b5a4651e0eccb4f9`
- Cost: Nemotron billed $0.0065, sandbox reported $52.2238 (total $52.2303; this search; ledger extraction is included only if it shared the search's router)
