# Gap Report: test-v13-07

Artifact `rlbench` · generated 2026-10-15 23:50 · 81 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explains target, conflicts with held-out | +89.0% | -5.3% | ±6.8% | `eps_decay=0.98`, `lr_schedule=inv` |

## C1: mean_reward (paper 89.7375)
**Explains target, conflicts with held-out** · gap +89.0% → -5.3% · 32 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0047`, `B0063`, `B0075` (3 run(s) of the same config)
- Config: `eps_decay` naive `0.99`, changed to `0.98`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command: not recorded
- Output: `mean_reward` 49.1, 84.98, 93.23; gap after -5.3%
- Effect: candidate 84.98 minus naive 169.6 = -84.61, 95% bootstrap interval [-120.9, -71.36] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 89.7 on CartPole; the worst of its seeds reaches 69.9.

- p. 1; value used: `mean_reward` = 89.7375 reward (headline claim)

### What did we measure?
- Naive median 169.6 over 5 runs; repeats: 159.3, 172.7, 169.6, 169.7, 165.2
- Spread: range 159.3 to 172.7, noise band ±6.14 (2 x MAD), CV 3.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +89.0% (noise band ±6.8% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -84.61 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `termination_angle`, `termination_position`, `reward_per_step`, `learning_rate_schedule_constant`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_decay=0.0198` (10.89 noise units, gap +14.5%); `eps_decay=0.198` (9.87 noise units, gap -21.4%); `eps_decay=0.099` (9.25 noise units, gap +25.7%); `eps_decay=0.0` (7.9 noise units, gap -35.0%); `eps_decay=0.495` (6.45 noise units, gap -44.8%)
- Near alternatives (closest across all claims):
  - `eps_decay=0.495`: this claim +0.5%, mean |gap| 42.9% (4 runs)
  - `eps_decay=0.0198`: this claim -8.7%, mean |gap| 46.8% (4 runs)
  - `eps_decay=0.099`: this claim -11.5%, mean |gap| 48.7% (4 runs)

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 4 tested configuration(s) fit C1, and every other claim (C2) fits some tested configuration, but none of the 32 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- Fit C1 alone (4; worst claim's implausibility in brackets, lowest is the least inconsistent): eps_decay=0.98, lr_schedule=inv (5.44); eps_decay=0.495 (5.89); eps_decay=0.0198 (5.99); eps_decay=0.099 (6.04)

Notes:
- {'eps_decay': '0.495'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'eps_decay': '0.495'} (gap +0.5%); it did not pass verification
- history matching: out-of-space suspected: 4 tested configuration(s) fit C1, and every other claim (C2) fits some tested configuration, but none of the 32 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- {'eps_decay': '0.98', 'lr_schedule': 'inv'} matches C1 (I=2.35) but breaks C2 (I=5.44); no tested condition matches all claims, so the rest of the gap probably lies in code, data or evaluation, which GapFinder doesn't change

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_decay=0.495` | 4 | +0.5% | -85.3% | 42.9% |
| `eps_decay=0.98`, `lr_schedule=inv` | 3 | -5.3% | -83.0% | 44.2% |
| `eps_decay=0.0198` | 4 | -8.7% | -85.0% | 46.8% |
| `eps_decay=0.099` | 4 | -11.5% | -85.9% | 48.7% |
| `lr_schedule=inv` | 4 | +46.1% | -54.8% | 50.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `termination_angle`, `termination_position`, `reward_per_step`, `learning_rate_schedule_constant`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
