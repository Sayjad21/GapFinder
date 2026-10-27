# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-15 00:18 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -34.3% | +0.8% | ±5.6% | `n=6000`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -34.3% → +0.8% · 57 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0053`, `B0104`, `B0105`, `B0106`, `B0107` (5 run(s) of the same config)
- Config: `n` naive `1200`, changed to `6000`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `59275e45-27a5-4a20-81b0-cc72cb0f89b6` and run
  ```
  RUN_TAG=a92a6d63a52f "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7475, 0.7483, 0.7492, 0.7458, 0.7458; gap after +0.8%; result checkpoint `167d1e26-6378-4132-a60d-fb819344cc8e`
- Effect: candidate 0.7475 minus naive 0.4875 = +0.26, 95% bootstrap interval [+0.2139, +0.281] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4875, 0.5333, 0.4667, 0.5333, 0.4667
- Spread: range 0.4667 to 0.5333, noise band ±0.0416 (2 x MAD), CV 6.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -34.3% (noise band ±5.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is +11.2% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -33.9% (it comes back)
- PASS · Held-out claim: C2: -30.9% to +2.4% (not worse beyond noise)
- FAIL · Evidence: `n=6000`: no evidence mentions '6000'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.26 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `hardware`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (2.9 noise units, gap -18.0%); `normalize=minmax` (2.6 noise units, gap -19.7%); `n=120` (2.3 noise units, gap -21.4%); `n=5000` (2.27 noise units, gap -21.5%); `class_weight=balanced` (1.1 noise units, gap -28.1%)
- Near alternatives (closest across all claims):
  - `n=120`, `normalize=zscore`: this claim -4.5%, mean |gap| 2.9% (5 runs)
  - `n=12000`, `normalize=zscore`: this claim +2.1%, mean |gap| 3.1% (5 runs)
  - `n=5000`, `normalize=zscore`: this claim +1.8%, mean |gap| 3.3% (5 runs)

### History matching (every measured configuration, all claims together)
- 24 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=600, normalize=zscore (max I 0); n=6000, normalize=zscore (max I 0.37); n=12000, normalize=minmax (max I 0.5); n=120, normalize=zscore (max I 0.57); +6 more

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'n': '12000'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=6000`, `normalize=zscore` | 5 | +0.8% | +2.4% | 1.6% |
| `n=120`, `normalize=zscore` | 5 | -4.5% | +1.3% | 2.9% |
| `n=12000`, `normalize=zscore` | 5 | +2.1% | +4.1% | 3.1% |
| `n=5000`, `normalize=zscore` | 5 | +1.8% | +4.8% | 3.3% |
| `n=1000`, `normalize=zscore` | 5 | +2.5% | +4.3% | 3.4% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `hardware`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
