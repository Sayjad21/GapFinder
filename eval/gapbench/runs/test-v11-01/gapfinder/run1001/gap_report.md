# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 00:21 · 177 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -48.3% | -6.3% | ±2.9% | `max_steps=2000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -48.3% → -6.3% · 72 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0019`, `B0054`, `B0055`, `B0070` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `2000`
- Command:

  Replay: fork checkpoint `cbdbccab-6fe3-4ab0-bbfb-0e5433fe0a2e` and run
  ```
  RUN_TAG=792889cf66c2 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 2000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 151.8, 567.4, 279, 383.5; gap after -6.3%; result checkpoint `f97e453c-9ef3-42f7-8712-86161dd0dc5a`
- Effect: candidate 331.3 minus naive 182.7 = +148.5, 95% bootstrap interval [+93.07, +389.6] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 182.7 over 5 runs; repeats: 182.7, 175.5, 177.6, 184.7, 188.6
- Spread: range 175.5 to 188.6, noise band ±10.2 (2 x MAD), CV 2.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -48.3% (noise band ±2.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -48.3% (it comes back)
- PASS · Held-out claim: C2: +45.7% to -18.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=2000`: no evidence mentions '2000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +148.5 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (10.32 noise units, gap -18.5%); `max_steps=400` (10.3 noise units, gap -18.6%); `max_steps=10000` (10.25 noise units, gap -18.7%); `max_steps=1000` (6.28 noise units, gap +30.2%); `gamma=0.998` (1.69 noise units, gap -43.4%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=400`, `gamma=0.995`: this claim -7.1%, mean |gap| 4.2% (3 runs)
  - `gamma=1.0`, `max_steps=1000`: this claim -12.8%, mean |gap| 14.1% (3 runs)
  - `gamma=0.995`, `max_steps=1000`: this claim -11.8%, mean |gap| 16.2% (3 runs)

### Equally good configurations
The target claim can't tell these 11 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=2000` (reported)
- `max_steps=1000`
- `max_steps=10000`
- `gamma=0.999, max_steps=2000`
- `gamma=0.999, max_steps=10000`
- `gamma=0.999, max_steps=400`
- `gamma=0.995, max_steps=500`
- `gamma=0.998, max_steps=400`
- `gamma=1.0, max_steps=1000`
- `gamma=0.995, max_steps=400`
- `gamma=0.995, max_steps=10000`

### History matching (every measured configuration, all claims together)
- 14 of 72 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=2000 (max I 0.44)
  - `gamma, max_steps`: gamma=0.999, max_steps=2000 (max I 0.82); gamma=0.999, max_steps=10000 (max I 1.25); gamma=0.995, max_steps=500 (max I 1.35); gamma=0.998, max_steps=400 (max I 1.5); +4 more
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=2000 (max I 1.05)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=2000; max_steps=1000; max_steps=10000; gamma=0.999, max_steps=2000; gamma=0.999, max_steps=10000; gamma=0.999, max_steps=400; gamma=0.995, max_steps=500; gamma=0.998, max_steps=400; gamma=1.0, max_steps=1000; gamma=0.995, max_steps=400; gamma=0.995, max_steps=10000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=400`, `gamma=0.995` | 3 | -7.1% | +1.3% | 4.2% |
| `max_steps=2000` | 4 | -6.3% | -18.1% | 12.2% |
| `gamma=1.0`, `max_steps=1000` | 3 | -12.8% | +15.5% | 14.1% |
| `gamma=0.995`, `max_steps=1000` | 3 | -11.8% | +20.5% | 16.2% |
| `max_steps=400` | 4 | -26.3% | +12.7% | 19.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
