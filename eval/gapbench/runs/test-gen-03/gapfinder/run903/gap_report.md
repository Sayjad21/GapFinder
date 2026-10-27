# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-14 23:41 · 99 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | -42.8% | -42.8% | ±2.8% | — |

## C1: mean_reward (paper 302.05)
**Unexplained** · gap -42.8% → -42.8% · 32 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (32 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 172.9 over 5 runs; repeats: 172.9, 164.7, 189.1, 172.5, 177.1
- Spread: range 164.7 to 189.1, noise band ±8.31 (2 x MAD), CV 5.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -42.8% (noise band ±2.8% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (14.65 noise units, gap -2.4%); `max_steps=500` (12.33 noise units, gap -8.8%); `max_steps=400` (7.97 noise units, gap -20.8%); `max_steps=2000` (3.08 noise units, gap +34.3%)
- Near alternatives (closest across all claims):
  - `max_steps=500`: this claim -8.4%, mean |gap| 10.9% (6 runs)
  - `max_steps=1000`: this claim -2.5%, mean |gap| 15.4% (6 runs)
  - `max_steps=2000`: this claim +18.5%, mean |gap| 16.8% (6 runs)

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=500 (max I 1.22); max_steps=1000 (max I 1.54); max_steps=400 (max I 2.14)

Notes:
- {'max_steps': '1000'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'max_steps': '1000'} (gap -2.5%); it did not pass verification
- history matching: 3 of 32 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 6 | -8.4% | +13.5% | 10.9% |
| `max_steps=1000` | 6 | -2.5% | -28.2% | 15.4% |
| `max_steps=2000` | 6 | +18.5% | +15.1% | 16.8% |
| `max_steps=400` | 6 | -6.9% | +39.5% | 23.2% |
| naive (reproduction as run) | 5 | -42.8% | +8.8% | 25.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
