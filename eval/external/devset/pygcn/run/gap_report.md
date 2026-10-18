# Gap Report: pygcn vs GCN (Kipf & Welling 2017), devset

Artifact `pygcn` · generated 2026-10-17 21:37 · 135 branch runs (0 build/load setups) · sandbox $20.3871

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_cora (cora_acc) | Unexplained | +2.5% | +2.5% | ±1.0% | — |

## C_cora: cora_acc (paper 81.5)
**Unexplained** · gap +2.5% → +2.5% · 46 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (46 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `cora_acc` = 81.5.

### What did we measure?
- Naive median 83.5 over 5 runs; repeats: 82.8, 83.4, 83.9, 83.6, 83.5
- Spread: range 82.8 to 83.9, noise band ±0.835 (2 x MAD), CV 0.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +2.5% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: `framework`, `--no-cuda`, `--seed`, `early_stopping_window`, `weight_initialization`, `feature_normalization`, `dataset_splits`, `test_set_size`, `validation_set_size`, `hyperparam_opt_dataset`, `adjacency_matrix`, `propagation_model`, `num_layers`, `residual_connections`, `--fastmode`, `label_rate`, `random_graph_hidden`, `random_graph_regularization`, `nell_preprocessing`, `optimizer`, `random_graph_feature_matrix`, `random_graph_edges`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `weight_decay=1e-4` (1.8 noise units, gap -0.6%); `weight_decay=5e-05` (1.32 noise units, gap +1.1%); `weight_decay=5e-06` (1.2 noise units, gap -1.2%)
- Near alternatives (closest across all claims):
  - `weight_decay=5e-06`: this claim -0.2%, mean |gap| 0.2% (4 runs)
  - `hidden=160`: this claim +1.5%, mean |gap| 1.5% (4 runs)
  - `weight_decay=1e-5`: this claim +1.5%, mean |gap| 1.5% (4 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `weight_decay`: weight_decay=5e-06 (max I 0.27); weight_decay=1e-5 (max I 1.05); weight_decay=0.00025 (max I 1.13); weight_decay=1e-4 (max I 1.4); +1 more
  - `hidden`: hidden=160 (max I 1.29); hidden=128 (max I 1.45)
  - `dropout`: dropout=0.05 (max I 1.45); dropout=0.25 (max I 1.45); dropout=0.1 (max I 1.5)

Notes:
- no hypothesis moved the gap by more than 1 noise units
- spec knobs no ledger assumption names (dropout, epochs, hidden, lr) were screened too; no better answer
- history matching: the naive configuration is within noise of every claim

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_cora | Mean |gap| |
|---|---|---|---|
| `weight_decay=5e-06` | 4 | -0.2% | 0.2% |
| `hidden=160` | 4 | +1.5% | 1.5% |
| `weight_decay=1e-5` | 4 | +1.5% | 1.5% |
| `hidden=128` | 4 | +1.5% | 1.5% |
| `dropout=0.1` | 4 | +1.6% | 1.6% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `dropout`: fraction (dropout.p (torch.nn.functional.dropout) at pygcn/models.py:16)
- `epochs`: count (range() bound at pygcn/train.py:100)
- `lr`: rate (optimizer.lr (Adam) at pygcn/train.py:49)
- `weight_decay`: rate0 (optimizer.weight_decay (Adam) at pygcn/train.py:49)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `framework`, `--no-cuda`, `--seed`, `early_stopping_window`, `weight_initialization`, `feature_normalization`, `dataset_splits`, `test_set_size`, `validation_set_size`, `hyperparam_opt_dataset`, `adjacency_matrix`, `propagation_model`, `num_layers`, `residual_connections`, `--fastmode`, `label_rate`, `random_graph_hidden`, `random_graph_regularization`, `nell_preprocessing`, `optimizer`, `random_graph_feature_matrix`, `random_graph_edges`

## Provenance
- GapFinder commit: `2af0c3af6b131fabc2f3684594cf852b93fe6830` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `e1ad0417966aac5dd97355eca164e9294df4ee273d9485a2e23dee6a762f050b`
- Cost: Nemotron billed $0.0000, sandbox reported $20.3871 (total $20.3871; this search; ledger extraction is included only if it shared the search's router)
