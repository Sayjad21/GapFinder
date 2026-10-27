# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 19:49 · 132 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -22.6% | -0.4% | ±2.4% | `n=6000`, `normalize=minmax` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -22.6% → -0.4% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0060`, `B0079`, `B0112` (3 run(s) of the same config)
- Config: `n` naive `1200`, changed to `6000`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `8e58b44e-c9b9-478d-8e5f-afb4b522a07e` and run
  ```
  RUN_TAG=53cbd118e0a0 "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7017, 0.7025, 0.7075; gap after -0.4%; result checkpoint `2820ffe8-a855-426b-87d3-af9734afaecc`
- Effect: candidate 0.7025 minus naive 0.5458 = +0.1567, 95% bootstrap interval [+0.1484, +0.1922] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.5583, 0.5, 0.5375, 0.55, 0.5458
- Spread: range 0.5 to 0.5583, noise band ±0.0166 (2 x MAD), CV 4.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -22.6% (noise band ±2.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is -15.5% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -19.1% (it comes back)
- PASS · Held-out claim: C2: -12.5% to -1.0% (not worse beyond noise)
- FAIL · Evidence: `n=6000`: no evidence mentions '6000'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1567 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=120` (7.28 noise units, gap -5.4%); `lr_schedule=cosine` (4.27 noise units, gap -12.5%); `normalize=zscore` (2.11 noise units, gap +17.6%)
- Near alternatives (closest across all claims):
  - `n=12000`, `lr_schedule=cosine`: this claim -5.4%, mean |gap| 4.4% (3 runs)
  - `n=12000`, `normalize=minmax`: this claim +4.0%, mean |gap| 6.0% (3 runs)
  - `lr_schedule=cosine`: this claim -11.9%, mean |gap| 6.6% (4 runs)

### History matching (every measured configuration, all claims together)
- 21 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.08); n=12000, normalize=minmax (max I 1.19); n=600, normalize=zscore (max I 2.06); n=24, normalize=minmax (max I 2.36)
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.97); lr_schedule=cosine, n=6000 (max I 2.15); lr_schedule=step, n=12000 (max I 2.19); lr_schedule=step, n=120 (max I 2.51)
  - `class_weight, n`: class_weight=balanced, n=120 (max I 2.05)
  - `lr_schedule`: lr_schedule=cosine (max I 2.16)
- 3 separate islands (no single-knob move joins them): lr_schedule=cosine, n=12000; lr_schedule=cosine, n=6000; lr_schedule=cosine | n=6000, normalize=minmax; n=12000, normalize=minmax; n=600, normalize=zscore | class_weight=balanced, n=120; class_weight=balanced, n=6000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=6000`, `normalize=minmax` | 3 | -0.4% | -1.0% | 0.7% |
| `n=12000`, `lr_schedule=cosine` | 3 | -5.4% | +3.4% | 4.4% |
| `n=12000`, `normalize=minmax` | 3 | +4.0% | +8.0% | 6.0% |
| `lr_schedule=cosine` | 4 | -11.9% | -1.2% | 6.6% |
| `class_weight=balanced`, `n=120` | 3 | -11.3% | -2.2% | 6.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
