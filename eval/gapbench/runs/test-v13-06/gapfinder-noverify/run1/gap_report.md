# Gap Report: test-v13-06

Artifact `mlbench` · generated 2026-10-15 23:45 · 128 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explained | -28.9% | -0.8% | ±0.7% | `normalize=zscore`, `n=6000` |

## C1: test_accuracy (paper 0.7558)
**Explained** · gap -28.9% → -0.8% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0043`, `B0082`, `B0115` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `6000`
- Command:

  Replay: fork checkpoint `6e17358a-da1e-4419-9b9f-88635eb4fee8` and run
  ```
  RUN_TAG=aa3d26088fd5 "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.75, 0.7475, 0.7508; gap after -0.8%; result checkpoint `2c8f6406-ccda-4d74-b987-6567ac052581`
- Effect: candidate 0.75 minus naive 0.5375 = +0.2125, 95% bootstrap interval [+0.1886, +0.2156] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.756 test accuracy and 0.728 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7558 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5333, 0.5375, 0.5375, 0.5375, 0.5667
- Spread: range 0.5333 to 0.5667, noise band ±0.005375 (2 x MAD), CV 2.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -28.9% (noise band ±0.7% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.2125 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (12.41 noise units, gap -20.1%); `normalize=minmax` (10.85 noise units, gap -21.2%); `n=10000` (10.7 noise units, gap -21.3%); `n=2400` (4.65 noise units, gap -25.6%); `class_weight=balanced` (3.87 noise units, gap -26.1%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `n=12000`: this claim +0.1%, mean |gap| 0.1% (3 runs)
  - `n=10000`, `normalize=zscore`: this claim -0.6%, mean |gap| 0.3% (3 runs)
  - `normalize=zscore`, `n=600`: this claim -1.9%, mean |gap| 2.8% (3 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=6000, normalize=zscore` (reported)
- `n=12000, normalize=zscore`
- `n=10000, normalize=zscore`
- `class_weight=balanced, normalize=minmax`
- `n=600, normalize=zscore`
- `n=12000, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 16 of 52 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=12000, normalize=zscore (max I 0.01); n=10000, normalize=zscore (max I 0.12); n=6000, normalize=zscore (max I 0.25); n=600, normalize=zscore (max I 0.73); +3 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.36); class_weight=balanced, normalize=zscore (max I 1.57)
  - `normalize`: normalize=zscore (max I 2.18)
- 2 separate islands (no single-knob move joins them): n=12000, normalize=zscore; n=10000, normalize=zscore; n=6000, normalize=zscore | lr_schedule=cosine, n=12000; lr_schedule=cosine, n=10000
- Equally good values: `n` in {6000, 10000, 12000}

Notes:
- configurations the target claim can't tell apart from the answer: n=6000, normalize=zscore; n=12000, normalize=zscore; n=10000, normalize=zscore; class_weight=balanced, normalize=minmax; n=600, normalize=zscore; n=12000, normalize=minmax
- equally good values within one noise band (measured): n in {6000, 10000, 12000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `n=12000` | 3 | +0.1% | +0.1% | 0.1% |
| `n=10000`, `normalize=zscore` | 3 | -0.6% | +0.0% | 0.3% |
| `n=6000`, `normalize=zscore` | 3 | -0.8% | -1.3% | 1.0% |
| `normalize=zscore`, `n=600` | 3 | -1.9% | -3.8% | 2.8% |
| `normalize=minmax`, `class_weight=balanced` | 3 | +0.9% | +7.3% | 4.1% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: crash, Setting n=1 resulted in an extremely small dataset; after splitting and preprocessing, the training set Xtr became empty, causing an IndexError when the code tried to access Xtr[0]. This is a runtime crash, not a direct rejection of the parameter value

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0005, sandbox reported $0.0000 (total $0.0005; this search; ledger extraction is included only if it shared the search's router)
