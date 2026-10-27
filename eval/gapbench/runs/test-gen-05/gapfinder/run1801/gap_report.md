# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-15 19:38 · 87 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +946.3% | -13.6% | ±73.1% | `eps_start=0.02` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +946.3% → -13.6% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0013`, `B0028`, `B0029`, `B0037` (4 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.02`
- Command:

  Replay: fork checkpoint `8e382a43-8173-42aa-ab46-35700919b00b` and run
  ```
  RUN_TAG=ae1a720fcf6a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.02 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 13, 12.21, 52.76, 16.91; gap after -13.6%; result checkpoint `39a0af17-8b04-432d-9ebf-826b9d800e2a`
- Effect: candidate 14.96 minus naive 181.1 = -166.2, 95% bootstrap interval [-173.9, -122.4] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 181.1 over 5 runs; repeats: 191.7, 168.4, 181.1, 174.8, 182.1
- Spread: range 168.4 to 191.7, noise band ±12.65 (2 x MAD), CV 4.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +946.3% (noise band ±73.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +946.3% (it comes back)
- PASS · Held-out claim: C2: +673.1% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.02`: no evidence mentions '0.02'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -166.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.2` (12.58 noise units, gap -27.1%); `eps_start=0.01` (12.55 noise units, gap +29.5%); `eps_start=0.0` (11.49 noise units, gap +106.9%); `eps_start=0.1` (10.22 noise units, gap +199.5%); `eps_start=0.5` (5 noise units, gap +580.7%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_start=0.1`, `lr_schedule=linear`: this claim -1.0%, mean |gap| 1.3% (3 runs)
  - `lr_schedule=inv`, `eps_start=0.1`: this claim +6.1%, mean |gap| 3.6% (3 runs)
  - `lr_schedule=inv`, `eps_start=0.01`: this claim +15.9%, mean |gap| 8.2% (3 runs)

### Equally good configurations
The target claim can't tell these 10 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.02` (reported)
- `eps_start=0.01`
- `eps_start=0.0`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.1, lr_schedule=linear`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.01, lr_schedule=inv`
- `eps_start=0.0, lr_schedule=linear`
- `eps_start=0.0, lr_schedule=inv`
- `eps_start=0.01, lr_schedule=linear`

### History matching (every measured configuration, all claims together)
- 12 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_start, lr_schedule`: eps_start=0.01, lr_schedule=inv (max I 0.08); eps_start=0.1, lr_schedule=inv (max I 0.1); eps_start=0.02, lr_schedule=linear (max I 0.16); eps_start=0.1, lr_schedule=linear (max I 0.34); +4 more
  - `eps_start`: eps_start=0.01 (max I 0.46); eps_start=0.02 (max I 1.06)
- Equally good values: `eps_start` in {0.0, 0.01, 0.02}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.02; eps_start=0.01; eps_start=0.0; eps_start=0.1, lr_schedule=inv; eps_start=0.1, lr_schedule=linear; eps_start=0.02, lr_schedule=linear; eps_start=0.01, lr_schedule=inv; eps_start=0.0, lr_schedule=linear; eps_start=0.0, lr_schedule=inv; eps_start=0.01, lr_schedule=linear
- equally good values within one noise band (measured): eps_start in {0.0, 0.01, 0.02}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.1`, `lr_schedule=linear` | 3 | -1.0% | +1.6% | 1.3% |
| `lr_schedule=inv`, `eps_start=0.1` | 3 | +6.1% | +1.1% | 3.6% |
| `eps_start=0.02` | 4 | -13.6% | +0.0% | 6.8% |
| `lr_schedule=inv`, `eps_start=0.01` | 3 | +15.9% | +0.5% | 8.2% |
| `eps_start=0.01` | 4 | +18.8% | +0.3% | 9.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
