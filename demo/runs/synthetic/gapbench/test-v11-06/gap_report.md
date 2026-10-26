# Gap Report: test-v11-06

Artifact `mlbench` · generated 2026-10-23 17:52 · 163 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Inconclusive | +5.8% | +5.8% | ±1.7% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.5038, measured 0.5387 (+6.9%, band ±1.4%)

## C1: test_accuracy (paper 0.5042)
**Inconclusive** · naive gap +5.8% is inside the noise band ±1.7%, but the band is too wide to call it a reproduction.

### Which experiment changed it?
- None could be tested: the noise band is too wide to tell values apart.

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.504 test accuracy.

- p. 1; value used: `test_accuracy` = 0.5042 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5375, 0.4875, 0.5333, 0.5333, 0.5375
- Spread: range 0.4875 to 0.5375, noise band ±0.0084 (2 x MAD), CV 4.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +5.8% (noise band ±1.7% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `positive_rate`, `SCALES`, `WEIGHTS`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=step` (3.46 noise units, gap +0.0%)
- Near alternatives (closest across all claims):
  - `n=1000`: this claim -0.8%, mean |gap| 0.4% (4 runs)
  - `lr=0.5`: this claim +1.6%, mean |gap| 1.2% (4 runs)
  - `label_noise=0.005`: this claim +1.2%, mean |gap| 1.3% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | no difference in reporting: the numbers as printed at the end of the run | settings | 29% | 0.8 sigma (fits every claim) | the settings search and the other classes |
| 2 | the setting n=1000, split=0.08 | settings | 25% | 0.1 sigma (fits every claim) | run with n=1000, split=0.08 |
| 3 | the setting n=1000 | settings | 9% | 0.2 sigma (fits every claim) | run with n=1000 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, split`: n=1000, split=0.08 (max I 0.08)
  - `lr, split`: lr=0.0, split=0.24 (max I 0.14)
  - `n`: n=1000 (max I 0.19)
  - `lr`: lr=0.1 (max I 0.21); lr=0.5 (max I 0.32)
  - `label_noise`: label_noise=0.005 (max I 0.22); label_noise=0.0 (max I 0.53)
  - `@ast:train.py:68:@mut.37.num.mul2`: @ast:train.py:68:@mut.37.num.mul2=1 (max I 0.24)
  - `threshold`: threshold=0.3 (max I 0.33)
  - `lr, lr_schedule`: lr=0.0, lr_schedule=cosine (max I 0.54)

Notes:
- no hypothesis moved the gap by more than 1 noise units
- spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, n, split, threshold, weight_decay) were screened too; no better answer
- the gap (+5.8%) is below the minimum detectable effect (±13.0% with 3 runs per configuration at 80% power): even a setting that closed it couldn't have been confirmed, so 'nothing explains it' can't be claimed either
- mutation round: train.py:68: `16` -> `32` fits, but moves only 0 claim(s) that were off as run: a code lead, not evidence for a cause (one number can't identify a code change)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=1000` | 4 | -0.8% | +0.1% | 0.4% |
| `lr=0.5` | 4 | +1.6% | +0.9% | 1.2% |
| `label_noise=0.005` | 4 | +1.2% | +1.3% | 1.3% |
| `lr=0.1` | 4 | +1.6% | +1.7% | 1.7% |
| `lr_schedule=step` | 4 | +2.5% | +1.9% | 2.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `split=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `positive_rate`, `SCALES`, `WEIGHTS`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `de26d6fac43e5062b63595b1b67ad854874dabdf1d4371c8a995874f6a166ce5`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
