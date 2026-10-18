# Gap Report: GAT (ICLR 2018), devbatch-1

Artifact `gat` · generated 2026-10-18 06:52 · 119 branch runs (0 build/load setups) · sandbox $1175.8694

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_gat_pubmed (gat_pubmed_acc) | Fits but unsupported | -2.2% | -0.4% | ±1.0% | `lr=0.05` |

## C_gat_pubmed: gat_pubmed_acc (paper 79)
**Fits but unsupported** · gap -2.2% → -0.4% · 74 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0009`, `B0035`, `B0034`, `B0013` (4 run(s) of the same config)
- Config: `lr` naive `0.005`, changed to `0.05`
- Command:

  Replay: fork checkpoint `3f93d0a9-644f-4d74-9d14-a62d484d4f10` and run
  ```
  RUN_TAG=85c2d5e53d76 bash gf_harness/run_cell.sh batch_size=1 nb_epochs=100000 patience=100 lr=0.05 l2_coef=0.0005 hid_units=8 n_heads=8,1 residual=False nonlinearity=tf.nn.elu model=SpGAT sparse=True
  ```
- Output: `gat_pubmed_acc` 77.7, 79.2, 78.4, 78.9; gap after -0.4%; result checkpoint `b7840775-79b1-4dbd-99da-eac5d3a27d95`
- Effect: candidate 78.65 minus naive 77.3 = +1.35, 95% bootstrap interval [+0.8267, +2.46] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `gat_pubmed_acc` = 79.

### What did we measure?
- Naive median 77.3 over 5 runs; repeats: 76.2, 77.8, 77.3, 77.7, 77.3
- Spread: range 76.2 to 77.8, noise band ±0.8 (2 x MAD), CV 0.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.2% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is -2.2% (it comes back)
- NOTE · Held-out claim, tuned separately: C_gat_cora: +0.5% to -1.0% (not worse beyond noise)
- NOTE · Held-out claim, tuned separately: C_gat_citeseer: +0.6% to -0.1% (not worse beyond noise)
- FAIL · Evidence: `lr=0.05`: no evidence mentions '0.05'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +1.35 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `patience=5000`, `patience=10000`
- Not settable with this harness: `num_attention_heads`, `dropout_rate`, `l2_reg_lambda`, `early_stopping_patience`, `num_runs`, `features_per_head`, `activation_function`, `skip_connections`, `initialization_method`, `optimizer_type`, `validation_metric`, `dataset_split_seed`, `use_sparse_implementation`, `attention_mechanism`, `num_layers`, `tensorflow_version`, `cuda_version`, `random_seed`, `dataset_preprocessing`, `validation_split_source`, `gpu_device_id`, `elapsed_epochs_max`, `attention_heads_aggregation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `lr=0.0025`: this claim -2.3%, mean |gap| 0.8% (4 runs)
  - `lr=0.025`: this claim -1.7%, mean |gap| 0.8% (4 runs)
  - `lr=0.01`: this claim -2.4%, mean |gap| 1.1% (4 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr`: lr=0.05 (max I 0.42); lr=0.025 (max I 1.27)
  - `patience`: patience=200 (max I 0.92); patience=20 (max I 1.25)
  - `nb_epochs`: nb_epochs=200000 (max I 1.09); nb_epochs=20000 (max I 1.25); nb_epochs=500000 (max I 1.25); nb_epochs=50000 (max I 1.34)
  - `hid_units`: hid_units=40 (max I 1.25); hid_units=16 (max I 1.34)

Notes:
- spec knobs no ledger assumption names (nb_epochs, patience, l2_coef, hid_units, residual, sparse) were screened too; no better answer

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_gat_pubmed | C_gat_cora | C_gat_citeseer | Mean |gap| |
|---|---|---|---|---|---|
| `lr=0.05` | 4 | -0.4% | -1.0% | -0.1% | 0.5% |
| `lr=0.0025` | 4 | -2.3% | +0.0% | -0.1% | 0.8% |
| `lr=0.025` | 4 | -1.7% | +0.0% | +0.8% | 0.8% |
| naive (reproduction as run) | 5 | -2.2% | +0.5% | +0.6% | 1.1% |
| `lr=0.01` | 4 | -2.4% | -0.6% | -0.3% | 1.1% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `batch_size=2`: other, The program produced no metrics when batch_size=2, indicating it rejected the value. [not taken as invalid_value: the log shows no rejection]
- `batch_size=4`: other, The program produced no metrics output when batch_size=4, indicating it likely rejected the value as invalid (e.g., unsupported batch size). A nearby valid batch size that preserves the intent of increasing batch size is 2. [not taken as invalid_value: the log shows no rejection]
- `batch_size=full`: other, The program expects batch_size to be a numeric value (e.g., integer) but received the string 'full', which it could not parse, resulting in no metrics being output. [not taken as invalid_value: the log shows no rejection]
- `batch_size=10`: other, The script did not parse any metrics when batch_size=10 was supplied, indicating the value was not accepted (likely due to expecting integer batch sizes that are powers of two or within a specific range). [not taken as invalid_value: the log shows no rejection]
- `lr=0.0001`: other, The program likely rejected the learning rate value as too small, causing numerical issues (e.g., gradients vanishing or optimizer updates ineffective). A nearby valid learning rate that preserves the intent of a small step size is 0.0002. [not taken as invalid_value: the log shows no rejection]
- `lr=5e-05`: other, The learning rate was specified in scientific notation (5e-05) which the program's parser does not accept; a decimal representation of the same value is valid. [not taken as invalid_value: the log shows no rejection]
- `batch_size=5`: other, The program likely requires batch_size to be a power of two; the value '5' is not accepted, causing no metrics to be parsed. [not taken as invalid_value: the log shows no rejection]
- `batch_size=50`: other, The program did not parse any metrics when batch_size was set to 50, indicating the value was rejected (likely outside allowed range or format). A nearby valid batch size that preserves the intent of using a larger batch is 64. [not taken as invalid_value: the log shows no rejection]
- `batch_size=100`: other, The run produced no metrics when batch_size was set to 100, indicating the value was rejected (likely too large for the model/memory). A valid batch size near the intended value is 64, which preserves the intent of using a larger batch while being accepted by the program. [not taken as invalid_value: the log shows no rejection]
- `sparse=False`: other, triage failed: Connection error
- `patience=500`: other, triage failed: Connection error

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `patience=5000`, `patience=10000`

## Knob names
- Ledger names mapped to spec knobs: `learning_rate` → `lr`
- Screened though no assumption named them (low prior, code-derived values): `nb_epochs`, `patience`, `l2_coef`, `hid_units`, `residual`, `sparse`
- Code defaults the code doesn't confirm, so no paper-artifact inconsistency is claimed on them: `lr`

## Runtime trace (one dry run)
9 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `hid_units`: count (range() bound at models/sp_gat.py:12)
- `lr`: rate (optimizer.learning_rate (AdamOptimizer) at models/base_gattn.py:20)
- `nb_epochs`: count (range() bound at out/cora/execute.py:109)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `num_attention_heads`, `dropout_rate`, `l2_reg_lambda`, `early_stopping_patience`, `num_runs`, `features_per_head`, `activation_function`, `skip_connections`, `initialization_method`, `optimizer_type`, `validation_metric`, `dataset_split_seed`, `use_sparse_implementation`, `attention_mechanism`, `num_layers`, `tensorflow_version`, `cuda_version`, `random_seed`, `dataset_preprocessing`, `validation_split_source`, `gpu_device_id`, `elapsed_epochs_max`, `attention_heads_aggregation`

## Provenance
- GapFinder commit: `2af0c3af6b131fabc2f3684594cf852b93fe6830`
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `38a2ad43df12da31f3d53a76c25a0125ff2553050e0c60cc6fa4e2d5f22a99e2`
- Cost: Nemotron billed $0.0049, sandbox reported $1175.8694 (total $1175.8743; this search; ledger extraction is included only if it shared the search's router)
