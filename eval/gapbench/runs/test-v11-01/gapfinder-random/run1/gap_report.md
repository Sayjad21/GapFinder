# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 11:06 · 98 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -48.7% | -6.3% | ±4.3% | `max_steps=1000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -48.7% → -6.3% · 46 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0018`, `B0030`, `B0031`, `B0032`, `B0033`, `B0034` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `bbd6efe9-e080-4943-a8f7-8b6cbfddb23b` and run
  ```
  RUN_TAG=3dee444b1ac0 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 313.1, 287.5, 393.3, 359.5, 349, 192.3; gap after -6.3%; result checkpoint `d436587f-6a14-477c-8ec3-211460d8d9e8`
- Effect: candidate 331.1 minus naive 181.5 = +149.6, 95% bootstrap interval [+50.75, +200.7] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 181.5 over 5 runs; repeats: 172.6, 183.2, 196.4, 173.8, 181.5
- Spread: range 172.6 to 196.4, noise band ±15.31 (2 x MAD), CV 5.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -48.7% (noise band ±4.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -48.7% (it comes back)
- PASS · Held-out claim: C2: +96.0% to -12.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +149.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (8.61 noise units, gap -11.4%); `max_steps=2000` (3.29 noise units, gap -34.4%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`, `gamma=0.999`: this claim +7.2%, mean |gap| 11.4% (5 runs)
  - `max_steps=2000`: this claim -2.4%, mean |gap| 25.9% (6 runs)
  - `max_steps=500`: this claim -8.5%, mean |gap| 28.9% (6 runs)

### History matching (every measured configuration, all claims together)
- 6 of 46 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `gamma, max_steps`: gamma=0.999, max_steps=1000 (max I 0.71); gamma=1.0, max_steps=500 (max I 1.7); gamma=0.999, max_steps=500 (max I 2.1)
  - `max_steps`: max_steps=1000 (max I 2.02); max_steps=500 (max I 2.08); max_steps=2000 (max I 2.08)
- Equally good values: `max_steps` in {500, 1000, 2000}

Notes:
- equally good values within one noise band (measured): max_steps in {500, 1000, 2000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 6 | -6.3% | -12.1% | 9.2% |
| `max_steps=1000`, `gamma=0.999` | 5 | +7.2% | +15.6% | 11.4% |
| `max_steps=2000` | 6 | -2.4% | +49.4% | 25.9% |
| `max_steps=500` | 6 | -8.5% | +49.2% | 28.9% |
| `max_steps=1000`, `gamma=1.0` | 5 | +29.7% | +56.9% | 43.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
