# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-14 21:42 · 158 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +1004.0% | -6.4% | ±85.7% | `eps_start=0.0` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +1004.0% → -6.4% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0023`, `B0024`, `B0025`, `B0026`, `B0027` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.0`
- Command:

  Replay: fork checkpoint `a387320e-51a9-4707-a1fc-7235060323e7` and run
  ```
  RUN_TAG=6ef0b55968d6 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 13.63, 10.07, 9.72, 18.79, 42.98, 30.11; gap after -6.4%; result checkpoint `bb808b1b-b28e-4de5-86d7-44bff96c131c`
- Effect: candidate 16.21 minus naive 191.1 = -174.9, 95% bootstrap interval [-181.4, -143.6] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 191.1 over 5 runs; repeats: 167.9, 180.5, 198.5, 191.4, 191.1
- Spread: range 167.9 to 198.5, noise band ±14.84 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +1004.0% (noise band ±85.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +1004.0% (it comes back)
- PASS · Held-out claim: C2: +1392.3% to +1.9% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.0`: no evidence mentions '0.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -174.9 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.02` (11.48 noise units, gap -19.8%); `eps_start=0.01` (10.51 noise units, gap +102.6%); `eps_start=0.1` (8.48 noise units, gap +277.2%); `eps_start=0.2` (8.42 noise units, gap +282.4%); `lr_schedule=inv` (6.25 noise units, gap +468.0%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_start=0.0`, `lr_schedule=linear`: this claim -22.2%, mean |gap| 11.4% (5 runs)
  - `lr_schedule=inv`, `eps_start=0.01`: this claim +21.9%, mean |gap| 11.5% (5 runs)
  - `lr_schedule=linear`, `eps_start=0.1`: this claim +27.7%, mean |gap| 14.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 12 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_start, lr_schedule`: eps_start=0.01, lr_schedule=inv (max I 0.26); eps_start=0.0, lr_schedule=linear (max I 0.51); eps_start=0.01, lr_schedule=linear (max I 0.52); eps_start=0.0, lr_schedule=inv (max I 0.85); +3 more
  - `eps_start`: eps_start=0.0 (max I 0.48); eps_start=0.02 (max I 0.91); eps_start=0.01 (max I 1.25)
- Equally good values: `eps_start` in {0.0, 0.01, 0.02}

Notes:
- equally good values within one noise band (measured): eps_start in {0.0, 0.01, 0.02}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.0` | 6 | -6.4% | +1.9% | 4.1% |
| `eps_start=0.0`, `lr_schedule=linear` | 5 | -22.2% | +0.5% | 11.4% |
| `lr_schedule=inv`, `eps_start=0.01` | 5 | +21.9% | +1.1% | 11.5% |
| `lr_schedule=linear`, `eps_start=0.1` | 5 | +27.7% | +0.5% | 14.1% |
| `eps_start=0.02` | 6 | +35.4% | +0.5% | 18.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
