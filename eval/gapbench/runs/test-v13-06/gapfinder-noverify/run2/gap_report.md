# Gap Report: test-v13-06

Artifact `mlbench` · generated 2026-10-16 00:14 · 182 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explained | -35.5% | +0.6% | ±5.5% | `normalize=zscore`, `n=1000` |

## C1: test_accuracy (paper 0.7558)
**Explained** · gap -35.5% → +0.6% · 64 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0065`, `B0101`, `B0134`, `B0135`, `B0136` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `1000`
- Command:

  Replay: fork checkpoint `a4374629-dae6-4690-8275-56b5f9cfff04` and run
  ```
  RUN_TAG=a1f7a93b5e54 "${PYTHON:-python3}" train.py --n 1000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.76, 0.76, 0.76, 0.765, 0.76; gap after +0.6%; result checkpoint `d3a522f6-3612-4404-a2a7-9620d65fefa9`
- Effect: candidate 0.76 minus naive 0.4875 = +0.2725, 95% bootstrap interval [+0.2269, +0.2943] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.756 test accuracy and 0.728 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7558 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4667, 0.4875, 0.4667, 0.5458, 0.4917
- Spread: range 0.4667 to 0.5458, noise band ±0.0416 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.5% (noise band ±5.5% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.2725 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.91 noise units, gap -14.0%); `normalize=minmax` (2.6 noise units, gap -21.2%); `n=120` (2.3 noise units, gap -22.8%); `n=240` (2.3 noise units, gap -22.8%); `n=12000` (1.59 noise units, gap -26.7%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=12000`, `normalize=zscore`: this claim +0.2%, mean |gap| 0.4% (5 runs)
  - `n=6000`, `normalize=zscore`: this claim -1.0%, mean |gap| 1.2% (5 runs)
  - `n=2000`, `normalize=zscore`: this claim +1.2%, mean |gap| 1.8% (5 runs)

### Equally good configurations
The target claim can't tell these 7 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=1000, normalize=zscore` (reported)
- `n=12000, normalize=zscore`
- `class_weight=balanced, normalize=minmax`
- `n=6000, normalize=zscore`
- `n=2000, normalize=zscore`
- `n=600, normalize=zscore`
- `n=120, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 16 of 60 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=12000, normalize=zscore (max I 0.02); n=1000, normalize=zscore (max I 0.12); n=6000, normalize=zscore (max I 0.24); n=2000, normalize=zscore (max I 0.4); +4 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.06); class_weight=balanced, normalize=zscore (max I 1.37)
- 2 separate islands (no single-knob move joins them): n=12000, normalize=zscore; n=1000, normalize=zscore; n=6000, normalize=zscore | lr_schedule=cosine, n=12000; lr_schedule=cosine, n=6000
- Equally good values: `n` in {120, 600, 1000, 2000, 2400, 6000, 12000}

Notes:
- configurations the target claim can't tell apart from the answer: n=1000, normalize=zscore; n=12000, normalize=zscore; class_weight=balanced, normalize=minmax; n=6000, normalize=zscore; n=2000, normalize=zscore; n=600, normalize=zscore; n=120, normalize=zscore
- equally good values within one noise band (measured): n in {120, 600, 1000, 2000, 2400, 6000, 12000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=12000`, `normalize=zscore` | 5 | +0.2% | +0.5% | 0.4% |
| `n=1000`, `normalize=zscore` | 5 | +0.6% | +0.4% | 0.5% |
| `n=6000`, `normalize=zscore` | 5 | -1.0% | -1.4% | 1.2% |
| `n=2000`, `normalize=zscore` | 5 | +1.2% | +2.3% | 1.8% |
| `n=120`, `normalize=zscore` | 5 | -0.8% | +2.8% | 1.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: invalid_value, Setting n=1 results in zero training samples after the 0.8 split, leaving Xtr empty and causing an IndexError when the code tries to access Xtr[0]. A value of n=2 yields at least one training sample while preserving the intent of using a small dataset for quick testing; retried as `n=2`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0008, sandbox reported $0.0000 (total $0.0008; this search; ledger extraction is included only if it shared the search's router)
