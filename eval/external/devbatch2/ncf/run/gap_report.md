# Gap Report: NCF (WWW 2017), devbatch-2

Artifact `ncf` · generated 2026-10-18 13:07 · 5 branch runs (0 build/load setups) · sandbox $116.6479

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_neumf_hr (neumf_hr) | Reproduced | -0.8% | n/a | ±1.0% | — |

## C_neumf_hr: neumf_hr (paper 0.688)
**Reproduced**: naive gap -0.8% is inside the noise band ±1.0%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `neumf_hr` = 0.688.

### What did we measure?
- Naive median 0.6825 over 5 runs; repeats: 0.6877, 0.6818, 0.6834, 0.6796, 0.6825
- Spread: range 0.6796 to 0.6877, noise band ±0.006825 (2 x MAD), CV 0.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -0.8% (noise band ±1.0% of the paper value)

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
| naive (reproduction as run) | 5 | -0.8% | -0.8% | +0.2% | +0.2% | -0.3% | -0.6% | 0.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `dataset`, `topK`, `evaluation_threads`, `negative_sampling_strategy`, `shuffle`, `num_layers_mlp`

## Provenance
- GapFinder commit: `e0117a22e2449e3a3f83893083a771a58c49de9f`
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `0541005bab8c109633b8383b939279f3956b0101668283c220e885458905065c`
- Cost: Nemotron billed $0.0011, sandbox reported $116.6479 (total $116.6490; this search; ledger extraction is included only if it shared the search's router)
