# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-14 00:28 · 49 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +966.1% | +10.9% | ±45.7% | `eps_start=0.02` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +966.1% → +10.9% · 12 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0029`, `B0030`, `B0031` (4 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.02`
- Command:

  Replay: fork checkpoint `4cfadff7-a9ef-4fd5-873d-3220234756e8` and run
  ```
  RUN_TAG=42b68c394f04 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.02 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 15.97, 10.62, 27.91, 22.42; gap after +10.9%; result checkpoint `a60727c9-8f54-4527-8bfd-b4634b3049bb`
- Effect: candidate 19.2 minus naive 184.5 = -165.3, 95% bootstrap interval [-178.8, -155.3] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 184.5 over 5 runs; repeats: 192.2, 184.5, 180.6, 193.7, 182.9
- Spread: range 180.6 to 193.7, noise band ±7.91 (2 x MAD), CV 3.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +966.1% (noise band ±45.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +966.1% (it comes back)
- PASS · Held-out claim: C2: +1401.1% to +0.8% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.02`: no evidence mentions '0.02'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -165.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (12.5 noise units, gap +394.7%); `eps_start=0.1` (12.17 noise units, gap +410.1%); `lr_schedule=inv` (6.34 noise units, gap +676.3%); `lr_schedule=linear` (2.42 noise units, gap +855.7%); `eps_start=0.8` (1.42 noise units, gap +901.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_start=0.02`: this claim -7.0%, mean |gap| 4.6% (3 runs)
  - `lr_schedule=linear`, `eps_start=0.02`: this claim -43.6%, mean |gap| 22.6% (3 runs)
  - `eps_start=0.1`: this claim +177.5%, mean |gap| 90.1% (4 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_start=0.02` | 3 | -7.0% | -2.2% | 4.6% |
| `eps_start=0.02` | 4 | +10.9% | +0.8% | 5.9% |
| `lr_schedule=linear`, `eps_start=0.02` | 3 | -43.6% | -1.6% | 22.6% |
| `eps_start=0.1` | 4 | +177.5% | +2.7% | 90.1% |
| `lr_schedule=inv`, `eps_start=0.5` | 3 | +331.2% | +37.9% | 184.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`

## Provenance
- GapFinder commit: `ab5d0e01d517ea012f76706719410d70d422f3f9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fedcbdf1b57461a1273eeb81ccb09c30931e58de34a306249ffd0422bbf51ae6`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
