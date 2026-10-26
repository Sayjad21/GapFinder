# Gap Report: RippleNet (batch-4)

Artifact `b4a` · generated 2026-10-26 03:33 · 170 branch runs (0 build/load setups) · sandbox $1084.1345

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_book_auc (book_auc) | Fits but unsupported | -11.6% | -4.9% | ±0.9% | `lr=0.002` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_book_acc (`book_acc`): paper 0.662, measured 0.6165 (-6.9%, band ±0.9%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `THRESHOLD`: "the threshold of rating is 4 for MovieLens-1M, while no threshold is set for Book-Crossing due to its sparsity" (p.6)
  - `baseline_latent_dim`: "For fair consideration, the latent dimensions of all compared baselines are set the same as in Table 2, while other hyper-parameters of baselines are set based on grid search." (p.7)
  - `train_eval_test_ratio`: "For each dataset, the ratio of training, evaluation, and test set is 6 : 2 : 2." (p.7)
  - `negative_sampling_strategy`: "sample an unwatched set marked as 0 for each user, which is of equal size with the rated ones" (p.6)
  - `baseline_hyperparam_search`: "other hyper-parameters of baselines are set based on grid search." (p.7)
  - `num_repetitions`: "Each experiment is repeated 5 times, and the average performance is reported." (p.7)

## C_book_auc: book_auc (paper 0.729)
**Fits but unsupported** · gap -11.6% → -4.9% · 48 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0034`, `B0064`, `B0065`, `B0135` (4 run(s) of the same config)
- Config: `lr` naive `0.02`, changed to `0.002`
- Command:

  Replay: fork checkpoint `ac13dc48-a859-4a2f-adcc-acdc56bf4780` and run
  ```
  @ast:src/data_loader.py:37:replace=False @ast:src/data_loader.py:39:replace=False @ast:src/main.py:20:default=True @ast:src/train.py:58:@mut.17.Call.red.sum=0 @ast:src/train.py:58:@mut.43.Call.red.sum=0 @ast:src/model.py:43:@mut.33.Call.xdiv2=0 @ast:src/model.py:43:@mut.33.Call.xmul2=0 @ast:src/model.py:46:@mut.35.Call.xdiv2=0 @ast:src/model.py:46:@mut.35.Call.xmul2=0 RUN_TAG=8055a5c2956d export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=1 TF_NUM_INTRAOP_THREADS=1 TF_NUM_INTEROP_THREADS=1; cd src; n=0; for r in 1 2 3 4 5; do python main.py --dataset book --dim 4 --n_hop 2 --kge_weight 0.01 --l2_weight 1e-7 --lr 0.002 --batch_size 1024 --n_epoch 10 --n_memory 32 --item_update_mode plus_transform > ../out/run$r.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; wait; cd ..; bash gf_harness/emit.sh
  ```
- Output: `book_auc` 0.695, 0.6895, 0.6913, 0.6955; gap after -4.9%; result checkpoint `4072b1b3-0d90-41e6-ae6b-7d01fd3fa886`
- Effect: candidate 0.6931 minus naive 0.6448 = +0.04835, 95% bootstrap interval [+0.04354, +0.05624] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `book_auc` = 0.729.

### What did we measure?
- Naive median 0.6448 over 5 runs; repeats: 0.6448, 0.6467, 0.6449, 0.6387, 0.6376
- Spread: range 0.6376 to 0.6467, noise band ±0.006448 (2 x MAD), CV 0.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -11.6% (noise band ±0.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is -11.6% (it comes back)
- PASS · Held-out claim: C_book_acc: -6.9% to -2.3% (not worse beyond noise)
- FAIL · Evidence: `lr=0.002`: no evidence mentions '0.002'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.04835 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `dim=200`, `dim=400`, `n_memory=320`, `n_memory=160`, `n_memory=1600`, `n_memory=3200`, `n_hop=5`, `n_hop=20`, `n_hop=10`, `n_hop=100`, `n_hop=200`, `n_epoch=100`, `n_epoch=500`, `n_epoch=1000`
- Not settable with this harness: `--dataset`, `THRESHOLD`, `using_all_hops`, `baseline_latent_dim`, `train_eval_test_ratio`, `negative_sampling_strategy`, `baseline_hyperparam_search`, `num_repetitions`, `news_entity_linking`, `statistical_test_alpha`, `kg_max_hops`, `ripple_set_sizes_table4`, `hop_numbers_table5`, `SEP`, `np.random.seed`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n_epoch=2` (6.03 noise units, gap -6.2%); `lr=0.001` (4.53 noise units, gap -7.5%); `batch_size=10240` (4.14 noise units, gap -7.9%); `batch_size=4096` (1.89 noise units, gap -9.9%); `dim=2` (1.78 noise units, gap -10.0%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `l2_weight=1e-5`, `lr=1e-3`, `n_hop=3`: this claim -5.0%, mean |gap| 3.4% (3 runs)
  - `lr=0.001`: this claim -5.1%, mean |gap| 4.4% (4 runs)
  - `n_epoch=2`: this claim -6.4%, mean |gap| 5.4% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 82% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | the setting lr=0.002 | settings | 18% | 3.3 sigma | run with lr=0.002 |
| 3 | no difference in reporting: the numbers as printed at the end of the run | settings | 0% | 8.0 sigma | the settings search and the other classes |

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C_book_auc, among 56 tested
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:37`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:39`)
  - fixed seed: random seed fixed to 555 (`src/main.py:6`)
  - unexposed setting: `add_argument(..., default=True)`: a switch fixed in the call; no flag sets it (`src/main.py:20`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/preprocess.py:68`)
  - fixed seed: random seed fixed to 555 (`src/preprocess.py:119`)

Notes:
- stopped early: run budget of 200 reached (wanted 1 more run(s) of {'l2_weight': '1e-5', 'lr': '1e-3'} for 'counterfactual')
- verified from runs already made, after the budget ran out
- patch round: none of 3 code-patch configurations fits every claim
- mutation round stopped early: run budget of 200 reached (wanted 1 more run(s) of {'@ast:src/model.py:52:@mut.32.Call.xdiv2': '1'} for 'mutation screen')
- value interval stopped early: run budget of 200 reached (wanted 1 more run(s) of {'lr': '0.001414'} for 'interval lr=0.001414')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_book_auc | C_book_acc | Mean |gap| |
|---|---|---|---|---|
| `l2_weight=1e-5`, `lr=1e-3`, `n_hop=3` | 3 | -5.0% | -1.8% | 3.4% |
| `lr=0.002` | 4 | -4.9% | -2.3% | 3.6% |
| `lr=0.001` | 4 | -5.1% | -3.7% | 4.4% |
| `n_epoch=2` | 4 | -6.4% | -4.3% | 5.4% |
| `batch_size=10240` | 4 | -8.1% | -3.6% | 5.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `dim=64`: other, The program expects dim to be a supported dimension size (likely powers of two up to 32); providing 64 caused the program to produce no metrics, indicating the value was rejected. [not taken as invalid_value: the log shows no rejection]

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
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `486129a52d2f9aa3c281001f447b6d07a241f0a5276d8aa1c82dce5f42a8d704`
- Cost: Nemotron billed $0.0024, sandbox reported $1084.1345 (total $1084.1369; this search; ledger extraction is included only if it shared the search's router)
