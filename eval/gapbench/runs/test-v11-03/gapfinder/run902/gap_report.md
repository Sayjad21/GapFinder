# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-14 23:47 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -32.4% | -32.4% | ±7.4% | — |

## C1: test_accuracy (paper 0.7833)
**Unexplained** · gap -32.4% → -32.4% · 34 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (34 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5292 over 5 runs; repeats: 0.475, 0.5583, 0.5292, 0.5375, 0.475
- Spread: range 0.475 to 0.5583, noise band ±0.0582 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -32.4% (noise band ±7.4% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation_method`, `run_tag_seeds`, `cpu`, `memory`, `os`, `python_version`, `random_module`, `disk`, `network`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (3.58 noise units, gap +5.9%); `lr_schedule=cosine` (1.57 noise units, gap -20.7%); `normalize=minmax` (1.14 noise units, gap -23.9%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`: this claim +5.6%, mean |gap| 6.6% (6 runs)
  - `lr_schedule=cosine`: this claim -20.7%, mean |gap| 19.4% (3 runs)
  - `batch_size=6`: this claim -30.3%, mean |gap| 28.7% (6 runs)

### History matching (every measured configuration, all claims together)
- 11 of 45 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.86 (max I 0.74); normalize=zscore, positive_rate=0.15 (max I 1.34)
  - `label_noise, normalize`: label_noise=0.981, normalize=zscore (max I 0.91); label_noise=0.025, normalize=zscore (max I 0.98); label_noise=0.001, normalize=zscore (max I 1.04)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 0.99); lr_schedule=step, normalize=zscore (max I 0.99)
  - `normalize`: normalize=zscore (max I 1.24)
  - `label_noise, lr_schedule`: label_noise=0.981, lr_schedule=cosine (max I 2.54); label_noise=0.001, lr_schedule=cosine (max I 2.61)
- 2 separate islands (no single-knob move joins them): normalize=zscore, positive_rate=0.86; label_noise=0.981, normalize=zscore; label_noise=0.025, normalize=zscore | label_noise=0.981, lr_schedule=cosine; label_noise=0.001, lr_schedule=cosine; label_noise=0.025, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 1 more run(s) of {'lr_schedule': 'cosine', 'positive_rate': '0.03'} for 'combine')
- closest configuration not verified: {'normalize': 'zscore', 'positive_rate': '0.15'} (gap -1.1%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: 11 of 45 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 6 | +5.6% | +7.5% | 6.6% |
| `lr_schedule=cosine` | 3 | -20.7% | -18.1% | 19.4% |
| `batch_size=6` | 6 | -30.3% | -27.1% | 28.7% |
| `normalize=minmax` | 3 | -23.9% | -33.5% | 28.7% |
| `label_noise=0.981` | 6 | -31.1% | -27.5% | 29.3% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation_method`, `run_tag_seeds`, `cpu`, `memory`, `os`, `python_version`, `random_module`, `disk`, `network`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
