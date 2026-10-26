# Gap Report: test-v13-09

Artifact `rlbench` · generated 2026-10-23 18:12 · 134 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +97.6% | -2.1% | ±2.6% | `max_steps=100` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`min_reward`): paper 96.75, measured 182.3 (+88.5%, band ±12.5%)

## C1: mean_reward (paper 99.495)
**Paper-artifact inconsistency** · gap +97.6% → -2.1% · 32 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0042`, `B0043`, `B0044` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `894473d8-7677-4bbb-ac07-1d81406d9f4c` and run
  ```
  RUN_TAG=02ac347e68dd export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.51, 98.4, 95.58, 93.13, 96.32, 99.81; gap after -2.1%; result checkpoint `a3bcb26f-be74-449b-b320-d1420b04d189`
- Effect: candidate 97.36 minus naive 196.6 = -99.26, 95% bootstrap interval [-102.3, -80.61] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 196.6 over 5 runs; repeats: 196.6, 173.1, 197.9, 196.7, 184.2
- Spread: range 173.1 to 197.9, noise band ±2.55 (2 x MAD), CV 5.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +97.6% (noise band ±2.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +97.6% (it comes back)
- PASS · Held-out claim: C2: +88.5% to -20.3% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -99.26 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (32.98 noise units, gap +13.1%); `lr_schedule=inv` (23.33 noise units, gap +37.8%); `max_steps=40` (14.75 noise units, gap -59.8%); `lr_schedule=linear` (9.3 noise units, gap +73.8%); `max_steps=20` (6.91 noise units, gap -79.9%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -3.1%, mean |gap| 14.4% (5 runs)
  - `max_steps=400`, `lr_schedule=linear`: this claim +74.5%, mean |gap| 38.7% (2 runs)
  - `max_steps=1000`, `lr_schedule=inv`: this claim +37.5%, mean |gap| 44.8% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting max_steps=100 | settings | 78% | 0.5 sigma (fits every claim) | run with max_steps=100 |
| 2 | the setting lr_schedule=linear, max_steps=100 | settings | 20% | 0.6 sigma (fits every claim) | run with lr_schedule=linear, max_steps=100 |
| 3 | a cause outside every class tested | outside | 1% |  | look for code, data or evaluation differences the classes don't cover |

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=100 (max I 0.51)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.63); lr_schedule=inv, max_steps=100 (max I 2.43)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100
- max_steps: values from 100 to 100 fit every claim (a bisection, 3 runs a side, one run a value: approximate)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | -2.1% | -20.3% | 11.2% |
| `max_steps=100`, `lr_schedule=linear` | 5 | -3.1% | -25.7% | 14.4% |
| `max_steps=400`, `lr_schedule=linear` | 2 | +74.5% | -2.8% | 38.7% |
| `max_steps=1000`, `lr_schedule=inv` | 5 | +37.5% | -52.2% | 44.8% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -26.8% | -66.0% | 46.4% |

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
