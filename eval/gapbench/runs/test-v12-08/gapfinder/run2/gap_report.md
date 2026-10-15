# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 08:36 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +86.7% | +1.3% | ±11.2% | `max_steps=100`, `lr=0.5` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +86.7% → +1.3% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0134`, `B0172`, `B0173`, `B0174`, `B0175` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Config: `lr` naive `0.1`, changed to `0.5`
- Command:

  Replay: fork checkpoint `bfb93af1-3857-48f7-ad2e-ccb08d6b111d` and run
  ```
  RUN_TAG=2c76c9711ecf "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.5 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 100, 100, 99.23, 100, 91.16; gap after +1.3%; result checkpoint `2586450a-aa68-49e5-8519-1fc9334e518c`
- Effect: candidate 100 minus naive 184.3 = -84.27, 95% bootstrap interval [-100.5, -74.53] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 184.3 over 5 runs; repeats: 189.8, 182.7, 169.5, 200, 184.3
- Spread: range 169.5 to 200, noise band ±11.06 (2 x MAD), CV 6.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +86.7% (noise band ±11.2% of the paper value)

### Why do we believe it?
- FAIL · Counterfactual (reversal test): without `max_steps` the gap is +11.6% (it did NOT come back)
- FAIL · Counterfactual (reversal test): without `lr` the gap is -3.2% (it did NOT come back)
- PASS · Held-out claim: C2: +42.8% to +4.8% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -84.27 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=1` (7.62 noise units, gap -1.3%); `lr=0.05` (7.25 noise units, gap +5.5%); `lr=0.002` (5.88 noise units, gap -20.9%); `lr=0.02` (5.02 noise units, gap -30.5%); `lr=0.01` (4.5 noise units, gap -36.3%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim -3.2%, mean |gap| 21.1% (6 runs)
  - `max_steps=100`, `lr=0.05`: this claim -15.0%, mean |gap| 38.6% (5 runs)
  - `lr=0.05`, `lr_schedule=inv`: this claim +4.6%, mean |gap| 43.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 16 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.03); lr_schedule=inv, max_steps=100 (max I 2.06)
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.4); lr=0.05, max_steps=100 (max I 2.22)
  - `max_steps`: max_steps=100 (max I 0.82)
  - `lr, lr_schedule`: lr=0.05, lr_schedule=linear (max I 2.2); lr=0.05, lr_schedule=inv (max I 2.33)
  - `lr`: lr=0.05 (max I 2.22); lr=0.5 (max I 2.25); lr=1 (max I 2.49)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr': '0.002', 'lr_schedule': 'inv'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr=0.5` | 5 | +1.3% | +4.8% | 3.1% |
| `max_steps=100` | 6 | -3.2% | -39.0% | 21.1% |
| `max_steps=100`, `lr=0.05` | 5 | -15.0% | -62.2% | 38.6% |
| `lr=0.05`, `lr_schedule=inv` | 5 | +4.6% | -82.1% | 43.4% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -16.3% | -70.8% | 43.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0552, sandbox reported $0.0000 (total $0.0552; this search; ledger extraction is included only if it shared the search's router)
