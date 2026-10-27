# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-16 01:46 · 99 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +941.4% | -5.5% | ±41.9% | `eps_start=0.1`, `lr_schedule=inv` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +941.4% → -5.5% · 32 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0059`, `B0074`, `B0091` (3 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `d45f2ffe-0ce5-464e-a8ad-69885fe01e17` and run
  ```
  RUN_TAG=55e8ec1e6c70 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 15.82, 18, 16.36; gap after -5.5%; result checkpoint `66869646-6afc-4353-9f73-835a9606494d`
- Effect: candidate 16.36 minus naive 180.3 = -163.9, 95% bootstrap interval [-176.6, -160.2] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 180.3 over 5 runs; repeats: 180.3, 191.1, 179.1, 176.6, 193.9
- Spread: range 176.6 to 193.9, noise band ±7.25 (2 x MAD), CV 4.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +941.4% (noise band ±41.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +676.4% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +185.8% (it comes back)
- PASS · Held-out claim: C2: +1464.3% to +1.1% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -163.9 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.02` (22.02 noise units, gap -18.9%); `eps_start=0.0` (21.51 noise units, gap -40.6%); `eps_start=0.2` (14.33 noise units, gap +341.2%); `eps_start=0.5` (8.47 noise units, gap +586.7%); `lr_schedule=linear` (1.12 noise units, gap +894.4%)
- Near alternatives (closest across all claims):
  - `eps_start=0.02`: this claim +4.1%, mean |gap| 2.2% (4 runs)
  - `eps_start=0.0`: this claim +11.7%, mean |gap| 6.0% (4 runs)
  - `lr_schedule=linear`, `eps_start=0.0`: this claim -13.6%, mean |gap| 7.6% (3 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.1, lr_schedule=inv` (reported)
- `eps_start=0.02, lr_schedule=inv`
- `eps_start=0.0, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=linear`

### History matching (every measured configuration, all claims together)
- 8 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `eps_start, lr_schedule`: eps_start=0.1, lr_schedule=linear (max I 0.07); eps_start=0.1, lr_schedule=inv (max I 0.1); eps_start=0.0, lr_schedule=linear (max I 0.28); eps_start=0.02, lr_schedule=inv (max I 0.29); +2 more
  - `eps_start`: eps_start=0.02 (max I 1.1); eps_start=0.0 (max I 1.48)
- Equally good values: `eps_start` in {0.0, 0.02, 0.1}; `lr_schedule` in {inv, linear}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.1, lr_schedule=inv; eps_start=0.02, lr_schedule=inv; eps_start=0.0, lr_schedule=linear; eps_start=0.1, lr_schedule=linear
- equally good values within one noise band (measured): eps_start in {0.0, 0.02, 0.1}; lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.02` | 4 | +4.1% | -0.3% | 2.2% |
| `lr_schedule=inv`, `eps_start=0.1` | 3 | -5.5% | +1.1% | 3.3% |
| `eps_start=0.0` | 4 | +11.7% | -0.3% | 6.0% |
| `lr_schedule=linear`, `eps_start=0.0` | 3 | -13.6% | -1.6% | 7.6% |
| `eps_start=0.02`, `lr_schedule=inv` | 3 | -17.9% | +0.0% | 8.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
