# Gap Report: test-v13-03

Artifact `rlbench` · generated 2026-10-23 18:07 · 200 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +83.9% | -0.6% | ±5.8% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Fits but unsupported** · gap +83.9% → -0.6% · 96 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0013`, `B0022`, `B0023`, `B0028`, `B0029`, `B0030` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `8de4be37-f676-4708-a569-68fb34cc7445` and run
  ```
  RUN_TAG=67fe05d1e89f export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 81.47, 92.78, 98.78, 99.12, 99.72, 99.17; gap after -0.6%; result checkpoint `76cf5098-d25c-42c3-aefd-ba9a91fd2036`
- Effect: candidate 98.95 minus naive 183 = -84.06, 95% bootstrap interval [-96.7, -77.14] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 183 over 5 runs; repeats: 198.6, 180.1, 185.1, 183, 173.2
- Spread: range 173.2 to 198.6, noise band ±5.78 (2 x MAD), CV 5.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +83.9% (noise band ±5.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +83.9% (it comes back)
- PASS · Held-out claim: C2: -13.7% to -2.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -84.06 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (13.78 noise units, gap +3.9%); `max_steps=10000` (7.63 noise units, gap +39.6%); `max_steps=40` (4.15 noise units, gap -59.8%); `lr_schedule=linear` (3.29 noise units, gap +64.8%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -1.5%, mean |gap| 2.3% (6 runs)
  - `episodes=4000`: this claim +77.5%, mean |gap| 43.5% (3 runs)
  - `episodes=1000`: this claim +79.5%, mean |gap| 43.6% (3 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting max_steps=100 | settings | 67% | 0.6 sigma (fits every claim) | run with max_steps=100 |
| 2 | the setting lr_schedule=linear, max_steps=100 | settings | 26% | 0.3 sigma (fits every claim) | run with lr_schedule=linear, max_steps=100 |
| 3 | the setting eps_decay=0.9 | settings | 2% | 2.2 sigma (fits every claim) | run with eps_decay=0.9 |

### History matching (every measured configuration, all claims together)
- 15 of 96 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.34); lr_schedule=inv, max_steps=400 (max I 1.98); lr_schedule=inv, max_steps=100 (max I 2.32)
  - `max_steps`: max_steps=100 (max I 0.56)
  - `theta_bins`: theta_bins=1 (max I 1.96)
  - `lr`: lr=0.01 (max I 2.03); lr=1 (max I 2.17); lr=0.02 (max I 2.21); lr=0.05 (max I 2.35)
  - `eps_decay`: eps_decay=0.9 (max I 2.19)
- 5 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; max_steps=100; lr_schedule=inv, max_steps=400 | lr=0.01; lr=1; lr=0.02 | eps_decay=0.9; eps_decay=0.0 | eps_start=0.2; eps_start=0.5

Notes:
- its runs spread 0.2x the naive run's noise band (reported, not used to judge)
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100
- spec knobs no ledger assumption names (episodes, eps_decay, eps_end, eps_start, eval_episodes, gamma, init_q, lr, omega_bins, reward_norm, seeds, theta_bins) were screened too; no better answer
- value interval stopped early: run budget of 200 reached (wanted 1 more run(s) of {'max_steps': '89'} for 'interval max_steps=89')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | -0.6% | -2.2% | 1.4% |
| `lr_schedule=linear`, `max_steps=100` | 6 | -1.5% | -3.2% | 2.3% |
| `episodes=4000` | 3 | +77.5% | -9.6% | 43.5% |
| `episodes=1000` | 3 | +79.5% | -7.7% | 43.6% |
| `eps_decay=0.9` | 6 | -2.3% | -88.7% | 45.5% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `28b211d810d1b9d96fc05d215b47c832dfb18c6d18bc5a8b475d528ad9c3b24a`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
