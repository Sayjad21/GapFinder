# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-14 21:42 · 113 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +977.8% | -3.6% | ±17.2% | `eps_start=0.1`, `lr_schedule=linear` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +977.8% → -3.6% · 32 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0061`, `B0088`, `B0089` (3 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Config: `lr_schedule` naive `const`, changed to `linear`
- Command:

  Replay: fork checkpoint `2b6ea1e6-b266-4988-ba0e-0d7f2552765a` and run
  ```
  RUN_TAG=775ed41007f4 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule linear --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 16.7, 31.54, 13.22; gap after -3.6%; result checkpoint `355a03bd-89a7-455b-a22e-16e981f7834c`
- Effect: candidate 16.7 minus naive 186.6 = -169.9, 95% bootstrap interval [-178.4, -153] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 186.6 over 5 runs; repeats: 185.1, 187.2, 186.6, 194.8, 182.9
- Spread: range 182.9 to 194.8, noise band ±2.97 (2 x MAD), CV 2.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +977.8% (noise band ±17.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +842.0% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +166.9% (it comes back)
- PASS · Held-out claim: C2: +1411.0% to +1.6% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=linear`: no evidence mentions 'linear'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -169.9 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.0` (55.23 noise units, gap +30.2%); `eps_start=0.02` (53.84 noise units, gap +54.1%); `eps_start=0.2` (48.01 noise units, gap +154.0%); `eps_start=0.5` (20.76 noise units, gap +621.6%); `lr_schedule=inv` (19.02 noise units, gap +651.4%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_start=0.1`: this claim -17.9%, mean |gap| 9.0% (3 runs)
  - `lr_schedule=inv`, `eps_start=0.02`: this claim -26.9%, mean |gap| 13.7% (3 runs)
  - `eps_start=0.0`, `lr_schedule=inv`: this claim -32.4%, mean |gap| 16.5% (3 runs)

### History matching (every measured configuration, all claims together)
- 6 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `eps_start, lr_schedule`: eps_start=0.0, lr_schedule=inv (max I 0.3); eps_start=0.02, lr_schedule=inv (max I 0.75); eps_start=0.1, lr_schedule=linear (max I 0.92); eps_start=0.1, lr_schedule=inv (max I 0.94); +2 more
- Equally good values: `lr_schedule` in {inv, linear}

Notes:
- equally good values within one noise band (measured): lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `eps_start=0.1` | 3 | -3.6% | +1.6% | 2.6% |
| `lr_schedule=inv`, `eps_start=0.1` | 3 | -17.9% | +0.0% | 9.0% |
| `lr_schedule=inv`, `eps_start=0.02` | 3 | -26.9% | -0.5% | 13.7% |
| `eps_start=0.0`, `lr_schedule=inv` | 3 | -32.4% | +0.5% | 16.5% |
| `eps_start=0.0` | 4 | +35.3% | +0.3% | 17.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
