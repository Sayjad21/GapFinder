# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-15 20:55 · 102 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +881.3% | -11.6% | ±141.7% | `eps_start=0.0` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +881.3% → -11.6% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0020`, `B0021`, `B0035`, `B0036`, `B0037` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.0`
- Command:

  Replay: fork checkpoint `9f31bfde-a3d5-45f6-970c-780ec44a54d8` and run
  ```
  RUN_TAG=9d437892e537 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 14.11, 15.48, 10.34, 15.12, 19, 29.2; gap after -11.6%; result checkpoint `e04e06f5-bb15-4b07-94d7-81d395e84f6d`
- Effect: candidate 15.3 minus naive 169.9 = -154.6, 95% bootstrap interval [-179.9, -140.2] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 169.9 over 5 runs; repeats: 197.5, 169.9, 197.8, 157.6, 166.5
- Spread: range 157.6 to 197.8, noise band ±24.52 (2 x MAD), CV 10.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +881.3% (noise band ±141.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +881.3% (it comes back)
- PASS · Held-out claim: C2: +450.0% to +1.1% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.0`: no evidence mentions '0.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -154.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.01` (6.06 noise units, gap -23.6%); `eps_start=0.02` (5.93 noise units, gap +41.2%); `eps_start=0.1` (4.03 noise units, gap +310.1%); `eps_start=0.2` (3.46 noise units, gap +391.8%); `eps_start=0.5` (1.57 noise units, gap +659.0%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `eps_start=0.1`: this claim -7.3%, mean |gap| 3.9% (5 runs)
  - `lr_schedule=linear`, `eps_start=0.01`: this claim -9.0%, mean |gap| 4.5% (5 runs)
  - `eps_start=0.01`: this claim -15.4%, mean |gap| 8.1% (6 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.0` (reported)
- `eps_start=0.01`
- `eps_start=0.02`
- `eps_start=0.01, lr_schedule=linear`
- `eps_start=0.02, lr_schedule=inv`
- `eps_start=0.1, lr_schedule=linear`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.2, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 15 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_start`: eps_start=0.0 (max I 0.01); eps_start=0.01 (max I 0.26); eps_start=0.02 (max I 0.56)
  - `eps_start, lr_schedule`: eps_start=0.1, lr_schedule=linear (max I 0.05); eps_start=0.01, lr_schedule=linear (max I 0.14); eps_start=0.02, lr_schedule=inv (max I 0.22); eps_start=0.02, lr_schedule=linear (max I 0.23); +3 more
- Equally good values: `eps_start` in {0.0, 0.01, 0.02, 0.1}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.0; eps_start=0.01; eps_start=0.02; eps_start=0.01, lr_schedule=linear; eps_start=0.02, lr_schedule=inv; eps_start=0.1, lr_schedule=linear; eps_start=0.02, lr_schedule=linear; eps_start=0.1, lr_schedule=inv; eps_start=0.2, lr_schedule=inv
- equally good values within one noise band (measured): eps_start in {0.0, 0.01, 0.02, 0.1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `eps_start=0.1` | 5 | -7.3% | +0.5% | 3.9% |
| `lr_schedule=linear`, `eps_start=0.01` | 5 | -9.0% | +0.0% | 4.5% |
| `eps_start=0.0` | 6 | -11.6% | +1.1% | 6.4% |
| `eps_start=0.01` | 6 | -15.4% | +0.8% | 8.1% |
| `lr_schedule=linear`, `eps_start=0.02` | 5 | +19.8% | +0.5% | 10.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
