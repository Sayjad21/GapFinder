# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-15 00:17 · 78 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -44.5% | +6.3% | ±1.0% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -44.5% → +6.3% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0040` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `5294e05f-82d1-45a3-bd01-c85a5744e035` and run
  ```
  RUN_TAG=ea985b14f5a5 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 247.2, 320.1, 322, 356.3; gap after +6.3%; result checkpoint `11406688-fae0-488d-be09-5752890d28ee`
- Effect: candidate 321 minus naive 167.8 = +153.3, 95% bootstrap interval [+142, +190.7] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 167.8 over 5 runs; repeats: 184.1, 166.3, 167.8, 163.2, 169
- Spread: range 163.2 to 184.1, noise band ±3.03 (2 x MAD), CV 4.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -44.5% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -44.5% (it comes back)
- PASS · Held-out claim: C2: +13.6% to -4.5% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +153.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (29.54 noise units, gap -14.8%); `max_steps=1000` (20.49 noise units, gap -23.9%); `lr_schedule=linear` (3 noise units, gap -41.4%)
- Near alternatives (closest across all claims):
  - `max_steps=2000`: this claim -7.2%, mean |gap| 11.0% (4 runs)
  - `max_steps=1000`: this claim +18.0%, mean |gap| 12.8% (4 runs)
  - `max_steps=10000`: this claim +36.3%, mean |gap| 20.6% (4 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=500` (reported)
- `max_steps=2000`
- `max_steps=1000`
- `max_steps=10000`

### History matching (every measured configuration, all claims together)
- 1 of 32 tested configurations fit every claim within 3 sigma
- Equally good values: `max_steps` in {500, 2000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=500; max_steps=2000; max_steps=1000; max_steps=10000
- equally good values within one noise band (measured): max_steps in {500, 2000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 4 | +6.3% | -4.5% | 5.4% |
| `max_steps=2000` | 4 | -7.2% | +14.9% | 11.0% |
| `max_steps=1000` | 4 | +18.0% | +7.6% | 12.8% |
| `max_steps=10000` | 4 | +36.3% | -4.9% | 20.6% |
| naive (reproduction as run) | 5 | -44.5% | +13.6% | 29.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
