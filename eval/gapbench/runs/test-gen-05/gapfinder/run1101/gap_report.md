# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-15 00:30 · 139 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +990.3% | +7.3% | ±83.5% | `eps_start=0.1`, `lr_schedule=linear` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +990.3% → +7.3% · 32 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0051`, `B0086`, `B0087`, `B0088`, `B0089` (5 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Config: `lr_schedule` naive `const`, changed to `linear`
- Command:

  Replay: fork checkpoint `60860441-0468-433a-92c9-4afd16ae78e9` and run
  ```
  RUN_TAG=af0bc2bae00c "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule linear --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 29.16, 16.82, 16.9, 18.58, 29.96; gap after +7.3%; result checkpoint `18e4d09a-eb62-4fd5-a00b-39eb3977fb98`
- Effect: candidate 18.58 minus naive 188.7 = -170.1, 95% bootstrap interval [-177.1, -146.6] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 188.7 over 5 runs; repeats: 181.5, 188.7, 195.7, 198.1, 165.3
- Spread: range 165.3 to 198.1, noise band ±14.45 (2 x MAD), CV 7.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +990.3% (noise band ±83.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +824.0% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +187.3% (it comes back)
- PASS · Held-out claim: C2: +1495.1% to +1.6% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=linear`: no evidence mentions 'linear'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -170.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.01` (11.6 noise units, gap +21.5%); `eps_start=0.0` (11.33 noise units, gap -44.7%); `eps_start=0.02` (8.78 noise units, gap +257.0%); `eps_start=0.2` (8.75 noise units, gap +259.8%); `eps_start=0.5` (4.58 noise units, gap +607.9%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `eps_start=0.01`: this claim -4.1%, mean |gap| 2.6% (5 runs)
  - `eps_start=0.02`, `lr_schedule=inv`: this claim +4.7%, mean |gap| 2.6% (5 runs)
  - `eps_start=0.0`: this claim -15.2%, mean |gap| 7.9% (6 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.1, lr_schedule=linear` (reported)
- `eps_start=0.0`
- `eps_start=0.02`
- `eps_start=0.02, lr_schedule=inv`
- `eps_start=0.01, lr_schedule=linear`
- `eps_start=0.0, lr_schedule=linear`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.01, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 13 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_start`: eps_start=0.0 (max I 0.03); eps_start=0.01 (max I 0.36)
  - `eps_start, lr_schedule`: eps_start=0.01, lr_schedule=linear (max I 0.03); eps_start=0.02, lr_schedule=inv (max I 0.05); eps_start=0.02, lr_schedule=linear (max I 0.07); eps_start=0.0, lr_schedule=linear (max I 0.11); +4 more
- Equally good values: `eps_start` in {0.0, 0.01, 0.02, 0.1, 0.2}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.1, lr_schedule=linear; eps_start=0.0; eps_start=0.02; eps_start=0.02, lr_schedule=inv; eps_start=0.01, lr_schedule=linear; eps_start=0.0, lr_schedule=linear; eps_start=0.02, lr_schedule=linear; eps_start=0.01, lr_schedule=inv
- equally good values within one noise band (measured): eps_start in {0.0, 0.01, 0.02, 0.1, 0.2}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `eps_start=0.01` | 5 | -4.1% | -1.1% | 2.6% |
| `eps_start=0.02`, `lr_schedule=inv` | 5 | +4.7% | +0.5% | 2.6% |
| `lr_schedule=linear`, `eps_start=0.1` | 5 | +7.3% | +1.6% | 4.5% |
| `eps_start=0.0` | 6 | -15.2% | +0.5% | 7.9% |
| `eps_start=0.01` | 3 | +21.5% | +0.5% | 11.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
