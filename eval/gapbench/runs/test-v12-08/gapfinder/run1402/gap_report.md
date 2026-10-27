# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 19:06 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +90.5% | -11.6% | ±16.7% | `lr=1` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +90.5% → -11.6% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0008`, `B0032`, `B0033`, `B0070`, `B0071`, `B0072` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `1`
- Command:

  Replay: fork checkpoint `09b0de84-c8f1-4318-9f48-ae30872a5e40` and run
  ```
  RUN_TAG=16346ea593c5 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 74.89, 116.2, 95.23, 79.28, 119.7, 55.31; gap after -11.6%; result checkpoint `4e7198ad-c561-43a4-8b1e-d6b9ce488199`
- Effect: candidate 87.25 minus naive 188 = -100.8, 95% bootstrap interval [-127.7, -65.64] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 188 over 5 runs; repeats: 196.2, 198.4, 182.4, 173.8, 188
- Spread: range 173.8 to 198.4, noise band ±16.45 (2 x MAD), CV 5.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +90.5% (noise band ±16.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +90.5% (it comes back)
- PASS · Held-out claim: C2: +36.2% to -87.1% (not worse beyond noise)
- FAIL · Evidence: `lr=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -100.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (5.14 noise units, gap -4.8%); `lr=0.02` (4.93 noise units, gap -8.3%); `lr=0.05` (4.18 noise units, gap +20.8%); `lr=0.5` (3.32 noise units, gap +35.2%); `max_steps=2000` (3.25 noise units, gap +36.3%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=0.5`, `max_steps=100`: this claim +1.2%, mean |gap| 2.1% (5 runs)
  - `lr_schedule=linear`, `max_steps=100`: this claim -1.5%, mean |gap| 3.4% (5 runs)
  - `max_steps=100`: this claim -3.9%, mean |gap| 24.4% (6 runs)

### History matching (every measured configuration, all claims together)
- 12 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.66); lr_schedule=inv, max_steps=100 (max I 1.36); lr_schedule=inv, max_steps=2000 (max I 2.07)
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.73); lr=0.05, max_steps=100 (max I 2.27)
  - `max_steps`: max_steps=100 (max I 0.84)
  - `lr, lr_schedule`: lr=0.05, lr_schedule=inv (max I 1.89); lr=0.02, lr_schedule=linear (max I 1.96)
  - `lr`: lr=1 (max I 2.07); lr=0.02 (max I 2.08)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; lr=0.5, max_steps=100; max_steps=100 | lr=0.05, lr_schedule=inv

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'max_steps': '2000', 'lr_schedule': 'inv'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=0.5`, `max_steps=100` | 5 | +1.2% | +3.0% | 2.1% |
| `lr_schedule=linear`, `max_steps=100` | 5 | -1.5% | -5.4% | 3.4% |
| `max_steps=100` | 6 | -3.9% | -45.0% | 24.4% |
| `lr_schedule=inv`, `lr=0.05` | 5 | -0.4% | -86.5% | 43.5% |
| `lr_schedule=inv` | 3 | +45.9% | -44.7% | 45.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
