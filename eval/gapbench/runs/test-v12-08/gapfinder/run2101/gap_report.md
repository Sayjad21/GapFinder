# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 21:10 · 142 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +65.8% | +14.7% | ±28.3% | `lr=0.05` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +65.8% → +14.7% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0028`, `B0029`, `B0059`, `B0060`, `B0061` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `0.05`
- Command:

  Replay: fork checkpoint `fb5ddca3-806d-4502-8c21-b86ebd5129b2` and run
  ```
  RUN_TAG=56ff14bfc932 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.05 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 149, 119.5, 106.8, 148.3, 101.2, 99.7; gap after +14.7%; result checkpoint `3a2bec02-ae1c-4dca-8e2b-0b0047e5a496`
- Effect: candidate 113.2 minus naive 163.6 = -50.43, 95% bootstrap interval [-85.69, -26.2] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 163.6 over 5 runs; repeats: 189.1, 157.6, 163.6, 149.7, 194.4
- Spread: range 149.7 to 194.4, noise band ±27.91 (2 x MAD), CV 11.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +65.8% (noise band ±28.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +65.8% (it comes back)
- PASS · Held-out claim: C2: -42.8% to -84.4% (not worse beyond noise)
- FAIL · Evidence: `lr=0.05`: no evidence mentions '0.05'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -50.43 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (2.26 noise units, gap -2.0%); `lr=0.002` (2.17 noise units, gap -4.3%); `lr=0.5` (1.92 noise units, gap +11.5%); `lr=0.01` (1.19 noise units, gap -32.2%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -1.6%, mean |gap| 1.5% (5 runs)
  - `max_steps=100`, `lr=0.5`: this claim +1.0%, mean |gap| 1.5% (5 runs)
  - `max_steps=100`: this claim -4.2%, mean |gap| 26.5% (6 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=0.05` (reported)
- `lr=0.02`
- `lr=1`
- `lr=0.01`
- `max_steps=100`
- `lr=0.5, max_steps=100`
- `lr_schedule=linear, max_steps=100`
- `lr_schedule=inv, max_steps=100`
- `lr=0.002, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 26 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.06); lr=0.001, max_steps=100 (max I 2.06); lr=0.002, max_steps=100 (max I 2.11); lr=1, max_steps=100 (max I 2.17)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.42); lr_schedule=inv, max_steps=100 (max I 1.43)
  - `max_steps`: max_steps=100 (max I 1.21)
  - `lr`: lr=0.05 (max I 1.85); lr=0.5 (max I 2.13)
  - `lr, lr_schedule`: lr=0.002, lr_schedule=inv (max I 2.08)
- Equally good values: `lr` in {0.002, 0.01, 0.02, 0.05, 0.5, 1}

Notes:
- configurations the target claim can't tell apart from the answer: lr=0.05; lr=0.02; lr=1; lr=0.01; max_steps=100; lr=0.5, max_steps=100; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100; lr=0.002, lr_schedule=inv
- equally good values within one noise band (measured): lr in {0.002, 0.01, 0.02, 0.05, 0.5, 1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | -1.6% | -1.3% | 1.5% |
| `max_steps=100`, `lr=0.5` | 5 | +1.0% | +1.9% | 1.5% |
| `max_steps=100` | 6 | -4.2% | -48.8% | 26.5% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -14.6% | -75.3% | 44.9% |
| `lr=0.2` | 6 | +75.2% | -16.3% | 45.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
