# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-14 23:25 · 145 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +999.7% | +36.4% | ±97.5% | `eps_start=0.02` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +999.7% → +36.4% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0013`, `B0026`, `B0027`, `B0034`, `B0035`, `B0036` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.02`
- Command:

  Replay: fork checkpoint `b84075c0-0c6d-435b-a9ca-51dff1146a1c` and run
  ```
  RUN_TAG=18490bc00c35 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.02 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 9.795, 18.99, 9.62, 34.42, 28.23, 38; gap after +36.4%; result checkpoint `831f77e6-80f1-44b4-bb3b-4c09060292f4`
- Effect: candidate 23.61 minus naive 190.4 = -166.7, 95% bootstrap interval [-179.5, -140.5] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 190.4 over 5 runs; repeats: 171.6, 171.4, 198.8, 190.4, 197
- Spread: range 171.4 to 198.8, noise band ±16.87 (2 x MAD), CV 7.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +999.7% (noise band ±97.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +999.7% (it comes back)
- PASS · Held-out claim: C2: +1500.0% to +1.1% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.02`: no evidence mentions '0.02'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -166.7 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.0` (9.5 noise units, gap +73.8%); `eps_start=0.2` (9.4 noise units, gap +83.2%); `eps_start=0.01` (7.9 noise units, gap +229.8%); `eps_start=0.1` (6.57 noise units, gap +359.3%); `eps_start=0.5` (3.65 noise units, gap +644.3%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_start=0.1`: this claim +21.9%, mean |gap| 11.8% (5 runs)
  - `eps_start=0.01`: this claim -29.9%, mean |gap| 15.3% (6 runs)
  - `lr_schedule=inv`, `eps_start=0.0`: this claim -42.1%, mean |gap| 21.3% (5 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.02` (reported)
- `eps_start=0.0`
- `eps_start=0.01`
- `eps_start=0.01, lr_schedule=inv`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.0, lr_schedule=inv`
- `eps_start=0.1, lr_schedule=linear`

### History matching (every measured configuration, all claims together)
- 12 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_start`: eps_start=0.0 (max I 0.06); eps_start=0.01 (max I 0.46); eps_start=0.02 (max I 0.7)
  - `eps_start, lr_schedule`: eps_start=0.02, lr_schedule=linear (max I 0.15); eps_start=0.01, lr_schedule=inv (max I 0.33); eps_start=0.0, lr_schedule=inv (max I 0.6); eps_start=0.02, lr_schedule=inv (max I 0.66); +3 more
- Equally good values: `eps_start` in {0.0, 0.01, 0.02}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.02; eps_start=0.0; eps_start=0.01; eps_start=0.01, lr_schedule=inv; eps_start=0.02, lr_schedule=linear; eps_start=0.1, lr_schedule=inv; eps_start=0.0, lr_schedule=inv; eps_start=0.1, lr_schedule=linear
- equally good values within one noise band (measured): eps_start in {0.0, 0.01, 0.02}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_start=0.1` | 5 | +21.9% | +1.6% | 11.8% |
| `eps_start=0.01` | 6 | -29.9% | +0.8% | 15.3% |
| `eps_start=0.02` | 6 | +36.4% | +1.1% | 18.7% |
| `lr_schedule=inv`, `eps_start=0.0` | 5 | -42.1% | -0.5% | 21.3% |
| `lr_schedule=linear`, `eps_start=0.02` | 5 | -42.8% | +0.0% | 21.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
