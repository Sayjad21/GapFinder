# Gap Report: SDCN (batch-5)

Artifact `harness-c7` · generated 2026-10-26 11:00 · 5 branch runs (0 build/load setups) · sandbox $709.4433

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_z_acc (c_z_acc) | Explained by the reporting rule | -1.9% | -0.4% | ±1.0% | reporting rule `best` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_z_nmi (`c_z_nmi`): paper 68.31, measured 63.96 (-6.4%, band ±0.9%)
  - C_z_ari (`c_z_ari`): paper 73.91, measured 69.73 (-5.7%, band ±0.9%)
  - C_z_f1 (`c_z_f1`): paper 90.42, measured 88.69 (-1.9%, band ±1.0%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `--name`: "Our proposed SDCN is evaluated on six datasets. The statistics of these datasets are shown in Table 1 and the detailed descriptions are the followings:" (p.6)
  - `The training loop uses a hardcoded 200 epochs for all datasets, but the paper specifies 50 epochs for graph datasets (ACM, DBLP, Citeseer) and 200 for non-graph datasets.`: "For the non-graph data, we train the SDCN with 200 epochs, and for graph data, we train it with 50 epochs." (p.8)
  - `epochs`: "For the non-graph data, we train the SDCN with 200 epochs, and for graph data, we train it with 50 epochs." (p.8)
  - `sigma`: "In previous experiments, in order to reduce hyperparameter search, we uniformly set the balance coefficient ε to 0.5." (p.9)
  - `alpha`: "For our SDCN, we uniformly set α = 0.1 and β = 0.01 for all the datasets because our method is not sensitive to hyperparameters." (p.8)
  - `beta`: "For our SDCN, we uniformly set α = 0.1 and β = 0.01 for all the datasets because our method is not sensitive to hyperparameters." (p.8)

## C_z_acc: c_z_acc (paper 90.45)
**Explained by the reporting rule** · gap -1.9% → -0.4% · 0 hypotheses tested
> Reporting rule: the paper reports each metric's best epoch, chosen with the test labels. Every claim fits under it, from the runs already made (a flaw in the paper's evaluation)

### Which experiment changed it?
- None was recorded.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `c_z_acc` = 90.45.

### What did we measure?
- Naive median 88.75 over 5 runs; repeats: 88.73, 88.73, 88.75, 88.82, 88.76
- Spread: range 88.73 to 88.82, noise band ±0.8875 (2 x MAD), CV 0.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -1.9% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `--name`, `The training loop uses a hardcoded 200 epochs for all datasets, but the paper specifies 50 epochs for graph datasets (ACM, DBLP, Citeseer) and 200 for non-graph datasets.`, `--pretrain_path`, `epochs`, `sigma`, `alpha`, `dataset_statistics`, `beta`, `gcn_depth`, `variant`, `update_interval`, `The code uses full-batch training (no DataLoader), but the paper specifies batch size 256.`, `v`, `graph_construction`, `optimizer`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the paper reports each metric's best epoch, chosen with the test labels | reporting | 64% | 0.9 sigma (fits every claim) | print the test metric per epoch: is the paper's number the maximum over epochs rather than the last value? |
| 2 | the paper picks one epoch by the headline metric on the test labels and reports every metric there | reporting | 36% | 1.0 sigma (fits every claim) | read every metric at the epoch where the headline test metric peaks |
| 3 | a cause outside every class tested | outside | 0% |  | look for code, data or evaluation differences the classes don't cover |

Notes:
- the paper reports each metric's best epoch, chosen with the test labels: every claim fits within 2 sigma under this reading of the naive runs (C_z_acc 90.13 vs 90.45, C_z_nmi 67.38 vs 68.31, C_z_ari 73.06 vs 73.91, C_z_f1 90.14 vs 90.42, C_q_acc 86.89 vs 86.95, C_q_nmi 58.99 vs 58.9, C_q_ari 65.17 vs 65.25, C_q_f1 86.81 vs 86.84), while the numbers as printed at the end miss the target by 1.3 sigma; no settings search was needed
- equally good readings: the paper picks one epoch by the headline metric on the test labels and reports every metric there
- a flaw in the paper's evaluation, not a reproduction error

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_z_acc | C_z_nmi | C_z_ari | C_z_f1 | C_q_acc | C_q_nmi | C_q_ari | C_q_f1 | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | -1.9% | -6.4% | -5.7% | -1.9% | -0.3% | -0.5% | -0.9% | -0.3% | 2.2% |

## Knob names
- Screened though no assumption named them (low prior, code-derived values): `gf_paper_era_code`

## Runtime trace (one dry run)
3 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `gf_paper_era_code`: rate0 (optimizer.weight_decay (Adam) at sdcn.py:120)
- `lr`: rate (optimizer.lr (Adam) at sdcn.py:120)
- `n_z`: size (width.out_features (Linear) at sdcn.py:32)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--name`, `The training loop uses a hardcoded 200 epochs for all datasets, but the paper specifies 50 epochs for graph datasets (ACM, DBLP, Citeseer) and 200 for non-graph datasets.`, `--pretrain_path`, `epochs`, `sigma`, `alpha`, `dataset_statistics`, `beta`, `gcn_depth`, `variant`, `update_interval`, `The code uses full-batch training (no DataLoader), but the paper specifies batch size 256.`, `v`, `graph_construction`, `optimizer`

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `cf500a6dbb99286aae33b7e12ceb3656c91f7cff264db12739dc4625971ac443`
- Cost: Nemotron billed $0.0020, sandbox reported $709.4433 (total $709.4453; this search; ledger extraction is included only if it shared the search's router)
