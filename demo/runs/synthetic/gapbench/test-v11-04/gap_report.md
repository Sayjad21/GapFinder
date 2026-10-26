# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-23 17:52 · 160 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +84.3% | -0.2% | ±19.1% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +84.3% → -0.2% · 34 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0023`, `B0028`, `B0029`, `B0070`, `B0071`, `B0072` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `b61849ee-6504-4ce8-b0fa-b7bb59b7cd79` and run
  ```
  RUN_TAG=b902f7231682 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 94.87, 99.34, 93.53, 94.63, 88.17, 99.91; gap after -0.2%; result checkpoint `39b186d0-c796-46a9-b814-136e1dc43019`
- Effect: candidate 94.75 minus naive 175 = -80.22, 95% bootstrap interval [-90.19, -48.42] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 175 over 5 runs; repeats: 179.4, 175, 165.8, 138.3, 184
- Spread: range 138.3 to 184, noise band ±18.11 (2 x MAD), CV 10.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +84.3% (noise band ±19.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +84.3% (it comes back)
- PASS · Held-out claim: C2: -6.7% to -13.3% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -80.22 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.2` (3.86 noise units, gap -10.6%); `eps_start=0.1` (3.3 noise units, gap -21.4%); `eps_start=0.5` (1.58 noise units, gap +54.1%); `max_steps=40` (1.39 noise units, gap -57.9%); `lr_schedule=inv` (1.13 noise units, gap +62.7%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=inv`: this claim -4.1%, mean |gap| 22.2% (6 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.6%, mean |gap| 23.7% (6 runs)
  - `lr_schedule=inv`: this claim +36.3%, mean |gap| 43.7% (6 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=inv, max_steps=100`
- `lr_schedule=linear, max_steps=100`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting max_steps=100 | settings | 67% | 0.1 sigma (fits every claim) | run with max_steps=100 |
| 2 | the setting lr_schedule=inv, max_steps=100 | settings | 16% | 0.8 sigma (fits every claim) | run with lr_schedule=inv, max_steps=100 |
| 3 | the setting lr_schedule=linear, max_steps=100 | settings | 13% | 1.0 sigma (fits every claim) | run with lr_schedule=linear, max_steps=100 |

### History matching (every measured configuration, all claims together)
- 8 of 34 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `max_steps`: max_steps=100 (max I 0.05)
  - `lr_schedule, max_steps`: lr_schedule=inv, max_steps=100 (max I 0.75); lr_schedule=linear, max_steps=100 (max I 1)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.85); eps_start=0.1, max_steps=100 (max I 2.61)
  - `eps_start`: eps_start=0.2 (max I 2.67); eps_start=0.1 (max I 2.69)
  - `lr_schedule`: lr_schedule=inv (max I 2.76)

Notes:
- its runs spread 0.3x the naive run's noise band (reported, not used to judge)
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=inv, max_steps=100; lr_schedule=linear, max_steps=100
- spec knobs no ledger assumption names (episodes, eps_decay, eps_end, eval_episodes, gamma, init_q, lr, omega_bins, reward_norm, seeds, theta_bins) were screened too; no better answer
- max_steps: values from 79 to 100 fit every claim (a bisection, 3 runs a side, one run a value: approximate)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | -0.2% | -13.3% | 6.8% |
| `max_steps=100`, `lr_schedule=inv` | 6 | -4.1% | -40.3% | 22.2% |
| `max_steps=100`, `lr_schedule=linear` | 6 | +2.6% | +44.9% | 23.7% |
| `lr_schedule=inv` | 6 | +36.3% | -51.2% | 43.7% |
| naive (reproduction as run) | 5 | +84.3% | -6.7% | 45.5% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `28b211d810d1b9d96fc05d215b47c832dfb18c6d18bc5a8b475d528ad9c3b24a`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
