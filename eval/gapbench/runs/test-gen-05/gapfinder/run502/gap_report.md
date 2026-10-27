# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-14 22:15 · 102 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +908.6% | +2.7% | ±66.1% | `eps_start=0.0` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +908.6% → +2.7% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0010`, `B0030`, `B0031`, `B0032` (4 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.0`
- Command:

  Replay: fork checkpoint `3bf73c51-eed1-4a41-bbb8-7b0500d03aad` and run
  ```
  RUN_TAG=a0b3e06fa08e "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 20.82, 10.3, 14.74, 61.76; gap after +2.7%; result checkpoint `46bbf0d2-2261-430c-b857-b1f85b0d582e`
- Effect: candidate 17.78 minus naive 174.6 = -156.8, 95% bootstrap interval [-171.3, -109.4] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 174.6 over 5 runs; repeats: 174.6, 168.9, 176.9, 188.7, 166.5
- Spread: range 166.5 to 188.7, noise band ±11.44 (2 x MAD), CV 5.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +908.6% (noise band ±66.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +908.6% (it comes back)
- PASS · Held-out claim: C2: +574.2% to +0.3% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.0`: no evidence mentions '0.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -156.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.02` (13.65 noise units, gap -6.4%); `eps_start=0.1` (13.14 noise units, gap +40.5%); `eps_start=0.2` (9.83 noise units, gap +259.1%); `eps_start=0.5` (6.6 noise units, gap +472.1%); `eps_start=0.8` (3.93 noise units, gap +648.9%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_start=0.02`, `lr_schedule=inv`: this claim -10.3%, mean |gap| 5.1% (3 runs)
  - `eps_start=0.02`: this claim -11.6%, mean |gap| 5.9% (4 runs)
  - `lr_schedule=inv`, `eps_start=0.0`: this claim -13.2%, mean |gap| 6.6% (3 runs)

### Equally good configurations
The target claim can't tell these 10 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.0` (reported)
- `eps_start=0.02`
- `eps_start=0.1`
- `eps_start=0.0, lr_schedule=inv`
- `eps_start=0.02, lr_schedule=inv`
- `eps_start=0.0, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.1, lr_schedule=linear`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.2, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 9 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `eps_start`: eps_start=0.02 (max I 0.01); eps_start=0.0 (max I 1.59); eps_start=0.1 (max I 2.47)
  - `eps_start, lr_schedule`: eps_start=0.02, lr_schedule=inv (max I 0.1); eps_start=0.0, lr_schedule=inv (max I 0.15); eps_start=0.0, lr_schedule=linear (max I 0.34); eps_start=0.1, lr_schedule=inv (max I 0.93); +2 more
- Equally good values: `eps_start` in {0.0, 0.02, 0.1}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.0; eps_start=0.02; eps_start=0.1; eps_start=0.0, lr_schedule=inv; eps_start=0.02, lr_schedule=inv; eps_start=0.0, lr_schedule=linear; eps_start=0.1, lr_schedule=inv; eps_start=0.1, lr_schedule=linear; eps_start=0.02, lr_schedule=linear; eps_start=0.2, lr_schedule=inv
- equally good values within one noise band (measured): eps_start in {0.0, 0.02, 0.1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.0` | 4 | +2.7% | +0.3% | 1.5% |
| `eps_start=0.02`, `lr_schedule=inv` | 3 | -10.3% | +0.0% | 5.1% |
| `eps_start=0.02` | 4 | -11.6% | +0.3% | 5.9% |
| `lr_schedule=inv`, `eps_start=0.0` | 3 | -13.2% | +0.0% | 6.6% |
| `lr_schedule=inv`, `eps_start=0.1` | 3 | +13.5% | +1.1% | 7.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
