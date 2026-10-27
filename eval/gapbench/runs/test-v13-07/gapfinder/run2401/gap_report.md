# Gap Report: test-v13-07

Artifact `rlbench` · generated 2026-10-16 01:37 · 102 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +95.3% | +95.3% | ±15.2% | — |

## C1: mean_reward (paper 89.7375)
**Unexplained** · gap +95.3% → +95.3% · 32 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (32 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 89.7 on CartPole; the worst of its seeds reaches 69.9.

- p. 1; value used: `mean_reward` = 89.7375 reward (headline claim)

### What did we measure?
- Naive median 175.2 over 5 runs; repeats: 182, 175.2, 167.4, 169.8, 189.7
- Spread: range 167.4 to 189.7, noise band ±13.62 (2 x MAD), CV 5.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +95.3% (noise band ±15.2% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `termination_angle`, `termination_position`, `reward_per_step`, `learning_rate_schedule_constant`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_decay=0.099` (4.54 noise units, gap -26.4%); `eps_decay=0.0198` (4.31 noise units, gap +29.9%); `eps_decay=0.198` (3.39 noise units, gap -43.8%); `eps_decay=0.0` (3.3 noise units, gap -45.2%); `eps_decay=0.495` (2.94 noise units, gap -50.7%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_decay=0.995`, `lr_schedule=inv`: this claim +69.9%, mean |gap| 42.6% (2 runs)
  - `lr_schedule=linear`, `eps_decay=0.495`: this claim -7.3%, mean |gap| 46.2% (5 runs)
  - `eps_decay=0.98`, `lr_schedule=inv`: this claim +26.8%, mean |gap| 49.8% (5 runs)

### History matching (every measured configuration, all claims together)
- 4 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `eps_decay, lr_schedule`: eps_decay=0.495, lr_schedule=linear (max I 1.59)
  - `eps_decay`: eps_decay=0.198 (max I 1.66); eps_decay=0.0198 (max I 1.74); eps_decay=0.495 (max I 2)

Notes:
- {'eps_decay': '0.495'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'eps_decay': '0.495'} (gap -19.3%); it did not pass verification
- history matching: 4 of 32 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_decay=0.995`, `lr_schedule=inv` | 2 | +69.9% | +15.3% | 42.6% |
| `lr_schedule=linear`, `eps_decay=0.495` | 5 | -7.3% | -85.1% | 46.2% |
| `eps_decay=0.98`, `lr_schedule=inv` | 5 | +26.8% | -72.7% | 49.8% |
| `eps_decay=0.0198` | 6 | -18.4% | -85.1% | 51.7% |
| `lr_schedule=inv` | 3 | +46.5% | -58.1% | 52.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `termination_angle`, `termination_position`, `reward_per_step`, `learning_rate_schedule_constant`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
