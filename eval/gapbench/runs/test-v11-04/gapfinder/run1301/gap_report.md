# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 01:14 · 166 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +87.0% | +4.2% | ±7.2% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +87.0% → +4.2% · 73 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0030`, `B0031`, `B0050` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `f030c290-8642-4c4a-9071-005b21729f9d` and run
  ```
  RUN_TAG=2c5800f21483 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 96.84, 99.37, 98.97, 98.91; gap after +4.2%; result checkpoint `f7be633c-f31b-4515-a1d1-c5db76d7a6b2`
- Effect: candidate 98.94 minus naive 177.5 = -78.59, 95% bootstrap interval [-88.08, -73.93] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 (headline claim)

### What did we measure?
- Naive median 177.5 over 5 runs; repeats: 171.9, 180.9, 176.5, 177.5, 189.6
- Spread: range 171.9 to 189.6, noise band ±6.84 (2 x MAD), CV 3.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +87.0% (noise band ±7.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +87.0% (it comes back)
- PASS · Held-out claim: C2: -9.9% to +48.4% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -78.59 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.2` (6.53 noise units, gap -40.0%); `eps_start=0.5` (6.4 noise units, gap +40.9%); `lr_schedule=inv` (4.98 noise units, gap +51.1%); `eps_start=0.1` (4.67 noise units, gap -53.3%); `eps_start=0.01` (4.37 noise units, gap -55.6%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -0.5%, mean |gap| 2.5% (3 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -6.7%, mean |gap| 25.6% (3 runs)
  - `eps_start=50`, `max_steps=100`: this claim +5.0%, mean |gap| 28.6% (3 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`
- `eps_start=2, max_steps=100`
- `lr_schedule=inv, max_steps=100`
- `eps_start=0.5, lr_schedule=inv`
- `eps_start=0.5, max_steps=100`

### History matching (every measured configuration, all claims together)
- 8 of 73 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.18); lr_schedule=inv, max_steps=100 (max I 1.37)
  - `eps_start, max_steps`: eps_start=2, max_steps=100 (max I 0.73); eps_start=50, max_steps=100 (max I 0.81); eps_start=5, max_steps=100 (max I 1); eps_start=10, max_steps=100 (max I 1.04)
  - `max_steps`: max_steps=100 (max I 0.78)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 2.11)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; eps_start=2, max_steps=100; max_steps=100 | eps_start=0.5, lr_schedule=linear

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100; eps_start=2, max_steps=100; lr_schedule=inv, max_steps=100; eps_start=0.5, lr_schedule=inv; eps_start=0.5, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 3 | -0.5% | -4.4% | 2.5% |
| `max_steps=100`, `lr_schedule=inv` | 3 | -6.7% | -44.5% | 25.6% |
| `max_steps=100` | 4 | +4.2% | +48.4% | 26.3% |
| `eps_start=50`, `max_steps=100` | 3 | +5.0% | +52.1% | 28.6% |
| `eps_start=2`, `max_steps=100` | 3 | +5.0% | +52.7% | 28.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
