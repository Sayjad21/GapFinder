# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-14 00:50 · 103 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +963.7% | -7.2% | ±37.3% | `eps_start=0.0` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +963.7% → -7.2% · 20 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0019`, `B0020`, `B0021`, `B0022`, `B0023` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.0`
- Command:

  Replay: fork checkpoint `0fe6268e-0615-458e-80f4-c800df672dc7` and run
  ```
  RUN_TAG=f2fd81a11849 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 13.83, 30.59, 18.29, 9.8, 32.16, 10.12; gap after -7.2%; result checkpoint `6a6341b3-84de-4dee-bd87-746c0467876c`
- Effect: candidate 16.06 minus naive 184.1 = -168.1, 95% bootstrap interval [-177.4, -148] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 184.1 over 5 runs; repeats: 181, 184.1, 187.4, 194.3, 168.7
- Spread: range 168.7 to 194.3, noise band ±6.46 (2 x MAD), CV 5.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +963.7% (noise band ±37.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +963.7% (it comes back)
- PASS · Held-out claim: C2: +1342.3% to +1.6% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.0`: no evidence mentions '0.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -168.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.02` (24.74 noise units, gap -40.4%); `eps_start=0.1` (22.4 noise units, gap +127.7%); `eps_start=0.5` (11.1 noise units, gap +549.6%); `lr_schedule=inv` (9.66 noise units, gap +603.1%); `lr_schedule=linear` (3.07 noise units, gap +849.2%)
- Near alternatives (closest across all claims):
  - `eps_start=0.1`, `lr_schedule=linear`: this claim +5.3%, mean |gap| 2.7% (5 runs)
  - `eps_start=0.0`, `lr_schedule=linear`: this claim -21.4%, mean |gap| 11.0% (5 runs)
  - `lr_schedule=inv`, `eps_start=0.02`: this claim -22.4%, mean |gap| 11.2% (5 runs)

### History matching (every measured configuration, all claims together)
- 8 of 20 tested configurations fit every claim within 3 sigma
- Equally good values: `eps_start` in {0.0, 0.02}

Notes:
- equally good values within one noise band (measured): eps_start in {0.0, 0.02}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.1`, `lr_schedule=linear` | 5 | +5.3% | +0.0% | 2.7% |
| `eps_start=0.0` | 6 | -7.2% | +1.6% | 4.4% |
| `eps_start=0.0`, `lr_schedule=linear` | 5 | -21.4% | +0.5% | 11.0% |
| `lr_schedule=inv`, `eps_start=0.02` | 5 | -22.4% | +0.0% | 11.2% |
| `lr_schedule=inv`, `eps_start=0.1` | 5 | +24.2% | +1.1% | 12.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `out`

## Provenance
- GapFinder commit: `ee5bfaf3f91999664f6df4e7df12a48c78c40f73` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fedcbdf1b57461a1273eeb81ccb09c30931e58de34a306249ffd0422bbf51ae6`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
