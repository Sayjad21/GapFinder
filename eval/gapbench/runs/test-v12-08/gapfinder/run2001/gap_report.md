# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 21:10 · 131 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +73.5% | -4.9% | ±53.7% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +73.5% → -4.9% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0023`, `B0048`, `B0049`, `B0053`, `B0054`, `B0055` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `13757b9c-5148-4901-9650-c744c4c4dc8d` and run
  ```
  RUN_TAG=f81a480f6c9f "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 96.89, 90.52, 93.45, 99.89, 84.19, 94.34; gap after -4.9%; result checkpoint `2e7dee60-52f3-4162-9ef1-47c2f6671cab`
- Effect: candidate 93.9 minus naive 171.2 = -77.35, 95% bootstrap interval [-109, -51.27] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 171.2 over 5 runs; repeats: 197.8, 171.2, 134.6, 200, 162.6
- Spread: range 134.6 to 200, noise band ±53 (2 x MAD), CV 15.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +73.5% (noise band ±53.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +73.5% (it comes back)
- PASS · Held-out claim: C2: -49.0% to -39.7% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -77.35 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.05` (1.24 noise units, gap +6.8%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -1.4%, mean |gap| 2.9% (5 runs)
  - `max_steps=100`, `lr=0.5`: this claim +1.3%, mean |gap| 3.1% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -14.4%, mean |gap| 41.5% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr=1`
- `lr=0.5, max_steps=100`
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 38 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.05); lr=0.05, max_steps=100 (max I 0.67); lr=1, max_steps=100 (max I 0.88)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.44); lr_schedule=inv, max_steps=100 (max I 1.07)
  - `max_steps`: max_steps=100 (max I 0.61)
  - `lr, lr_schedule`: lr=0.001, lr_schedule=inv (max I 0.81); lr=0.05, lr_schedule=linear (max I 0.88); lr=0.05, lr_schedule=inv (max I 0.96)
  - `lr_schedule`: lr_schedule=inv (max I 1.11)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr=1; lr=0.5, max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | -1.4% | -4.4% | 2.9% |
| `max_steps=100`, `lr=0.5` | 5 | +1.3% | +4.8% | 3.1% |
| `max_steps=100` | 6 | -4.9% | -39.7% | 22.3% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -14.4% | -68.7% | 41.5% |
| `lr=1` | 6 | +3.7% | -85.1% | 44.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
