# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 19:54 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +81.3% | -3.7% | ±8.2% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +81.3% → -3.7% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0058`, `B0059`, `B0075`, `B0076`, `B0077` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `db3c5093-8106-4232-8d58-42f5080639ca` and run
  ```
  RUN_TAG=e023e2531f05 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 97.58, 90.86, 92.91, 96.24, 93.8, 98.73; gap after -3.7%; result checkpoint `7d10ac86-64ab-4de5-9b1c-c8c07401775f`
- Effect: candidate 95.02 minus naive 178.9 = -83.86, 95% bootstrap interval [-89.24, -66.25] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 178.9 over 5 runs; repeats: 169.9, 182.9, 181.9, 178.9, 159.2
- Spread: range 159.2 to 182.9, noise band ±8.08 (2 x MAD), CV 5.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +81.3% (noise band ±8.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +81.3% (it comes back)
- PASS · Held-out claim: C2: -31.4% to -29.9% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -83.86 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.01` (9.66 noise units, gap -2.2%); `lr=1` (7.81 noise units, gap +17.3%); `lr=0.001` (6.31 noise units, gap -29.6%); `lr=0.05` (5.86 noise units, gap +33.3%); `lr=0.2` (5.53 noise units, gap +36.0%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -1.6%, mean |gap| 1.2% (5 runs)
  - `lr=1`, `lr_schedule=inv`, `max_steps=100`: this claim +1.3%, mean |gap| 3.1% (5 runs)
  - `lr=0.05`, `max_steps=100`: this claim -11.0%, mean |gap| 38.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 7 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `lr, lr_schedule, max_steps`: lr=1, lr_schedule=inv, max_steps=100 (max I 0.2)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.54); lr_schedule=inv, max_steps=100 (max I 2.97)
  - `max_steps`: max_steps=100 (max I 1.32)
  - `lr, max_steps`: lr=0.05, max_steps=100 (max I 2.7); lr=1, max_steps=100 (max I 2.77)
  - `lr, lr_schedule`: lr=0.01, lr_schedule=inv (max I 2.95)
- 2 separate islands (no single-knob move joins them): lr=1, lr_schedule=inv, max_steps=100; lr_schedule=linear, max_steps=100; max_steps=100 | lr=0.01, lr_schedule=inv

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'max_steps': '100', 'lr': '1'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | -1.6% | -0.9% | 1.2% |
| `lr=1`, `lr_schedule=inv`, `max_steps=100` | 5 | +1.3% | +4.8% | 3.1% |
| `max_steps=100` | 6 | -3.7% | -29.9% | 16.8% |
| `lr=0.05`, `max_steps=100` | 5 | -11.0% | -65.2% | 38.1% |
| `lr_schedule=inv` | 6 | +32.7% | -51.8% | 42.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
