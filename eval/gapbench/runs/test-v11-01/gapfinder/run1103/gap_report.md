# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 00:33 · 154 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -51.8% | +4.3% | ±1.4% | `max_steps=1000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -51.8% → +4.3% · 70 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0034`, `B0035`, `B0064` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `4dc8ef24-6f74-46a0-87bb-1230d6b73d94` and run
  ```
  RUN_TAG=7f96260510e6 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 323.4, 414.1, 498.4, 293; gap after +4.3%; result checkpoint `93d5fd90-5efc-4d95-a11f-ae4bea25d3a6`
- Effect: candidate 368.7 minus naive 170.3 = +198.4, 95% bootstrap interval [+119.6, +329.6] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 170.3 over 5 runs; repeats: 177.1, 165.6, 169.4, 170.3, 172.8
- Spread: range 165.6 to 177.1, noise band ±4.96 (2 x MAD), CV 2.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -51.8% (noise band ±1.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -51.8% (it comes back)
- PASS · Held-out claim: C2: +17.6% to +92.7% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +198.4 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=2000` (26.07 noise units, gap -15.2%); `max_steps=400` (24.84 noise units, gap -16.9%); `max_steps=500` (14 noise units, gap -32.2%); `init_q=-1.0` (4.83 noise units, gap -45.0%); `gamma=1.0` (4.6 noise units, gap -45.3%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=2000`: this claim +6.3%, mean |gap| 11.0% (4 runs)
  - `max_steps=1000`, `init_q=1.0`: this claim +21.5%, mean |gap| 11.4% (3 runs)
  - `gamma=0.999`, `max_steps=2000`: this claim -14.5%, mean |gap| 14.3% (3 runs)

### Equally good configurations
The target claim can't tell these 16 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=1000` (reported)
- `max_steps=2000`
- `max_steps=10000`
- `max_steps=500`
- `max_steps=400`
- `gamma=1.0, max_steps=1000`
- `init_q=0, max_steps=1000`
- `gamma=0.999, max_steps=2000`
- `gamma=0.995, max_steps=1000`
- `init_q=1.0, max_steps=2000`
- `init_q=0, max_steps=2000`
- `gamma=0.95, max_steps=2000`
- `gamma=0.998, max_steps=1000`
- `init_q=-1.0, max_steps=1000`
- `init_q=1.0, max_steps=1000`
- `gamma=0.95, max_steps=1000`

### History matching (every measured configuration, all claims together)
- 10 of 67 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `gamma, max_steps`: gamma=0.999, max_steps=2000 (max I 0.14); gamma=0.95, max_steps=2000 (max I 0.91); gamma=1.0, max_steps=1000 (max I 1.57); gamma=0.995, max_steps=1000 (max I 1.86)
  - `init_q, max_steps`: init_q=0, max_steps=1000 (max I 0.41); init_q=1.0, max_steps=2000 (max I 0.46)
  - `max_steps`: max_steps=1000 (max I 1.61); max_steps=2000 (max I 2.33); max_steps=400 (max I 2.7)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=2000 (max I 2.88)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=1000; max_steps=2000; max_steps=10000; max_steps=500; max_steps=400; gamma=1.0, max_steps=1000; init_q=0, max_steps=1000; gamma=0.999, max_steps=2000; gamma=0.995, max_steps=1000; init_q=1.0, max_steps=2000; init_q=0, max_steps=2000; gamma=0.95, max_steps=2000; gamma=0.998, max_steps=1000; init_q=-1.0, max_steps=1000; init_q=1.0, max_steps=1000; gamma=0.95, max_steps=1000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=2000` | 4 | +6.3% | -15.7% | 11.0% |
| `max_steps=1000`, `init_q=1.0` | 3 | +21.5% | +1.4% | 11.4% |
| `gamma=0.999`, `max_steps=2000` | 3 | -14.5% | +14.0% | 14.3% |
| `max_steps=1000`, `gamma=0.95` | 3 | -18.3% | +10.7% | 14.5% |
| `max_steps=1000`, `init_q=0` | 3 | -10.0% | +23.3% | 16.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The argument --init_q expects a floating‑point number, but the supplied value 'zero' cannot be parsed as a float, causing the program to reject it; retried as `init_q=0`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
