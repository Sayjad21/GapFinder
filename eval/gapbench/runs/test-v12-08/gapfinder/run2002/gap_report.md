# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 21:11 · 175 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +75.8% | -3.1% | ±32.9% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +75.8% → -3.1% · 45 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0023`, `B0058`, `B0059`, `B0068`, `B0069`, `B0070` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `e38190ee-a64c-4bba-a41a-59324f4cb409` and run
  ```
  RUN_TAG=d9075f514409 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.34, 86.08, 93.44, 99.72, 97.76, 90.86; gap after -3.1%; result checkpoint `8733659d-d5fc-451f-987c-4eeef20094f3`
- Effect: candidate 95.6 minus naive 173.5 = -77.87, 95% bootstrap interval [-101.2, -62.94] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 173.5 over 5 runs; repeats: 173.5, 192.5, 192.4, 160.4, 157.2
- Spread: range 157.2 to 192.5, noise band ±32.44 (2 x MAD), CV 9.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +75.8% (noise band ±32.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +75.8% (it comes back)
- PASS · Held-out claim: C2: -40.1% to -25.8% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -77.87 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.01` (1.7 noise units, gap -19.8%); `lr=1` (1.66 noise units, gap +21.4%); `lr=0.002` (1.64 noise units, gap -21.9%); `lr=0.001` (1.52 noise units, gap -25.8%); `lr=0.5` (1.44 noise units, gap +28.4%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -1.0%, mean |gap| 1.9% (5 runs)
  - `lr=1`: this claim -1.6%, mean |gap| 43.0% (6 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -20.0%, mean |gap| 43.7% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 19 of 45 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.35); lr_schedule=inv, max_steps=100 (max I 1.65)
  - `max_steps`: max_steps=100 (max I 0.63)
  - `lr`: lr=0.05 (max I 1.81); lr=1 (max I 2.08); lr=0.02 (max I 2.17); lr=0.01 (max I 2.25)
  - `lr, lr_schedule`: lr=0.001, lr_schedule=linear (max I 2.02)
  - `lr, max_steps`: lr=0.001, max_steps=10000 (max I 2.09); lr=1, max_steps=100 (max I 2.1)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | -1.0% | -2.7% | 1.9% |
| `max_steps=100` | 6 | -3.1% | -25.8% | 14.5% |
| `lr=1` | 6 | -1.6% | -84.5% | 43.0% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -20.0% | -67.4% | 43.7% |
| `lr=0.2` | 6 | +81.4% | -7.2% | 44.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
