# Gap Report: planted L2-vgae-h-s7-1

Artifact `vgae` · generated 2026-10-24 14:58 · 14 branch runs (0 build/load setups) · sandbox $29.1448

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C46 (c46_auc) | Reproduced | -0.0% | n/a | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- Tested: switching this code off moved no claim beyond noise: `gae/preprocessing.py:76` `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C46 (`c46_auc`): paper 85.74, as run 85.74, without it 85.16 (difference 95% CI [-1.12, +0.485])
  - C47 (`c47_ap`): paper 87.99, as run 88.05, without it 87.68 (difference 95% CI [-0.856, +0.363])
- Tested: switching this code off moved no claim beyond noise: `gae/preprocessing.py:79` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C46 (`c46_auc`): paper 85.74, as run 85.74, without it 86.12 (difference 95% CI [-0.366, +0.658])
  - C47 (`c47_ap`): paper 87.99, as run 88.05, without it 88.15 (difference 95% CI [-0.327, +0.616])
- Tested: switching this code off moved no claim beyond noise: `gae/preprocessing.py:106` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C46 (`c46_auc`): paper 85.74, as run 85.74, without it 86.33 (difference 95% CI [-0.152, +0.785])
  - C47 (`c47_ap`): paper 87.99, as run 88.05, without it 88.34 (difference 95% CI [-0.494, +0.544])

## C46: c46_auc (paper 85.74)
**Reproduced**: naive gap -0.0% is inside the noise band ±1.0%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `c46_auc` = 85.74.

### What did we measure?
- Naive median 85.74 over 5 runs; repeats: 85.74, 85.98, 85.45, 85.43, 86.76
- Spread: range 85.43 to 86.76, noise band ±0.8574 (2 x MAD), CV 0.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -0.0% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `@ast:gae/preprocessing.py:79:assume_unique=False`: this claim +0.4%, mean |gap| 0.3% (3 runs)
  - `@ast:gae/preprocessing.py:76:replace=False`: this claim -0.7%, mean |gap| 0.5% (3 runs)
  - `@ast:gae/preprocessing.py:106:assume_unique=False`: this claim +0.7%, mean |gap| 0.5% (3 runs)

Notes:
- naive run is within the noise band of the paper's value

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C46 | C47 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | -0.0% | +0.1% | 0.0% |
| `@ast:gae/preprocessing.py:79:assume_unique=False` | 3 | +0.4% | +0.2% | 0.3% |
| `@ast:gae/preprocessing.py:76:replace=False` | 3 | -0.7% | -0.4% | 0.5% |
| `@ast:gae/preprocessing.py:106:assume_unique=False` | 3 | +0.7% | +0.4% | 0.5% |

## Runtime trace (one dry run)
5 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at gae/train.py:142)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at gae/optimizer.py:37)

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f834b91915d18e8df77b309b8dfa2b22d5d914828f89e865a0c9a7bc8226132c`
- Cost: Nemotron billed $0.0000, sandbox reported $29.1448 (total $29.1448; this search; ledger extraction is included only if it shared the search's router)
