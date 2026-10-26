# Gap Report: test-v13-08

Artifact `mlbench` · generated 2026-10-23 18:11 · 170 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Inconclusive | +9.0% | +9.0% | ±1.7% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.5261, measured 0.5422 (+3.1%, band ±1.3%)

## C1: test_accuracy (paper 0.4931)
**Inconclusive** · naive gap +9.0% is inside the noise band ±1.7%, but the band is too wide to call it a reproduction.

### Which experiment changed it?
- None could be tested: the noise band is too wide to tell values apart.

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.493 test accuracy.

- p. 1; value used: `test_accuracy` = 0.4931 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5333, 0.5583, 0.5375, 0.4792, 0.5375
- Spread: range 0.4792 to 0.5583, noise band ±0.0084 (2 x MAD), CV 5.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +9.0% (noise band ±1.7% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=step` (3.63 noise units, gap -2.8%)
- Near alternatives (closest across all claims):
  - `n=600`: this claim +1.4%, mean |gap| 2.3% (6 runs)
  - `n=1000`: this claim +1.4%, mean |gap| 2.5% (6 runs)
  - `positive_rate=0.93`: this claim +6.0%, mean |gap| 3.1% (6 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | no difference in reporting: the numbers as printed at the end of the run | settings | 31% | 1.1 sigma (fits every claim) | the settings search and the other classes |
| 2 | the setting threshold=0.3 | settings | 22% | 0.5 sigma (fits every claim) | run with threshold=0.3 |
| 3 | the setting n=1000 | settings | 8% | 0.6 sigma (fits every claim) | run with n=1000 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `threshold`: threshold=0.3 (max I 0.56)
  - `n`: n=600 (max I 0.58); n=1000 (max I 0.64); n=2000 (max I 0.72)
  - `batch_size`: batch_size=6 (max I 0.63)
  - `positive_rate`: positive_rate=0.15 (max I 0.69); positive_rate=0.1 (max I 0.78)
  - `label_noise`: label_noise=0.025 (max I 0.7); label_noise=0.525 (max I 0.78)
  - `split`: split=0.4 (max I 0.78)

Notes:
- no hypothesis moved the gap by more than 1 noise units
- spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, n, positive_rate, split, threshold, weight_decay) were screened too; no better answer
- the gap (+9.0%) is below the minimum detectable effect (±12.1% with 5 runs per configuration at 80% power): even a setting that closed it couldn't have been confirmed, so 'nothing explains it' can't be claimed either

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=600` | 6 | +1.4% | -3.1% | 2.3% |
| `n=1000` | 6 | +1.4% | -3.5% | 2.5% |
| `positive_rate=0.93` | 6 | +6.0% | +0.1% | 3.1% |
| `label_noise=0.025` | 6 | +3.5% | -2.8% | 3.2% |
| `batch_size=6` | 6 | +4.4% | -2.0% | 3.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `split=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `1fd3d59022925491b04c41fd5e5ed48e25739b360d0d1093aefdff9298c5fcf4`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
