# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-15 21:01 · 200 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.9% | -0.5% | ±13.8% | `normalize=minmax`, `positive_rate=0.5` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -31.9% → -0.5% · 55 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0142`, `B0152`, `B0164`, `B0165`, `B0166` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `positive_rate` naive `0.3`, changed to `0.5`
- Command:

  Replay: fork checkpoint `7db0d532-387d-4b5b-a389-67b3c0cba989` and run
  ```
  RUN_TAG=c4e4f7fb3884 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.5 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7875, 0.7792, 0.7875, 0.775, 0.775; gap after -0.5%; result checkpoint `a4fa37d5-4324-4239-a1a4-a45fc16f997b`
- Effect: candidate 0.7792 minus naive 0.5333 = +0.2459, 95% bootstrap interval [+0.205, +0.3109] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5875, 0.4708, 0.475, 0.5458, 0.5333
- Spread: range 0.4708 to 0.5875, noise band ±0.1084 (2 x MAD), CV 9.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.9% (noise band ±13.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -33.0% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -23.9% (it comes back)
- PASS · Held-out claim: C2: -28.4% to +3.8% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2459 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation_method`, `run_tag_seeds`, `cpu`, `memory`, `os`, `python_version`, `random_module`, `disk`, `network`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (1.88 noise units, gap +5.9%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `positive_rate=0.5`: this claim +0.5%, mean |gap| 2.6% (5 runs)
  - `normalize=zscore`, `batch_size=1`: this claim +2.7%, mean |gap| 3.6% (5 runs)
  - `normalize=zscore`, `label_noise=0.1`: this claim +3.2%, mean |gap| 4.0% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=minmax, positive_rate=0.5` (reported)
- `normalize=zscore, positive_rate=0.5`
- `batch_size=1, normalize=zscore`
- `lr_schedule=cosine, positive_rate=0.03`

### History matching (every measured configuration, all claims together)
- 16 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, normalize`: batch_size=1, normalize=zscore (max I 0.37); batch_size=1, normalize=minmax (max I 0.92); batch_size=160, normalize=zscore (max I 1.13)
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.5 (max I 0.59); normalize=zscore, positive_rate=0.5 (max I 0.72)
  - `label_noise, normalize`: label_noise=0.1, normalize=zscore (max I 0.76)
  - `batch_size, lr_schedule`: batch_size=1, lr_schedule=cosine (max I 1.08)
  - `normalize`: normalize=zscore (max I 1.16)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.17); lr_schedule=step, normalize=zscore (max I 1.17)
- Equally good values: `normalize` in {minmax, zscore}; `positive_rate` in {0.03, 0.5}

Notes:
- configurations the target claim can't tell apart from the answer: normalize=minmax, positive_rate=0.5; normalize=zscore, positive_rate=0.5; batch_size=1, normalize=zscore; lr_schedule=cosine, positive_rate=0.03
- equally good values within one noise band (measured): normalize in {minmax, zscore}; positive_rate in {0.03, 0.5}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `positive_rate=0.5` | 5 | -0.5% | +3.8% | 2.2% |
| `normalize=zscore`, `positive_rate=0.5` | 5 | +0.5% | +4.7% | 2.6% |
| `normalize=zscore`, `batch_size=1` | 5 | +2.7% | +4.5% | 3.6% |
| `normalize=zscore`, `label_noise=0.1` | 5 | +3.2% | +4.8% | 4.0% |
| `batch_size=1`, `normalize=minmax` | 5 | +3.7% | +6.1% | 4.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation_method`, `run_tag_seeds`, `cpu`, `memory`, `os`, `python_version`, `random_module`, `disk`, `network`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
