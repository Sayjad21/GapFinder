# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 08:37 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | +95.6% | +242.0% | ±10.8% | `max_steps=10000` |

## C1: mean_reward (paper 98.685)
**Explained** · gap +95.6% → +242.0% · 54 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0025`, `B0066`, `B0067`, `B0093`, `B0094`, `B0095` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `10000`
- Command:

  Replay: fork checkpoint `ca565bf9-2c03-4703-ad2c-96b0b3938c4a` and run
  ```
  RUN_TAG=093be6bc0d68 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 10000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 136.6, 377.8, 613, 117.1, 421.6, 297.1; gap after +242.0%; result checkpoint `82be4940-9761-4b20-b9ee-730875e3da4d`
- Effect: candidate 337.5 minus naive 193 = +144.4, 95% bootstrap interval [-21.05, +384.8] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 193 over 5 runs; repeats: 193, 182.5, 193.3, 198.4, 173.7
- Spread: range 173.7 to 198.4, noise band ±10.65 (2 x MAD), CV 5.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +95.6% (noise band ±10.8% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- FAIL · Effect vs noise: candidate minus naive is +144.4 with a 95% bootstrap interval that includes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.001` (8.13 noise units, gap -7.9%); `max_steps=100` (7.98 noise units, gap -9.5%); `lr=0.5` (7.37 noise units, gap +16.1%); `lr=0.002` (7.18 noise units, gap -18.1%); `lr=1` (7.13 noise units, gap -18.6%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=0.5`, `max_steps=100`: this claim +1.3%, mean |gap| 3.1% (5 runs)
  - `max_steps=100`: this claim -3.8%, mean |gap| 14.2% (6 runs)
  - `lr_schedule=linear`: this claim +65.1%, mean |gap| 35.6% (3 runs)

### History matching (every measured configuration, all claims together)
- 16 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.03); lr_schedule=inv, max_steps=10000 (max I 1.57); lr_schedule=inv, max_steps=100 (max I 1.84)
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.16); lr=1, max_steps=10000 (max I 2.11); lr=0.002, max_steps=10000 (max I 2.18)
  - `max_steps`: max_steps=100 (max I 0.77)
  - `lr`: lr=0.05 (max I 1.89); lr=0.5 (max I 2.09); lr=1 (max I 2.16)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; lr=0.5, max_steps=100; max_steps=100 | lr=0.001, lr_schedule=linear; lr=0.002, lr_schedule=inv; lr=0.002, lr_schedule=linear

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr': '0.001', 'lr_schedule': 'linear'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=0.5`, `max_steps=100` | 5 | +1.3% | +4.8% | 3.1% |
| `max_steps=100` | 6 | -3.8% | -24.5% | 14.2% |
| `lr_schedule=linear` | 3 | +65.1% | -6.2% | 35.6% |
| `lr_schedule=inv` | 3 | +54.4% | -25.7% | 40.0% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -19.8% | -62.8% | 41.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
