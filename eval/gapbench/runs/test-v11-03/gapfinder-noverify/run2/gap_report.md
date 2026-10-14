# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-14 11:44 · 180 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explained | -34.6% | +0.0% | ±6.4% | `normalize=minmax`, `positive_rate=0.5` |

## C1: test_accuracy (paper 0.7833)
**Explained** · gap -34.6% → +0.0% · 64 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0115`, `B0173`, `B0174` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `positive_rate` naive `0.3`, changed to `0.5`
- Command:

  Replay: fork checkpoint `d527dfc2-c398-4779-8965-2f39647ca845` and run
  ```
  RUN_TAG=7fabb6293020 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.5 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.7833, 0.7792; gap after +0.0%; result checkpoint `99e9282d-9306-427a-ba59-0e3b8d57c7f8`
- Effect: candidate 0.7833 minus naive 0.5125 = +0.2708, 95% bootstrap interval [+0.2431, +0.2958] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5125 over 5 runs; repeats: 0.5375, 0.4875, 0.5375, 0.5125, 0.4875
- Spread: range 0.4875 to 0.5375, noise band ±0.05 (2 x MAD), CV 4.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -34.6% (noise band ±6.4% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.2708 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation_method`, `run_tag_seeds`, `cpu`, `memory`, `os`, `python_version`, `random_module`, `disk`, `network`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (4.5 noise units, gap +5.9%); `lr_schedule=cosine` (2.17 noise units, gap -20.7%); `label_noise=0.005` (1.5 noise units, gap -25.0%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `batch_size=3`: this claim +0.5%, mean |gap| 1.0% (3 runs)
  - `positive_rate=0.5`, `normalize=zscore`: this claim +0.5%, mean |gap| 2.6% (3 runs)
  - `label_noise=0.1`, `normalize=zscore`: this claim +3.2%, mean |gap| 4.0% (3 runs)

### History matching (every measured configuration, all claims together)
- 11 of 63 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, normalize`: batch_size=3, normalize=minmax (max I 0.11); batch_size=3, normalize=zscore (max I 1.16); batch_size=320, normalize=zscore (max I 1.19)
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.5 (max I 0.71); normalize=zscore, positive_rate=0.5 (max I 0.78)
  - `label_noise, normalize`: label_noise=0.1, normalize=zscore (max I 0.86); label_noise=0.005, normalize=zscore (max I 1.4)
  - `normalize`: normalize=zscore (max I 1.31)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.33); lr_schedule=step, normalize=zscore (max I 1.33)
- 2 separate islands (no single-knob move joins them): batch_size=3, normalize=minmax; normalize=minmax, positive_rate=0.5; normalize=zscore, positive_rate=0.5 | batch_size=3, lr_schedule=cosine
- Equally good values: `normalize` in {minmax, zscore}; `positive_rate` in {0.5, 0.93}

Notes:
- equally good values within one noise band (measured): normalize in {minmax, zscore}; positive_rate in {0.5, 0.93}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `batch_size=3` | 3 | +0.5% | +1.6% | 1.0% |
| `normalize=minmax`, `positive_rate=0.5` | 3 | +0.0% | +4.2% | 2.1% |
| `positive_rate=0.5`, `normalize=zscore` | 3 | +0.5% | +4.7% | 2.6% |
| `label_noise=0.1`, `normalize=zscore` | 3 | +3.2% | +4.8% | 4.0% |
| `batch_size=3`, `normalize=zscore` | 3 | +4.8% | +7.0% | 5.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The code computes log(positive_rate/(1-positive_rate)), which requires positive_rate strictly between 0 and 1. Setting it to 0.0 leads to log(0) and a math domain error; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation_method`, `run_tag_seeds`, `cpu`, `memory`, `os`, `python_version`, `random_module`, `disk`, `network`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0005, sandbox reported $0.0000 (total $0.0005; this search; ledger extraction is included only if it shared the search's router)
