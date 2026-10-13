# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-14 00:51 · 198 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -34.3% | -1.5% | ±5.6% | `normalize=minmax`, `n=12000` |

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -34.3% → -1.5% · 49 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0073`, `B0155`, `B0156`, `B0157`, `B0158` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `n` naive `1200`, changed to `12000`
- Command:

  Replay: fork checkpoint `55bb0c5d-9e5b-475a-8cb9-78a957a67b10` and run
  ```
  RUN_TAG=6ade372ed89d "${PYTHON:-python3}" train.py --n 12000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7204, 0.7308, 0.7371, 0.725, 0.7367; gap after -1.5%; result checkpoint `41b12ec7-aa14-47a2-9158-2ddc549f5809`
- Effect: candidate 0.7308 minus naive 0.4875 = +0.2433, 95% bootstrap interval [+0.1858, +0.2626] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.5375, 0.4667, 0.475, 0.5458, 0.4875
- Spread: range 0.4667 to 0.5458, noise band ±0.0416 (2 x MAD), CV 7.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -34.3% (noise band ±5.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -30.7% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is -19.7% (it comes back)
- PASS · Held-out claim: C2: -30.9% to -4.3% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=12000`: no evidence mentions '12000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2433 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `hardware`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (4.11 noise units, gap +11.2%); `lr_schedule=cosine` (3.2 noise units, gap -16.3%); `n=5000` (2.56 noise units, gap -19.9%); `n=120` (2.3 noise units, gap -21.4%); `class_weight=balanced` (1.4 noise units, gap -26.4%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=5000`, `normalize=zscore`: this claim +1.7%, mean |gap| 3.1% (5 runs)
  - `n=12000`, `normalize=zscore`: this claim +2.1%, mean |gap| 3.1% (5 runs)
  - `n=1000`, `normalize=zscore`: this claim +2.5%, mean |gap| 3.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 16 of 43 tested configurations fit every claim within 3 sigma
- Equally good values: `normalize` in {minmax, zscore}; `n` in {5000, 12000}

Notes:
- equally good values within one noise band (measured): normalize in {minmax, zscore}; n in {5000, 12000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=12000`, `normalize=minmax` | 5 | -1.5% | -4.3% | 2.9% |
| `n=5000`, `normalize=zscore` | 5 | +1.7% | +4.6% | 3.1% |
| `n=12000`, `normalize=zscore` | 5 | +2.1% | +4.2% | 3.1% |
| `n=1000`, `normalize=zscore` | 5 | +2.5% | +4.3% | 3.4% |
| `n=120`, `normalize=zscore` | 5 | +1.1% | +6.8% | 4.0% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `hardware`

## Provenance
- GapFinder commit: `e89cebde86417c8c65704c51b94620ddb20a97ce` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `bfdd41b8caf786503bc4ee736dca20ece1be6a7c560eb6cb028e538e361e4388`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
