# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 19:45 · 132 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +94.0% | +2.6% | ±20.6% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +94.0% → +2.6% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0030`, `B0031`, `B0046`, `B0047`, `B0048` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `d7babe8b-99c8-4205-b325-d03a73de3291` and run
  ```
  RUN_TAG=f9b8d1ddd9dc "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 98.06, 92.73, 96.7, 98.53, 99.64, 91.39; gap after +2.6%; result checkpoint `5be127e1-f5f6-423c-85a9-eade23564887`
- Effect: candidate 97.38 minus naive 184.2 = -86.82, 95% bootstrap interval [-98.51, -60.82] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 (headline claim)

### What did we measure?
- Naive median 184.2 over 5 runs; repeats: 197.2, 187.9, 174.4, 184.2, 151.5
- Spread: range 151.5 to 197.2, noise band ±19.52 (2 x MAD), CV 9.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +94.0% (noise band ±20.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +94.0% (it comes back)
- PASS · Held-out claim: C2: +109.6% to +22.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -86.82 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (3.37 noise units, gap +24.7%); `eps_start=0.1` (3.03 noise units, gap -31.8%); `lr_schedule=inv` (2.77 noise units, gap +37.0%); `eps_start=0.2` (2.45 noise units, gap -43.6%); `eps_start=0.5` (2.28 noise units, gap +47.2%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +1.0%, mean |gap| 4.3% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -11.0%, mean |gap| 37.2% (5 runs)
  - `max_steps=100`, `eps_start=0.5`: this claim -9.4%, mean |gap| 39.5% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`
- `eps_start=0.5, lr_schedule=linear`
- `eps_start=0.5, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 10 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.2); lr_schedule=inv, max_steps=100 (max I 0.9)
  - `max_steps`: max_steps=100 (max I 0.22)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.12); eps_start=0.1, max_steps=1000 (max I 2.1); eps_start=0.2, max_steps=1000 (max I 2.23)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=inv (max I 1.21); eps_start=0.5, lr_schedule=linear (max I 1.25)
  - `eps_start`: eps_start=0.2 (max I 2.35); eps_start=0.5 (max I 2.85)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100; eps_start=0.5, lr_schedule=linear; eps_start=0.5, lr_schedule=inv

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | +1.0% | +7.7% | 4.3% |
| `max_steps=100` | 6 | +2.6% | +22.6% | 12.6% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -11.0% | -63.4% | 37.2% |
| `max_steps=100`, `eps_start=0.5` | 5 | -9.4% | -69.6% | 39.5% |
| `eps_start=0.5` | 6 | +34.5% | -45.2% | 39.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
