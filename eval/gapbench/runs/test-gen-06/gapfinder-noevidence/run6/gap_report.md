# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-13 00:12 · 62 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -28.1% | +3.1% | ±1.1% | `normalize=zscore`, `n=2000` |

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -28.1% → +3.1% · 13 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0039`, `B0051`, `B0052`, `B0053`, `B0054` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `2000`
- Command:

  Replay: fork checkpoint `3ef20efd-29c3-44e4-8dd9-db6c8462f281` and run
  ```
  RUN_TAG=d6a47d9a5725 "${PYTHON:-python3}" train.py --n 2000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.765, 0.765, 0.765, 0.7675, 0.765; gap after +3.1%; result checkpoint `4b0310a1-3dd0-46f5-8b74-55efbf3a4748`
- Effect: candidate 0.765 minus naive 0.5333 = +0.2317, 95% bootstrap interval [+0.2118, +0.2713] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5375, 0.5333, 0.4667, 0.5667, 0.5333
- Spread: range 0.4667 to 0.5667, noise band ±0.0084 (2 x MAD), CV 7.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -28.1% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.2% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +11.8% (it comes back)
- PASS · Held-out claim: C2: -23.1% to +6.3% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `n=2000`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.2317 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (8.93 noise units, gap -18.0%); `normalize=minmax` (7.44 noise units, gap -19.7%); `class_weight=balanced` (5.46 noise units, gap -21.9%); `lr_schedule=step` (2.98 noise units, gap -24.7%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `class_weight=balanced`: this claim +5.6%, mean |gap| 8.8% (5 runs)
  - `normalize=zscore`: this claim +11.8%, mean |gap| 13.7% (5 runs)
  - `normalize=zscore`, `lr_schedule=cosine`: this claim +11.8%, mean |gap| 13.7% (5 runs)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `n=2000` | 5 | +3.1% | +6.3% | 4.7% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +5.6% | +12.1% | 8.8% |
| `normalize=zscore` | 5 | +11.8% | +15.7% | 13.7% |
| `normalize=zscore`, `lr_schedule=cosine` | 5 | +11.8% | +15.7% | 13.7% |
| `class_weight=balanced`, `lr_schedule=cosine` | 5 | -18.0% | -11.7% | 14.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `81ad24a2c635c2279bd33ad3363ed7dfbe8e21683f613c866dc86e070854c074`
- Cost: Nemotron billed $0.0476, sandbox reported $0.0000 (total $0.0476; this search; ledger extraction is included only if it shared the search's router)
