# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 00:15 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +52.0% | +8.7% | ±8.6% | `lr_schedule=inv` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +52.0% → +8.7% · 70 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0026`, `B0049`, `B0050`, `B0051`, `B0052`, `B0053` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `3df9d663-94b3-4dde-9b81-0baad9151cca` and run
  ```
  RUN_TAG=0771f3d0fc59 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 118.6, 128, 144.7, 135.7, 117.8, 130.6; gap after +8.7%; result checkpoint `d785ba57-8a83-46eb-9bf3-8d4748850105`
- Effect: candidate 129.3 minus naive 180.8 = -51.46, 95% bootstrap interval [-61.27, -27.53] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 180.8 over 5 runs; repeats: 185.9, 180.4, 186.6, 155.2, 180.8
- Spread: range 155.2 to 186.6, noise band ±10.22 (2 x MAD), CV 7.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +52.0% (noise band ±8.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +52.0% (it comes back)
- PASS · Held-out claim: C2: +58.5% to -56.0% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -51.46 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=1` (4.9 noise units, gap +9.9%); `theta_bins=30` (2.55 noise units, gap -30.1%); `eps_end=0.1` (1.9 noise units, gap +35.7%); `theta_bins=3` (1.81 noise units, gap +36.5%); `lr_schedule=linear` (1.43 noise units, gap +39.7%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `theta_bins=12`: this claim +13.2%, mean |gap| 11.0% (5 runs)
  - `lr_schedule=inv`, `eps_end=0.0`: this claim +11.4%, mean |gap| 25.3% (5 runs)
  - `theta_bins=12`: this claim +43.0%, mean |gap| 27.7% (6 runs)

### History matching (every measured configuration, all claims together)
- 26 of 70 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, theta_bins`: lr_schedule=linear, theta_bins=12 (max I 1.06); lr_schedule=inv, theta_bins=4 (max I 1.52)
  - `eps_end, lr_schedule`: eps_end=0.0, lr_schedule=inv (max I 1.18); eps_end=0.005, lr_schedule=inv (max I 1.32); eps_end=0.525, lr_schedule=inv (max I 1.39); eps_end=0.01, lr_schedule=inv (max I 1.45); +1 more
  - `eps_end, theta_bins`: eps_end=0.025, theta_bins=1 (max I 1.23); eps_end=0.81, theta_bins=1 (max I 1.36)
  - `lr_schedule`: lr_schedule=inv (max I 1.59)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, theta_bins=12; eps_end=0.0, lr_schedule=inv; eps_end=0.005, lr_schedule=inv | eps_end=0.025, theta_bins=1; eps_end=0.81, theta_bins=1; eps_end=0.001, theta_bins=1

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'theta_bins': '30', 'eps_end': '0.981'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `theta_bins=12` | 5 | +13.2% | +8.7% | 11.0% |
| `lr_schedule=inv`, `eps_end=0.0` | 5 | +11.4% | -39.1% | 25.3% |
| `theta_bins=12` | 6 | +43.0% | -12.4% | 27.7% |
| `eps_end=0.1` | 6 | +43.7% | -14.2% | 29.0% |
| `theta_bins=4` | 6 | +54.0% | +8.8% | 31.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
