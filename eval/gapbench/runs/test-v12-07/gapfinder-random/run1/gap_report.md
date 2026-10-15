# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 07:31 · 20 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +86.8% | +86.8% | ±12.1% | — |

## C1: mean_reward (paper 98.685)
**Unexplained** · gap +86.8% → +86.8% · 5 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (5 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 184.3 over 5 runs; repeats: 190.3, 184.3, 175.2, 168.1, 185.7
- Spread: range 168.1 to 190.3, noise band ±11.99 (2 x MAD), CV 4.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +86.8% (noise band ±12.1% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (4.12 noise units, gap +36.8%); `lr_schedule=linear` (1.01 noise units, gap +74.5%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `reward_norm=on`: this claim +33.3%, mean |gap| 45.7% (3 runs)
  - `lr_schedule=inv`: this claim +43.7%, mean |gap| 51.4% (4 runs)
  - `lr_schedule=linear`, `reward_norm=on`: this claim +73.2%, mean |gap| 63.2% (3 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, among 5 tested

Notes:
- reward_norm dropped: with repeats, {'lr_schedule': 'inv', 'reward_norm': 'on'} fits {'lr_schedule': 'inv'}'s gap by less than one noise band, so it is not needed
- closest configuration tried: {'lr_schedule': 'inv'} (gap +43.7%); it did not pass verification
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C1, among 5 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | +86.8% | -4.4% | 45.6% |
| `lr_schedule=inv`, `reward_norm=on` | 3 | +33.3% | -58.1% | 45.7% |
| `lr_schedule=inv` | 4 | +43.7% | -59.1% | 51.4% |
| `lr_schedule=linear`, `reward_norm=on` | 3 | +73.2% | +53.2% | 63.2% |
| `lr_schedule=linear` | 4 | +75.4% | +57.5% | 66.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
