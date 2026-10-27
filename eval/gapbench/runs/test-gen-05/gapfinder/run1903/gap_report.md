# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-15 19:38 · 92 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +974.3% | -8.3% | ±78.3% | `eps_start=0.01` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +974.3% → -8.3% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0017`, `B0036`, `B0037`, `B0038` (4 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.01`
- Command:

  Replay: fork checkpoint `2f3ccf2b-3e5e-46c0-b757-b25e7a4cdfc5` and run
  ```
  RUN_TAG=de78be4cf7dd "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.01 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 23.21, 21.45, 9.795, 10.29; gap after -8.3%; result checkpoint `682cd9a0-e28c-4872-a4f8-d6bdca8beb89`
- Effect: candidate 15.88 minus naive 186 = -170.1, 95% bootstrap interval [-185.5, -161.1] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 186 over 5 runs; repeats: 198, 192.7, 180.9, 186, 176.7
- Spread: range 176.7 to 198, noise band ±13.55 (2 x MAD), CV 4.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +974.3% (noise band ±78.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +974.3% (it comes back)
- PASS · Held-out claim: C2: +761.5% to +0.8% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.01`: no evidence mentions '0.01'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -170.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.1` (12.21 noise units, gap +18.3%); `eps_start=0.0` (11.94 noise units, gap -39.8%); `eps_start=0.02` (11.91 noise units, gap -42.2%); `eps_start=0.2` (9.04 noise units, gap +266.6%); `lr_schedule=inv` (3.77 noise units, gap +678.8%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `eps_start=0.02`: this claim +2.5%, mean |gap| 1.2% (3 runs)
  - `eps_start=0.1`, `lr_schedule=linear`: this claim -5.6%, mean |gap| 3.9% (3 runs)
  - `eps_start=0.1`, `lr_schedule=inv`: this claim -7.8%, mean |gap| 4.2% (3 runs)

### Equally good configurations
The target claim can't tell these 10 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.01` (reported)
- `eps_start=0.0`
- `eps_start=0.02`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.02, lr_schedule=inv`
- `eps_start=0.01, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=linear`
- `eps_start=0.0, lr_schedule=inv`
- `eps_start=0.2, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 13 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_start, lr_schedule`: eps_start=0.02, lr_schedule=linear (max I 0.06); eps_start=0.1, lr_schedule=inv (max I 0.17); eps_start=0.01, lr_schedule=linear (max I 0.4); eps_start=0.02, lr_schedule=inv (max I 0.45); +4 more
  - `eps_start`: eps_start=0.01 (max I 0.19); eps_start=0.0 (max I 1)
- Equally good values: `eps_start` in {0.0, 0.01, 0.02}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.01; eps_start=0.0; eps_start=0.02; eps_start=0.02, lr_schedule=linear; eps_start=0.1, lr_schedule=inv; eps_start=0.02, lr_schedule=inv; eps_start=0.01, lr_schedule=linear; eps_start=0.1, lr_schedule=linear; eps_start=0.0, lr_schedule=inv; eps_start=0.2, lr_schedule=inv
- equally good values within one noise band (measured): eps_start in {0.0, 0.01, 0.02}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `eps_start=0.02` | 3 | +2.5% | +0.0% | 1.2% |
| `eps_start=0.1`, `lr_schedule=linear` | 3 | -5.6% | +2.2% | 3.9% |
| `eps_start=0.1`, `lr_schedule=inv` | 3 | -7.8% | +0.5% | 4.2% |
| `eps_start=0.01` | 4 | -8.3% | +0.8% | 4.6% |
| `lr_schedule=inv`, `eps_start=0.0` | 3 | -23.0% | +0.0% | 11.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
