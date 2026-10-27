# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 21:09 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -36.8% | +1.1% | ±5.4% | `normalize=zscore`, `positive_rate=0.15` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -36.8% → +1.1% · 59 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0128`, `B0133`, `B0172`, `B0173`, `B0174` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `positive_rate` naive `0.3`, changed to `0.15`
- Command:

  Replay: fork checkpoint `78d44627-d831-468c-9681-b4705ed111fe` and run
  ```
  RUN_TAG=227fd9dd463a "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.15 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7792, 0.7792, 0.7792, 0.775, 0.7792; gap after +1.1%; result checkpoint `4f961b9f-9c79-4314-8767-5174cba9704f`
- Effect: candidate 0.7792 minus naive 0.4875 = +0.2917, 95% bootstrap interval [+0.2151, +0.3067] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4667, 0.5708, 0.5375, 0.4792, 0.4875
- Spread: range 0.4667 to 0.5708, noise band ±0.0416 (2 x MAD), CV 8.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -36.8% (noise band ±5.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -33.5% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is +7.0% (it comes back)
- PASS · Held-out claim: C2: -35.0% to -8.7% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.15`: no evidence mentions '0.15'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2917 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.61 noise units, gap -17.3%); `positive_rate=0.93` (2.7 noise units, gap -22.2%); `normalize=minmax` (2.6 noise units, gap -22.7%); `lr_schedule=step` (2 noise units, gap -25.9%); `positive_rate=0.1` (1.7 noise units, gap -27.6%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `positive_rate=0.5`: this claim +1.6%, mean |gap| 3.4% (5 runs)
  - `normalize=zscore`, `positive_rate=0.86`: this claim +5.4%, mean |gap| 5.1% (5 runs)
  - `normalize=zscore`, `positive_rate=0.65`: this claim +6.5%, mean |gap| 7.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 17 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.84); normalize=zscore, positive_rate=0.86 (max I 0.85); normalize=zscore, positive_rate=0.65 (max I 1.33); normalize=zscore, positive_rate=0.15 (max I 1.39)
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-4 (max I 1.18); normalize=zscore, weight_decay=1e-3 (max I 1.35)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.21); lr_schedule=step, normalize=zscore (max I 1.21)
  - `normalize`: normalize=zscore (max I 1.33)
  - `lr_schedule, positive_rate`: lr_schedule=cosine, positive_rate=0.93 (max I 2.33)

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'weight_decay': '1e-4'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `positive_rate=0.5` | 5 | +1.6% | +5.2% | 3.4% |
| `normalize=zscore`, `positive_rate=0.15` | 5 | +1.1% | -8.7% | 4.9% |
| `normalize=zscore`, `positive_rate=0.86` | 5 | +5.4% | -4.9% | 5.1% |
| `normalize=zscore`, `positive_rate=0.65` | 5 | +6.5% | +8.4% | 7.4% |
| `normalize=zscore` | 6 | +7.0% | +8.3% | 7.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
