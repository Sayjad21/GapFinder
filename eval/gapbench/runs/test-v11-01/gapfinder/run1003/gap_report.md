# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 00:21 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -49.7% | +3.7% | ±3.1% | `max_steps=1000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -49.7% → +3.7% · 76 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0034`, `B0035`, `B0060`, `B0061`, `B0062` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `9ec637a2-d3fd-4d3d-950e-f5d53bb5154a` and run
  ```
  RUN_TAG=49331b196796 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 493.9, 302.7, 534.8, 392.1, 341.1, 255.3; gap after +3.7%; result checkpoint `46452c4b-220d-4b16-ae2b-b56c509f8764`
- Effect: candidate 366.6 minus naive 177.8 = +188.8, 95% bootstrap interval [+98.98, +324.6] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 177.8 over 5 runs; repeats: 177.8, 189.7, 183.3, 176.8, 142.2
- Spread: range 142.2 to 189.7, noise band ±11 (2 x MAD), CV 10.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -49.7% (noise band ±3.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -49.7% (it comes back)
- PASS · Held-out claim: C2: +33.4% to +20.7% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +188.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=2000` (10.17 noise units, gap +18.0%); `max_steps=500` (9.03 noise units, gap -21.6%); `gamma=0.998` (1.92 noise units, gap -43.7%); `max_steps=400` (1.65 noise units, gap -44.5%)
- Near alternatives (closest across all claims):
  - `gamma=0.995`, `max_steps=1000`: this claim +7.7%, mean |gap| 12.0% (5 runs)
  - `max_steps=2000`, `init_q=1.0`: this claim -5.7%, mean |gap| 12.5% (5 runs)
  - `max_steps=500`, `gamma=0.998`: this claim -19.5%, mean |gap| 14.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 12 of 73 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `init_q, max_steps`: init_q=1.0, max_steps=1000 (max I 0.41); init_q=1.0, max_steps=500 (max I 0.48); init_q=1.0, max_steps=2000 (max I 1.53); init_q=-1.0, max_steps=500 (max I 2.43); +1 more
  - `gamma, max_steps`: gamma=1.0, max_steps=1000 (max I 1.05); gamma=0.995, max_steps=1000 (max I 1.1)
  - `max_steps`: max_steps=1000 (max I 1.57); max_steps=500 (max I 1.89); max_steps=2000 (max I 2.5)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '2000', 'gamma': '0.999'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `gamma=0.995`, `max_steps=1000` | 5 | +7.7% | +16.4% | 12.0% |
| `max_steps=1000` | 6 | +3.7% | +20.7% | 12.2% |
| `max_steps=2000`, `init_q=1.0` | 5 | -5.7% | +19.3% | 12.5% |
| `max_steps=500`, `gamma=0.998` | 5 | -19.5% | +9.3% | 14.4% |
| `gamma=1.0`, `max_steps=1000` | 5 | +8.9% | +20.6% | 14.7% |

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
