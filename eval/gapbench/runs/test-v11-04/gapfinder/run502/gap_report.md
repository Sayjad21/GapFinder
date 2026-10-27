# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 22:18 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +99.6% | -4.9% | ±9.8% | `lr=0.02` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +99.6% → -4.9% · 57 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0108`, `B0109`, `B0110`, `B0111`, `B0112` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `0.02`
- Command:

  Replay: fork checkpoint `9ab4acf0-9840-458d-a126-4111088d419b` and run
  ```
  RUN_TAG=4a06280cc862 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.02 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 72.69, 98.56, 88.73, 91.86, 44.99, 92.09; gap after -4.9%; result checkpoint `d69c6110-1860-4a3c-8455-2054fd86c0f3`
- Effect: candidate 90.3 minus naive 189.5 = -99.19, 95% bootstrap interval [-135.3, -70.94] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 189.5 over 5 runs; repeats: 150.7, 189.5, 191, 198.1, 184.8
- Spread: range 150.7 to 198.1, noise band ±9.33 (2 x MAD), CV 10.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +99.6% (noise band ±9.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +99.6% (it comes back)
- PASS · Held-out claim: C2: +117.1% to -82.0% (not worse beyond noise)
- FAIL · Evidence: `lr=0.02`: no evidence mentions '0.02'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -99.19 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (9.68 noise units, gap +4.5%); `eps_start=0.2` (9.59 noise units, gap -5.4%); `lr=0.001` (9.04 noise units, gap -10.8%); `lr=0.01` (8.71 noise units, gap -14.0%); `lr=1` (8.71 noise units, gap -14.0%) (and 14 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim +4.5%, mean |gap| 27.8% (6 runs)
  - `lr_schedule=inv`: this claim +49.8%, mean |gap| 41.1% (6 runs)
  - `max_steps=40`: this claim -57.9%, mean |gap| 47.6% (6 runs)

### History matching (every measured configuration, all claims together)
- 13 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=100 (max I 0.7)
  - `lr, lr_schedule`: lr=0.0, lr_schedule=linear (max I 1.02); lr=5, lr_schedule=inv (max I 1.03)
  - `lr`: lr=0.02 (max I 1.78); lr=0.01 (max I 1.8); lr=1 (max I 1.91); lr=0.05 (max I 2.21); +1 more
  - `eps_start, max_steps`: eps_start=0.01, max_steps=2000 (max I 2.06)
  - `eps_start`: eps_start=0.2 (max I 2.07)
- 6 separate islands (no single-knob move joins them): lr=0.02; lr=0.01; lr=1 | eps_start=0.2; eps_start=0.5 | max_steps=100 | lr=0.0, lr_schedule=linear

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '2000', 'lr': '5'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +4.5% | +51.0% | 27.8% |
| `lr_schedule=inv` | 6 | +49.8% | -32.3% | 41.1% |
| `lr=0.02` | 6 | -4.9% | -82.0% | 43.4% |
| `max_steps=40` | 6 | -57.9% | -37.4% | 47.6% |
| `lr=1` | 6 | -21.1% | -79.5% | 50.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
