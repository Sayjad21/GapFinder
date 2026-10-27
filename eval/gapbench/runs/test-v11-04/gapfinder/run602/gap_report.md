# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 22:35 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +77.6% | +3.6% | ±10.5% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +77.6% → +3.6% · 57 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0033`, `B0128`, `B0129`, `B0130`, `B0131`, `B0132` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `50452491-e0e1-44f6-abed-2e2e829b3408` and run
  ```
  RUN_TAG=8cb3ad68493b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 97.11, 93.19, 99.62, 99.61, 95.25, 99.92; gap after +3.6%; result checkpoint `0590673a-cf9a-4893-b082-4d63e17e6aaf`
- Effect: candidate 98.36 minus naive 168.6 = -70.22, 95% bootstrap interval [-82.17, -57.9] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 168.6 over 5 runs; repeats: 163.6, 182.1, 152.2, 172.5, 168.6
- Spread: range 152.2 to 182.1, noise band ±10 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +77.6% (noise band ±10.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +77.6% (it comes back)
- PASS · Held-out claim: C2: +9.0% to +32.8% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -70.22 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.02` (7.35 noise units, gap +0.1%); `lr=0.01` (7.33 noise units, gap +0.4%); `lr=0.001` (7.25 noise units, gap -1.2%); `lr=1` (6.51 noise units, gap +9.0%); `lr=0.05` (6.05 noise units, gap +13.9%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `eps_start=0.2`, `lr_schedule=inv`, `lr=1`: this claim +5.3%, mean |gap| 30.9% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -11.9%, mean |gap| 33.1% (5 runs)
  - `lr_schedule=inv`: this claim +38.1%, mean |gap| 34.5% (6 runs)

### History matching (every measured configuration, all claims together)
- 16 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.65); lr_schedule=inv, max_steps=100 (max I 1.74)
  - `max_steps`: max_steps=100 (max I 0.83)
  - `lr, lr_schedule`: lr=0.02, lr_schedule=linear (max I 1.31); lr=0.01, lr_schedule=linear (max I 1.38); lr=0.01, lr_schedule=inv (max I 2.1)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.39)
  - `eps_start, lr, lr_schedule, max_steps`: eps_start=0.2, lr=1, lr_schedule=inv, max_steps=100 (max I 1.52)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.68)
  - `lr`: lr=1 (max I 2.09)
- 5 separate islands (no single-knob move joins them): lr=0.02, lr_schedule=linear; lr=0.01, lr_schedule=linear; lr=1 | lr_schedule=linear, max_steps=100; max_steps=100; eps_start=0.5, max_steps=100 | eps_start=0.5, lr_schedule=linear; eps_start=0.5, lr_schedule=inv | eps_start=0.2, lr=1, lr_schedule=inv, max_steps=100

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr': '0.02', 'eps_start': '0.2'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +3.6% | +32.8% | 18.2% |
| `max_steps=100`, `eps_start=0.2`, `lr_schedule=inv`, `lr=1` | 5 | +5.3% | +56.5% | 30.9% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -11.9% | -54.3% | 33.1% |
| `lr_schedule=inv` | 6 | +38.1% | -30.9% | 34.5% |
| `max_steps=100`, `eps_start=0.5` | 5 | -11.2% | -68.1% | 39.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
