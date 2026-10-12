# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-12 22:25 · 50 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -27.5% | +3.1% | ±6.7% | `normalize=zscore`, `n=2000` |

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -27.5% → +3.1% · 13 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0026`, `B0035`, `B0036`, `B0037`, `B0038` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `2000`
- Command:

  Replay: fork checkpoint `123f326f-a39e-46eb-a774-8f7e9d130689` and run
  ```
  RUN_TAG=119e838e19aa "${PYTHON:-python3}" train.py --n 2000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.765, 0.765, 0.765, 0.765, 0.765; gap after +3.1%; result checkpoint `556b0568-495d-429a-bb63-5d9c4f3c0162`
- Effect: candidate 0.765 minus naive 0.5375 = +0.2275, 95% bootstrap interval [+0.2125, +0.2775] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.4667, 0.55, 0.5375, 0.5625, 0.4875
- Spread: range 0.4667 to 0.5625, noise band ±0.05 (2 x MAD), CV 8.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -27.5% (noise band ±6.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.6% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +11.2% (it comes back)
- PASS · Held-out claim: C2: -22.6% to +6.3% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=2000`: no evidence mentions '2000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2275 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `hardware`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.67 noise units, gap -16.3%); `normalize=minmax` (1.17 noise units, gap -19.7%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `class_weight=balanced`: this claim +6.2%, mean |gap| 9.4% (5 runs)
  - `normalize=zscore`: this claim +11.2%, mean |gap| 13.2% (5 runs)
  - `normalize=zscore`, `lr_schedule=cosine`: this claim +11.8%, mean |gap| 13.7% (5 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=2000`, `normalize=zscore` | 5 | +3.1% | +6.3% | 4.7% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +6.2% | +12.6% | 9.4% |
| `normalize=zscore` | 5 | +11.2% | +15.2% | 13.2% |
| `normalize=zscore`, `lr_schedule=cosine` | 5 | +11.8% | +15.7% | 13.7% |
| `lr_schedule=cosine` | 5 | -16.3% | -11.7% | 14.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `hardware`

## Provenance
- GapFinder commit: `56779a9cc2cef642dbf91ede59da97a848c305cd` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `81ad24a2c635c2279bd33ad3363ed7dfbe8e21683f613c866dc86e070854c074`
- Cost: Nemotron billed $0.0451, sandbox reported $0.0000 (total $0.0451; this search; ledger extraction is included only if it shared the search's router)
