# Gap Report: test-gen-07

Artifact `mlbench` · generated 2026-10-15 00:48 · 21 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | +8.8% | +1.7% | ±1.1% | `lr_schedule=step` |

## C1: test_accuracy (paper 0.4938)
**Fits but unsupported** · gap +8.8% → +1.7% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0011`, `B0012`, `B0013` (4 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `step`
- Command:

  Replay: fork checkpoint `5f976995-8f9b-43d9-b471-c93c1d8c3b0f` and run
  ```
  RUN_TAG=f14de6b71dbe "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule step --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.5083, 0.4833, 0.5125, 0.4958; gap after +1.7%; result checkpoint `1ddd08a5-c387-4b58-b9bb-23eea05b59c1`
- Effect: candidate 0.502 minus naive 0.5375 = -0.03545, 95% bootstrap interval [-0.05252, -0.02332] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.494 test accuracy.

- p. 1; value used: `test_accuracy` = 0.4938 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5333, 0.5375, 0.5375, 0.5333, 0.5375
- Spread: range 0.5333 to 0.5375, noise band ±0.005375 (2 x MAD), CV 0.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +8.8% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +8.8% (it comes back)
- PASS · Held-out claim: C2: +11.9% to +2.9% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=step`: no evidence mentions 'step'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -0.03545 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs_aggregation`, `run_seeds`, `init_scale`, `splitting_method`, `python_version`, `os`, `hardware`, `gauss_algorithm`, `random_algorithm`, `normalizer_scope`, `shuffle_per_epoch`, `loss_function`, `gradient_calculation`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule`: lr_schedule=step (max I 0.5)
  - `class_weight`: class_weight=balanced (max I 2.37)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 2.52)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=step` | 4 | +1.7% | +2.9% | 2.3% |
| naive (reproduction as run) | 5 | +8.8% | +11.9% | 10.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs_aggregation`, `run_seeds`, `init_scale`, `splitting_method`, `python_version`, `os`, `hardware`, `gauss_algorithm`, `random_algorithm`, `normalizer_scope`, `shuffle_per_epoch`, `loss_function`, `gradient_calculation`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
