# Gap Report: PyG GAT vs GCN (devbatch-2)

Artifact `pyg` · generated 2026-10-26 03:29 · 5 branch runs (0 build/load setups) · sandbox $82.4991

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C34 (gat_cora_acc) | Reproduced | -0.1% | n/a | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **How the code computes the reported number** (test-score selection, label-based edits, switches fixed for evaluation):
  - `benchmark/inference/inference_benchmark.py:212`: `test(..., progress_bar=True)` on evaluation data: it changes how the evaluation is computed
- **The paper's own comparisons, as measured:**
  - C46 (p.8): "we are able to improve upon GCNs by a margin of 1.5% and 1.6% on Cora and Citeseer, respectively"; gat_cora_acc minus gcn_cora_acc: paper +1.5, measured +1.6 (noise 1.2): holds
  - C47 (p.8): "we are able to improve upon GCNs by a margin of 1.5% and 1.6% on Cora and Citeseer, respectively"; gat_citeseer_acc minus gcn_citeseer_acc: paper +1.6, measured -0.4 (noise 1): **smaller than claimed**
- **Held-out claims outside noise:**
  - C35 (`gat_citeseer_acc`): paper 72.5, measured 70.8 (-2.3%, band ±1.0%)
  - C_gcn_citeseer (`gcn_citeseer_acc`): paper 70.3, measured 71.2 (+1.3%, band ±1.0%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `runs`: "we report the mean classification accuracy (with standard deviation) on the test nodes of our method after 100 runs" (p.7)
  - `batch_size`: "We utilize a batch size of 2 graphs during training" (p.7)
  - `weight_initialization`: "Both models are initialized using Glorot initialization (Glorot & Bengio, 2010)" (p.7)
  - `dataset_splits`: "We allow for only 20 nodes per class to be used for training—however, honoring the transductive setup, the training algorithm has access to all of the nodes' feature vectors. The predictive power of t" (p.6)
  - `ppi_architecture`: "we have, however, successfully employed skip connections (He et al., 2016) across the intermediate attentional layer. We utilize a batch size of 2 graphs during training." (p.7)
  - `skip_connections`: "we have, however, successfully employed skip connections (He et al., 2016) across the intermediate attentional layer" (p.7)

## C34: gat_cora_acc (paper 83)
**Reproduced**: naive gap -0.1% is inside the noise band ±1.0%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
> 83.0 ± 0.7%

- p. 8, Table 2; value used: `gat_cora_acc` = 83 % (headline claim)

### What did we measure?
- Naive median 82.9 over 5 runs; repeats: 82.9, 82.8, 82.9, 83.3, 82.9
- Spread: range 82.8 to 83.3, noise band ±0.829 (2 x MAD), CV 0.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -0.1% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `output_heads`, `runs`, `activation`, `num_layers`, `batch_size`, `weight_initialization`, `dataset_splits`, `ppi_architecture`, `skip_connections`, `const_gat`, `initialization`, `bf16`, `optimizer`, `attention_dropout`, `profile`, `inference`, `cheb_num_hops`, `multi_head_aggregation`, `PPI_dataset_split`, `hardware_device`, `concat`, `validation_metric`, `test_set_size`, `num_classes`, `edge_index_handling`, `permute_masks`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

Notes:
- naive run is within the noise band of the paper's value

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C34 | C35 | C_gcn_cora | C_gcn_citeseer | Mean |gap| |
|---|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | -0.1% | -2.3% | -0.2% | +1.3% | 1.0% |

## Knob names
- Ledger names mapped to spec knobs: `lr` → `gat_lr, gcn_lr`, `weight_decay` → `gat_weight_decay, gcn_weight_decay`, `dropout` → `gat_dropout, gcn_dropout`, `hidden` → `gat_hidden, gcn_hidden`, `heads` → `gat_heads, gat_output_heads`, `early_stopping` → `gat_early_stopping, gcn_early_stopping`, `epochs` → `gat_epochs, gcn_epochs`
- Code defaults the code doesn't confirm, so no paper-artifact inconsistency is claimed on them: `gat_lr`, `gat_weight_decay`, `gcn_lr`, `gcn_weight_decay`

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
Assumptions about knobs the harness spec can't set: `output_heads`, `runs`, `activation`, `num_layers`, `batch_size`, `weight_initialization`, `dataset_splits`, `ppi_architecture`, `skip_connections`, `const_gat`, `initialization`, `bf16`, `optimizer`, `attention_dropout`, `profile`, `inference`, `cheb_num_hops`, `multi_head_aggregation`, `PPI_dataset_split`, `hardware_device`, `concat`, `validation_metric`, `test_set_size`, `num_classes`, `edge_index_handling`, `permute_masks`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `cc82cd7f34b14bb7beaca25ff183fd302b878f6f74d9f181f3d4a56f6263a68a`
- Cost: Nemotron billed $0.0027, sandbox reported $82.4991 (total $82.5018; this search; ledger extraction is included only if it shared the search's router)
