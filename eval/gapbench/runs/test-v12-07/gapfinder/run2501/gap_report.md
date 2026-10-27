# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-16 01:59 · 33 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +89.0% | +89.0% | ±15.7% | — |

## C1: mean_reward (paper 98.685)
**Unexplained** · gap +89.0% → +89.0% · 5 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (5 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 186.5 over 5 runs; repeats: 168.7, 194.2, 166.8, 186.5, 186.6
- Spread: range 166.8 to 194.2, noise band ±15.54 (2 x MAD), CV 6.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +89.0% (noise band ±15.7% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (2.69 noise units, gap +46.6%); `lr_schedule=linear` (1.85 noise units, gap +59.8%); `reward_norm=on` (1.33 noise units, gap +68.0%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `reward_norm=on`: this claim +60.4%, mean |gap| 44.0% (5 runs)
  - `lr_schedule=inv`: this claim +46.7%, mean |gap| 50.5% (6 runs)
  - `lr_schedule=inv`, `reward_norm=on`: this claim +43.9%, mean |gap| 57.3% (5 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, among 5 tested

Notes:
- reward_norm dropped: with repeats, {'lr_schedule': 'inv', 'reward_norm': 'on'} fits {'lr_schedule': 'inv'}'s gap by less than one noise band, so it is not needed
- closest configuration tried: {'lr_schedule': 'inv'} (gap +46.7%); it did not pass verification
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C1, among 5 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `reward_norm=on` | 5 | +60.4% | -27.6% | 44.0% |
| `lr_schedule=inv` | 6 | +46.7% | -54.4% | 50.5% |
| `lr_schedule=inv`, `reward_norm=on` | 5 | +43.9% | -70.7% | 57.3% |
| `lr_schedule=linear` | 6 | +68.1% | +53.2% | 60.6% |
| `reward_norm=on` | 6 | +79.4% | -46.4% | 62.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
