# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-15 00:30 · 157 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +896.2% | +62.0% | ±53.3% | `eps_start=0.0` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +896.2% → +62.0% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0010`, `B0026`, `B0027`, `B0042`, `B0043`, `B0044` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.0`
- Command:

  Replay: fork checkpoint `858152fd-371c-42d7-8129-3ebdd1c84fc4` and run
  ```
  RUN_TAG=c353f29b132d "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 11.96, 19.91, 14.69, 38.74, 44.4, 36.2; gap after +62.0%; result checkpoint `a5fbfb73-8ff9-449a-9722-e0dd8797e62b`
- Effect: candidate 28.05 minus naive 172.4 = -144.4, 95% bootstrap interval [-154.4, -120.3] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 172.4 over 5 runs; repeats: 156.6, 173, 177.1, 172.4, 161.1
- Spread: range 156.6 to 177.1, noise band ±9.23 (2 x MAD), CV 5.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +896.2% (noise band ±53.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +896.2% (it comes back)
- PASS · Held-out claim: C2: +436.3% to +0.5% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.0`: no evidence mentions '0.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -144.4 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.02` (16.16 noise units, gap +34.7%); `eps_start=0.1` (12.51 noise units, gap +229.0%); `eps_start=0.5` (10.35 noise units, gap +344.5%); `eps_start=0.2` (10.35 noise units, gap +344.1%); `eps_start=0.8` (5.98 noise units, gap +577.5%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_start=0.02`, `lr_schedule=linear`: this claim -41.0%, mean |gap| 20.8% (5 runs)
  - `lr_schedule=linear`, `eps_start=0.0`: this claim -42.8%, mean |gap| 22.0% (5 runs)
  - `eps_start=0.02`, `lr_schedule=inv`: this claim -43.8%, mean |gap| 22.2% (5 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.0` (reported)
- `eps_start=0.02`
- `eps_start=0.1`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.02, lr_schedule=inv`
- `eps_start=0.1, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.0, lr_schedule=linear`
- `eps_start=0.2, lr_schedule=linear`

### History matching (every measured configuration, all claims together)
- 8 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `eps_start, lr_schedule`: eps_start=0.02, lr_schedule=linear (max I 0.48); eps_start=0.02, lr_schedule=inv (max I 0.91); eps_start=0.0, lr_schedule=linear (max I 0.91); eps_start=0.0, lr_schedule=inv (max I 1.12); +2 more
  - `eps_start`: eps_start=0.02 (max I 1.49); eps_start=0.0 (max I 1.88)
- Equally good values: `eps_start` in {0.0, 0.02}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.0; eps_start=0.02; eps_start=0.1; eps_start=0.02, lr_schedule=linear; eps_start=0.02, lr_schedule=inv; eps_start=0.1, lr_schedule=linear; eps_start=0.1, lr_schedule=inv; eps_start=0.0, lr_schedule=linear; eps_start=0.2, lr_schedule=linear
- equally good values within one noise band (measured): eps_start in {0.0, 0.02}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.02`, `lr_schedule=linear` | 5 | -41.0% | +0.5% | 20.8% |
| `lr_schedule=linear`, `eps_start=0.0` | 5 | -42.8% | +1.1% | 22.0% |
| `eps_start=0.02`, `lr_schedule=inv` | 5 | -43.8% | -0.5% | 22.2% |
| `lr_schedule=inv`, `eps_start=0.0` | 5 | -45.1% | +0.5% | 22.8% |
| `lr_schedule=inv`, `eps_start=0.1` | 5 | +49.7% | +1.6% | 25.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
