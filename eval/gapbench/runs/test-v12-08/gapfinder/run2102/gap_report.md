# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 21:11 · 184 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +74.7% | +0.0% | ±7.0% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +74.7% → +0.0% · 40 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0023`, `B0060`, `B0061`, `B0070`, `B0071`, `B0072` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `1dd6f447-8eed-4dff-846b-d323c2aa1666` and run
  ```
  RUN_TAG=45679a93314d "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.78, 93.92, 99, 99.75, 98.44, 93.78; gap after +0.0%; result checkpoint `7ebbbb7c-4acf-46f4-a272-2d1bd64349d2`
- Effect: candidate 98.72 minus naive 172.4 = -73.64, 95% bootstrap interval [-79.23, -56.85] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 172.4 over 5 runs; repeats: 175.8, 172.5, 161.3, 172.4, 152.5
- Spread: range 152.5 to 175.8, noise band ±6.88 (2 x MAD), CV 5.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +74.7% (noise band ±7.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +74.7% (it comes back)
- PASS · Held-out claim: C2: -60.4% to -3.8% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -73.64 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.02` (9.52 noise units, gap -8.3%); `lr_schedule=inv` (8.84 noise units, gap +13.0%); `lr=1` (8.18 noise units, gap -17.6%); `lr=0.001` (7.08 noise units, gap -25.3%); `lr=0.5` (7.03 noise units, gap +25.6%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -1.3%, mean |gap| 2.4% (5 runs)
  - `max_steps=100`, `lr=0.5`: this claim +1.3%, mean |gap| 3.1% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -7.3%, mean |gap| 28.4% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr=0.5, max_steps=100`
- `lr_schedule=linear, max_steps=100`
- `lr=0.02, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 4 of 40 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.47)
  - `max_steps`: max_steps=100 (max I 1.07)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 1.11); lr_schedule=inv, max_steps=100 (max I 2.86)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr=0.5, max_steps=100; lr_schedule=linear, max_steps=100; lr=0.02, lr_schedule=inv

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +0.0% | -3.8% | 1.9% |
| `max_steps=100`, `lr_schedule=linear` | 5 | -1.3% | -3.4% | 2.4% |
| `max_steps=100`, `lr=0.5` | 5 | +1.3% | +4.8% | 3.1% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -7.3% | -49.6% | 28.4% |
| `lr=0.02`, `lr_schedule=inv` | 5 | -7.4% | -86.8% | 47.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
