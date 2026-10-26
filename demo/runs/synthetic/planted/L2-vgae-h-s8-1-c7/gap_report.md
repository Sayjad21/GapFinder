# Gap Report: planted L2-vgae-h-s8-1

Artifact `vgae` · generated 2026-10-26 23:57 · 14 branch runs (0 build/load setups) · sandbox $25.1208

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C46 (c46_auc) | Reproduced | -0.6% | n/a | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- Tested: switching this code off moved no claim beyond noise: `gae/preprocessing.py:76` `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C46 (`c46_auc`): paper 86.08, as run 85.58, without it 85.99 (difference 95% CI [-0.0773, +0.47])
  - C47 (`c47_ap`): paper 88.18, as run 87.86, without it 88.04 (difference 95% CI [-0.284, +0.353])
- Tested: switching this code off moved no claim beyond noise: `gae/preprocessing.py:79` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C46 (`c46_auc`): paper 86.08, as run 85.58, without it 85.88 (difference 95% CI [-0.409, +0.924])
  - C47 (`c47_ap`): paper 88.18, as run 87.86, without it 88.02 (difference 95% CI [-0.312, +0.531])
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:106` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C46 (`c46_auc`): paper 86.08, as run 85.58, without it 86.15 (difference 95% CI [+0.137, +0.863])
  - C47 (`c47_ap`): paper 88.18, as run 87.86, without it 88.31 (difference 95% CI [+0.00864, +0.557])

## C46: c46_auc (paper 86.08)
**Reproduced**: naive gap -0.6% is inside the noise band ±1.0%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `c46_auc` = 86.08.

### What did we measure?
- Naive median 85.58 over 5 runs; repeats: 85.71, 85.54, 85.58, 86.02, 85.41
- Spread: range 85.41 to 86.02, noise band ±0.8558 (2 x MAD), CV 0.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -0.6% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `@ast:gae/preprocessing.py:106:assume_unique=False`: this claim +0.1%, mean |gap| 0.1% (3 runs)
  - `@ast:gae/preprocessing.py:76:replace=False`: this claim -0.1%, mean |gap| 0.1% (3 runs)
  - `@ast:gae/preprocessing.py:79:assume_unique=False`: this claim -0.2%, mean |gap| 0.2% (3 runs)

Notes:
- naive run is within the noise band of the paper's value

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C46 | C47 | Mean |gap| |
|---|---|---|---|---|
| `@ast:gae/preprocessing.py:106:assume_unique=False` | 3 | +0.1% | +0.1% | 0.1% |
| `@ast:gae/preprocessing.py:76:replace=False` | 3 | -0.1% | -0.2% | 0.1% |
| `@ast:gae/preprocessing.py:79:assume_unique=False` | 3 | -0.2% | -0.2% | 0.2% |
| naive (reproduction as run) | 5 | -0.6% | -0.4% | 0.5% |

## Runtime trace (one dry run)
5 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at gae/train.py:142)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at gae/optimizer.py:37)

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f834b91915d18e8df77b309b8dfa2b22d5d914828f89e865a0c9a7bc8226132c`
- Cost: Nemotron billed $0.0000, sandbox reported $25.1208 (total $25.1208; this search; ledger extraction is included only if it shared the search's router)
