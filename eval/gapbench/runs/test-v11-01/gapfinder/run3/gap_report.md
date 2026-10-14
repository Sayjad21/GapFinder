# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 12:20 · 85 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -49.0% | -0.2% | ±3.4% | `max_steps=500` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -49.0% → -0.2% · 42 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0024`, `B0025`, `B0026` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `b2560f6a-d032-4bfb-8ee1-cc292c6ab989` and run
  ```
  RUN_TAG=ff7c70b39755 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 382.5, 337.4, 353.7, 351.4; gap after -0.2%; result checkpoint `d599870f-1541-4b6b-8b97-d89cbf1628a7`
- Effect: candidate 352.6 minus naive 180.4 = +172.1, 95% bootstrap interval [+155.4, +181.2] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 180.4 over 5 runs; repeats: 180.4, 168.4, 182.2, 172.8, 186.4
- Spread: range 168.4 to 186.4, noise band ±12 (2 x MAD), CV 4.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -49.0% (noise band ±3.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -49.0% (it comes back)
- PASS · Held-out claim: C2: +43.1% to +18.3% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +172.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (13.54 noise units, gap -3.0%); `max_steps=2000` (9.13 noise units, gap +18.0%)
- Near alternatives (closest across all claims):
  - `init_q=1.0`, `max_steps=500`: this claim -6.7%, mean |gap| 7.0% (3 runs)
  - `gamma=1.0`, `max_steps=500`: this claim +7.4%, mean |gap| 10.7% (3 runs)
  - `max_steps=1000`, `init_q=1.0`: this claim -0.3%, mean |gap| 21.5% (3 runs)

### History matching (every measured configuration, all claims together)
- 7 of 41 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `max_steps`: max_steps=500 (max I 0.34); max_steps=2000 (max I 0.9)
  - `gamma, max_steps`: gamma=1.0, max_steps=500 (max I 1.02); gamma=0.999, max_steps=500 (max I 1.91)
  - `init_q, max_steps`: init_q=1.0, max_steps=500 (max I 1.92); init_q=1.0, max_steps=1000 (max I 1.96); init_q=-1.0, max_steps=500 (max I 2.83)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `init_q=1.0`, `max_steps=500` | 3 | -6.7% | +7.3% | 7.0% |
| `max_steps=500` | 4 | -0.2% | +18.3% | 9.3% |
| `gamma=1.0`, `max_steps=500` | 3 | +7.4% | +14.1% | 10.7% |
| `max_steps=1000`, `init_q=1.0` | 3 | -0.3% | -42.8% | 21.5% |
| `max_steps=1000`, `gamma=0.999` | 3 | +41.8% | +28.5% | 35.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The program expects a numeric float for --init_q; the supplied string 'zero' cannot be parsed as a float, causing the argument parser to reject it; retried as `init_q=0`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0527, sandbox reported $0.0000 (total $0.0527; this search; ledger extraction is included only if it shared the search's router)
