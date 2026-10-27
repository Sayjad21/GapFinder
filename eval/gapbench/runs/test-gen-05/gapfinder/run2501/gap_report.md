# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-16 01:46 · 101 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +941.7% | +8.1% | ±145.2% | `eps_start=0.02` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +941.7% → +8.1% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0015`, `B0026`, `B0027`, `B0033`, `B0034`, `B0035` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.02`
- Command:

  Replay: fork checkpoint `25a9bb3e-eee4-41ff-8898-0a992b22c1a4` and run
  ```
  RUN_TAG=76ac4888901a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.02 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 16.24, 21.18, 31.05, 13.04, 9.98, 22.82; gap after +8.1%; result checkpoint `33f00c4c-b68c-44f6-9ee3-fc31c80323fe`
- Effect: candidate 18.71 minus naive 180.3 = -161.6, 95% bootstrap interval [-178.3, -146.2] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 180.3 over 5 runs; repeats: 200, 163.7, 192.9, 180.3, 176.2
- Spread: range 163.7 to 200, noise band ±25.13 (2 x MAD), CV 7.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +941.7% (noise band ±145.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +941.7% (it comes back)
- PASS · Held-out claim: C2: +1150.0% to +0.5% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.02`: no evidence mentions '0.02'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -161.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.01` (6.21 noise units, gap -40.7%); `eps_start=0.0` (6.16 noise units, gap +47.9%); `eps_start=0.1` (5.41 noise units, gap +156.7%); `eps_start=0.2` (3.99 noise units, gap +362.9%); `lr_schedule=inv` (1.48 noise units, gap +726.9%)
- Near alternatives (closest across all claims):
  - `eps_start=0.01`: this claim +23.1%, mean |gap| 12.2% (6 runs)
  - `eps_start=0.1`, `lr_schedule=linear`: this claim -25.6%, mean |gap| 13.1% (5 runs)
  - `eps_start=0.0`: this claim +26.1%, mean |gap| 13.9% (6 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.02` (reported)
- `eps_start=0.0`
- `eps_start=0.01`
- `eps_start=0.1`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=linear`
- `eps_start=0.01, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 13 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_start, lr_schedule`: eps_start=0.1, lr_schedule=linear (max I 0.05); eps_start=0.02, lr_schedule=linear (max I 0.39); eps_start=0.01, lr_schedule=linear (max I 0.54); eps_start=0.1, lr_schedule=inv (max I 0.57); +3 more
  - `eps_start`: eps_start=0.02 (max I 0.2); eps_start=0.0 (max I 0.36); eps_start=0.01 (max I 0.5)
- Equally good values: `eps_start` in {0.0, 0.01, 0.02, 0.1}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.02; eps_start=0.0; eps_start=0.01; eps_start=0.1; eps_start=0.02, lr_schedule=linear; eps_start=0.1, lr_schedule=linear; eps_start=0.01, lr_schedule=linear; eps_start=0.1, lr_schedule=inv
- equally good values within one noise band (measured): eps_start in {0.0, 0.01, 0.02, 0.1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.02` | 6 | +8.1% | +0.5% | 4.3% |
| `eps_start=0.01` | 6 | +23.1% | +1.4% | 12.2% |
| `eps_start=0.1`, `lr_schedule=linear` | 5 | -25.6% | +0.5% | 13.1% |
| `eps_start=0.0` | 6 | +26.1% | +1.6% | 13.9% |
| `lr_schedule=inv`, `eps_start=0.1` | 5 | +40.9% | +1.1% | 21.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
