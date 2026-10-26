# Gap Report: RippleNet (batch-4)

Artifact `b4a` · generated 2026-10-27 02:36 · 170 branch runs (0 build/load setups) · sandbox $1212.9827

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_book_auc (book_auc) | Unexplained | -12.1% | -12.1% | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_book_acc (`book_acc`): paper 0.662, measured 0.6119 (-7.6%, band ±1.1%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `THRESHOLD`: "the threshold of rating is 4 for MovieLens-1M, while no threshold is set for Book-Crossing due to its sparsity" (p.6)
  - `baseline_latent_dim`: "For fair consideration, the latent dimensions of all compared baselines are set the same as in Table 2, while other hyper-parameters of baselines are set based on grid search." (p.7)
  - `train_eval_test_ratio`: "For each dataset, the ratio of training, evaluation, and test set is 6 : 2 : 2." (p.7)
  - `negative_sampling_strategy`: "sample an unwatched set marked as 0 for each user, which is of equal size with the rated ones" (p.6)
  - `baseline_hyperparam_search`: "other hyper-parameters of baselines are set based on grid search." (p.7)
  - `num_repetitions`: "Each experiment is repeated 5 times, and the average performance is reported." (p.7)

## C_book_auc: book_auc (paper 0.729)
**Unexplained** · gap -12.1% → -12.1% · 48 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (48 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `book_auc` = 0.729.

### What did we measure?
- Naive median 0.641 over 5 runs; repeats: 0.641, 0.6447, 0.6419, 0.634, 0.6357
- Spread: range 0.634 to 0.6447, noise band ±0.0074 (2 x MAD), CV 0.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -12.1% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: `dim=200`, `dim=400`, `n_memory=320`, `n_memory=160`, `n_memory=1600`, `n_memory=3200`, `n_hop=5`, `n_hop=20`, `n_hop=10`, `n_hop=100`, `n_hop=200`, `n_epoch=100`, `n_epoch=500`, `n_epoch=1000`
- Not settable with this harness: `--dataset`, `THRESHOLD`, `using_all_hops`, `baseline_latent_dim`, `train_eval_test_ratio`, `negative_sampling_strategy`, `baseline_hyperparam_search`, `num_repetitions`, `news_entity_linking`, `statistical_test_alpha`, `kg_max_hops`, `ripple_set_sizes_table4`, `hop_numbers_table5`, `SEP`, `np.random.seed`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.002` (6.32 noise units, gap -5.7%); `lr=0.001` (5.26 noise units, gap -6.7%); `n_epoch=2` (5.03 noise units, gap -7.0%); `n_epoch=1` (4.53 noise units, gap -7.5%); `batch_size=10240` (4.05 noise units, gap -8.0%) (and 10 more in the JSON)
- Near alternatives (closest across all claims):
  - `l2_weight=1e-5`, `lr=1e-3`, `n_hop=3`: this claim -4.3%, mean |gap| 3.0% (3 runs)
  - `lr=0.002`: this claim -6.2%, mean |gap| 4.8% (4 runs)
  - `n_epoch=2`: this claim -6.8%, mean |gap| 6.0% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 100% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | no difference in reporting: the numbers as printed at the end of the run | settings | 0% | 8.3 sigma | the settings search and the other classes |

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C_book_auc, among 57 tested
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:37`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:39`)
  - fixed seed: random seed fixed to 555 (`src/main.py:6`)
  - unexposed setting: `add_argument(..., default=True)`: a switch fixed in the call; no flag sets it (`src/main.py:20`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/preprocess.py:68`)
  - fixed seed: random seed fixed to 555 (`src/preprocess.py:119`)

Notes:
- stopped early: run budget of 200 reached (wanted 1 more run(s) of {'n_hop': '3', 'lr': '1e-3'} for 'counterfactual')
- {'dim': '2'} (gap -11.1%) was verified from existing runs and rejected: did not pass verification
- {'lr': '0.01'} (gap -11.5%) was verified from existing runs and rejected: did not pass verification
- closest configuration not verified: {'l2_weight': '1e-5', 'lr': '1e-3'} (gap -4.0%, 1 of 3 confirmation runs); the budget ran out first, so no attribution is made
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C_book_auc, among 57 tested
- patch round: none of 3 code-patch configurations fits every claim
- mutation round stopped early: run budget of 200 reached (wanted 1 more run(s) of {'@ast:src/model.py:52:@mut.32.Call.xdiv2': '1'} for 'mutation screen')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_book_auc | C_book_acc | Mean |gap| |
|---|---|---|---|---|
| `l2_weight=1e-5`, `lr=1e-3`, `n_hop=3` | 3 | -4.3% | -1.7% | 3.0% |
| `lr=0.002` | 4 | -6.2% | -3.4% | 4.8% |
| `n_epoch=2` | 4 | -6.8% | -5.2% | 6.0% |
| `batch_size=10240` | 4 | -8.8% | -4.1% | 6.5% |
| `lr=0.005` | 4 | -9.1% | -5.1% | 7.1% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `dim=64`: other, The program rejected dim=64, indicating that value is not supported (likely only certain dimensions like powers of two up to 32 are allowed). A nearby valid value preserving the intent of a larger dimension is 32. [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `dim=200`, `dim=400`, `n_memory=320`, `n_memory=160`, `n_memory=1600`, `n_memory=3200`, `n_hop=5`, `n_hop=20`, `n_hop=10`, `n_hop=100`, `n_hop=200`, `n_epoch=100`, `n_epoch=500`, `n_epoch=1000`

## Runtime trace (one dry run)
6 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `lr`: rate (optimizer.learning_rate (AdamOptimizer) at src/model.py:150)
- `n_epoch`: count (range() bound at src/train.py:18)
- `n_hop`: count (range() bound at src/data_loader.py:100)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--dataset`, `THRESHOLD`, `using_all_hops`, `baseline_latent_dim`, `train_eval_test_ratio`, `negative_sampling_strategy`, `baseline_hyperparam_search`, `num_repetitions`, `news_entity_linking`, `statistical_test_alpha`, `kg_max_hops`, `ripple_set_sizes_table4`, `hop_numbers_table5`, `SEP`, `np.random.seed`

## Provenance
- GapFinder commit: `f90b212a502334f9d48b56cb5c3d25e25859b4f0` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `36141cda589016c3e2bb78d87059735564180be5b09f4a23c631656f638fe425`
- Cost: Nemotron billed $0.0026, sandbox reported $1212.9827 (total $1212.9853; this search; ledger extraction is included only if it shared the search's router)
