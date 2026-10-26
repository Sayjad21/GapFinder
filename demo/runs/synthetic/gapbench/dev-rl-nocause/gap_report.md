# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-23 17:38 · 170 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +54.2% | +6.3% | ±7.5% | `lr_schedule=inv` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +54.2% → +6.3% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0015`, `B0037`, `B0038`, `B0051`, `B0052`, `B0053` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `120a4314-f472-4608-9426-e541cbc7bb32` and run
  ```
  RUN_TAG=44cc190427fa export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 109.3, 155.5, 116, 136.8, 141.7, 106.7; gap after +6.3%; result checkpoint `35c073d0-00cc-4001-a24c-78abefca726d`
- Effect: candidate 126.4 minus naive 183.4 = -57.01, 95% bootstrap interval [-71.21, -21.64] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 183.4 over 5 runs; repeats: 158, 187.9, 183.4, 187, 169.9
- Spread: range 158 to 187.9, noise band ±8.91 (2 x MAD), CV 7.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +54.2% (noise band ±7.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +54.2% (it comes back)
- PASS · Held-out claim: C2: -27.8% to -55.5% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -57.01 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=30` (7.24 noise units, gap +0.0%); `theta_bins=12` (3.25 noise units, gap +29.9%); `theta_bins=3` (2.74 noise units, gap +33.7%); `lr_schedule=linear` (2.24 noise units, gap +37.5%); `theta_bins=1` (1.51 noise units, gap -42.9%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `theta_bins=3`: this claim +50.8%, mean |gap| 27.0% (6 runs)
  - `theta_bins=3`, `eps_end=0.905`: this claim +42.9%, mean |gap| 28.4% (2 runs)
  - `theta_bins=12`, `lr_schedule=linear`: this claim +8.9%, mean |gap| 31.4% (5 runs)

### Equally good configurations
The target claim can't tell these 7 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=inv` (reported)
- `theta_bins=30`
- `theta_bins=1`
- `lr_schedule=linear, theta_bins=12`
- `eps_end=0.01, theta_bins=30`
- `eps_end=0.01, lr_schedule=inv`
- `lr_schedule=inv, theta_bins=12`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting lr_schedule=inv | settings | 56% | 0.9 sigma (fits every claim) | run with lr_schedule=inv |
| 2 | the setting lr_schedule=linear, theta_bins=12 | settings | 18% | 0.9 sigma (fits every claim) | run with lr_schedule=linear, theta_bins=12 |
| 3 | the setting lr_schedule=inv, theta_bins=12 | settings | 7% | 1.4 sigma (fits every claim) | run with lr_schedule=inv, theta_bins=12 |

### History matching (every measured configuration, all claims together)
- 8 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `lr_schedule`: lr_schedule=inv (max I 0.95)
  - `lr_schedule, theta_bins`: lr_schedule=linear, theta_bins=12 (max I 1.11); lr_schedule=inv, theta_bins=12 (max I 1.38)
  - `eps_end, lr_schedule`: eps_end=0.01, lr_schedule=inv (max I 1.51)
  - `eps_end, theta_bins`: eps_end=0.01, theta_bins=30 (max I 1.66); eps_end=0.01, theta_bins=1 (max I 2.18); eps_end=0.525, theta_bins=3 (max I 2.85)
  - `theta_bins`: theta_bins=30 (max I 2)
- 3 separate islands (no single-knob move joins them): lr_schedule=inv; lr_schedule=linear, theta_bins=12; lr_schedule=inv, theta_bins=12 | eps_end=0.01, theta_bins=30; theta_bins=30; eps_end=0.01, theta_bins=1 | eps_end=0.525, theta_bins=3

Notes:
- configurations the target claim can't tell apart from the answer: lr_schedule=inv; theta_bins=30; theta_bins=1; lr_schedule=linear, theta_bins=12; eps_end=0.01, theta_bins=30; eps_end=0.01, lr_schedule=inv; lr_schedule=inv, theta_bins=12
- spec knobs no ledger assumption names (episodes, eps_decay, eps_start, eval_episodes, gamma, init_q, lr, max_steps, omega_bins, reward_norm, seeds) were screened too; no better answer
- not identifiable from the paper's numbers: 4 configuration(s) of other knobs fit every claim as well as the answer (lr_schedule=inv: eps_end=0.01, theta_bins=30; lr_schedule=linear, theta_bins=12; theta_bins=1; theta_bins=30), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause
- the paper states lr_schedule = const ("constant learning rate"), but const leaves the gap at +54.2% (beyond noise); inv closes it: the stated value is likely not the one behind the paper's numbers

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `theta_bins=3` | 6 | +50.8% | -3.3% | 27.0% |
| `theta_bins=3`, `eps_end=0.905` | 2 | +42.9% | +13.9% | 28.4% |
| `lr_schedule=inv` | 6 | +6.3% | -55.5% | 30.9% |
| `theta_bins=12`, `lr_schedule=linear` | 5 | +8.9% | -54.0% | 31.4% |
| `eps_end=0.01`, `theta_bins=12` | 2 | +46.3% | +25.0% | 35.7% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `28b211d810d1b9d96fc05d215b47c832dfb18c6d18bc5a8b475d528ad9c3b24a`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
