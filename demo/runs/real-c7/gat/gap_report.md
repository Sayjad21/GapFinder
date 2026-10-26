# Gap Report: GAT (devset)

Artifact `gat` · generated 2026-10-26 13:09 · 5 branch runs (0 build/load setups) · sandbox $253.2325

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_gat_pubmed (gat_pubmed_acc) | Reproduced | -2.2% | n/a | ±2.5% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_gat_citeseer (`gat_citeseer_acc`): paper 72.5, measured 71.7 (-1.1%, band ±1.0%) (tuned separately in the paper)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `dropout_rate`: "Furthermore, dropout (Srivastava et al., 2014) with p = 0.6 is applied to both layers' inputs, as well as to the normalized attention coefficients" (p.7)
  - `num_runs`: "we report the mean classification accuracy (with standard deviation) on the test nodes of our method after 100 runs" (p.7)
  - `initialization_method`: "Both models are initialized using Glorot initialization (Glorot & Bengio, 2010)" (p.7)
  - `optimizer_type`: "trained to minimize cross-entropy on the training nodes using the Adam SGD optimizer (Kingma & Ba, 2014)" (p.7)
  - `validation_metric`: "early stopping strategy on both the cross-entropy loss and accuracy (transductive) or micro-F1 (inductive) score on the validation nodes" (p.7)
  - `attention_mechanism`: "we also provide the results when a constant attention mechanism, a(x, y) = 1, is used, with the same architecture—this will assign the same weight to every neighbor" (p.7)

## C_gat_pubmed: gat_pubmed_acc (paper 79)
**Reproduced**: naive gap -2.2% is inside the noise band ±2.5%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `gat_pubmed_acc` = 79.

### What did we measure?
- Naive median 77.3 over 5 runs; repeats: 77.4, 75.2, 78.3, 77.3, 76
- Spread: range 75.2 to 78.3, noise band ±2 (2 x MAD), CV 1.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.2% (noise band ±2.5% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `dropout_rate`, `num_runs`, `features_per_head`, `initialization_method`, `optimizer_type`, `validation_metric`, `dataset_split_seed`, `attention_mechanism`, `num_layers`, `tensorflow_version`, `cuda_version`, `random_seed`, `dataset_preprocessing`, `validation_split_source`, `gpu_device_id`, `attention_heads_aggregation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

Notes:
- naive run is within the noise band of the paper's value

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_gat_pubmed | C_gat_cora | C_gat_citeseer | Mean |gap| |
|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | -2.2% | -0.4% | -1.1% | 1.2% |

## Knob names
- Ledger names mapped to spec knobs: `learning_rate` → `lr`, `num_attention_heads` → `n_heads`, `activation_function` → `nonlinearity`, `skip_connections` → `residual`, `use_sparse_implementation` → `sparse`, `l2_reg_lambda` → `l2_coef`, `early_stopping_patience` → `patience`, `elapsed_epochs_max` → `nb_epochs`
- Screened though no assumption named them (low prior, code-derived values): `hid_units`, `model`
- Code defaults the code doesn't confirm, so no paper-artifact inconsistency is claimed on them: `lr`, `residual`

## Runtime trace (one dry run)
9 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `hid_units`: count (range() bound at models/sp_gat.py:12)
- `lr`: rate (optimizer.learning_rate (AdamOptimizer) at models/base_gattn.py:20)
- `nb_epochs`: count (range() bound at out/cora/execute.py:109)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `dropout_rate`, `num_runs`, `features_per_head`, `initialization_method`, `optimizer_type`, `validation_metric`, `dataset_split_seed`, `attention_mechanism`, `num_layers`, `tensorflow_version`, `cuda_version`, `random_seed`, `dataset_preprocessing`, `validation_split_source`, `gpu_device_id`, `attention_heads_aggregation`

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fc48020a37b3caa9b960469768fdcdf9c10084714282df5b984ace12deb2f08e`
- Cost: Nemotron billed $0.0018, sandbox reported $253.2325 (total $253.2344; this search; ledger extraction is included only if it shared the search's router)
