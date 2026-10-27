# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 19:21 · 135 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +84.4% | +2.5% | ±8.2% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +84.4% → +2.5% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0028`, `B0029`, `B0048`, `B0049`, `B0050` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `53690ca6-1361-4965-90e1-283bc964efe9` and run
  ```
  RUN_TAG=892fe3297b41 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 90.67, 95.8, 99.88, 98.84, 92.11, 99.98; gap after +2.5%; result checkpoint `13997dca-cc81-41da-a71b-e3fbadaa5686`
- Effect: candidate 97.32 minus naive 175 = -77.7, 95% bootstrap interval [-83.52, -63.24] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 (headline claim)

### What did we measure?
- Naive median 175 over 5 runs; repeats: 180.4, 158, 178.7, 175, 171.1
- Spread: range 158 to 180.4, noise band ±7.74 (2 x MAD), CV 5.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +84.4% (noise band ±8.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +84.4% (it comes back)
- PASS · Held-out claim: C2: -9.5% to +19.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -77.7 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (5.83 noise units, gap +36.8%); `eps_start=0.02` (5.03 noise units, gap -43.3%); `eps_start=0.2` (4.88 noise units, gap -44.5%); `eps_start=0.1` (4.34 noise units, gap -49.0%); `lr_schedule=linear` (4.18 noise units, gap +50.3%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +2.2%, mean |gap| 23.1% (5 runs)
  - `lr_schedule=inv`: this claim +49.1%, mean |gap| 26.5% (6 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -12.1%, mean |gap| 33.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 5 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.13); lr_schedule=inv, max_steps=100 (max I 2.56)
  - `max_steps`: max_steps=100 (max I 0.46)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 2.42)
  - `eps_start`: eps_start=0.5 (max I 2.99)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +2.5% | +19.1% | 10.8% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +2.2% | +44.1% | 23.1% |
| `lr_schedule=inv` | 6 | +49.1% | +4.0% | 26.5% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -12.1% | -55.7% | 33.9% |
| `max_steps=100`, `eps_start=0.5` | 5 | -10.8% | -74.4% | 42.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
