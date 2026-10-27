# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 21:06 · 170 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -23.2% | -0.5% | ±3.5% | `n=6000`, `normalize=minmax` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -23.2% → -0.5% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0047`, `B0093`, `B0123`, `B0124`, `B0125` (5 run(s) of the same config)
- Config: `n` naive `1200`, changed to `6000`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `bce524d8-fa27-4bf3-ba89-63fdff051d7f` and run
  ```
  RUN_TAG=b4d6de793051 "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7, 0.7, 0.7108, 0.7083, 0.7017; gap after -0.5%; result checkpoint `b5e5df9c-8429-4569-9f8e-a2c358cfc159`
- Effect: candidate 0.7017 minus naive 0.5417 = +0.16, 95% bootstrap interval [+0.1453, +0.214] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.5417 over 5 runs; repeats: 0.5625, 0.5417, 0.5375, 0.475, 0.5542
- Spread: range 0.475 to 0.5625, noise band ±0.025 (2 x MAD), CV 6.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -23.2% (noise band ±3.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is -15.5% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -17.8% (it comes back)
- PASS · Held-out claim: C2: -13.3% to -1.2% (not worse beyond noise)
- FAIL · Evidence: `n=6000`: no evidence mentions '6000'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.16 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (2 noise units, gap -16.1%); `normalize=zscore` (1.73 noise units, gap +17.0%); `n=120` (1.66 noise units, gap -17.3%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `n=12000`: this claim -4.7%, mean |gap| 4.3% (5 runs)
  - `n=12000`, `normalize=minmax`: this claim +3.8%, mean |gap| 5.6% (5 runs)
  - `n=6000`, `lr_schedule=cosine`: this claim -11.0%, mean |gap| 6.7% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=6000, normalize=minmax` (reported)
- `n=240, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 27 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.04); n=12000, normalize=minmax (max I 1.1); n=600, normalize=zscore (max I 1.92); n=240, normalize=zscore (max I 2.33); +2 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.81); lr_schedule=cosine, n=6000 (max I 1.89); lr_schedule=cosine, n=2400 (max I 2.36)
  - `lr_schedule`: lr_schedule=cosine (max I 2.14)
- Equally good values: `n` in {6000, 12000}

Notes:
- configurations the target claim can't tell apart from the answer: n=6000, normalize=minmax; n=240, normalize=zscore
- equally good values within one noise band (measured): n in {6000, 12000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=6000`, `normalize=minmax` | 5 | -0.5% | -1.2% | 0.8% |
| `lr_schedule=cosine`, `n=12000` | 5 | -4.7% | +3.9% | 4.3% |
| `n=12000`, `normalize=minmax` | 5 | +3.8% | +7.5% | 5.6% |
| `n=6000`, `lr_schedule=cosine` | 5 | -11.0% | -2.4% | 6.7% |
| `lr_schedule=cosine` | 6 | -12.5% | -1.9% | 7.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
