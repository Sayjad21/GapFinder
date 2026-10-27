# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 19:42 · 198 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -46.8% | -1.2% | ±3.6% | `max_steps=1000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -46.8% → -1.2% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0017`, `B0050`, `B0051`, `B0068`, `B0069`, `B0070` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `48b678b9-7e8e-465c-aff8-2d66be12619a` and run
  ```
  RUN_TAG=74cc9379a187 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 320.4, 231, 386.9, 238.7, 377.7, 482.4; gap after -1.2%; result checkpoint `37e6d674-4174-4b6c-b1ca-26c58b067139`
- Effect: candidate 349.1 minus naive 188 = +161, 95% bootstrap interval [+40.05, +279.2] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 188 over 5 runs; repeats: 194.3, 200, 186.5, 188, 151.7
- Spread: range 151.7 to 200, noise band ±12.55 (2 x MAD), CV 10.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -46.8% (noise band ±3.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -46.8% (it comes back)
- PASS · Held-out claim: C2: +227.7% to +42.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +161 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (9.14 noise units, gap -14.4%); `max_steps=2000` (7.68 noise units, gap -19.5%); `max_steps=500` (6.58 noise units, gap -23.4%); `max_steps=10000` (4.19 noise units, gap -31.9%)
- Near alternatives (closest across all claims):
  - `max_steps=500`, `gamma=0.998`: this claim -1.6%, mean |gap| 5.4% (5 runs)
  - `gamma=0.999`, `max_steps=400`: this claim -2.9%, mean |gap| 5.7% (5 runs)
  - `max_steps=500`, `gamma=1.0`: this claim +6.2%, mean |gap| 15.5% (5 runs)

### Equally good configurations
The target claim can't tell these 12 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=1000` (reported)
- `max_steps=400`
- `max_steps=2000`
- `max_steps=500`
- `gamma=0.999, max_steps=500`
- `gamma=1.0, max_steps=400`
- `gamma=0.998, max_steps=500`
- `gamma=0.995, max_steps=1000`
- `gamma=1.0, max_steps=2000`
- `gamma=1.0, max_steps=500`
- `gamma=0.999, max_steps=400`
- `gamma=0.995, max_steps=400`

### History matching (every measured configuration, all claims together)
- 15 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=1000 (max I 0.65); max_steps=10000 (max I 1.9); max_steps=400 (max I 2.37)
  - `gamma, max_steps`: gamma=0.995, max_steps=1000 (max I 0.78); gamma=0.998, max_steps=500 (max I 1); gamma=0.999, max_steps=500 (max I 1.18); gamma=1.0, max_steps=2000 (max I 1.69); +3 more

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=1000; max_steps=400; max_steps=2000; max_steps=500; gamma=0.999, max_steps=500; gamma=1.0, max_steps=400; gamma=0.998, max_steps=500; gamma=0.995, max_steps=1000; gamma=1.0, max_steps=2000; gamma=1.0, max_steps=500; gamma=0.999, max_steps=400; gamma=0.995, max_steps=400

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500`, `gamma=0.998` | 5 | -1.6% | +9.2% | 5.4% |
| `gamma=0.999`, `max_steps=400` | 5 | -2.9% | +8.4% | 5.7% |
| `max_steps=500`, `gamma=1.0` | 5 | +6.2% | +24.8% | 15.5% |
| `max_steps=400`, `gamma=0.995` | 5 | -13.8% | +21.7% | 17.8% |
| `max_steps=2000`, `gamma=0.995` | 2 | -20.6% | +20.8% | 20.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
