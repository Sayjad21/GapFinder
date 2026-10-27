# Gap Report: dev-rl-schedule

Artifact `rlbench` · generated 2026-10-15 00:28 · 13 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +25.1% | +25.1% | ±1.3% | — |

## C1: mean_reward (paper 139.35)
**Unexplained** · gap +25.1% → +25.1% · 2 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (2 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over six pole-angle and six angular-velocity bins balances CartPole for a mean of 139.3 steps after 400 training episodes.

- p. 1; value used: `mean_reward` = 139.35 steps (headline claim)

### What did we measure?
- Naive median 174.4 over 5 runs; repeats: 174.8, 174.4, 175.2, 168.1, 173.4
- Spread: range 168.1 to 175.2, noise band ±1.744 (2 x MAD), CV 1.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +25.1% (noise band ±1.3% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `discretise_theta_range`, `discretise_omega_range`, `cartpole_g`, `cartpole_dt`, `reset_uniform_range`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `RUN_TAG`, `greedy_evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (16.68 noise units, gap +4.3%); `lr_schedule=linear` (1.28 noise units, gap +23.5%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +2.8%, mean |gap| 52.3% (4 runs)
  - `lr_schedule=linear`: this claim +14.2%, mean |gap| 139.0% (4 runs)

### History matching (every measured configuration, all claims together)
- 1 of 2 tested configurations fit every claim within 3 sigma

Notes:
- {'lr_schedule': 'inv'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr_schedule': 'inv'} (gap +2.8%); it did not pass verification
- history matching: 1 of 2 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | +25.1% | +64.0% | 44.6% |
| `lr_schedule=inv` | 4 | +2.8% | +101.9% | 52.3% |
| `lr_schedule=linear` | 4 | +14.2% | +263.8% | 139.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `discretise_theta_range`, `discretise_omega_range`, `cartpole_g`, `cartpole_dt`, `reset_uniform_range`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `RUN_TAG`, `greedy_evaluation_policy`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
