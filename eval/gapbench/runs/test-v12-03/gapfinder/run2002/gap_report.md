# Gap Report: test-v12-03

Artifact `mlbench` · generated 2026-10-15 21:07 · 131 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -23.2% | -23.2% | ±0.8% | — |

## C1: test_accuracy (paper 0.7)
**Unexplained** · gap -23.2% → -23.2% · 57 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (57 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.700 test accuracy and 0.500 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5458, 0.5375, 0.5375, 0.5333, 0.5375
- Spread: range 0.5333 to 0.5458, noise band ±0.005375 (2 x MAD), CV 0.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -23.2% (noise band ±0.8% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `training_loop_bugs`, `RUN_TAG`, `aggregation_method`, `num_runs`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `sigmoid_clamp`, `python_random_module`, `logit_bias_term`, `feature_generation_gaussian`, `balanced_accuracy_formula`, `label_noise_application`, `python_version`, `hardware_cpu`, `os_settings`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (18.6 noise units, gap -8.9%); `normalize=minmax` (10.85 noise units, gap -14.9%); `normalize=zscore` (6.2 noise units, gap +18.5%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `positive_rate=0.86`: this claim +7.1%, mean |gap| 3.6% (3 runs)
  - `positive_rate=0.1`, `normalize=minmax`: this claim +11.9%, mean |gap| 6.0% (3 runs)
  - `normalize=minmax`: this claim -14.9%, mean |gap| 7.4% (3 runs)

### History matching (every measured configuration, all claims together)
- 5 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.86 (max I 1.42); normalize=minmax, positive_rate=0.1 (max I 2.37)
  - `normalize`: normalize=minmax (max I 2.96)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 2.96); lr_schedule=step, normalize=minmax (max I 2.96)

Notes:
- {'lr_schedule': 'cosine', 'positive_rate': '0.15'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr_schedule': 'cosine', 'positive_rate': '0.15'} (gap -6.0%); it did not pass verification
- history matching: 5 of 55 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `positive_rate=0.86` | 3 | +7.1% | +0.0% | 3.6% |
| `positive_rate=0.1`, `normalize=minmax` | 3 | +11.9% | +0.0% | 6.0% |
| `normalize=minmax` | 3 | -14.9% | +0.0% | 7.4% |
| `normalize=minmax`, `lr_schedule=cosine` | 2 | -14.9% | +0.0% | 7.4% |
| `normalize=minmax`, `lr_schedule=step` | 2 | -14.9% | +0.0% | 7.4% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `training_loop_bugs`, `RUN_TAG`, `aggregation_method`, `num_runs`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `sigmoid_clamp`, `python_random_module`, `logit_bias_term`, `feature_generation_gaussian`, `balanced_accuracy_formula`, `label_noise_application`, `python_version`, `hardware_cpu`, `os_settings`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
