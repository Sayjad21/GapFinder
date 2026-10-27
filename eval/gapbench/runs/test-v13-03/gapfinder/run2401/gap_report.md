# Gap Report: test-v13-03

Artifact `rlbench` · generated 2026-10-16 01:34 · 81 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +82.0% | -3.6% | ±13.5% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Fits but unsupported** · gap +82.0% → -3.6% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0013`, `B0028`, `B0029`, `B0030`, `B0031`, `B0032` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `7b77779b-d042-4efa-8996-3ebe56093bf9` and run
  ```
  RUN_TAG=d2d9e40f1ad2 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 94.67, 96.62, 93.58, 95.14, 100, 97.39; gap after -3.6%; result checkpoint `faf49293-135f-4a86-a3ae-a7e715dc96bc`
- Effect: candidate 95.88 minus naive 181.1 = -85.25, 95% bootstrap interval [-89.12, -65.46] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 181.1 over 5 runs; repeats: 187.9, 181.1, 156.8, 166.2, 182.1
- Spread: range 156.8 to 187.9, noise band ±13.47 (2 x MAD), CV 7.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +82.0% (noise band ±13.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +82.0% (it comes back)
- PASS · Held-out claim: C2: -48.1% to -38.4% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -85.25 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (5.64 noise units, gap +5.7%); `lr_schedule=inv` (4.71 noise units, gap +18.2%); `max_steps=40` (1.58 noise units, gap -60.7%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -2.3%, mean |gap| 3.2% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -9.7%, mean |gap| 37.2% (5 runs)
  - `lr_schedule=inv`: this claim +33.6%, mean |gap| 41.9% (6 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.51); lr_schedule=inv, max_steps=100 (max I 1.6)
  - `max_steps`: max_steps=100 (max I 0.93)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | -2.3% | -4.2% | 3.2% |
| `max_steps=100` | 6 | -3.6% | -38.4% | 21.0% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -9.7% | -64.7% | 37.2% |
| `lr_schedule=inv` | 6 | +33.6% | -50.2% | 41.9% |
| `max_steps=10000`, `lr_schedule=inv` | 2 | +43.4% | -51.6% | 47.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
