# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-14 00:28 · 124 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -27.5% | +1.5% | ±1.1% | `n=5000`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -27.5% → +1.5% · 29 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0053`, `B0085`, `B0086`, `B0087`, `B0088` (5 run(s) of the same config)
- Config: `n` naive `1200`, changed to `5000`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `9eca7865-3d28-4eee-97a5-235c0f131642` and run
  ```
  RUN_TAG=3054140e7c15 "${PYTHON:-python3}" train.py --n 5000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.751, 0.753, 0.753, 0.751, 0.756; gap after +1.5%; result checkpoint `127ff687-8a67-4df9-8d64-83ee45e22b86`
- Effect: candidate 0.753 minus naive 0.5375 = +0.2155, 95% bootstrap interval [+0.1955, +0.2553] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5375, 0.5417, 0.5625, 0.4875
- Spread: range 0.4875 to 0.5625, noise band ±0.0084 (2 x MAD), CV 5.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -27.5% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is +11.2% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -23.4% (it comes back)
- PASS · Held-out claim: C2: -22.6% to +4.4% (not worse beyond noise)
- FAIL · Evidence: `n=5000`: no evidence mentions '5000'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2155 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `hardware`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=120` (15.38 noise units, gap -10.1%); `lr_schedule=cosine` (12.4 noise units, gap -13.5%); `normalize=minmax` (6.94 noise units, gap -19.7%); `class_weight=balanced` (1.49 noise units, gap -25.8%)
- Near alternatives (closest across all claims):
  - `n=120`, `normalize=zscore`: this claim +1.1%, mean |gap| 4.0% (5 runs)
  - `n=120`, `lr_schedule=cosine`: this claim -10.1%, mean |gap| 7.6% (5 runs)
  - `normalize=minmax`, `class_weight=balanced`: this claim +3.9%, mean |gap| 7.8% (5 runs)

Notes:
- equally good values within one noise band (measured): n in {120, 5000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=5000`, `normalize=zscore` | 5 | +1.5% | +4.4% | 3.0% |
| `n=120`, `normalize=zscore` | 5 | +1.1% | +6.8% | 4.0% |
| `n=120`, `lr_schedule=cosine` | 5 | -10.1% | -5.2% | 7.6% |
| `normalize=minmax`, `class_weight=balanced` | 5 | +3.9% | +11.8% | 7.8% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +5.6% | +12.1% | 8.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `hardware`

## Provenance
- GapFinder commit: `ab5d0e01d517ea012f76706719410d70d422f3f9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `bfdd41b8caf786503bc4ee736dca20ece1be6a7c560eb6cb028e538e361e4388`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
