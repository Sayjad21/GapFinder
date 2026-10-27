# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 19:53 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.8% | +1.1% | ±1.1% | `positive_rate=0.15`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -30.8% → +1.1% · 70 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0134`, `B0148`, `B0187`, `B0188`, `B0189` (5 run(s) of the same config)
- Config: `positive_rate` naive `0.3`, changed to `0.15`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `8f67f7e4-8c52-450a-93e3-668ea64daf88` and run
  ```
  RUN_TAG=6a6aa904f349 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.15 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7792, 0.7792, 0.7792, 0.7792, 0.7792; gap after +1.1%; result checkpoint `322b9330-4b39-4385-97d7-84889e1b1fe4`
- Effect: candidate 0.7792 minus naive 0.5333 = +0.2459, 95% bootstrap interval [+0.2417, +0.3083] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5333, 0.5375, 0.4875, 0.5375, 0.4667
- Spread: range 0.4667 to 0.5375, noise band ±0.0084 (2 x MAD), CV 6.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.8% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is +7.6% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -32.2% (it comes back)
- PASS · Held-out claim: C2: -27.7% to -8.7% (not worse beyond noise)
- FAIL · Evidence: `positive_rate=0.15`: no evidence mentions '0.15'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2459 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (9.93 noise units, gap -20.0%); `normalize=minmax` (7.44 noise units, gap -22.7%); `weight_decay=1e-4` (5.46 noise units, gap -24.9%); `class_weight=balanced` (2.98 noise units, gap -27.6%); `lr_schedule=step` (1.49 noise units, gap -29.2%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `class_weight=balanced`: this claim -0.5%, mean |gap| 2.1% (5 runs)
  - `positive_rate=0.5`, `normalize=minmax`: this claim +1.6%, mean |gap| 3.3% (5 runs)
  - `positive_rate=0.5`, `normalize=zscore`: this claim +1.6%, mean |gap| 3.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 16 of 67 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.74); class_weight=balanced, normalize=zscore (max I 0.88)
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.5 (max I 0.82); normalize=zscore, positive_rate=0.86 (max I 0.87); normalize=zscore, positive_rate=0.5 (max I 0.9); normalize=zscore, positive_rate=0.65 (max I 1.29)
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-4 (max I 1.29); normalize=zscore, weight_decay=1e-3 (max I 1.32)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.32); lr_schedule=step, normalize=zscore (max I 1.32)
- 2 separate islands (no single-knob move joins them): class_weight=balanced, normalize=minmax; normalize=minmax, positive_rate=0.5; normalize=zscore, positive_rate=0.86 | lr_schedule=cosine, positive_rate=0.93; lr_schedule=cosine, positive_rate=0.86; lr_schedule=cosine, positive_rate=0.15

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'class_weight': 'balanced'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `class_weight=balanced` | 5 | -0.5% | +3.8% | 2.1% |
| `positive_rate=0.5`, `normalize=minmax` | 5 | +1.6% | +5.0% | 3.3% |
| `positive_rate=0.5`, `normalize=zscore` | 5 | +1.6% | +5.2% | 3.4% |
| `class_weight=balanced`, `normalize=zscore` | 2 | +2.2% | +5.9% | 4.0% |
| `positive_rate=0.15`, `normalize=zscore` | 5 | +1.1% | -8.7% | 4.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
