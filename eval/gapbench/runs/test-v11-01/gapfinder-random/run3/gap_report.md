# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 12:21 · 86 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -49.8% | -25.8% | ±6.1% | `max_steps=1000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -49.8% → -25.8% · 42 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0014`, `B0034`, `B0035`, `B0036`, `B0037`, `B0038` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `a37905c5-04fb-4ee4-812f-b53ffe9df0fc` and run
  ```
  RUN_TAG=6f61e2440e43 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 291, 424.3, 233.5, 386.3, 216.8, 176.8; gap after -25.8%; result checkpoint `72e05ecf-63d3-445b-a835-5e847b927abc`
- Effect: candidate 262.2 minus naive 177.6 = +84.66, 95% bootstrap interval [+12.36, +218.3] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 177.6 over 5 runs; repeats: 161.1, 177.6, 184, 166.9, 200
- Spread: range 161.1 to 200, noise band ±21.4 (2 x MAD), CV 8.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -49.8% (noise band ±6.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -49.8% (it comes back)
- PASS · Held-out claim: C2: +25.1% to +26.5% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +84.66 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (4.42 noise units, gap +23.0%); `max_steps=2000` (2.79 noise units, gap +32.8%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`, `gamma=1.0`: this claim -4.4%, mean |gap| 7.7% (5 runs)
  - `max_steps=1000`, `init_q=-1.0`: this claim -4.9%, mean |gap| 10.9% (5 runs)
  - `max_steps=500`, `init_q=-1.0`: this claim -10.4%, mean |gap| 18.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 7 of 41 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `gamma, max_steps`: gamma=1.0, max_steps=500 (max I 0.24); gamma=1.0, max_steps=1000 (max I 0.42); gamma=0.999, max_steps=500 (max I 1.34)
  - `init_q, max_steps`: init_q=-1.0, max_steps=1000 (max I 0.74); init_q=-1.0, max_steps=500 (max I 2.02)
  - `max_steps`: max_steps=2000 (max I 1.56); max_steps=500 (max I 2.5)
- Equally good values: `max_steps` in {500, 1000, 2000}

Notes:
- equally good values within one noise band (measured): max_steps in {500, 1000, 2000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000`, `gamma=1.0` | 5 | -4.4% | +11.1% | 7.7% |
| `max_steps=1000`, `init_q=-1.0` | 5 | -4.9% | +17.0% | 10.9% |
| `max_steps=500`, `init_q=-1.0` | 5 | -10.4% | +25.7% | 18.1% |
| `max_steps=2000` | 6 | -2.3% | -37.7% | 20.0% |
| `max_steps=500`, `gamma=1.0` | 5 | -4.6% | -43.4% | 24.0% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The argument --init_q expects a floating‑point number, but the supplied value 'zero' cannot be parsed as a float, causing the program to reject it; retried as `init_q=0`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
