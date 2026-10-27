# Gap Report: test-v13-07

Artifact `rlbench` · generated 2026-10-16 01:37 · 17 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +103.2% | +103.2% | ±8.6% | — |

## C1: mean_reward (paper 89.7375)
**Unexplained** · gap +103.2% → +103.2% · 2 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (2 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 89.7 on CartPole; the worst of its seeds reaches 69.9.

- p. 1; value used: `mean_reward` = 89.7375 (headline claim)

### What did we measure?
- Naive median 182.3 over 5 runs; repeats: 170.5, 141.5, 182.3, 186.2, 184.7
- Spread: range 141.5 to 186.2, noise band ±7.72 (2 x MAD), CV 10.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +103.2% (noise band ±8.6% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `g`, `mc`, `mp`, `l`, `f`, `dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `x_threshold`, `theta_threshold`, `init_state_range`, `RUN_TAG`, `RL_SEED_BASE`, `force_sign`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (5.26 noise units, gap +57.9%); `lr_schedule=linear` (1.03 noise units, gap +94.3%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +53.1%, mean |gap| 45.4% (6 runs)
  - `lr_schedule=linear`: this claim +82.5%, mean |gap| 83.6% (6 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, among 2 tested

Notes:
- {'lr_schedule': 'inv'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr_schedule': 'inv'} (gap +53.1%); it did not pass verification
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C1, among 2 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 6 | +53.1% | -37.6% | 45.4% |
| naive (reproduction as run) | 5 | +103.2% | -19.3% | 61.3% |
| `lr_schedule=linear` | 6 | +82.5% | +84.8% | 83.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `g`, `mc`, `mp`, `l`, `f`, `dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `x_threshold`, `theta_threshold`, `init_state_range`, `RUN_TAG`, `RL_SEED_BASE`, `force_sign`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
