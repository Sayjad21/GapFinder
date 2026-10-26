# Gap Report: NCF (devbatch-2)

Artifact `ncf` · generated 2026-10-26 03:07 · 14 branch runs (0 build/load setups) · sandbox $255.9429

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_neumf_hr (neumf_hr) | Reproduced | -0.7% | n/a | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- Tested: switching this code off moved no claim beyond noise: `GMF.py:164` the code selects best_hr, best_ndcg, best_iter by comparing hr > best_hr over epoch in xrange(epochs): it scores on TEST data (leakage); switched off (3 runs):
  - C_neumf_hr (`neumf_hr`): paper 0.688, as run 0.6833, without it 0.6839 (difference 95% CI [-0.00663, +0.00147])
  - C_neumf_ndcg (`neumf_ndcg`): paper 0.41, as run 0.4111, without it 0.4086 (difference 95% CI [-0.0041, +0.00152])
  - C_mlp_hr (`mlp_hr`): paper 0.671, as run 0.6738, without it 0.6712 (difference 95% CI [-0.00746, +0.00106])
  - C_mlp_ndcg (`mlp_ndcg`): paper 0.399, as run 0.3979, without it 0.3937 (difference 95% CI [-0.00965, +0.0009])
- Tested: switching this code off moved no claim beyond noise: `MLP.py:171` the code selects best_hr, best_ndcg, best_iter by comparing hr > best_hr over epoch in xrange(epochs): it scores on TEST data (leakage); switched off (3 runs):
  - C_neumf_hr (`neumf_hr`): paper 0.688, as run 0.6833, without it 0.6856 (difference 95% CI [-0.00552, +0.0034])
  - C_neumf_ndcg (`neumf_ndcg`): paper 0.41, as run 0.4111, without it 0.4073 (difference 95% CI [-0.00736, +0.00431])
  - C_gmf_hr (`gmf_hr`): paper 0.642, as run 0.6379, without it 0.6369 (difference 95% CI [-0.00319, +0.000193])
  - C_gmf_ndcg (`gmf_ndcg`): paper 0.371, as run 0.3687, without it 0.368 (difference 95% CI [-0.00205, +0.0012])
- **Measured: the reported numbers depend on this code**: `NeuMF.py:227` the code selects best_hr, best_ndcg, best_iter by comparing hr > best_hr over epoch in xrange(num_epochs): it scores on TEST data (leakage); switched off (3 runs):
  - C_mlp_hr (`mlp_hr`): paper 0.671, as run 0.6738, without it 0.668 (difference 95% CI [-0.00819, -0.00317])
  - C_mlp_ndcg (`mlp_ndcg`): paper 0.399, as run 0.3979, without it 0.3938 (difference 95% CI [-0.00576, -0.00112])
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `dataset`: "Extensive experiments on two real-world datasets show significant improvements of our proposed NCF framework over the state-of-the-art methods." (p.1)
  - `negative_sampling_strategy`: "For the negative instances Y-, we uniformly sample them from unobserved interactions in each iteration and control the sampling ratio w.r.t. the number of observed interactions." (p.4)

## C_neumf_hr: neumf_hr (paper 0.688)
**Reproduced**: naive gap -0.7% is inside the noise band ±1.0%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `neumf_hr` = 0.688.

### What did we measure?
- Naive median 0.6833 over 5 runs; repeats: 0.6887, 0.681, 0.6833, 0.6828, 0.6906
- Spread: range 0.681 to 0.6906, noise band ±0.006833 (2 x MAD), CV 0.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -0.7% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `dataset`, `topK`, `evaluation_threads`, `negative_sampling_strategy`, `shuffle`, `num_layers_mlp`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

Notes:
- naive run is within the noise band of the paper's value

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_neumf_hr | C_neumf_ndcg | C_mlp_hr | C_mlp_ndcg | C_gmf_hr | C_gmf_ndcg | Mean |gap| |
|---|---|---|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | -0.7% | +0.3% | +0.4% | -0.3% | -0.6% | -0.6% | 0.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `dataset`, `topK`, `evaluation_threads`, `negative_sampling_strategy`, `shuffle`, `num_layers_mlp`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `a4007f85978475f8782a4b8cf8b12566cd6f8424fd22d365997e74dbaee0b904`
- Cost: Nemotron billed $0.0009, sandbox reported $255.9429 (total $255.9438; this search; ledger extraction is included only if it shared the search's router)
