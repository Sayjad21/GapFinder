# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-16 02:02 · 164 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +95.5% | -1.1% | ±5.6% | `lr=0.01`, `lr_schedule=linear` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +95.5% → -1.1% · 55 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0111`, `B0126`, `B0154` (3 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `0.01`
- Config: `lr_schedule` naive `const`, changed to `linear`
- Command:

  Replay: fork checkpoint `1eb48b9e-f0dd-49e6-b715-e21535ec3384` and run
  ```
  RUN_TAG=7c3458693c2e "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.01 --lr_schedule linear --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 97.57, 103.2, 76.75; gap after -1.1%; result checkpoint `592786f3-e6b2-4758-a89c-94be6d94da5b`
- Effect: candidate 97.57 minus naive 193 = -95.4, 95% bootstrap interval [-119.6, -86.14] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 193 over 5 runs; repeats: 195.7, 198.6, 190.2, 188.1, 193
- Spread: range 188.1 to 198.6, noise band ±5.53 (2 x MAD), CV 2.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +95.5% (noise band ±5.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +75.5% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -32.3% (it comes back)
- PASS · Held-out claim: C2: +75.6% to -89.4% (not worse beyond noise)
- FAIL · Evidence: `lr=0.01`: no evidence mentions '0.01'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=linear`: no evidence mentions 'linear'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -95.4 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (15.45 noise units, gap -9.0%); `lr=0.001` (12.87 noise units, gap -23.4%); `lr=1` (12.01 noise units, gap +28.2%); `lr=0.02` (10.04 noise units, gap -39.3%); `lr=0.05` (9.08 noise units, gap +44.7%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -1.1%, mean |gap| 1.2% (3 runs)
  - `lr_schedule=inv`, `max_steps=100`, `lr=1`: this claim +1.3%, mean |gap| 3.1% (3 runs)
  - `max_steps=100`: this claim -5.0%, mean |gap| 25.7% (4 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=0.01, lr_schedule=linear` (reported)
- `lr=1`
- `max_steps=100`
- `lr=0.001`
- `lr_schedule=linear, max_steps=100`
- `lr=0.01, lr_schedule=inv`
- `lr_schedule=inv, max_steps=100`
- `lr=0.02, lr_schedule=inv`
- `lr=1, lr_schedule=inv, max_steps=100`

### History matching (every measured configuration, all claims together)
- 3 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.23); lr_schedule=inv, max_steps=100 (max I 2.99)
  - `lr, lr_schedule, max_steps`: lr=1, lr_schedule=inv, max_steps=100 (max I 0.29)

Notes:
- configurations the target claim can't tell apart from the answer: lr=0.01, lr_schedule=linear; lr=1; max_steps=100; lr=0.001; lr_schedule=linear, max_steps=100; lr=0.01, lr_schedule=inv; lr_schedule=inv, max_steps=100; lr=0.02, lr_schedule=inv; lr=1, lr_schedule=inv, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 3 | -1.1% | -1.3% | 1.2% |
| `lr_schedule=inv`, `max_steps=100`, `lr=1` | 3 | +1.3% | +4.8% | 3.1% |
| `max_steps=100` | 4 | -5.0% | -46.5% | 25.7% |
| `max_steps=100`, `lr_schedule=inv` | 3 | -11.5% | -56.0% | 33.7% |
| `lr=0.2` | 4 | +68.9% | -5.2% | 37.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
