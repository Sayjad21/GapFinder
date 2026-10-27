# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-15 19:15 · 141 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +950.9% | +42.3% | ±10.5% | `eps_start=0.0` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +950.9% → +42.3% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0010`, `B0026`, `B0027`, `B0045`, `B0046`, `B0047` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.0`
- Command:

  Replay: fork checkpoint `de40e3e2-556f-4590-bf4a-d7d884cc090d` and run
  ```
  RUN_TAG=0bfcfacc4c29 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 9.565, 54.15, 11.84, 29.41, 19.85, 31.25; gap after +42.3%; result checkpoint `95248255-ad81-4930-ae34-b68205e92c22`
- Effect: candidate 24.63 minus naive 181.9 = -157.3, 95% bootstrap interval [-166.4, -123.4] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 181.9 over 5 runs; repeats: 182, 181.9, 181.2, 158.5, 184.2
- Spread: range 158.5 to 184.2, noise band ±1.819 (2 x MAD), CV 6.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +950.9% (noise band ±10.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +950.9% (it comes back)
- PASS · Held-out claim: C2: +577.5% to +0.3% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.0`: no evidence mentions '0.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -157.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.02` (78.88 noise units, gap +122.0%); `eps_start=0.1` (73.79 noise units, gap +175.4%); `eps_start=0.2` (63.08 noise units, gap +288.0%); `eps_start=0.5` (29.45 noise units, gap +641.4%); `lr_schedule=inv` (13.88 noise units, gap +805.1%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `eps_start=0.1`: this claim -2.4%, mean |gap| 2.0% (5 runs)
  - `lr_schedule=inv`, `eps_start=0.0`: this claim -19.1%, mean |gap| 9.8% (5 runs)
  - `eps_start=0.02`, `lr_schedule=linear`: this claim -18.7%, mean |gap| 9.9% (5 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.0` (reported)
- `eps_start=0.02`
- `eps_start=0.02, lr_schedule=inv`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.1, lr_schedule=linear`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.0, lr_schedule=linear`
- `eps_start=0.0, lr_schedule=inv`
- `eps_start=0.2, lr_schedule=linear`

### History matching (every measured configuration, all claims together)
- 9 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `eps_start, lr_schedule`: eps_start=0.02, lr_schedule=linear (max I 0.15); eps_start=0.02, lr_schedule=inv (max I 0.27); eps_start=0.1, lr_schedule=linear (max I 0.48); eps_start=0.1, lr_schedule=inv (max I 0.51); +3 more
  - `eps_start`: eps_start=0.02 (max I 1.15); eps_start=0.0 (max I 1.29)

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.0; eps_start=0.02; eps_start=0.02, lr_schedule=inv; eps_start=0.1, lr_schedule=inv; eps_start=0.1, lr_schedule=linear; eps_start=0.02, lr_schedule=linear; eps_start=0.0, lr_schedule=linear; eps_start=0.0, lr_schedule=inv; eps_start=0.2, lr_schedule=linear

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `eps_start=0.1` | 5 | -2.4% | +1.6% | 2.0% |
| `lr_schedule=inv`, `eps_start=0.0` | 5 | -19.1% | -0.5% | 9.8% |
| `eps_start=0.02`, `lr_schedule=linear` | 5 | -18.7% | +1.1% | 9.9% |
| `lr_schedule=inv`, `eps_start=0.1` | 5 | -37.9% | +0.0% | 19.0% |
| `eps_start=0.02`, `lr_schedule=inv` | 5 | -40.6% | +0.5% | 20.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
