# Gap Report: FastGCN (blind-1)

Artifact `fastgcn` · generated 2026-10-26 05:03 · 200 branch runs (0 build/load setups) · sandbox $65.9940

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_trans_cora_f1 (trans_cora_acc) | Unexplained | -2.2% | -2.2% | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: ind_cora_acc 0.723 > ind_pubmed_acc 0.721; measured: ind_cora_acc 0.703 < ind_pubmed_acc 0.723 (margin -0.02, noise 0.0123)
- **Held-out claims outside noise:**
  - C_ind_cora_f1 (`ind_cora_acc`): paper 0.723, measured 0.703 (-2.8%, band ±1.4%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `sample_size_layer1`: "The sample sizes for FastGCN are 400, 100, and 400, respectively for the three data sets." (p.8)
  - `sampling_method`: "Hence, later experiments will apply importance sampling." (p.8)
  - `cpu_model`: "Hardware: Running time is compared on a single machine with 4-core 2.5 GHz Intel Core i7, and 16G RAM." (p.13)
  - `graphsage_sample_size_1`: "Following the setting of Hamilton et al. (2017), we use two layers with neighborhood sample sizes S1 = 25 and S2 = 10." (p.12)
  - `graphsage_sample_size_2`: "Following the setting of Hamilton et al. (2017), we use two layers with neighborhood sample sizes S1 = 25 and S2 = 10." (p.12)
  - `precompute_AH0`: "Hence, one may precompute the product rather than sampling this layer to gain efficiency. The compared results are listed on the right part of Table 2 (columns under "Precompute"). One sees that the t" (p.8)

## C_trans_cora_f1: trans_cora_acc (paper 0.818)
**Unexplained** · gap -2.2% → -2.2% · 48 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (48 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `trans_cora_acc` = 0.818.

### What did we measure?
- Naive median 0.8 over 5 runs; repeats: 0.796, 0.8, 0.801, 0.801, 0.796
- Spread: range 0.796 to 0.801, noise band ±0.008 (2 x MAD), CV 0.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.2% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: `epochs=5000`, `epochs=10000`
- Not settable with this harness: `sample_size_layer1`, `sampling_method`, `cpu_model`, `graphsage_sample_size_1`, `graphsage_sample_size_2`, `precompute_AH0`, `dataset_split`, `framework`, `sample_size_layer2`, `graphsage_aggregator`, `gcn_batched`, `graphsage_new_implementation`, `graphsage_hidden_dim`, `ram_size`, `weight_initialization`, `feature_normalization`, `validation_test_indices`, `optimizer`, `random_seed`, `activation_function`, `gradient_clipping`, `num_layers`, `loss_function`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `learning_rate=0.001` (2.25 noise units, gap +0.0%); `learning_rate=0.002` (1.5 noise units, gap -0.7%); `early_stopping=1` (1 noise units, gap -1.2%)
- Near alternatives (closest across all claims):
  - `hidden1=32`, `learning_rate=0.002`, `@ast:layers.py:203:rank=200`: this claim -0.7%, mean |gap| 0.7% (3 runs)
  - `learning_rate=0.005`: this claim -1.5%, mean |gap| 1.0% (4 runs)
  - `hidden1=32`, `learning_rate=0.002`: this claim -0.3%, mean |gap| 1.1% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting hidden1=32, learning_rate=0.002 | settings | 37% | 0.8 sigma (fits every claim) | run with hidden1=32, learning_rate=0.002 |
| 2 | no difference in reporting: the numbers as printed at the end of the run | settings | 25% | 1.6 sigma (fits every claim) | the settings search and the other classes |
| 3 | the setting learning_rate=0.005 | settings | 11% | 1.0 sigma (fits every claim) | run with learning_rate=0.005 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `hidden1, learning_rate`: hidden1=32, learning_rate=0.002 (max I 0.99)
  - `learning_rate`: learning_rate=0.005 (max I 1.47)
  - `early_stopping`: early_stopping=50 (max I 2.01); early_stopping=5 (max I 2.12); early_stopping=1000 (max I 2.12); early_stopping=100 (max I 2.23); +2 more
  - `early_stopping, learning_rate`: early_stopping=1, learning_rate=0.002 (max I 2.23)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `__init__(..., rank=100)`: a default no call in the repo overrides (8 call(s)) (`layers.py:203`)
  - unexposed setting: `dot(..., sparse=True)`: a switch fixed in the call; no flag sets it (`layers.py:192`)
  - unexposed setting: `dot(..., sparse=True)`: a switch fixed in the call; no flag sets it (`layers.py:243`)
  - unexposed setting: `dot(..., sparse=True)`: a switch fixed in the call; no flag sets it (`layers.py:271`)
  - unexposed setting: `Dense(..., sparse_inputs=True)`: a switch fixed in the call; no flag sets it (`models.py:113`)
  - unexposed setting: `GraphConvolution(..., sparse_inputs=True)`: a switch fixed in the call; no flag sets it (`models.py:163`)
  - unexposed setting: `GraphConvolution(..., sparse_inputs=False)`: a switch fixed in the call; no flag sets it (`models.py:210`)
  - unexposed setting: `Dense(..., sparse_inputs=False)`: a switch fixed in the call; no flag sets it (`models.py:258`)

Notes:
- {'learning_rate': '0.002'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'learning_rate': '0.002'} (gap -0.4%); it did not pass verification
- spec knobs no ledger assumption names (weight_decay, max_degree) were screened too; no better answer
- history matching: the naive configuration is within noise of every claim
- patch round: {'@ast:layers.py:203:rank': '200', 'hidden1': '32', 'learning_rate': '0.002'} fits every claim but did not pass verification
- mutation round: none of 6 mutants moved C_trans_cora_f1 toward the paper

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_trans_cora_f1 | C_trans_pubmed_f1 | C_ind_cora_f1 | C_ind_pubmed_f1 | Mean |gap| |
|---|---|---|---|---|---|---|
| `hidden1=32`, `learning_rate=0.002`, `@ast:layers.py:203:rank=200` | 3 | -0.7% | +0.1% | -0.7% | -1.1% | 0.7% |
| `learning_rate=0.005` | 4 | -1.5% | -0.5% | -1.1% | -1.0% | 1.0% |
| `hidden1=32`, `learning_rate=0.002` | 4 | -0.3% | -1.0% | -1.4% | -1.6% | 1.1% |
| `learning_rate=0.001`, `epochs=200` | 4 | -0.1% | -0.6% | -3.2% | +0.4% | 1.1% |
| naive (reproduction as run) | 5 | -2.2% | +0.0% | -2.8% | +0.3% | 1.3% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `early_stopping=None`: other, The program expected early_stopping to be an integer (or a numeric value controlling patience), but received the string 'None', which it could not parse, resulting in no metrics being produced. [not taken as invalid_value: the log shows no rejection]

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
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `a63b1093a4d73861d3d773718ac7bc08bd8bee0db210f241e121a9a9872ca7b7`
- Cost: Nemotron billed $0.0053, sandbox reported $65.9940 (total $65.9993; this search; ledger extraction is included only if it shared the search's router)
