# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 21:13 · 153 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +101.7% | -0.4% | ±6.0% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +101.7% → -0.4% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0031`, `B0032`, `B0033` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `dc2a97ed-0f19-4e54-9102-8cd33c110a7e` and run
  ```
  RUN_TAG=dedf2159498b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 94.15, 94.03, 96.39, 94.89; gap after -0.4%; result checkpoint `36227c6e-274b-4bbe-a2d8-e0b056a1b0ce`
- Effect: candidate 94.52 minus naive 191.5 = -96.97, 95% bootstrap interval [-100.5, -89.22] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 (headline claim)

### What did we measure?
- Naive median 191.5 over 5 runs; repeats: 195.6, 191.5, 189.1, 182.8, 194.3
- Spread: range 182.8 to 195.6, noise band ±5.69 (2 x MAD), CV 2.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +101.7% (noise band ±6.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +101.7% (it comes back)
- PASS · Held-out claim: C2: +137.9% to -26.4% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -96.97 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (12.04 noise units, gap +29.5%); `eps_start=0.2` (11.23 noise units, gap -34.4%); `eps_start=0.02` (8.46 noise units, gap -51.0%); `lr_schedule=inv` (7.78 noise units, gap +55.1%); `max_steps=40` (7.32 noise units, gap -57.9%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -2.0%, mean |gap| 2.1% (3 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -10.1%, mean |gap| 27.9% (3 runs)
  - `lr_schedule=inv`, `eps_start=0.5`: this claim -3.8%, mean |gap| 43.5% (3 runs)

### History matching (every measured configuration, all claims together)
- 6 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `max_steps`: max_steps=100 (max I 0.44)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.51); lr_schedule=inv, max_steps=100 (max I 1.44)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=inv (max I 1.58); eps_start=0.5, lr_schedule=linear (max I 1.66)
  - `eps_start`: eps_start=0.5 (max I 2.67)
- 2 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100 | eps_start=0.5, lr_schedule=inv; eps_start=0.5, lr_schedule=linear; eps_start=0.5

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 3 | -2.0% | +2.1% | 2.1% |
| `max_steps=100` | 4 | -0.4% | -26.4% | 13.4% |
| `max_steps=100`, `lr_schedule=inv` | 3 | -10.1% | -45.7% | 27.9% |
| `lr_schedule=inv`, `eps_start=0.5` | 3 | -3.8% | -83.2% | 43.5% |
| `eps_start=0.5` | 4 | +16.1% | -76.6% | 46.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `958fafed572bbbf30aedd8af86ba04a1fefc05c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
