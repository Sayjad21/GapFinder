# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 19:53 · 132 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +87.1% | -0.4% | ±7.0% | `lr=0.05` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +87.1% → -0.4% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0028`, `B0029`, `B0059` (4 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `0.05`
- Command:

  Replay: fork checkpoint `852db02a-9309-453b-9bd6-2d647c989b4a` and run
  ```
  RUN_TAG=15d81e63f747 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.05 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 87.3, 146.9, 93.2, 103.3; gap after -0.4%; result checkpoint `e4b23878-7a4e-4e49-8de1-4cb4c4eb1dc9`
- Effect: candidate 98.25 minus naive 184.6 = -86.37, 95% bootstrap interval [-99.26, -33.44] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 184.6 over 5 runs; repeats: 184.6, 186.7, 181.2, 200, 175.7
- Spread: range 175.7 to 200, noise band ±6.92 (2 x MAD), CV 4.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +87.1% (noise band ±7.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +87.1% (it comes back)
- PASS · Held-out claim: C2: +10.6% to -82.4% (not worse beyond noise)
- FAIL · Evidence: `lr=0.05`: no evidence mentions '0.05'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -86.37 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (12.26 noise units, gap +1.1%); `lr=0.002` (11.76 noise units, gap -4.6%); `lr=1` (10.48 noise units, gap -13.6%); `lr=0.001` (10.08 noise units, gap -16.4%); `lr=0.5` (8.38 noise units, gap +28.3%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -0.5%, mean |gap| 1.5% (3 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -4.5%, mean |gap| 11.0% (3 runs)
  - `max_steps=100`: this claim -1.5%, mean |gap| 12.2% (4 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=0.05` (reported)
- `max_steps=100`
- `lr=0.002`
- `lr=0.01`
- `lr_schedule=linear, max_steps=100`
- `lr_schedule=inv, max_steps=100`
- `lr=0.05, lr_schedule=linear`
- `lr=0.05, lr_schedule=inv`
- `lr=0.001, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 12 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.09); lr_schedule=inv, max_steps=100 (max I 0.71)
  - `max_steps`: max_steps=100 (max I 0.5)
  - `lr, lr_schedule`: lr=0.05, lr_schedule=inv (max I 1.41); lr=0.05, lr_schedule=linear (max I 1.6); lr=0.002, lr_schedule=linear (max I 2.37)
  - `lr`: lr=0.05 (max I 1.59); lr=1 (max I 1.75); lr=0.002 (max I 2.25)
  - `lr, max_steps`: lr=1, max_steps=100 (max I 2.16)

Notes:
- configurations the target claim can't tell apart from the answer: lr=0.05; max_steps=100; lr=0.002; lr=0.01; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100; lr=0.05, lr_schedule=linear; lr=0.05, lr_schedule=inv; lr=0.001, lr_schedule=inv

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 3 | -0.5% | -2.4% | 1.5% |
| `lr_schedule=inv`, `max_steps=100` | 3 | -4.5% | -17.6% | 11.0% |
| `max_steps=100` | 4 | -1.5% | -22.9% | 12.2% |
| `lr=0.05` | 4 | -0.4% | -82.4% | 41.4% |
| `lr_schedule=linear`, `lr=0.05` | 3 | +11.7% | -84.2% | 47.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
