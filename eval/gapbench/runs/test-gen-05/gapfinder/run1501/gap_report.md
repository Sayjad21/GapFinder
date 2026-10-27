# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-15 19:14 · 81 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +954.0% | +6.3% | ±73.3% | `eps_start=0.0` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +954.0% → +6.3% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0020`, `B0021`, `B0033` (4 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.0`
- Command:

  Replay: fork checkpoint `034385d4-b6c8-4133-a96a-61d7aa1b45e3` and run
  ```
  RUN_TAG=7ceb02a0bcd4 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 37, 10.09, 15.04, 21.75; gap after +6.3%; result checkpoint `36cdac9e-9513-4b07-b5f9-353422684c4d`
- Effect: candidate 18.39 minus naive 182.5 = -164.1, 95% bootstrap interval [-179.6, -157.8] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 182.5 over 5 runs; repeats: 188.8, 180.6, 173.8, 195.1, 182.5
- Spread: range 173.8 to 195.1, noise band ±12.69 (2 x MAD), CV 4.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +954.0% (noise band ±73.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +954.0% (it comes back)
- PASS · Held-out claim: C2: +1383.5% to +2.5% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.0`: no evidence mentions '0.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -164.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.01` (12.83 noise units, gap +13.6%); `eps_start=0.2` (12.55 noise units, gap +34.1%); `eps_start=0.02` (11.86 noise units, gap +84.5%); `eps_start=0.1` (11.35 noise units, gap +122.1%); `eps_start=0.5` (6.08 noise units, gap +508.3%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_start=0.02`: this claim +6.6%, mean |gap| 4.7% (4 runs)
  - `eps_start=0.01`, `lr_schedule=linear`: this claim -9.7%, mean |gap| 5.1% (3 runs)
  - `eps_start=0.1`, `lr_schedule=inv`: this claim +11.3%, mean |gap| 5.9% (3 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.0` (reported)
- `eps_start=0.02`
- `eps_start=0.1`
- `eps_start=0.01, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.0, lr_schedule=inv`
- `eps_start=0.1, lr_schedule=linear`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.2, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 13 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_start, lr_schedule`: eps_start=0.1, lr_schedule=inv (max I 0.11); eps_start=0.01, lr_schedule=linear (max I 0.47); eps_start=0.0, lr_schedule=inv (max I 0.64); eps_start=0.1, lr_schedule=linear (max I 0.77); +4 more
  - `eps_start`: eps_start=0.02 (max I 0.43); eps_start=0.0 (max I 0.65)
- Equally good values: `eps_start` in {0.0, 0.01, 0.02, 0.1}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.0; eps_start=0.02; eps_start=0.1; eps_start=0.01, lr_schedule=linear; eps_start=0.1, lr_schedule=inv; eps_start=0.0, lr_schedule=inv; eps_start=0.1, lr_schedule=linear; eps_start=0.02, lr_schedule=linear; eps_start=0.2, lr_schedule=inv
- equally good values within one noise band (measured): eps_start in {0.0, 0.01, 0.02, 0.1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.0` | 4 | +6.3% | +2.5% | 4.4% |
| `eps_start=0.02` | 4 | +6.6% | +2.7% | 4.7% |
| `eps_start=0.01`, `lr_schedule=linear` | 3 | -9.7% | -0.5% | 5.1% |
| `eps_start=0.1`, `lr_schedule=inv` | 3 | +11.3% | +0.5% | 5.9% |
| `eps_start=0.1`, `lr_schedule=linear` | 3 | +19.2% | -1.1% | 10.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
