# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-14 00:51 · 73 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +979.2% | +41.1% | ±34.8% | `eps_start=0.1` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +979.2% → +41.1% · 20 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0008`, `B0020`, `B0021`, `B0022` (4 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Command:

  Replay: fork checkpoint `72dc5288-ac7c-4332-b6b0-a18d8c857d06` and run
  ```
  RUN_TAG=feebc4713512 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 14.13, 34.71, 50.66, 13.03; gap after +41.1%; result checkpoint `ddfcba84-7be9-4188-8c01-90586dcab4d4`
- Effect: candidate 24.42 minus naive 186.8 = -162.4, 95% bootstrap interval [-174.8, -127.3] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 186.8 over 5 runs; repeats: 186.8, 187.4, 183.8, 190.6, 167.8
- Spread: range 167.8 to 190.6, noise band ±6.02 (2 x MAD), CV 4.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +979.2% (noise band ±34.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +979.2% (it comes back)
- PASS · Held-out claim: C2: +1383.5% to +1.1% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -162.4 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.0` (28.04 noise units, gap -4.0%); `lr_schedule=inv` (9.49 noise units, gap +649.2%); `eps_start=0.5` (8.41 noise units, gap +686.9%); `eps_start=0.8` (6 noise units, gap +770.5%); `lr_schedule=linear` (1.81 noise units, gap +916.3%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `eps_start=0.1`: this claim -17.3%, mean |gap| 9.5% (3 runs)
  - `lr_schedule=linear`, `eps_start=0.0`: this claim -43.5%, mean |gap| 21.8% (3 runs)
  - `eps_start=0.0`: this claim +43.7%, mean |gap| 22.3% (4 runs)

### History matching (every measured configuration, all claims together)
- 6 of 20 tested configurations fit every claim within 3 sigma
- Equally good values: `eps_start` in {0.0, 0.1}

Notes:
- equally good values within one noise band (measured): eps_start in {0.0, 0.1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `eps_start=0.1` | 3 | -17.3% | +1.6% | 9.5% |
| `eps_start=0.1` | 4 | +41.1% | +1.1% | 21.1% |
| `lr_schedule=linear`, `eps_start=0.0` | 3 | -43.5% | +0.0% | 21.8% |
| `eps_start=0.0` | 4 | +43.7% | +0.8% | 22.3% |
| `lr_schedule=inv`, `eps_start=0.0` | 3 | -45.3% | +0.5% | 22.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`

## Provenance
- GapFinder commit: `e89cebde86417c8c65704c51b94620ddb20a97ce` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fedcbdf1b57461a1273eeb81ccb09c30931e58de34a306249ffd0422bbf51ae6`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
