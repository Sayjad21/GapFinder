# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-14 23:42 · 111 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +895.5% | +13.9% | ±154.1% | `eps_start=0.01` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +895.5% → +13.9% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0017`, `B0030`, `B0031`, `B0035`, `B0036`, `B0037` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.01`
- Command:

  Replay: fork checkpoint `97ad625d-392b-45a1-9f8c-be6ecdef08a3` and run
  ```
  RUN_TAG=73768e1e1796 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.01 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 39.07, 9.645, 15.42, 22.14, 47.58, 17.28; gap after +13.9%; result checkpoint `ca81a6e6-8579-4e3b-9de7-cf966bce325d`
- Effect: candidate 19.71 minus naive 172.3 = -152.6, 95% bootstrap interval [-174.7, -130.3] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 172.3 over 5 runs; repeats: 185.7, 158.9, 198.3, 165.6, 172.3
- Spread: range 158.9 to 198.3, noise band ±26.68 (2 x MAD), CV 9.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +895.5% (noise band ±154.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +895.5% (it comes back)
- PASS · Held-out claim: C2: +1027.5% to +1.9% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.01`: no evidence mentions '0.01'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -152.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.02` (5.67 noise units, gap +21.5%); `eps_start=0.0` (5.52 noise units, gap -44.9%); `eps_start=0.1` (5.18 noise units, gap +97.8%); `eps_start=0.2` (2.64 noise units, gap +489.1%); `eps_start=0.5` (2.37 noise units, gap +529.5%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `eps_start=0.01`: this claim +2.6%, mean |gap| 1.3% (5 runs)
  - `lr_schedule=inv`, `eps_start=0.01`: this claim -5.4%, mean |gap| 3.5% (5 runs)
  - `lr_schedule=inv`, `eps_start=0.02`: this claim -6.5%, mean |gap| 3.8% (5 runs)

### Equally good configurations
The target claim can't tell these 13 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.01` (reported)
- `eps_start=0.0`
- `eps_start=0.02`
- `eps_start=0.1`
- `eps_start=0.02, lr_schedule=inv`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.01, lr_schedule=inv`
- `eps_start=0.0, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=linear`
- `eps_start=0.01, lr_schedule=linear`
- `eps_start=0.0, lr_schedule=inv`
- `eps_start=0.2, lr_schedule=linear`
- `eps_start=0.2, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 14 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_start, lr_schedule`: eps_start=0.02, lr_schedule=inv (max I 0.05); eps_start=0.1, lr_schedule=inv (max I 0.07); eps_start=0.01, lr_schedule=inv (max I 0.1); eps_start=0.0, lr_schedule=linear (max I 0.26); +4 more
  - `eps_start`: eps_start=0.0 (max I 0.23); eps_start=0.02 (max I 0.76)
- Equally good values: `eps_start` in {0.0, 0.01, 0.02, 0.1}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.01; eps_start=0.0; eps_start=0.02; eps_start=0.1; eps_start=0.02, lr_schedule=inv; eps_start=0.1, lr_schedule=inv; eps_start=0.01, lr_schedule=inv; eps_start=0.0, lr_schedule=linear; eps_start=0.1, lr_schedule=linear; eps_start=0.01, lr_schedule=linear; eps_start=0.0, lr_schedule=inv; eps_start=0.2, lr_schedule=linear; eps_start=0.2, lr_schedule=inv
- equally good values within one noise band (measured): eps_start in {0.0, 0.01, 0.02, 0.1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `eps_start=0.01` | 5 | +2.6% | +0.0% | 1.3% |
| `lr_schedule=inv`, `eps_start=0.01` | 5 | -5.4% | +1.6% | 3.5% |
| `lr_schedule=inv`, `eps_start=0.02` | 5 | -6.5% | +1.1% | 3.8% |
| `eps_start=0.01` | 6 | +13.9% | +1.9% | 7.9% |
| `eps_start=0.0` | 6 | -15.9% | +1.9% | 8.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
