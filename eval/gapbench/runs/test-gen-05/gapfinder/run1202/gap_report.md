# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-15 00:49 · 174 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +958.5% | +98.9% | ±28.3% | `eps_start=0.02` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +958.5% → +98.9% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0014`, `B0034`, `B0035`, `B0042`, `B0043`, `B0044` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.02`
- Command:

  Replay: fork checkpoint `8e06d673-2ab6-480e-b02b-21bedb389827` and run
  ```
  RUN_TAG=5be1f4a4322f "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.02 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 43.17, 39.79, 10.02, 9.915, 56.38, 29.07; gap after +98.9%; result checkpoint `98585cff-54d0-4fe8-bc4a-7773bc9e6ec2`
- Effect: candidate 34.43 minus naive 183.2 = -148.8, 95% bootstrap interval [-171.1, -116.3] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 183.2 over 5 runs; repeats: 184.9, 185.7, 151.5, 183.2, 159.9
- Spread: range 151.5 to 185.7, noise band ±4.9 (2 x MAD), CV 9.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +958.5% (noise band ±28.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +958.5% (it comes back)
- PASS · Held-out claim: C2: +438.5% to +0.5% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.02`: no evidence mentions '0.02'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -148.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.0` (32.35 noise units, gap -42.8%); `eps_start=0.1` (31.81 noise units, gap +57.9%); `eps_start=0.2` (23.86 noise units, gap +282.9%); `lr_schedule=inv` (12.23 noise units, gap +612.2%); `eps_start=0.5` (9.63 noise units, gap +685.7%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_start=0.1`, `lr_schedule=linear`: this claim +3.2%, mean |gap| 1.9% (5 runs)
  - `lr_schedule=inv`, `eps_start=0.1`: this claim -11.2%, mean |gap| 6.2% (5 runs)
  - `eps_start=0.0`: this claim -42.0%, mean |gap| 21.3% (6 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.02` (reported)
- `eps_start=0.0`
- `eps_start=0.1`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.02, lr_schedule=inv`
- `eps_start=0.1, lr_schedule=linear`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.2, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 11 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_start, lr_schedule`: eps_start=0.1, lr_schedule=inv (max I 0.14); eps_start=0.02, lr_schedule=inv (max I 0.25); eps_start=0.1, lr_schedule=linear (max I 0.3); eps_start=0.02, lr_schedule=linear (max I 0.55); +3 more
  - `eps_start`: eps_start=0.0 (max I 0.24); eps_start=0.02 (max I 1.4); eps_start=0.1 (max I 1.51)
- Equally good values: `eps_start` in {0.0, 0.02, 0.1}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.02; eps_start=0.0; eps_start=0.1; eps_start=0.1, lr_schedule=inv; eps_start=0.02, lr_schedule=inv; eps_start=0.1, lr_schedule=linear; eps_start=0.02, lr_schedule=linear; eps_start=0.2, lr_schedule=inv
- equally good values within one noise band (measured): eps_start in {0.0, 0.02, 0.1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.1`, `lr_schedule=linear` | 5 | +3.2% | +0.5% | 1.9% |
| `lr_schedule=inv`, `eps_start=0.1` | 5 | -11.2% | +1.1% | 6.2% |
| `eps_start=0.0` | 6 | -42.0% | +0.5% | 21.3% |
| `lr_schedule=inv`, `eps_start=0.02` | 5 | -42.7% | -0.5% | 21.6% |
| `eps_start=0.02`, `lr_schedule=linear` | 5 | -42.9% | +0.5% | 21.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
