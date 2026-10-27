# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 19:46 · 194 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +82.6% | +1.4% | ±18.0% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +82.6% → +1.4% · 57 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0033`, `B0076`, `B0077`, `B0104`, `B0105`, `B0106` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `36ab266c-96ef-4766-a34e-b919c2a31df8` and run
  ```
  RUN_TAG=c17974edaadb "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.61, 99.53, 98.81, 92.8, 93.62, 92.55; gap after +1.4%; result checkpoint `e47557e4-042b-41ff-847d-73c776899228`
- Effect: candidate 96.22 minus naive 173.3 = -77.07, 95% bootstrap interval [-95.41, -61.2] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 173.3 over 5 runs; repeats: 173.3, 164.8, 153.8, 174.8, 193.6
- Spread: range 153.8 to 193.6, noise band ±17.05 (2 x MAD), CV 8.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +82.6% (noise band ±18.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +82.6% (it comes back)
- PASS · Held-out claim: C2: -14.2% to +2.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -77.07 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.002` (3.9 noise units, gap -12.4%); `lr=0.05` (3.6 noise units, gap +17.8%); `lr=0.5` (3.51 noise units, gap -19.5%); `eps_start=0.1` (3.47 noise units, gap -20.3%); `eps_start=0.2` (3.46 noise units, gap -20.4%) (and 9 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +3.0%, mean |gap| 25.5% (5 runs)
  - `lr_schedule=inv`: this claim +43.8%, mean |gap| 28.2% (3 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -9.7%, mean |gap| 29.3% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr=1`

### History matching (every measured configuration, all claims together)
- 16 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=100 (max I 0.12)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.86); lr_schedule=inv, max_steps=100 (max I 1.31)
  - `lr`: lr=1 (max I 1.3); lr=0.002 (max I 1.55); lr=0.02 (max I 1.92); lr=0.001 (max I 1.99)
  - `lr, lr_schedule`: lr=0.05, lr_schedule=inv (max I 1.35); lr=0.05, lr_schedule=linear (max I 2.01)
  - `lr, max_steps`: lr=0.05, max_steps=100 (max I 1.52)
- 3 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; lr=1 | eps_start=0.2, lr=1, max_steps=100 | eps_start=0.2

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr=1

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +1.4% | +2.2% | 1.8% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +3.0% | +48.1% | 25.5% |
| `lr_schedule=inv` | 3 | +43.8% | -12.6% | 28.2% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -9.7% | -48.8% | 29.3% |
| `lr_schedule=linear`, `lr=0.05` | 5 | +23.8% | -54.7% | 39.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
