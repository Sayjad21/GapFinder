# Gap Report: RippleNet (CIKM 2018), batch-4

Artifact `b4a` · generated 2026-10-19 18:34 · 150 branch runs (0 build/load setups) · sandbox $684.9000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_book_auc (book_auc) | Fits but unsupported | -11.9% | -5.1% | ±1.6% | `lr=0.001` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_book_acc (`book_acc`): paper 0.662, measured 0.613 (-7.4%, band ±1.5%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `THRESHOLD`: "the threshold of rating is 4 for MovieLens-1M, while no threshold is set for Book-Crossing due to its sparsity" (p.6)
  - `baseline_latent_dim`: "For fair consideration, the latent dimensions of all compared baselines are set the same as in Table 2, while other hyper-parameters of baselines are set based on grid search." (p.7)
  - `train_eval_test_ratio`: "For each dataset, the ratio of training, evaluation, and test set is 6 : 2 : 2." (p.7)
  - `negative_sampling_strategy`: "sample an unwatched set marked as 0 for each user, which is of equal size with the rated ones" (p.6)
  - `baseline_hyperparam_search`: "other hyper-parameters of baselines are set based on grid search." (p.7)
  - `num_repetitions`: "Each experiment is repeated 5 times, and the average performance is reported." (p.7)

## C_book_auc: book_auc (paper 0.729)
**Fits but unsupported** · gap -11.9% → -5.1% · 48 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0030`, `B0101`, `B0102`, `B0126` (4 run(s) of the same config)
- Config: `lr` naive `0.02`, changed to `0.001`
- Command:

  Replay: fork checkpoint `ac13dc48-a859-4a2f-adcc-acdc56bf4780` and run
  ```
  RUN_TAG=ed7a4fec54f0 cd /work; mkdir -p out; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=1 TF_NUM_INTRAOP_THREADS=1 TF_NUM_INTEROP_THREADS=1; cd src; n=0; for r in 1 2 3 4 5; do python main.py --dataset book --dim 4 --n_hop 2 --kge_weight 0.01 --l2_weight 1e-7 --lr 0.001 --batch_size 1024 --n_epoch 10 --n_memory 32 --item_update_mode plus_transform > ../out/run$r.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; wait; cd ..; bash gf_harness/emit.sh
  ```
- Output: `book_auc` 0.699, 0.6948, 0.6891, 0.6778; gap after -5.1%; result checkpoint `7ee171de-a881-46e9-9753-aa7ad9c36f8a`
- Effect: candidate 0.692 minus naive 0.642 = +0.04995, 95% bootstrap interval [+0.03321, +0.05254] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `book_auc` = 0.729.

### What did we measure?
- Naive median 0.642 over 5 runs; repeats: 0.6408, 0.635, 0.6479, 0.652, 0.642
- Spread: range 0.635 to 0.652, noise band ±0.0118 (2 x MAD), CV 1.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -11.9% (noise band ±1.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is -11.9% (it comes back)
- PASS · Held-out claim: C_book_acc: -7.4% to -3.8% (not worse beyond noise)
- PASS · Evidence: `lr=0.001`: paper states 'movie:0.02, book:0.001, news:0.005'
- PASS · Effect vs noise: candidate minus naive is +0.04995 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `dim=200`, `dim=400`, `n_memory=320`, `n_memory=160`, `n_memory=1600`, `n_memory=3200`, `n_hop=5`, `n_hop=20`, `n_hop=10`, `n_hop=100`, `n_hop=200`, `n_epoch=100`, `n_epoch=500`, `n_epoch=1000`
- Not settable with this harness: `--dataset`, `THRESHOLD`, `using_all_hops`, `baseline_latent_dim`, `train_eval_test_ratio`, `negative_sampling_strategy`, `baseline_hyperparam_search`, `num_repetitions`, `news_entity_linking`, `statistical_test_alpha`, `kg_max_hops`, `ripple_set_sizes_table4`, `hop_numbers_table5`, `SEP`, `np.random.seed`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.002` (4.53 noise units, gap -4.6%); `n_epoch=1` (3.72 noise units, gap -5.9%); `n_epoch=2` (3.33 noise units, gap -6.5%); `batch_size=10240` (2.68 noise units, gap -7.6%); `lr=0.005` (2.19 noise units, gap -8.4%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=0.002`: this claim -5.5%, mean |gap| 4.1% (4 runs)
  - `n_epoch=2`: this claim -6.9%, mean |gap| 5.9% (4 runs)
  - `lr=0.005`: this claim -8.2%, mean |gap| 6.2% (4 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C_book_auc, among 47 tested
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:37`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/data_loader.py:39`)
  - fixed seed: random seed fixed to 555 (`src/main.py:6`)
  - unexposed setting: `add_argument(..., default=True)`: a switch fixed in the call; no flag sets it (`src/main.py:20`)
  - unexposed setting: `choice(..., replace=False)`: a switch fixed in the call; no flag sets it (`src/preprocess.py:68`)
  - fixed seed: random seed fixed to 555 (`src/preprocess.py:119`)
- Where the code differs from the paper (model-proposed, checked against the repo; literal ones were tried as patch knobs, structural ones are not tested):
  - `src/model.py:34`: paper says H = 3; code does n_hop = 2
  - `src/model.py:150`: paper says η = 0.001; code does learning_rate = 0.02

Notes:
- stopped early: run budget of 150 reached (wanted 1 more run(s) of {'kge_weight': '0.001'} for 'confirm')
- verified from runs already made, after the budget ran out
- capped at Fits but unsupported (was Partially explained): the run budget ran out before the search finished
- patch round stopped early: run budget of 150 reached (wanted 1 more run(s) of {'@ast:src/data_loader.py:37:replace': 'True'} for 'patch screen')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_book_auc | C_book_acc | Mean |gap| |
|---|---|---|---|---|
| `lr=0.002` | 4 | -5.5% | -2.7% | 4.1% |
| `lr=0.001` | 4 | -5.1% | -3.8% | 4.4% |
| `n_epoch=2` | 4 | -6.9% | -4.8% | 5.9% |
| `lr=0.005` | 4 | -8.2% | -4.2% | 6.2% |
| `n_epoch=1` | 4 | -7.5% | -5.9% | 6.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `dim=64`: other, The program produced no parsable metrics when dim=64, indicating the value was rejected (likely due to exceeding allowable model size). A smaller dimension such as 32 preserves the intent of increasing embedding size while remaining within valid bounds. [not taken as invalid_value: the log shows no rejection]

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
- GapFinder commit: `bae25f4f1f69a47fb5def43fc4006a466f1280e7`
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `61be742c0f12d248bf2349aeff13ffb08292a545ed7cdf5fcedfb98bb48d2074`
- Cost: Nemotron billed $0.0055, sandbox reported $684.9000 (total $684.9055; this search; ledger extraction is included only if it shared the search's router)
