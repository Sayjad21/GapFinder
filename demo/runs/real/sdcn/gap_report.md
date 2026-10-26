# Gap Report: SDCN (batch-5)

Artifact `harness` · generated 2026-10-26 09:44 · 155 branch runs (0 build/load setups) · sandbox $9084.4452

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_z_acc (c_z_acc) | Unexplained | -2.1% | -2.1% | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_z_nmi (`c_z_nmi`): paper 68.31, measured 63.7 (-6.7%, band ±0.9%)
  - C_z_ari (`c_z_ari`): paper 73.91, measured 69.34 (-6.2%, band ±0.9%)
  - C_z_f1 (`c_z_f1`): paper 90.42, measured 88.5 (-2.1%, band ±1.0%)
  - C_q_nmi (`c_q_nmi`): paper 58.9, measured 58.25 (-1.1%, band ±1.0%)
  - C_q_ari (`c_q_ari`): paper 65.25, measured 64.24 (-1.5%, band ±1.0%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `--name`: "Our proposed SDCN is evaluated on six datasets. The statistics of these datasets are shown in Table 1 and the detailed descriptions are the followings:" (p.6)
  - `The training loop uses a hardcoded 200 epochs for all datasets, but the paper specifies 50 epochs for graph datasets (ACM, DBLP, Citeseer) and 200 for non-graph datasets.`: "For the non-graph data, we train the SDCN with 200 epochs, and for graph data, we train it with 50 epochs." (p.8)
  - `epochs`: "For the non-graph data, we train the SDCN with 200 epochs, and for graph data, we train it with 50 epochs." (p.8)
  - `sigma`: "In previous experiments, in order to reduce hyperparameter search, we uniformly set the balance coefficient ε to 0.5." (p.9)
  - `alpha`: "For our SDCN, we uniformly set α = 0.1 and β = 0.01 for all the datasets because our method is not sensitive to hyperparameters." (p.8)
  - `beta`: "For our SDCN, we uniformly set α = 0.1 and β = 0.01 for all the datasets because our method is not sensitive to hyperparameters." (p.8)

## C_z_acc: c_z_acc (paper 90.45)
**Unexplained** · gap -2.1% → -2.1% · 55 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (55 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `c_z_acc` = 90.45.

### What did we measure?
- Naive median 88.56 over 5 runs; repeats: 88.56, 88.62, 88.75, 88.54, 88.53
- Spread: range 88.53 to 88.75, noise band ±0.8856 (2 x MAD), CV 0.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.1% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `--name`, `The training loop uses a hardcoded 200 epochs for all datasets, but the paper specifies 50 epochs for graph datasets (ACM, DBLP, Citeseer) and 200 for non-graph datasets.`, `--pretrain_path`, `epochs`, `sigma`, `alpha`, `dataset_statistics`, `beta`, `gcn_depth`, `variant`, `update_interval`, `The code uses full-batch training (no DataLoader), but the paper specifies batch size 256.`, `v`, `graph_construction`, `optimizer`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `n_clusters=10`: this claim -1.8%, mean |gap| 2.2% (4 runs)
  - `k=5`: this claim -1.9%, mean |gap| 2.4% (4 runs)
  - `k=2`: this claim -2.0%, mean |gap| 2.4% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 100% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | no difference in reporting: the numbers as printed at the end of the run | settings | 0% | 4.5 sigma | the settings search and the other classes |

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C_z_nmi, C_z_ari, among 32 tested
- Fit C_z_acc alone (10; worst claim's implausibility in brackets, lowest is the least inconsistent): k=10, lr=1e-4 (4.74); lr=1e-4, n_clusters=4 (5.17); k=2, lr=1e-4 (5.43); k=10, lr=5e-4 (5.83); lr=1e-4, n_clusters=10 (5.91); lr=5e-4, n_clusters=4 (5.95)
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
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C_z_nmi, C_z_ari, among 32 tested
- patch round: none of 18 code-patch configurations fits every claim
- mutation round: none of 14 mutants moved C_z_acc toward the paper

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_z_acc | C_z_nmi | C_z_ari | C_z_f1 | C_q_acc | C_q_nmi | C_q_ari | C_q_f1 | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `n_clusters=10` | 4 | -1.8% | -6.1% | -5.4% | -1.8% | -0.4% | -0.8% | -1.2% | -0.4% | 2.2% |
| `k=5` | 4 | -1.9% | -6.5% | -5.7% | -1.9% | -0.4% | -0.9% | -1.2% | -0.4% | 2.4% |
| `k=2` | 4 | -2.0% | -6.6% | -6.0% | -2.1% | -0.3% | -0.7% | -1.0% | -0.3% | 2.4% |
| `n_clusters=2` | 4 | -2.0% | -6.7% | -6.1% | -2.1% | -0.3% | -0.6% | -1.0% | -0.3% | 2.4% |
| `n_clusters=4` | 4 | -2.0% | -6.7% | -6.0% | -2.0% | -0.4% | -0.9% | -1.2% | -0.4% | 2.5% |

## Runtime trace (one dry run)
12 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `lr`: rate (optimizer.lr (Adam) at sdcn.py:120)
- `n_z`: size (width.out_features (Linear) at sdcn.py:32)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--name`, `The training loop uses a hardcoded 200 epochs for all datasets, but the paper specifies 50 epochs for graph datasets (ACM, DBLP, Citeseer) and 200 for non-graph datasets.`, `--pretrain_path`, `epochs`, `sigma`, `alpha`, `dataset_statistics`, `beta`, `gcn_depth`, `variant`, `update_interval`, `The code uses full-batch training (no DataLoader), but the paper specifies batch size 256.`, `v`, `graph_construction`, `optimizer`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `64a46cdf0e6db35374b675b92242d901c63686b4eb80a984474af0913dec50ae`
- Cost: Nemotron billed $0.0023, sandbox reported $9084.4452 (total $9084.4475; this search; ledger extraction is included only if it shared the search's router)
