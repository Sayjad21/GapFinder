# Gap Report: Structural Deep Clustering Network (b5b)

Artifact `harness` · generated 2026-10-20 17:12 · 134 branch runs (0 build/load setups) · sandbox $2025.0154

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_z_acc (c_z_acc) | Unexplained | -2.0% | -2.0% | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_z_nmi (`c_z_nmi`): paper 68.31, measured 63.81 (-6.6%, band ±0.9%)
  - C_z_ari (`c_z_ari`): paper 73.91, measured 69.47 (-6.0%, band ±0.9%)
  - C_z_f1 (`c_z_f1`): paper 90.42, measured 88.58 (-2.0%, band ±1.0%)
  - C_q_ari (`c_q_ari`): paper 65.25, measured 64.6 (-1.0%, band ±1.0%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `--name`: "Our proposed SDCN is evaluated on six datasets. The statistics of these datasets are shown in Table 1 and the detailed descriptions are the followings:" (p.6)
  - `The training loop uses a hardcoded 200 epochs for all datasets, but the paper specifies 50 epochs for graph datasets (ACM, DBLP, Citeseer) and 200 for non-graph datasets.`: "For the non-graph data, we train the SDCN with 200 epochs, and for graph data, we train it with 50 epochs." (p.8)
  - `epochs`: "For the non-graph data, we train the SDCN with 200 epochs, and for graph data, we train it with 50 epochs." (p.8)
  - `sigma`: "In previous experiments, in order to reduce hyperparameter search, we uniformly set the balance coefficient ε to 0.5." (p.9)
  - `alpha`: "For our SDCN, we uniformly set α = 0.1 and β = 0.01 for all the datasets because our method is not sensitive to hyperparameters." (p.8)
  - `beta`: "For our SDCN, we uniformly set α = 0.1 and β = 0.01 for all the datasets because our method is not sensitive to hyperparameters." (p.8)

## C_z_acc: c_z_acc (paper 90.45)
**Unexplained** · gap -2.0% → -2.0% · 31 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (31 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `c_z_acc` = 90.45.

### What did we measure?
- Naive median 88.62 over 5 runs; repeats: 88.61, 88.62, 88.69, 88.49, 88.8
- Spread: range 88.49 to 88.8, noise band ±0.8862 (2 x MAD), CV 0.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.0% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `--name`, `The training loop uses a hardcoded 200 epochs for all datasets, but the paper specifies 50 epochs for graph datasets (ACM, DBLP, Citeseer) and 200 for non-graph datasets.`, `--pretrain_path`, `epochs`, `sigma`, `alpha`, `dataset_statistics`, `beta`, `gcn_depth`, `variant`, `update_interval`, `The code uses full-batch training (no DataLoader), but the paper specifies batch size 256.`, `v`, `graph_construction`, `optimizer`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C_z_nmi, C_z_ari, among 20 tested
- Fit C_z_acc alone (9; worst claim's implausibility in brackets, lowest is the least inconsistent): lr=1e-4 (4.77); n_clusters=30 (5.58); lr=0.0002 (5.67); k=2 (6.15); lr=5e-4 (6.3); k=30 (6.45)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `DataLoader(..., batch_size=256)`: fixed in the call; no flag sets it (`data/pretrain.py:65`)
  - unexposed setting: `topk = 10` is fixed in the code; no flag sets it (`calcu_graph.py:8`)
  - unexposed setting: `DataLoader(..., shuffle=True)`: a switch fixed in the call; no flag sets it (`data/pretrain.py:65`)
  - unexposed setting: `gnn_5(..., active=False)`: a switch fixed in the call; no flag sets it (`sdcn.py:96`)
- Code constants that differ from a value the paper states (matched by name; tried as patch knobs):
  - `data/evaluation.py:66`: the paper states epochs = 200 for non-graph (USPS, HHAR, Reuters), 50 for graph (ACM, DBLP, Citeseer); code has `epoch = 0` (paper: "For the non-graph data, we train the SDCN with 200 epochs, and for graph data, we train it with 50 epochs.")
  - `evaluation.py:66`: the paper states epochs = 200 for non-graph (USPS, HHAR, Reuters), 50 for graph (ACM, DBLP, Citeseer); code has `epoch = 0` (paper: "For the non-graph data, we train the SDCN with 200 epochs, and for graph data, we train it with 50 epochs.")

Notes:
- no hypothesis moved the gap by more than 1 noise units
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C_z_nmi, C_z_ari, among 20 tested
- patch round: none of 18 code-patch configurations fits every claim

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_z_acc | C_z_nmi | C_z_ari | C_z_f1 | C_q_acc | C_q_nmi | C_q_ari | C_q_f1 | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | -2.0% | -6.6% | -6.0% | -2.0% | -0.4% | -0.7% | -1.0% | -0.3% | 2.4% |

## Runtime trace (one dry run)
12 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `lr`: rate (optimizer.lr (Adam) at sdcn.py:120)
- `n_z`: size (width.out_features (Linear) at sdcn.py:32)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--name`, `The training loop uses a hardcoded 200 epochs for all datasets, but the paper specifies 50 epochs for graph datasets (ACM, DBLP, Citeseer) and 200 for non-graph datasets.`, `--pretrain_path`, `epochs`, `sigma`, `alpha`, `dataset_statistics`, `beta`, `gcn_depth`, `variant`, `update_interval`, `The code uses full-batch training (no DataLoader), but the paper specifies batch size 256.`, `v`, `graph_construction`, `optimizer`

## Provenance
- GapFinder commit: `e925a0fae7f1cc50e5f09a1b495decf401d47b77`
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `c0790200f2fedbc9741fe2796e88c1c6a20ad18c85047c03f7e1ba185d459761`
- Cost: Nemotron billed $0.0026, sandbox reported $2025.0154 (total $2025.0180; this search; ledger extraction is included only if it shared the search's router)
