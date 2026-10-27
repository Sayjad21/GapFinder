# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 19:30 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +95.4% | -2.9% | ±8.6% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +95.4% → -2.9% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0058`, `B0059`, `B0078`, `B0079`, `B0080` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `9d1fd3aa-3596-425c-8253-f44b2386555d` and run
  ```
  RUN_TAG=31bc7a74d486 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 96.11, 96.2, 93.91, 95.48, 88.72, 96.55; gap after -2.9%; result checkpoint `b9f8ddc5-5e06-4a31-b159-c158371aba46`
- Effect: candidate 95.8 minus naive 192.8 = -97.03, 95% bootstrap interval [-104.7, -73.19] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 192.8 over 5 runs; repeats: 195.1, 168.2, 168.8, 192.8, 197
- Spread: range 168.2 to 197, noise band ±8.44 (2 x MAD), CV 7.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +95.4% (noise band ±8.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +95.4% (it comes back)
- PASS · Held-out claim: C2: +79.3% to -35.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -97.03 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.001` (10.83 noise units, gap -2.8%); `lr=0.05` (10.32 noise units, gap +7.2%); `lr=0.02` (9.96 noise units, gap +10.2%); `lr=0.5` (8.77 noise units, gap -20.4%); `lr=0.002` (8.62 noise units, gap -21.6%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -1.4%, mean |gap| 2.3% (5 runs)
  - `max_steps=100`, `lr=0.5`: this claim +1.3%, mean |gap| 3.1% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -9.7%, mean |gap| 39.8% (2 runs)

### History matching (every measured configuration, all claims together)
- 19 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.12); lr=0.02, max_steps=10000 (max I 1.54); lr=0.05, max_steps=100 (max I 1.56)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.31); lr_schedule=inv, max_steps=100 (max I 1.22)
  - `max_steps`: max_steps=100 (max I 1.01)
  - `lr, lr_schedule`: lr=0.05, lr_schedule=linear (max I 1.43); lr=0.02, lr_schedule=linear (max I 1.62); lr=0.05, lr_schedule=inv (max I 1.64)
  - `lr`: lr=0.5 (max I 1.85)

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'max_steps': '100', 'lr_schedule': 'inv'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | -1.4% | -3.1% | 2.3% |
| `max_steps=100`, `lr=0.5` | 5 | +1.3% | +4.8% | 3.1% |
| `max_steps=100` | 6 | -2.9% | -35.2% | 19.1% |
| `max_steps=100`, `lr_schedule=inv` | 2 | -9.7% | -69.9% | 39.8% |
| `lr=0.05` | 6 | +16.6% | -66.0% | 41.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
