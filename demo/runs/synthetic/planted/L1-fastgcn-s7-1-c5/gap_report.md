# Gap Report: planted L1-fastgcn-s7-1

Artifact `fastgcn` · generated 2026-10-24 06:12 · 5 branch runs (0 build/load setups) · sandbox $2.1213

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_trans_cora_f1 (trans_cora_acc) | Reproduced | +0.5% | n/a | ±1.0% | — |

## C_trans_cora_f1: trans_cora_acc (paper 0.797)
**Reproduced**: naive gap +0.5% is inside the noise band ±1.0%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `trans_cora_acc` = 0.797.

### What did we measure?
- Naive median 0.801 over 5 runs; repeats: 0.8, 0.796, 0.801, 0.801, 0.803
- Spread: range 0.796 to 0.803, noise band ±0.00801 (2 x MAD), CV 0.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +0.5% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

Notes:
- naive run is within the noise band of the paper's value

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_trans_cora_f1 | C_trans_pubmed_f1 | C_ind_cora_f1 | C_ind_pubmed_f1 | Mean |gap| |
|---|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | +0.5% | +0.3% | -0.1% | +0.7% | 0.4% |

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at pubmed-original_transductive_FastGCN.py:139)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at models.py:58)

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `322f37b98c5a961dd6e44a41ea94efbad7ecef315914f3d5af0cc4d1b6d242bb`
- Cost: Nemotron billed $0.0000, sandbox reported $2.1213 (total $2.1213; this search; ledger extraction is included only if it shared the search's router)
