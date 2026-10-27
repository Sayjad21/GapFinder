# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 23:32 · 134 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +91.1% | -1.3% | ±24.5% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +91.1% → -1.3% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0028`, `B0029`, `B0042`, `B0043`, `B0044` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `d5a32da4-f9ae-48a5-a71f-53aa8cfeb5a2` and run
  ```
  RUN_TAG=3549b60bea24 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 100, 86.73, 92.2, 94.53, 99.92, 92.94; gap after -1.3%; result checkpoint `934c13c5-6889-402b-86eb-768da52cad31`
- Effect: candidate 93.74 minus naive 181.4 = -87.71, 95% bootstrap interval [-98.74, -69.1] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 (headline claim)

### What did we measure?
- Naive median 181.4 over 5 runs; repeats: 161.2, 187.7, 161.4, 181.4, 193.1
- Spread: range 161.2 to 193.1, noise band ±23.24 (2 x MAD), CV 8.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +91.1% (noise band ±24.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +91.1% (it comes back)
- PASS · Held-out claim: C2: +65.8% to -26.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -87.71 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (3.17 noise units, gap +13.5%); `eps_start=0.2` (2.25 noise units, gap -36.0%); `lr_schedule=inv` (2.14 noise units, gap +38.9%); `eps_start=0.1` (1.63 noise units, gap -51.2%); `max_steps=40` (1.36 noise units, gap -57.9%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +2.6%, mean |gap| 24.0% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -5.0%, mean |gap| 28.2% (5 runs)
  - `lr_schedule=inv`: this claim +41.4%, mean |gap| 42.8% (6 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=inv, max_steps=100`
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 6 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `max_steps`: max_steps=100 (max I 0.12)
  - `lr_schedule, max_steps`: lr_schedule=inv, max_steps=100 (max I 0.54); lr_schedule=linear, max_steps=100 (max I 0.68)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.59)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.86)
  - `eps_start`: eps_start=0.2 (max I 2.01)
- 3 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=inv, max_steps=100; lr_schedule=linear, max_steps=100 | eps_start=0.5, lr_schedule=linear | eps_start=0.2

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=inv, max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | -1.3% | -26.2% | 13.7% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +2.6% | +45.5% | 24.0% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -5.0% | -51.5% | 28.2% |
| `lr_schedule=inv` | 6 | +41.4% | -44.3% | 42.8% |
| `max_steps=100`, `eps_start=0.5` | 5 | -13.3% | -76.9% | 45.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
