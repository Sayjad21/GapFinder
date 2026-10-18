# Gap Report: GAT vs GCN (PyG benchmark), devbatch-2

Artifact `pyg` · generated 2026-10-18 15:12 · 5 branch runs (0 build/load setups) · sandbox $71.6812

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C34 (gat_cora_acc) | Reproduced | +0.0% | n/a | ±1.0% | — |

## C34: gat_cora_acc (paper 83)
**Reproduced**: naive gap +0.0% is inside the noise band ±1.0%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
> 83.0 ± 0.7%

- p. 8, Table 2; value used: `gat_cora_acc` = 83 % (headline claim)

### What did we measure?
- Naive median 83 over 5 runs; repeats: 83, 83, 83.1, 83, 83.1
- Spread: range 83 to 83.1, noise band ±0.83 (2 x MAD), CV 0.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +0.0% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `lr`, `weight_decay`, `output_heads`, `dropout`, `hidden`, `heads`, `early_stopping`, `epochs`, `runs`, `activation`, `num_layers`, `batch_size`, `weight_initialization`, `dataset_splits`, `ppi_architecture`, `skip_connections`, `const_gat`, `initialization`, `bf16`, `optimizer`, `attention_dropout`, `profile`, `inference`, `cheb_num_hops`, `multi_head_aggregation`, `PPI_dataset_split`, `hardware_device`, `concat`, `validation_metric`, `test_set_size`, `num_classes`, `edge_index_handling`, `permute_masks`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

Notes:
- naive run is within the noise band of the paper's value

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C34 | C35 | C_gcn_cora | C_gcn_citeseer | Mean |gap| |
|---|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | +0.0% | -2.3% | -0.2% | +1.1% | 0.9% |

## Knob names
- Screened though no assumption named them (low prior, code-derived values): `gcn_epochs`, `gcn_lr`, `gcn_weight_decay`, `gcn_early_stopping`, `gcn_hidden`, `gcn_dropout`, `gat_epochs`, `gat_lr`, `gat_weight_decay`, `gat_early_stopping`, `gat_hidden`, `gat_dropout`, `gat_heads`, `gat_output_heads`

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `gat_dropout`: fraction (dropout.p (torch.nn.functional.dropout) at benchmark/citation/gat.py:44)
- `gat_early_stopping`: count (range() bound at benchmark/citation/train_eval.py:41)
- `gat_lr`: rate (optimizer.lr (Adam) at benchmark/citation/train_eval.py:48)
- `gcn_dropout`: fraction (dropout.p (torch.nn.functional.dropout) at benchmark/citation/gcn.py:40)
- `gcn_early_stopping`: count (range() bound at benchmark/citation/train_eval.py:41)
- `gcn_lr`: rate (optimizer.lr (Adam) at benchmark/citation/train_eval.py:48)
- 4 sink value(s) shared by several knobs: no role assigned

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `lr`, `weight_decay`, `output_heads`, `dropout`, `hidden`, `heads`, `early_stopping`, `epochs`, `runs`, `activation`, `num_layers`, `batch_size`, `weight_initialization`, `dataset_splits`, `ppi_architecture`, `skip_connections`, `const_gat`, `initialization`, `bf16`, `optimizer`, `attention_dropout`, `profile`, `inference`, `cheb_num_hops`, `multi_head_aggregation`, `PPI_dataset_split`, `hardware_device`, `concat`, `validation_metric`, `test_set_size`, `num_classes`, `edge_index_handling`, `permute_masks`

## Provenance
- GapFinder commit: `e0117a22e2449e3a3f83893083a771a58c49de9f`
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `a2c807a448b9dad3a7910a9de3fe96cfd21f21753fc169bd889305f5df8f55d5`
- Cost: Nemotron billed $0.0045, sandbox reported $71.6812 (total $71.6857; this search; ledger extraction is included only if it shared the search's router)
