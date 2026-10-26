# Gap Report: GAT (devset)

Artifact `gat` · generated 2026-10-26 09:26 · 172 branch runs (0 build/load setups) · sandbox $4441.0787

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_gat_pubmed (gat_pubmed_acc) | Inconclusive | -1.5% | -1.5% | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `dropout_rate`: "Furthermore, dropout (Srivastava et al., 2014) with p = 0.6 is applied to both layers' inputs, as well as to the normalized attention coefficients" (p.7)
  - `num_runs`: "we report the mean classification accuracy (with standard deviation) on the test nodes of our method after 100 runs" (p.7)
  - `initialization_method`: "Both models are initialized using Glorot initialization (Glorot & Bengio, 2010)" (p.7)
  - `optimizer_type`: "trained to minimize cross-entropy on the training nodes using the Adam SGD optimizer (Kingma & Ba, 2014)" (p.7)
  - `validation_metric`: "early stopping strategy on both the cross-entropy loss and accuracy (transductive) or micro-F1 (inductive) score on the validation nodes" (p.7)
  - `attention_mechanism`: "we also provide the results when a constant attention mechanism, a(x, y) = 1, is used, with the same architecture—this will assign the same weight to every neighbor" (p.7)

## C_gat_pubmed: gat_pubmed_acc (paper 79)
**Inconclusive** · naive gap -1.5% is inside the noise band ±1.0%, but the band is too wide to call it a reproduction.

### Which experiment changed it?
- None could be tested: the noise band is too wide to tell values apart.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `gat_pubmed_acc` = 79.

### What did we measure?
- Naive median 77.8 over 5 runs; repeats: 77.2, 78.4, 77.8, 78.2, 77.8
- Spread: range 77.2 to 78.4, noise band ±0.8 (2 x MAD), CV 0.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -1.5% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: `patience=5000`, `patience=10000`
- Not settable with this harness: `dropout_rate`, `num_runs`, `initialization_method`, `optimizer_type`, `validation_metric`, `dataset_split_seed`, `attention_mechanism`, `num_layers`, `tensorflow_version`, `cuda_version`, `random_seed`, `dataset_preprocessing`, `validation_split_source`, `gpu_device_id`, `attention_heads_aggregation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n_heads=6` (1.5 noise units, gap +0.0%); `lr=0.05` (1.12 noise units, gap -0.4%)
- Near alternatives (closest across all claims):
  - `n_heads=6`, `lr=0.05`: this claim -0.3%, mean |gap| 0.3% (4 runs)
  - `nb_epochs=1000000`, `n_heads=6`: this claim -0.6%, mean |gap| 0.4% (4 runs)
  - `n_heads=4`, `lr=0.05`: this claim -0.5%, mean |gap| 0.4% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | no difference in reporting: the numbers as printed at the end of the run | settings | 29% | 1.0 sigma (fits every claim) | the settings search and the other classes |
| 2 | the setting lr=0.05, n_heads=6 | settings | 22% | 0.2 sigma (fits every claim) | run with lr=0.05, n_heads=6 |
| 3 | the setting lr=0.05, nb_epochs=1000000 | settings | 7% | 0.3 sigma (fits every claim) | run with lr=0.05, nb_epochs=1000000 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, n_heads`: lr=0.05, n_heads=6 (max I 0.24); lr=0.05, n_heads=4 (max I 0.42); lr=0.01, n_heads=6 (max I 0.98)
  - `lr, nb_epochs`: lr=0.05, nb_epochs=1000000 (max I 0.34)
  - `n_heads, nb_epochs`: n_heads=6, nb_epochs=1000000 (max I 0.48); n_heads=6, nb_epochs=10000 (max I 0.88)
  - `lr`: lr=0.01 (max I 0.98); lr=0.05 (max I 1.14)
  - `hid_units, lr`: hid_units=121, lr=0.01 (max I 1.11)
  - `hid_units, n_heads`: hid_units=32, n_heads=6 (max I 1.17)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `conv1d(..., use_bias=False)`: a switch fixed in the call; no flag sets it (`utils/layers.py:11`)
  - unexposed setting: `conv1d(..., use_bias=False)`: a switch fixed in the call; no flag sets it (`utils/layers.py:43`)
- Where the code differs from the paper (model-proposed, checked against the repo; literal ones were tried as patch knobs, structural ones are not tested):
  - `models/base_gattn.py:20`: paper says initial learning rate of 0.01 for Pubmed; code does learning_rate=0.005
  - `models/sp_gat.py:18`: paper says we have applied K = 8 output attention heads (instead of one); code does second layer uses 1 attention head

Notes:
- no hypothesis moved the gap by more than 1 noise units
- spec knobs no ledger assumption names (model, patience) were screened too; no better answer
- the gap (-1.5%) is below the minimum detectable effect (±1.8% with 3 runs per configuration at 80% power): even a setting that closed it couldn't have been confirmed, so 'nothing explains it' can't be claimed either
- patch round: {'@ast:utils/layers.py:11:use_bias': 'True', 'lr': '0.05', 'n_heads': '6'} fits every claim but did not pass verification

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_gat_pubmed | C_gat_cora | C_gat_citeseer | Mean |gap| |
|---|---|---|---|---|---|
| `n_heads=6`, `lr=0.05` | 4 | -0.3% | +0.4% | +0.2% | 0.3% |
| `nb_epochs=1000000`, `n_heads=6` | 4 | -0.6% | -0.4% | -0.1% | 0.4% |
| `n_heads=4`, `lr=0.05` | 4 | -0.5% | -0.6% | -0.2% | 0.4% |
| `lr=0.01`, `hid_units=121` | 4 | -1.5% | -0.1% | -0.1% | 0.5% |
| `n_heads=6`, `@ast:utils/layers.py:11:use_bias=True`, `lr=0.05` | 3 | -0.8% | +0.0% | -1.1% | 0.6% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `batch_size=2`: other, The harness treated batch_size as a string and the downstream parser expected a numeric value, causing no metrics to be produced. Changing batch_size to an integer like 3 keeps the intent of increasing batch size while being a valid value. [not taken as invalid_value: the log shows no rejection]
- `batch_size=4`: other, The script did not parse any metrics when batch_size was set to '4', indicating the value was not accepted (likely due to type or constraint). A nearby valid integer batch size is 2, which retains the intent of using a small batch larger than the default. [not taken as invalid_value: the log shows no rejection]
- `batch_size=full`: other, The program expects batch_size to be a numeric value; the string 'full' is not accepted, causing the script to produce no output. [not taken as invalid_value: the log shows no rejection]
- `batch_size=10`: other, The program likely expects batch_size to be a power of two; value 10 is not accepted, resulting in no metrics output. [not taken as invalid_value: the log shows no rejection]
- `nonlinearity=elu`: other, The harness expects a callable activation function (e.g., tf.nn.elu or tf.keras.activations.elu) but received the bare string 'elu', which is not recognized, causing the run to produce no metrics. [not taken as invalid_value: the log shows no rejection]
- `nonlinearity=relu`: other, The program does not recognize 'relu' as a valid activation; it expects a TensorFlow function reference such as tf.nn.relu. [not taken as invalid_value: the log shows no rejection]
- `nonlinearity=tanh`: other, The program likely expects a TensorFlow activation function identifier (e.g., tf.nn.tanh) rather than the plain string 'tanh', causing it to reject the value and produce no metrics. [not taken as invalid_value: the log shows no rejection]
- `nonlinearity=sigmoid`: other, The program expects a TensorFlow activation function reference (e.g., tf.nn.sigmoid) rather than the bare string 'sigmoid', causing it to reject the value and produce no metrics. [not taken as invalid_value: the log shows no rejection]
- `sparse=False`: other, The sparse flag was provided as the string 'False', which the parser did not recognize as a valid boolean value, causing the script to produce no metrics. [not taken as invalid_value: the log shows no rejection]
- `hid_units=1`: other, The model requires hid_units to be an integer greater than 1; a value of 1 leads to no usable features and thus no metrics are produced. [not taken as invalid_value: the log shows no rejection]
- `batch_size=5`: other, The program expects batch_size to be a power of two (or similar constraint); value '5' is invalid, causing no metrics to be parsed. [not taken as invalid_value: the log shows no rejection]
- `batch_size=50`: other, The program did not parse any metrics when batch_size was set to 50, indicating the value was rejected (likely due to type or constraints). A nearby valid batch size is 64. [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `patience=5000`, `patience=10000`

## Knob names
- Ledger names mapped to spec knobs: `learning_rate` → `lr`, `num_attention_heads` → `n_heads`, `activation_function` → `nonlinearity`, `skip_connections` → `residual`, `use_sparse_implementation` → `sparse`, `l2_reg_lambda` → `l2_coef`, `early_stopping_patience` → `patience`, `features_per_head` → `hid_units`, `elapsed_epochs_max` → `nb_epochs`
- Screened though no assumption named them (low prior, code-derived values): `model`
- Code defaults the code doesn't confirm, so no paper-artifact inconsistency is claimed on them: `lr`, `residual`

## Runtime trace (one dry run)
9 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `hid_units`: count (range() bound at models/sp_gat.py:12)
- `lr`: rate (optimizer.learning_rate (AdamOptimizer) at models/base_gattn.py:20)
- `nb_epochs`: count (range() bound at out/cora/execute.py:109)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `dropout_rate`, `num_runs`, `initialization_method`, `optimizer_type`, `validation_metric`, `dataset_split_seed`, `attention_mechanism`, `num_layers`, `tensorflow_version`, `cuda_version`, `random_seed`, `dataset_preprocessing`, `validation_split_source`, `gpu_device_id`, `attention_heads_aggregation`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f8a90dde57cb456c705c32030baddfa2e8037d63b42cae153f0f939605dda90c`
- Cost: Nemotron billed $0.0107, sandbox reported $4441.0787 (total $4441.0894; this search; ledger extraction is included only if it shared the search's router)
