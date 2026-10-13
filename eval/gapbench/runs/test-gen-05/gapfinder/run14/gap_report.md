# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-14 00:27 · 58 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +905.9% | +33.1% | ±133.2% | `eps_start=0.0` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +905.9% → +33.1% · 12 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0019`, `B0020`, `B0021`, `B0022`, `B0023` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.0`
- Command:

  Replay: fork checkpoint `d4950702-cfa7-4ad8-9b4c-1c35bfd8e75c` and run
  ```
  RUN_TAG=22e69ed538db "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 20.03, 22.6, 23.5, 12.02, 42.09, 25.82; gap after +33.1%; result checkpoint `6704535b-d89d-4546-9c97-3b8c89c9156c`
- Effect: candidate 23.05 minus naive 174.1 = -151.1, 95% bootstrap interval [-167, -134.3] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 174.1 over 5 runs; repeats: 162.6, 164, 174.1, 189.5, 187.8
- Spread: range 162.6 to 189.5, noise band ±23.06 (2 x MAD), CV 7.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +905.9% (noise band ±133.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +905.9% (it comes back)
- PASS · Held-out claim: C2: +531.9% to +0.5% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.0`: no evidence mentions '0.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -151.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.02` (6.19 noise units, gap +81.9%); `eps_start=0.1` (5.1 noise units, gap +226.7%); `eps_start=0.5` (3.41 noise units, gap +451.7%); `lr_schedule=inv` (2.31 noise units, gap +597.8%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_start=0.0`: this claim -6.6%, mean |gap| 3.6% (5 runs)
  - `lr_schedule=linear`, `eps_start=0.02`: this claim +12.0%, mean |gap| 6.0% (5 runs)
  - `eps_start=0.02`: this claim +31.9%, mean |gap| 16.3% (6 runs)

Notes:
- equally good values within one noise band (measured): eps_start in {0.0, 0.02, 0.1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_start=0.0` | 5 | -6.6% | +0.5% | 3.6% |
| `lr_schedule=linear`, `eps_start=0.02` | 5 | +12.0% | +0.0% | 6.0% |
| `eps_start=0.02` | 6 | +31.9% | +0.8% | 16.3% |
| `eps_start=0.0` | 6 | +33.1% | +0.5% | 16.8% |
| `eps_start=0.0`, `lr_schedule=linear` | 5 | -44.6% | +0.5% | 22.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `out`

## Provenance
- GapFinder commit: `ab5d0e01d517ea012f76706719410d70d422f3f9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fedcbdf1b57461a1273eeb81ccb09c30931e58de34a306249ffd0422bbf51ae6`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
