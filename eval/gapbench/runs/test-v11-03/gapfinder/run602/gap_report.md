# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-14 22:33 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -38.3% | +0.0% | ±1.1% | `normalize=zscore`, `label_noise=0.905` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -38.3% → +0.0% · 72 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0141`, `B0184`, `B0185` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `label_noise` naive `0.05`, changed to `0.905`
- Command:

  Replay: fork checkpoint `9d59af59-b5d2-4c10-8aa2-0012fc8ae3fa` and run
  ```
  RUN_TAG=157a89de3449 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.905 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.7833, 0.7833; gap after +0.0%; result checkpoint `7137039a-232a-4c77-aa5a-205c48cd031c`
- Effect: candidate 0.7833 minus naive 0.4833 = +0.3, 95% bootstrap interval [+0.2966, +0.3166] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.4833, 0.4833, 0.4667, 0.4667, 0.4875
- Spread: range 0.4667 to 0.4875, noise band ±0.0084 (2 x MAD), CV 2.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -38.3% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -36.2% (it comes back)
- PASS · Counterfactual (reversal test): without `label_noise` the gap is +5.9% (it comes back)
- PASS · Held-out claim: C2: -36.3% to +1.5% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `label_noise=0.905`: no evidence mentions '0.905'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation_method`, `run_tag_seeds`, `cpu`, `memory`, `os`, `python_version`, `random_module`, `disk`, `network`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (18.36 noise units, gap -18.6%); `normalize=minmax` (13.39 noise units, gap -23.9%); `label_noise=0.1` (11.9 noise units, gap -25.5%); `positive_rate=0.15` (7.94 noise units, gap -29.8%); `batch_size=64` (7.44 noise units, gap -30.3%) (and 15 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `label_noise=0.1`: this claim +3.2%, mean |gap| 4.0% (3 runs)
  - `positive_rate=0.86`, `normalize=zscore`: this claim +3.7%, mean |gap| 4.8% (3 runs)
  - `positive_rate=0.15`, `normalize=zscore`: this claim -0.5%, mean |gap| 5.1% (3 runs)

### History matching (every measured configuration, all claims together)
- 8 of 72 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.3); label_noise=0.1, normalize=zscore (max I 0.98); label_noise=0.981, normalize=zscore (max I 1.31)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.86 (max I 1.14); normalize=zscore, positive_rate=0.15 (max I 1.95)
  - `normalize`: normalize=zscore (max I 1.5)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.52); lr_schedule=step, normalize=zscore (max I 1.52)

Notes:
- stopped early: run budget of 200 reached (wanted 2 more run(s) of {'lr_schedule': 'cosine', 'positive_rate': '0.86'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `label_noise=0.905` | 3 | +0.0% | +1.5% | 0.8% |
| `normalize=zscore`, `label_noise=0.1` | 3 | +3.2% | +4.8% | 4.0% |
| `positive_rate=0.86`, `normalize=zscore` | 3 | +3.7% | -5.8% | 4.8% |
| `positive_rate=0.15`, `normalize=zscore` | 3 | -0.5% | -9.6% | 5.1% |
| `normalize=zscore`, `label_noise=0.981` | 3 | +4.8% | +6.4% | 5.6% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation_method`, `run_tag_seeds`, `cpu`, `memory`, `os`, `python_version`, `random_module`, `disk`, `network`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
