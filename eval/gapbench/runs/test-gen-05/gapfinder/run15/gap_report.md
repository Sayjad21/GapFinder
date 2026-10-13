# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-13 20:58 · 73 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +989.9% | +24.4% | ±80.6% | `eps_start=0.02` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +989.9% → +24.4% · 12 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0039`, `B0040`, `B0041`, `B0042`, `B0043` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.02`
- Command:

  Replay: fork checkpoint `8726c426-ae77-4f12-807e-3f7547ddb30c` and run
  ```
  RUN_TAG=455a3c607384 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.02 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 21.5, 21.57, 45.63, 13.07, 22.24, 10.12; gap after +24.4%; result checkpoint `74b7f120-238a-4746-8c21-6b7531db9e25`
- Effect: candidate 21.54 minus naive 188.7 = -167.1, 95% bootstrap interval [-180.9, -133.5] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 188.7 over 5 runs; repeats: 184.5, 152.1, 197.6, 195.6, 188.7
- Spread: range 152.1 to 197.6, noise band ±13.95 (2 x MAD), CV 10.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +989.9% (noise band ±80.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +989.9% (it comes back)
- PASS · Held-out claim: C2: +1587.4% to +0.5% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.02`: no evidence mentions '0.02'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -167.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.1` (10.6 noise units, gap +135.7%); `eps_start=0.5` (4.1 noise units, gap +659.3%); `lr_schedule=inv` (1.95 noise units, gap +832.8%); `lr_schedule=linear` (1.56 noise units, gap +864.1%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_start=0.1`: this claim +33.2%, mean |gap| 17.2% (5 runs)
  - `lr_schedule=inv`, `eps_start=0.02`: this claim -34.4%, mean |gap| 17.2% (5 runs)
  - `eps_start=0.02`, `lr_schedule=linear`: this claim -40.4%, mean |gap| 20.5% (5 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.02` | 6 | +24.4% | +0.5% | 12.5% |
| `lr_schedule=inv`, `eps_start=0.1` | 5 | +33.2% | +1.1% | 17.2% |
| `lr_schedule=inv`, `eps_start=0.02` | 5 | -34.4% | +0.0% | 17.2% |
| `eps_start=0.02`, `lr_schedule=linear` | 5 | -40.4% | +0.5% | 20.5% |
| `lr_schedule=linear`, `eps_start=0.1` | 5 | +43.9% | +1.6% | 22.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`

## Provenance
- GapFinder commit: `c5b1a93e0b25688f10e132758f8a6371b4ebbf19` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `7e8e15007902d4b39f8940e3fb2a13a0e258c9d87b46215a72cd3b65ed9d57d9`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
