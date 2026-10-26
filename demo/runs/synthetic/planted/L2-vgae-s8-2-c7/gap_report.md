# Gap Report: planted L2-vgae-s8-2

Artifact `vgae` · generated 2026-10-27 00:18 · 14 branch runs (0 build/load setups) · sandbox $52.0995

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Reproduced | -0.1% | n/a | ±1.4% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:76` `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_cora_auc (`vgae_cora_auc`): paper 85.46, as run 85.35, without it 86.79 (difference 95% CI [+0.509, +2.19])
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 87.9, as run 87.83, without it 88.6 (difference 95% CI [+0.0756, +1.71])
  - C_gae_cora_auc (`gae_cora_auc`): paper 85.68, as run 86.1, without it 85.23 (difference 95% CI [-1.5, -0.112])
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:79` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 86.9, as run 86.98, without it 88.04 (difference 95% CI [+0.511, +1.2])
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 88.77, as run 88.88, without it 89.54 (difference 95% CI [+0.403, +1.04])
  - C_gae_citeseer_ap (`gae_citeseer_ap`): paper 86.9, as run 87.5, without it 85.39 (difference 95% CI [-4.94, -0.257])
- **Measured: the reported numbers depend on this code**: `gae/preprocessing.py:106` `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed; switched off (3 runs):
  - C_vgae_cora_auc (`vgae_cora_auc`): paper 85.46, as run 85.35, without it 86.14 (difference 95% CI [+0.224, +2.08])
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 86.9, as run 86.98, without it 86.8 (difference 95% CI [-1.53, -0.00287])
  - C_gae_cora_auc (`gae_cora_auc`): paper 85.68, as run 86.1, without it 84.25 (difference 95% CI [-3.14, -1.16])
  - C_gae_cora_ap (`gae_cora_ap`): paper 88.06, as run 88.5, without it 86.6 (difference 95% CI [-2.65, -0.521])

## C_vgae_cora_auc: vgae_cora_auc (paper 85.46)
**Reproduced**: naive gap -0.1% is inside the noise band ±1.4%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 85.46.

### What did we measure?
- Naive median 85.35 over 5 runs; repeats: 85.35, 84.85, 85.94, 84.13, 86.1
- Spread: range 84.13 to 86.1, noise band ±1.176 (2 x MAD), CV 1.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -0.1% (noise band ±1.4% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `@ast:gae/preprocessing.py:106:assume_unique=False`: this claim +0.8%, mean |gap| 0.7% (3 runs)
  - `@ast:gae/preprocessing.py:79:assume_unique=False`: this claim +0.3%, mean |gap| 0.8% (3 runs)
  - `@ast:gae/preprocessing.py:76:replace=False`: this claim +1.6%, mean |gap| 0.9% (3 runs)

Notes:
- naive run is within the noise band of the paper's value

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | -0.1% | -0.1% | +0.1% | +0.1% | +0.5% | +0.5% | +1.8% | +0.7% | 0.5% |
| `@ast:gae/preprocessing.py:106:assume_unique=False` | 3 | +0.8% | -0.1% | -0.1% | +0.1% | -1.7% | -1.7% | +1.2% | -0.3% | 0.7% |
| `@ast:gae/preprocessing.py:79:assume_unique=False` | 3 | +0.3% | +0.2% | +1.3% | +0.9% | +0.2% | +0.5% | -0.9% | -1.7% | 0.8% |
| `@ast:gae/preprocessing.py:76:replace=False` | 3 | +1.6% | +0.8% | +0.7% | +0.9% | -0.5% | -0.6% | -0.9% | -1.5% | 0.9% |

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at gae/train.py:142)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at gae/optimizer.py:37)

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `c1e5c82d8951e6fe9ecf9924c1eadbb90900b22b18822db11c582ef2c95c3a15`
- Cost: Nemotron billed $0.0000, sandbox reported $52.0995 (total $52.0995; this search; ledger extraction is included only if it shared the search's router)
