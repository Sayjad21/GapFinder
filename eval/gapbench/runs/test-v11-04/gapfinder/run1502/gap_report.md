# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 19:21 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +92.7% | -2.5% | ±17.0% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +92.7% → -2.5% · 57 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0033`, `B0078`, `B0079`, `B0082`, `B0083`, `B0084` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `295b1ed0-c199-4bbb-82af-16721010139c` and run
  ```
  RUN_TAG=47810db089fd "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.91, 93.39, 87.17, 99.48, 91.7, 87.43; gap after -2.5%; result checkpoint `7f8b727d-081e-4c97-8690-7278e71aa380`
- Effect: candidate 92.55 minus naive 182.9 = -90.37, 95% bootstrap interval [-101.7, -75.74] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 182.9 over 5 runs; repeats: 182.9, 191.2, 191, 166.7, 177.4
- Spread: range 166.7 to 191.2, noise band ±16.14 (2 x MAD), CV 5.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +92.7% (noise band ±17.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +92.7% (it comes back)
- PASS · Held-out claim: C2: +8.0% to -34.4% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -90.37 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.02` (5.31 noise units, gap -2.4%); `lr=1` (5.16 noise units, gap -4.9%); `lr=0.01` (4.48 noise units, gap -16.4%); `eps_start=0.5` (3.94 noise units, gap +25.8%); `eps_start=0.2` (3.49 noise units, gap -33.4%) (and 11 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -1.1%, mean |gap| 9.6% (5 runs)
  - `lr=1`, `max_steps=100`: this claim -10.3%, mean |gap| 26.4% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -14.5%, mean |gap| 28.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 14 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.17); lr_schedule=inv, max_steps=100 (max I 1.37)
  - `max_steps`: max_steps=100 (max I 0.26)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.4)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.41)
  - `eps_start, lr`: eps_start=0.5, lr=1 (max I 1.62); eps_start=0.2, lr=1 (max I 1.66)
  - `lr, lr_schedule`: lr=0.02, lr_schedule=linear (max I 1.7)
  - `lr`: lr=1 (max I 1.74); lr=0.02 (max I 1.75)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; max_steps=100; lr_schedule=inv, max_steps=100 | eps_start=0.5, lr_schedule=linear; eps_start=0.2, lr_schedule=linear

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'max_steps': '100', 'eps_start': '0.5'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | -1.1% | -18.2% | 9.6% |
| `max_steps=100` | 6 | -2.5% | -34.4% | 18.5% |
| `lr=1`, `max_steps=100` | 5 | -10.3% | -42.5% | 26.4% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -14.5% | -41.6% | 28.1% |
| `max_steps=100`, `eps_start=0.5` | 2 | -14.7% | -49.2% | 32.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
