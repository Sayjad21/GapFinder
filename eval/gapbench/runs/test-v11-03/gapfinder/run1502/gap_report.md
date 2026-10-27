# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-15 19:20 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.9% | +5.6% | ±1.1% | `normalize=zscore` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -31.9% → +5.6% · 34 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0035`, `B0096`, `B0097`, `B0104`, `B0105`, `B0106` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `61d79698-f619-4c6e-858a-f7120c29a3da` and run
  ```
  RUN_TAG=30f4a29de5cc "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.825, 0.8292, 0.8292, 0.825, 0.8292, 0.825; gap after +5.6%; result checkpoint `c0f96630-5cad-44a9-9e4d-e44067898cf6`
- Effect: candidate 0.8271 minus naive 0.5333 = +0.2938, 95% bootstrap interval [+0.2883, +0.3442] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5333, 0.5333, 0.4708, 0.5375, 0.5375
- Spread: range 0.4708 to 0.5375, noise band ±0.0084 (2 x MAD), CV 5.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.9% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -31.9% (it comes back)
- PASS · Held-out claim: C2: -28.4% to +7.5% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2938 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation_method`, `run_tag_seeds`, `cpu`, `memory`, `os`, `python_version`, `random_module`, `disk`, `network`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (9.93 noise units, gap -21.3%); `normalize=minmax` (7.44 noise units, gap -23.9%); `batch_size=16` (3.98 noise units, gap -27.7%); `batch_size=6` (3.98 noise units, gap -27.7%); `label_noise=0.905` (2.98 noise units, gap -28.7%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`: this claim -21.3%, mean |gap| 19.9% (3 runs)
  - `batch_size=6`: this claim -29.5%, mean |gap| 27.9% (6 runs)
  - `batch_size=16`: this claim -30.1%, mean |gap| 28.5% (6 runs)

### History matching (every measured configuration, all claims together)
- 8 of 40 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.22); label_noise=0.81, normalize=zscore (max I 1.4)
  - `batch_size, normalize`: batch_size=6, normalize=zscore (max I 0.92); batch_size=16, normalize=zscore (max I 0.95)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.65 (max I 1.05); normalize=zscore, positive_rate=0.15 (max I 1.38)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.12)
  - `normalize`: normalize=zscore (max I 1.32)

Notes:
- stopped early: run budget of 200 reached (wanted 1 more run(s) of {'normalize': 'zscore', 'lr_schedule': 'step'} for 'combine')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 6 | +5.6% | +7.5% | 6.6% |
| `lr_schedule=cosine` | 3 | -21.3% | -18.6% | 19.9% |
| `batch_size=6` | 6 | -29.5% | -26.4% | 27.9% |
| `batch_size=16` | 6 | -30.1% | -26.9% | 28.5% |
| `normalize=minmax` | 3 | -23.9% | -33.5% | 28.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation_method`, `run_tag_seeds`, `cpu`, `memory`, `os`, `python_version`, `random_module`, `disk`, `network`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
