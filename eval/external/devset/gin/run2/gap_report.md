# Gap Report: GIN (ICLR 2019), devbatch-1

Artifact `gin` · generated 2026-10-18 05:08 · 80 branch runs (0 build/load setups) · sandbox $1392.5136

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C69 (imdbb_acc) | Inconclusive | -1.6% | -1.6% | ±1.0% | — |

## C69: imdbb_acc (paper 75.1)
**Inconclusive** · naive gap -1.6% is inside the noise band ±1.0%, but the band is too wide to call it a reproduction.

### Which experiment changed it?
- None could be tested: the noise band is too wide to tell values apart.

### What did the paper report?
> 75.1 ± 5.1

- p. 10, Table 1; value used: `imdbb_acc` = 75.1 % (headline claim)

### What did we measure?
- Naive median 73.9 over 5 runs; repeats: 74.5, 73.8, 73.9, 74.1, 73.2
- Spread: range 73.2 to 74.5, noise band ±0.739 (2 x MAD), CV 0.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -1.6% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: `hidden_dim=640`, `hidden_dim=320`, `hidden_dim=3200`, `hidden_dim=6400`, `batch_size=320`, `batch_size=160`, `batch_size=1600`, `batch_size=3200`, `epochs=3500`, `epochs=1750`, `epochs=17500`, `epochs=35000`, `iters_per_epoch=500`, `iters_per_epoch=250`, `iters_per_epoch=2500`, `iters_per_epoch=5000`, `num_layers=50`, `num_layers=10`, `num_layers=25`, `num_layers=250`, `num_layers=500`, `num_mlp_layers=20`, `num_mlp_layers=10`, `num_mlp_layers=100`, `num_mlp_layers=200`
- Not settable with this harness: `--degree_as_tag`, `--learn_eps`, `--fold_idx`, `dataset.zip contents / unzip`, `--neighbor_pooling_type`, `Reddit node features (all same)`, `social non-Reddit node features (degree one-hot)`, `readout function (sum vs mean)`, `Adam optimizer`, `batch normalization`, `bioinformatics node features (categorical)`, `--device`, `hardware (CPU/GPU/memory)`, `--seed`, `WL iterations`, `SVM C parameter (WL kernel)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `lr=0.002`: this claim -1.5%, mean |gap| 1.1% (4 runs)
  - `lr=0.005`: this claim -1.2%, mean |gap| 1.5% (4 runs)
  - `graph_pooling_type=average`: this claim -1.0%, mean |gap| 1.5% (4 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `lr`: lr=0.005 (max I 1.01); lr=0.002 (max I 1.33)
  - `graph_pooling_type`: graph_pooling_type=average (max I 1.06)
  - `iters_per_epoch`: iters_per_epoch=25 (max I 1.09); iters_per_epoch=100 (max I 1.19); iters_per_epoch=5 (max I 1.39)
  - `hidden_dim`: hidden_dim=6 (max I 1.36); hidden_dim=16 (max I 1.44)
  - `batch_size`: batch_size=64 (max I 1.41)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `pass_data_iteratively(..., minibatch_size=64)`: a default no call in the repo overrides (2 call(s)) (`main.py:52`)
  - unexposed setting: `StepLR(..., gamma=0.5)`: fixed in the call; no flag sets it (`main.py:137`)
  - fixed seed: random seed fixed to 0 (`main.py:123`)
  - fixed seed: random seed fixed to 0 (`main.py:124`)
- Where the code differs from the paper (model-proposed, checked against the repo; literal ones were tried as patch knobs, structural ones are not tested):
  - `main.py:52`: paper says minibatch of size 128; code does minibatch_size = 64
  - `main.py:140`: paper says a single epoch with the best cross-validation accuracy averaged over the 10 folds was selected.; code does fixed 350 epochs training loop

Notes:
- stopped early: run budget of 80 reached (wanted 1 more run(s) of {'lr': '0.1'} for 'confirm')
- {'hidden_dim': '32'} (gap -1.8%) was verified from existing runs and rejected: did not pass verification
- {'hidden_dim': '16'} (gap -1.6%) was verified from existing runs and rejected: did not pass verification
- {'batch_size': '128'} (gap -2.5%) was verified from existing runs and rejected: did not pass verification
- closest configuration not verified: {'iters_per_epoch': '25'} (gap -1.5%, 1 of 3 confirmation runs); the budget ran out first, so no attribution is made
- spec knobs no ledger assumption names (final_dropout, num_layers, num_mlp_layers) were screened too; no better answer
- the gap (-1.6%) is below the minimum detectable effect (±1.9% with 3 runs per configuration at 80% power): even a setting that closed it couldn't have been confirmed, so 'nothing explains it' can't be claimed either

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C69 | C70 | C76 | C74 | Mean |gap| |
|---|---|---|---|---|---|---|
| `lr=0.002` | 4 | -1.5% | -0.8% | -1.7% | -0.3% | 1.1% |
| `lr=0.005` | 4 | -1.2% | -2.2% | -2.1% | -0.3% | 1.5% |
| `graph_pooling_type=average` | 4 | -1.0% | -1.6% | -2.5% | -0.9% | 1.5% |
| `lr=0.001` | 4 | -1.9% | -1.0% | -3.4% | -0.9% | 1.8% |
| `hidden_dim=6` | 4 | -1.7% | -2.1% | -4.4% | -1.2% | 2.4% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `hidden_dim=640`, `hidden_dim=320`, `hidden_dim=3200`, `hidden_dim=6400`, `batch_size=320`, `batch_size=160`, `batch_size=1600`, `batch_size=3200`, `epochs=3500`, `epochs=1750`, `epochs=17500`, `epochs=35000`, `iters_per_epoch=500`, `iters_per_epoch=250`, `iters_per_epoch=2500`, `iters_per_epoch=5000`, `num_layers=50`, `num_layers=10`, `num_layers=25`, `num_layers=250`, `num_layers=500`, `num_mlp_layers=20`, `num_mlp_layers=10`, `num_mlp_layers=100`, `num_mlp_layers=200`

## Runtime trace (one dry run)
41 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `batch_size`: count (range() bound at models/graphcnn.py:131)
- `final_dropout`: fraction (scheduler.gamma (StepLR) at main.py:137)
- `iters_per_epoch`: count (scheduler.step_size (StepLR) at main.py:137)
- `lr`: rate (optimizer.lr (Adam) at main.py:136)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--degree_as_tag`, `--learn_eps`, `--fold_idx`, `dataset.zip contents / unzip`, `--neighbor_pooling_type`, `Reddit node features (all same)`, `social non-Reddit node features (degree one-hot)`, `readout function (sum vs mean)`, `Adam optimizer`, `batch normalization`, `bioinformatics node features (categorical)`, `--device`, `hardware (CPU/GPU/memory)`, `--seed`, `WL iterations`, `SVM C parameter (WL kernel)`

## Provenance
- GapFinder commit: `2af0c3af6b131fabc2f3684594cf852b93fe6830`
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `312c9757c513e99287d08b787a2416db4d263deeb9c09a04e70ab30660fda3b3`
- Cost: Nemotron billed $0.0050, sandbox reported $1392.5136 (total $1392.5186; this search; ledger extraction is included only if it shared the search's router)
