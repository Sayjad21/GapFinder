# Gap Report: G-Mixup (ICML 2022), devbatch-1

Artifact `gmixup` · generated 2026-10-17 22:47 · 5 branch runs (0 build/load setups) · sandbox $86.9245

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C34 (gin_imdbb_gmixup_acc) | Reproduced | -2.7% | n/a | ±4.2% | — |

## C34: gin_imdbb_gmixup_acc (paper 71.94)
**Reproduced**: naive gap -2.7% is inside the noise band ±4.2%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
> w/ G-Mixup 71.94±3.00 50.46±1.49 92.90±0.87 55.49±0.53 50.50±0.41

- p. 7, Table 2; value used: `gin_imdbb_gmixup_acc` = 71.94 percentage

### What did we measure?
- Naive median 70 over 5 runs; repeats: 68.5, 74.5, 76.5, 69.5, 70
- Spread: range 68.5 to 76.5, noise band ±3 (2 x MAD), CV 4.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.7% (noise band ±4.2% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `ge`, `lam_range`, `dataset`, `model`, `gmixup`, `seed`, `weight_decay`, `resolution`, `device`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

Notes:
- naive run is within the noise band of the paper's value

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C34 | C29 | C34_imdbm | C29_imdbm | Mean |gap| |
|---|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | -2.7% | -2.2% | -4.2% | -1.0% | 2.5% |

## Knob names
- Screened though no assumption named them (low prior, code-derived values): `lam_lo`, `lam_hi`

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `aug_num`: count (range() bound at src/utils.py:212)
- `batch_size`: size (batch.batch_size (DataLoader) at src/gmixup.py:260)
- `epoch`: count (range() bound at src/gmixup.py:275)
- `lr`: rate (optimizer.lr (Adam) at src/gmixup.py:271)
- `num_hidden`: size (width.out_features (Linear) at src/models.py:41)
- literal `weight_decay = 0.0005` at src/gmixup.py:271 reaches optimizer.weight_decay (Adam), with no knob behind it: a patch-knob lead
- literal `step_size = 100` at src/gmixup.py:272 reaches scheduler.step_size (StepLR), with no knob behind it: a patch-knob lead
- literal `gamma = 0.5` at src/gmixup.py:272 reaches scheduler.gamma (StepLR), with no knob behind it: a patch-knob lead

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `ge`, `lam_range`, `dataset`, `model`, `gmixup`, `seed`, `weight_decay`, `resolution`, `device`

## Provenance
- GapFinder commit: `d6562d2774e44a34f45631a3179b8702973d32a0` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `ce6309932f8e6684cfb2278c8e26e5ca1e7988f6a6cc369f0221e45fd20ef3fd`
- Cost: Nemotron billed $0.0000, sandbox reported $86.9245 (total $86.9245; this search; ledger extraction is included only if it shared the search's router)
