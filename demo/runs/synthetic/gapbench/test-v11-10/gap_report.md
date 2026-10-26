# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-23 17:56 · 177 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +95.3% | +4.0% | ±9.2% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Partially explained** · gap +95.3% → +4.0% · 93 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0042` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `00280c86-9038-4bc2-b199-01ce9ed9fa18` and run
  ```
  RUN_TAG=b8c3be71fefc export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.12, 90.62, 99.61, 98.34; gap after +4.0%; result checkpoint `0b5a122c-fb7a-409f-8a34-01d4635b01c0`
- Effect: candidate 98.73 minus naive 185.4 = -86.68, 95% bootstrap interval [-99.68, -80.51] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 185.4 over 5 runs; repeats: 185.4, 177.4, 183.1, 189.8, 192.1
- Spread: range 177.4 to 192.1, noise band ±8.72 (2 x MAD), CV 3.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +95.3% (noise band ±9.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +95.3% (it comes back)
- PASS · Held-out claim: C2: +84.1% to +44.8% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -86.68 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `cartpole_physics`, `discretization_bounds`, `done_thresholds`, `reset_distribution`, `force_magnitude`, `RL_SEED_BASE`, `RUN_TAG`, `timestep_dt`, `discretization_formula`, `pole_length`, `mass_cart`, `mass_pole`, `action_tiebreak`, `epsilon_decay_timing`, `q_lazy_init`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (6.56 noise units, gap +35.1%); `max_steps=40` (3.85 noise units, gap -60.0%); `max_steps=20` (1.78 noise units, gap -78.9%); `lr_schedule=linear` (1.32 noise units, gap +83.2%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +3.0%, mean |gap| 25.2% (4 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -10.2%, mean |gap| 33.6% (3 runs)
  - `lr=1`: this claim +6.8%, mean |gap| 42.3% (4 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`
- `lr_schedule=inv, max_steps=100`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting max_steps=100 | settings | 63% | 0.6 sigma (fits every claim) | run with max_steps=100 |
| 2 | the setting lr_schedule=linear, max_steps=100 | settings | 22% | 0.6 sigma (fits every claim) | run with lr_schedule=linear, max_steps=100 |
| 3 | the setting lr_schedule=inv, max_steps=100 | settings | 4% | 1.3 sigma (fits every claim) | run with lr_schedule=inv, max_steps=100 |

### History matching (every measured configuration, all claims together)
- 8 of 93 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.55); lr_schedule=inv, max_steps=100 (max I 1.77)
  - `max_steps`: max_steps=100 (max I 0.6)
  - `lr`: lr=1 (max I 1.6); lr=0.02 (max I 2.08); lr=0.01 (max I 2.17)
  - `eps_decay`: eps_decay=0.495 (max I 1.82)
  - `theta_bins`: theta_bins=1 (max I 2.54)
- 4 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; max_steps=100; lr_schedule=inv, max_steps=100 | lr=1; lr=0.02; lr=0.01 | eps_decay=0.495 | theta_bins=1

Notes:
- its runs spread 0.1x the naive run's noise band (reported, not used to judge)
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100
- spec knobs no ledger assumption names (episodes, eps_decay, eps_end, eps_start, eval_episodes, gamma, init_q, lr, omega_bins, reward_norm, seeds, theta_bins) were screened too; no better answer
- max_steps: values from 100 to 100 fit every claim (a bisection, 3 runs a side, one run a value: approximate)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 4 | +4.0% | +44.8% | 24.4% |
| `lr_schedule=linear`, `max_steps=100` | 4 | +3.0% | +47.3% | 25.2% |
| `max_steps=100`, `lr_schedule=inv` | 3 | -10.2% | -57.0% | 33.6% |
| `lr=1` | 4 | +6.8% | -77.9% | 42.3% |
| `lr=0.02` | 4 | -6.5% | -81.0% | 43.7% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `cartpole_physics`, `discretization_bounds`, `done_thresholds`, `reset_distribution`, `force_magnitude`, `RL_SEED_BASE`, `RUN_TAG`, `timestep_dt`, `discretization_formula`, `pole_length`, `mass_cart`, `mass_pole`, `action_tiebreak`, `epsilon_decay_timing`, `q_lazy_init`, `evaluation_policy`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `28b211d810d1b9d96fc05d215b47c832dfb18c6d18bc5a8b475d528ad9c3b24a`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
