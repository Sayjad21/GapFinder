# Gap Report: test-v12-09

Artifact `rlbench` · generated 2026-10-15 21:09 · 7 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Inconclusive | -4.2% | -4.2% | ±1.9% | — |

## C1: mean_reward (paper 185.879)
**Inconclusive** · naive gap -4.2% is inside the noise band ±1.9%, but the band is too wide to call it a reproduction.

### Which experiment changed it?
- None could be tested: the noise band is too wide to tell values apart.

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 185.9 on CartPole; the worst of its seeds reaches 98.4.

- p. 1; value used: `mean_reward` = 185.879 (headline claim)

### What did we measure?
- Naive median 178.1 over 5 runs; repeats: 176.4, 192.3, 178.1, 177.3, 188.6
- Spread: range 176.4 to 192.3, noise band ±3.54 (2 x MAD), CV 4.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -4.2% (noise band ±1.9% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim

Notes:
- no hypothesis moved the gap by more than 1 noise units
- the gap (-4.2%) is below the minimum detectable effect (±12.0% with 3 runs per configuration at 80% power): even a setting that closed it couldn't have been confirmed, so 'nothing explains it' can't be claimed either

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | -4.2% | -32.9% | 18.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
