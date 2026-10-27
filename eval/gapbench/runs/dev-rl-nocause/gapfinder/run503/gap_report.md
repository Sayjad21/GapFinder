# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-14 22:13 · 167 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +52.6% | +12.6% | ±3.6% | `lr_schedule=inv` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +52.6% → +12.6% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0026`, `B0082`, `B0083`, `B0084`, `B0085`, `B0086` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `06be3501-8c3e-4ff9-800e-0bd35b9d1e31` and run
  ```
  RUN_TAG=02e122b6a1db "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 150.6, 136.1, 128.2, 136.4, 131.6, 129.1; gap after +12.6%; result checkpoint `b31de53f-662d-4207-a331-e9f99c978a7e`
- Effect: candidate 133.9 minus naive 181.5 = -47.65, 95% bootstrap interval [-52.96, -33] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 181.5 over 5 runs; repeats: 166.8, 181.5, 181.9, 183.7, 165.3
- Spread: range 165.3 to 183.7, noise band ±4.34 (2 x MAD), CV 5.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +52.6% (noise band ±3.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +52.6% (it comes back)
- PASS · Held-out claim: C2: -1.7% to -19.1% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -47.65 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=30` (9.3 noise units, gap -18.7%); `theta_bins=1` (6.44 noise units, gap -29.1%); `theta_bins=4` (4.73 noise units, gap +35.4%); `theta_bins=8` (3.26 noise units, gap +40.7%); `lr_schedule=linear` (1.95 noise units, gap +45.5%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_end=0.1`, `lr_schedule=inv`: this claim +14.4%, mean |gap| 12.8% (5 runs)
  - `eps_end=0.005`, `lr_schedule=inv`: this claim +10.2%, mean |gap| 16.8% (5 runs)
  - `eps_end=0.01`, `lr_schedule=inv`: this claim +10.5%, mean |gap| 21.9% (5 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=inv` (reported)
- `eps_end=0.01, lr_schedule=inv`
- `eps_end=0.005, lr_schedule=inv`
- `eps_end=0.025, lr_schedule=inv`
- `eps_end=0.1, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 8 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `eps_end, lr_schedule`: eps_end=0.01, lr_schedule=inv (max I 1.36); eps_end=0.005, lr_schedule=inv (max I 1.57); eps_end=0.1, lr_schedule=inv (max I 2.28); eps_end=0.025, lr_schedule=inv (max I 2.56)
  - `lr_schedule`: lr_schedule=inv (max I 2.01)
  - `theta_bins`: theta_bins=30 (max I 2.41)
  - `eps_end, theta_bins`: eps_end=0.01, theta_bins=1 (max I 2.81); eps_end=0.005, theta_bins=1 (max I 2.81)
- 3 separate islands (no single-knob move joins them): eps_end=0.01, lr_schedule=inv; eps_end=0.005, lr_schedule=inv; lr_schedule=inv | eps_end=0.01, theta_bins=1; eps_end=0.005, theta_bins=1 | theta_bins=30

Notes:
- configurations the target claim can't tell apart from the answer: lr_schedule=inv; eps_end=0.01, lr_schedule=inv; eps_end=0.005, lr_schedule=inv; eps_end=0.025, lr_schedule=inv; eps_end=0.1, lr_schedule=inv

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_end=0.1`, `lr_schedule=inv` | 5 | +14.4% | -11.1% | 12.8% |
| `lr_schedule=inv` | 6 | +12.6% | -19.1% | 15.8% |
| `eps_end=0.005`, `lr_schedule=inv` | 5 | +10.2% | -23.4% | 16.8% |
| `eps_end=0.01`, `lr_schedule=inv` | 5 | +10.5% | -33.2% | 21.9% |
| `theta_bins=8` | 6 | +48.6% | -0.2% | 24.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
