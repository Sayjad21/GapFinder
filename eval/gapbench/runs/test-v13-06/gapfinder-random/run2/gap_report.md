# Gap Report: test-v13-06

Artifact `mlbench` · generated 2026-10-16 00:15 · 120 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -28.9% | +1.2% | ±1.1% | `n=1000`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7558)
**Fits but unsupported** · gap -28.9% → +1.2% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0057`, `B0082`, `B0108` (3 run(s) of the same config)
- Config: `n` naive `1200`, changed to `1000`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `657d4ab6-655b-478d-9e86-7b6219e3e340` and run
  ```
  RUN_TAG=c643bec41536 "${PYTHON:-python3}" train.py --n 1000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.765, 0.76, 0.765; gap after +1.2%; result checkpoint `7aa47a79-c516-4c69-8657-3efeed1ae70d`
- Effect: candidate 0.765 minus naive 0.5375 = +0.2275, 95% bootstrap interval [+0.205, +0.23] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.756 test accuracy and 0.728 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7558 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5417, 0.5625, 0.5333, 0.5375, 0.5375
- Spread: range 0.5333 to 0.5625, noise band ±0.0084 (2 x MAD), CV 2.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -28.9% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is +9.7% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -35.8% (it comes back)
- PASS · Held-out claim: C2: -25.5% to +0.9% (not worse beyond noise)
- FAIL · Evidence: `n=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2275 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=24` (20.73 noise units, gap +5.8%); `lr_schedule=cosine` (9.43 noise units, gap -18.4%); `normalize=minmax` (6.94 noise units, gap -21.2%); `n=6000` (6.35 noise units, gap -21.8%); `lr_schedule=step` (3.96 noise units, gap -24.5%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `n=12000`: this claim +0.0%, mean |gap| 0.1% (3 runs)
  - `normalize=zscore`, `n=6000`: this claim -1.0%, mean |gap| 1.2% (3 runs)
  - `n=2000`, `normalize=zscore`: this claim +1.2%, mean |gap| 1.8% (3 runs)

### Equally good configurations
The target claim can't tell these 7 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=1000, normalize=zscore` (reported)
- `n=24`
- `n=12000, normalize=zscore`
- `class_weight=balanced, normalize=minmax`
- `n=6000, normalize=zscore`
- `n=2000, normalize=zscore`
- `n=600, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 13 of 52 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=12000, normalize=zscore (max I 0.02); n=1000, normalize=zscore (max I 0.19); n=6000, normalize=zscore (max I 0.27); n=2000, normalize=zscore (max I 0.46); +2 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.31); class_weight=balanced, normalize=zscore (max I 1.55)
  - `normalize`: normalize=zscore (max I 2.18)
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 2.22)
- 2 separate islands (no single-knob move joins them): n=12000, normalize=zscore; n=1000, normalize=zscore; n=6000, normalize=zscore | lr_schedule=cosine, n=12000
- Equally good values: `n` in {600, 1000, 2000, 6000, 12000}

Notes:
- configurations the target claim can't tell apart from the answer: n=1000, normalize=zscore; n=24; n=12000, normalize=zscore; class_weight=balanced, normalize=minmax; n=6000, normalize=zscore; n=2000, normalize=zscore; n=600, normalize=zscore
- equally good values within one noise band (measured): n in {600, 1000, 2000, 6000, 12000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `n=12000` | 3 | +0.0% | +0.2% | 0.1% |
| `normalize=zscore`, `n=1000` | 3 | +1.2% | +0.9% | 1.1% |
| `normalize=zscore`, `n=6000` | 3 | -1.0% | -1.4% | 1.2% |
| `n=2000`, `normalize=zscore` | 3 | +1.2% | +2.3% | 1.8% |
| `normalize=zscore`, `n=600` | 3 | -1.9% | -3.8% | 2.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: crash, The script crashed with an IndexError when trying to access Xtr[0]; setting n=1 likely resulted in too few training samples, causing an empty dataset and the subsequent indexing failure

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0005, sandbox reported $0.0000 (total $0.0005; this search; ledger extraction is included only if it shared the search's router)
