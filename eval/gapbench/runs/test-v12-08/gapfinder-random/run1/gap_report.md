# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 07:35 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +93.1% | +0.6% | ±7.6% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +93.1% → +0.6% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0034`, `B0035`, `B0056`, `B0057`, `B0058` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `a8e5ebe9-6e42-4629-bdf4-ed6df902851b` and run
  ```
  RUN_TAG=b8f4cec0be46 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.25, 99.66, 93.97, 99.39, 94.59, 99.53; gap after +0.6%; result checkpoint `c519bb79-9b7e-4261-94ce-b7697e348438`
- Effect: candidate 99.31 minus naive 190.6 = -91.28, 95% bootstrap interval [-96.79, -51.84] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 190.6 over 5 runs; repeats: 175.8, 190.8, 190.6, 194.4, 142.5
- Spread: range 142.5 to 194.4, noise band ±7.54 (2 x MAD), CV 12.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +93.1% (noise band ±7.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +93.1% (it comes back)
- PASS · Held-out claim: C2: +13.5% to +0.9% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -91.28 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.5` (10.25 noise units, gap +14.8%); `max_steps=2000` (8.99 noise units, gap +24.4%); `lr=0.002` (8.44 noise units, gap -28.6%); `lr=1` (8.28 noise units, gap -29.9%); `lr=0.02` (8.07 noise units, gap -31.4%) (and 8 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -0.8%, mean |gap| 1.8% (5 runs)
  - `max_steps=100`, `lr=0.5`: this claim +1.3%, mean |gap| 3.1% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -7.2%, mean |gap| 36.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 24 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.07); lr_schedule=inv, max_steps=100 (max I 1.64)
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.14)
  - `max_steps`: max_steps=100 (max I 0.5)
  - `lr`: lr=0.5 (max I 2.06); lr=1 (max I 2.14); lr=0.001 (max I 2.2); lr=0.01 (max I 2.22); +1 more
  - `lr_schedule`: lr_schedule=inv (max I 2.26)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '20', 'lr': '0.002'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +0.6% | +0.9% | 0.8% |
| `max_steps=100`, `lr_schedule=linear` | 5 | -0.8% | -2.7% | 1.8% |
| `max_steps=100`, `lr=0.5` | 5 | +1.3% | +4.8% | 3.1% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -7.2% | -65.0% | 36.1% |
| `lr=0.5` | 6 | +24.8% | -53.0% | 38.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
