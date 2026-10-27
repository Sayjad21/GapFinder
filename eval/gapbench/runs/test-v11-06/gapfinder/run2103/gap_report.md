# Gap Report: test-v11-06

Artifact `mlbench` · generated 2026-10-15 21:02 · 5 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Reproduced | -3.3% | n/a | ±8.3% | — |

## C1: test_accuracy (paper 0.5042)
**Reproduced**: naive gap -3.3% is inside the noise band ±8.3%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.504 test accuracy.

- p. 1; value used: `test_accuracy` = 0.5042 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.5375, 0.4667, 0.5542, 0.4875, 0.4875
- Spread: range 0.4667 to 0.5542, noise band ±0.0416 (2 x MAD), CV 7.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -3.3% (noise band ±8.3% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `positive_rate`, `shuffling_seeds`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `num_runs`, `python_version`, `random_module_implementation`, `sigmoid_clip`, `os_environment`, `cpu_architecture`, `lr_schedule_step_decay_fraction`, `lr_schedule_cosine_steps`, `class_weight_balanced_formula`, `memory_size`, `storage_device`, `os_settings`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

Notes:
- naive run is within the noise band of the paper's value

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | -3.3% | -4.0% | 3.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `positive_rate`, `shuffling_seeds`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `num_runs`, `python_version`, `random_module_implementation`, `sigmoid_clip`, `os_environment`, `cpu_architecture`, `lr_schedule_step_decay_fraction`, `lr_schedule_cosine_steps`, `class_weight_balanced_formula`, `memory_size`, `storage_device`, `os_settings`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `89cbb67063cd32fad21ec54bbbcae03db5bfd20f203bc3007a9bb958f0c115b1`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
