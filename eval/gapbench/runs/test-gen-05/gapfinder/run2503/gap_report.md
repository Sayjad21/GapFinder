# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-16 01:46 · 104 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +863.1% | -7.1% | ±155.7% | `eps_start=0.0` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +863.1% → -7.1% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0024`, `B0025`, `B0035`, `B0036`, `B0037` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.0`
- Command:

  Replay: fork checkpoint `d2cb754a-281d-44e7-92f9-8eccef2a074d` and run
  ```
  RUN_TAG=cdeab85cf082 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 21.99, 10.16, 9.615, 29.7, 42.8, 9.67; gap after -7.1%; result checkpoint `5288c31b-aa27-4bd9-82cf-00f9576d2027`
- Effect: candidate 16.07 minus naive 166.7 = -150.6, 95% bootstrap interval [-172.6, -127.2] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 166.7 over 5 runs; repeats: 183.8, 158.1, 153.2, 191.9, 166.7
- Spread: range 153.2 to 191.9, noise band ±26.96 (2 x MAD), CV 9.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +863.1% (noise band ±155.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +863.1% (it comes back)
- PASS · Held-out claim: C2: +590.7% to +0.3% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.0`: no evidence mentions '0.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -150.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.02` (5.27 noise units, gap -42.7%); `eps_start=0.1` (4.26 noise units, gap +199.8%); `eps_start=0.01` (3.39 noise units, gap +335.5%); `eps_start=0.5` (2.27 noise units, gap +510.2%); `eps_start=0.2` (1.74 noise units, gap +592.4%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_start=0.1`, `lr_schedule=inv`: this claim -5.7%, mean |gap| 3.1% (5 runs)
  - `lr_schedule=inv`, `eps_start=0.02`: this claim +7.3%, mean |gap| 3.9% (5 runs)
  - `eps_start=0.0`, `lr_schedule=inv`: this claim -8.1%, mean |gap| 4.3% (5 runs)

### Equally good configurations
The target claim can't tell these 10 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.0` (reported)
- `eps_start=0.02`
- `eps_start=0.01`
- `eps_start=0.02, lr_schedule=inv`
- `eps_start=0.0, lr_schedule=inv`
- `eps_start=0.01, lr_schedule=inv`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.0, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=linear`

### History matching (every measured configuration, all claims together)
- 14 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_start, lr_schedule`: eps_start=0.02, lr_schedule=inv (max I 0.03); eps_start=0.0, lr_schedule=inv (max I 0.19); eps_start=0.01, lr_schedule=inv (max I 0.23); eps_start=0.02, lr_schedule=linear (max I 0.28); +4 more
  - `eps_start`: eps_start=0.0 (max I 0.32); eps_start=0.02 (max I 0.47)
- Equally good values: `eps_start` in {0.0, 0.01, 0.02, 0.1}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.0; eps_start=0.02; eps_start=0.01; eps_start=0.02, lr_schedule=inv; eps_start=0.0, lr_schedule=inv; eps_start=0.01, lr_schedule=inv; eps_start=0.02, lr_schedule=linear; eps_start=0.1, lr_schedule=inv; eps_start=0.0, lr_schedule=linear; eps_start=0.1, lr_schedule=linear
- equally good values within one noise band (measured): eps_start in {0.0, 0.01, 0.02, 0.1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.1`, `lr_schedule=inv` | 5 | -5.7% | +0.5% | 3.1% |
| `eps_start=0.0` | 6 | -7.1% | +0.3% | 3.7% |
| `lr_schedule=inv`, `eps_start=0.02` | 5 | +7.3% | +0.5% | 3.9% |
| `eps_start=0.0`, `lr_schedule=inv` | 5 | -8.1% | +0.5% | 4.3% |
| `lr_schedule=inv`, `eps_start=0.01` | 5 | -18.8% | +1.1% | 10.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
