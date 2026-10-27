# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 22:37 · 153 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +104.7% | +4.6% | ±10.1% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Partially explained** · gap +104.7% → +4.6% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0020`, `B0021`, `B0022` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `a4b29c57-09a5-4621-9efa-ea81b3878235` and run
  ```
  RUN_TAG=0353ef743c70 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.64, 95.52, 99.17, 99.4, 98.67, 99.67; gap after +4.6%; result checkpoint `8a2cb3c5-aca8-4570-8140-933a6e3b2c2c`
- Effect: candidate 99.28 minus naive 194.3 = -95, 95% bootstrap interval [-100.3, -75.88] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 194.3 over 5 runs; repeats: 199.1, 194.3, 195.2, 177.8, 173.4
- Spread: range 173.4 to 199.1, noise band ±9.56 (2 x MAD), CV 6.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +104.7% (noise band ±10.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +104.7% (it comes back)
- PASS · Held-out claim: C2: +138.3% to +47.9% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -95 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (4.98 noise units, gap +54.5%); `max_steps=40` (4.39 noise units, gap -60.4%); `max_steps=20` (2.54 noise units, gap -79.0%); `lr_schedule=linear` (2.36 noise units, gap +80.9%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +2.2%, mean |gap| 23.0% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -7.4%, mean |gap| 26.8% (5 runs)
  - `max_steps=1000`, `lr_schedule=inv`: this claim +58.1%, mean |gap| 30.9% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.14); lr_schedule=inv, max_steps=100 (max I 0.84)
  - `max_steps`: max_steps=100 (max I 0.59)

Notes:
- lr_schedule dropped: with repeats, {'max_steps': '100', 'lr_schedule': 'linear'} fits {'max_steps': '100'}'s gap by less than one noise band, so it is not needed
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | +2.2% | +43.7% | 23.0% |
| `max_steps=100` | 6 | +4.6% | +47.9% | 26.3% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -7.4% | -46.2% | 26.8% |
| `max_steps=1000`, `lr_schedule=inv` | 5 | +58.1% | +3.7% | 30.9% |
| `max_steps=400`, `lr_schedule=inv` | 5 | +71.9% | -0.8% | 36.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
