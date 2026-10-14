# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 11:13 · 145 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +107.4% | +0.7% | ±3.8% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +107.4% → +0.7% · 47 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0026`, `B0027`, `B0028` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `34dcdf3b-4483-4d8c-ae41-77f935978c30` and run
  ```
  RUN_TAG=01657a573234 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 93.06, 90.43, 98.17, 99.31; gap after +0.7%; result checkpoint `d72f1036-37ec-4ba7-b17a-216dd8c2c510`
- Effect: candidate 95.62 minus naive 196.9 = -101.3, 95% bootstrap interval [-105.1, -83.69] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 (headline claim)

### What did we measure?
- Naive median 196.9 over 5 runs; repeats: 179.2, 198.7, 196.9, 181.7, 197.6
- Spread: range 179.2 to 198.7, noise band ±3.57 (2 x MAD), CV 5.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +107.4% (noise band ±3.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +107.4% (it comes back)
- PASS · Held-out claim: C2: +175.7% to -5.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -101.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (18.42 noise units, gap +38.1%); `eps_start=0.1` (18.21 noise units, gap -38.9%); `eps_start=0.5` (14.59 noise units, gap +52.5%); `lr_schedule=linear` (11.1 noise units, gap +65.7%); `max_steps=20` (7.58 noise units, gap -78.9%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +2.6%, mean |gap| 24.9% (3 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -7.4%, mean |gap| 30.0% (3 runs)
  - `eps_start=10`, `max_steps=100`: this claim +5.3%, mean |gap| 30.9% (3 runs)

### History matching (every measured configuration, all claims together)
- 6 of 47 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `max_steps`: max_steps=100 (max I 0.04)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.2); lr_schedule=inv, max_steps=100 (max I 0.96)
  - `eps_start, max_steps`: eps_start=10, max_steps=100 (max I 0.66); eps_start=0.5, max_steps=100 (max I 2.15)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 2.35)
- 2 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; eps_start=10, max_steps=100 | eps_start=0.5, lr_schedule=linear

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 4 | +0.7% | -5.2% | 2.9% |
| `lr_schedule=linear`, `max_steps=100` | 3 | +2.6% | +47.3% | 24.9% |
| `lr_schedule=inv`, `max_steps=100` | 3 | -7.4% | -52.5% | 30.0% |
| `eps_start=10`, `max_steps=100` | 3 | +5.3% | +56.5% | 30.9% |
| `lr_schedule=inv` | 4 | +47.2% | -21.3% | 34.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0463, sandbox reported $0.0000 (total $0.0463; this search; ledger extraction is included only if it shared the search's router)
