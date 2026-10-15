# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 09:00 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -36.8% | +0.5% | ±1.1% | `positive_rate=0.1`, `lr_schedule=cosine` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -36.8% → +0.5% · 68 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0089`, `B0187`, `B0188`, `B0189`, `B0190` (5 run(s) of the same config)
- Config: `positive_rate` naive `0.3`, changed to `0.1`
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Command:

  Replay: fork checkpoint `cfe77cc3-edc3-4cf9-96ff-c350d734c91e` and run
  ```
  RUN_TAG=35dfd963b761 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.1 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.725, 0.7833, 0.7875, 0.775, 0.725; gap after +0.5%; result checkpoint `a6bf595b-5004-4a31-b0e7-76a5af964c60`
- Effect: candidate 0.775 minus naive 0.4875 = +0.2875, 95% bootstrap interval [+0.2158, +0.3058] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4667, 0.4917, 0.5375, 0.4875, 0.4875
- Spread: range 0.4667 to 0.5375, noise band ±0.0084 (2 x MAD), CV 5.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -36.8% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -18.9% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -34.1% (it comes back)
- PASS · Held-out claim: C2: -35.0% to -18.2% (not worse beyond noise)
- FAIL · Evidence: `positive_rate=0.1`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `lr_schedule=cosine`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.2875 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (26.77 noise units, gap +7.6%); `normalize=minmax` (12.89 noise units, gap -22.7%); `positive_rate=0.15` (9.43 noise units, gap -26.5%); `weight_decay=1e-3` (8.93 noise units, gap -27.0%); `positive_rate=0.65` (6.45 noise units, gap -29.7%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `positive_rate=0.15`: this claim +1.1%, mean |gap| 4.9% (5 runs)
  - `normalize=zscore`, `positive_rate=0.86`: this claim +5.4%, mean |gap| 5.1% (5 runs)
  - `normalize=zscore`, `positive_rate=0.65`: this claim +6.5%, mean |gap| 7.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 10 of 65 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.86); normalize=zscore, positive_rate=0.86 (max I 0.99); normalize=zscore, positive_rate=0.65 (max I 1.48); normalize=zscore, positive_rate=0.15 (max I 1.58)
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-4 (max I 1.47); normalize=zscore, weight_decay=1e-3 (max I 1.51)
  - `normalize`: normalize=zscore (max I 1.52)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.56); lr_schedule=step, normalize=zscore (max I 1.56)
  - `lr_schedule, positive_rate`: lr_schedule=cosine, positive_rate=0.93 (max I 2.77)
- 2 separate islands (no single-knob move joins them): normalize=zscore, positive_rate=0.5; normalize=zscore, positive_rate=0.86; normalize=zscore, weight_decay=1e-4 | lr_schedule=cosine, positive_rate=0.93

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'positive_rate': '0.86'} for 'confirm-combo')
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `positive_rate=0.15` | 5 | +1.1% | -8.7% | 4.9% |
| `normalize=zscore`, `positive_rate=0.86` | 5 | +5.4% | -4.9% | 5.1% |
| `normalize=zscore`, `positive_rate=0.65` | 5 | +6.5% | +8.4% | 7.4% |
| `weight_decay=1e-4`, `normalize=zscore` | 5 | +7.0% | +8.3% | 7.7% |
| `normalize=zscore` | 6 | +7.3% | +8.6% | 7.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The code computes math.log(positive_rate / (1 - positive_rate)), which requires the argument to be > 0. Setting positive_rate to 0.0 makes the argument 0, causing a math domain error; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0005, sandbox reported $0.0000 (total $0.0005; this search; ledger extraction is included only if it shared the search's router)
