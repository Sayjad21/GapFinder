# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 23:33 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +85.8% | +3.2% | ±8.6% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +85.8% → +3.2% · 57 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0033`, `B0076`, `B0077`, `B0104`, `B0105`, `B0106` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `265756da-60d7-4837-8e6d-b9dc748dbb24` and run
  ```
  RUN_TAG=04826c19d7f2 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.6, 99.89, 99.72, 93.42, 96.36, 88.91; gap after +3.2%; result checkpoint `8ac4f1fb-622a-4331-8dc3-96b78e1b02eb`
- Effect: candidate 97.98 minus naive 176.4 = -78.4, 95% bootstrap interval [-96.51, -74.66] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 176.4 over 5 runs; repeats: 189.3, 173.6, 192.9, 172.3, 176.4
- Spread: range 172.3 to 192.9, noise band ±8.14 (2 x MAD), CV 5.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +85.8% (noise band ±8.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +85.8% (it comes back)
- PASS · Held-out claim: C2: -17.5% to +29.3% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -78.4 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.05` (9.09 noise units, gap -7.9%); `lr=0.02` (8.68 noise units, gap -11.4%); `lr=0.002` (8.52 noise units, gap -12.7%); `lr=0.5` (8.5 noise units, gap +12.9%); `eps_start=0.5` (7.51 noise units, gap +21.4%) (and 9 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=inv`: this claim -6.3%, mean |gap| 24.5% (5 runs)
  - `eps_start=0.2`, `lr=1`, `max_steps=100`, `lr_schedule=inv`: this claim +5.3%, mean |gap| 30.9% (5 runs)
  - `lr_schedule=inv`: this claim +31.1%, mean |gap| 34.1% (6 runs)

### History matching (every measured configuration, all claims together)
- 17 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.43); lr_schedule=inv, max_steps=100 (max I 0.89)
  - `max_steps`: max_steps=100 (max I 0.46)
  - `lr, lr_schedule`: lr=0.02, lr_schedule=linear (max I 0.78); lr=0.02, lr_schedule=inv (max I 1.2); lr=0.05, lr_schedule=linear (max I 1.53); lr=0.05, lr_schedule=inv (max I 1.71)
  - `eps_start, lr, lr_schedule, max_steps`: eps_start=0.2, lr=1, lr_schedule=inv, max_steps=100 (max I 0.87)
  - `eps_start, lr`: eps_start=0.5, lr=0.05 (max I 1.29)
  - `lr`: lr=1 (max I 1.32)
- 4 separate islands (no single-knob move joins them): lr=0.02, lr_schedule=linear; lr=0.02, lr_schedule=inv; eps_start=0.5, lr=0.05 | lr_schedule=linear, max_steps=100; max_steps=100; lr_schedule=inv, max_steps=100 | eps_start=0.5, lr_schedule=linear; eps_start=0.5, lr_schedule=inv | eps_start=0.2, lr=1, lr_schedule=inv, max_steps=100

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '40', 'lr': '0.05'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +3.2% | +29.3% | 16.3% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -6.3% | -42.6% | 24.5% |
| `eps_start=0.2`, `lr=1`, `max_steps=100`, `lr_schedule=inv` | 5 | +5.3% | +56.5% | 30.9% |
| `lr_schedule=inv` | 6 | +31.1% | -37.1% | 34.1% |
| `lr=0.02`, `lr_schedule=inv` | 5 | -7.0% | -76.1% | 41.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
