# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 07:34 · 156 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +68.3% | -1.2% | ±27.1% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +68.3% → -1.2% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0048`, `B0049`, `B0052`, `B0053`, `B0054` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `f016b62b-2450-4cac-ab18-179cb581eef1` and run
  ```
  RUN_TAG=9d585d0f2231 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 95.53, 99.62, 99.82, 94.23, 99.5, 87.95; gap after -1.2%; result checkpoint `91c881cf-dacc-4006-8129-b57e0a506546`
- Effect: candidate 97.52 minus naive 166.1 = -68.57, 95% bootstrap interval [-88.87, -58.09] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 166.1 over 5 runs; repeats: 179.5, 161.9, 166.1, 186.7, 152.7
- Spread: range 152.7 to 186.7, noise band ±26.75 (2 x MAD), CV 8.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +68.3% (noise band ±27.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +68.3% (it comes back)
- PASS · Held-out claim: C2: -47.5% to -19.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -68.57 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.5` (2.36 noise units, gap +4.3%); `lr=0.01` (2.16 noise units, gap -9.8%); `lr=0.02` (1.82 noise units, gap -18.9%); `lr=0.001` (1.61 noise units, gap -24.7%); `lr_schedule=inv` (1.46 noise units, gap +28.7%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -1.2%, mean |gap| 2.6% (5 runs)
  - `lr=0.5`, `max_steps=100`: this claim +1.3%, mean |gap| 3.1% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -11.4%, mean |gap| 36.9% (5 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr=0.02`
- `lr=1`
- `lr=0.5, max_steps=100`
- `lr_schedule=linear, max_steps=100`
- `lr=0.02, lr_schedule=linear`

### History matching (every measured configuration, all claims together)
- 11 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.12)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.66); lr_schedule=inv, max_steps=100 (max I 1.55)
  - `max_steps`: max_steps=100 (max I 0.76)
  - `lr, lr_schedule`: lr=0.02, lr_schedule=linear (max I 2.18); lr=0.001, lr_schedule=inv (max I 2.57)
  - `lr`: lr=0.5 (max I 2.19); lr=1 (max I 2.26); lr=0.02 (max I 2.41); lr=0.01 (max I 2.51)
- 2 separate islands (no single-knob move joins them): lr=0.5, max_steps=100; lr_schedule=linear, max_steps=100; max_steps=100 | lr=0.001, lr_schedule=inv

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr=0.02; lr=1; lr=0.5, max_steps=100; lr_schedule=linear, max_steps=100; lr=0.02, lr_schedule=linear

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | -1.2% | -4.1% | 2.6% |
| `lr=0.5`, `max_steps=100` | 5 | +1.3% | +4.8% | 3.1% |
| `max_steps=100` | 6 | -1.2% | -19.1% | 10.1% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -11.4% | -62.4% | 36.9% |
| `lr_schedule=inv` | 6 | +28.7% | -60.3% | 44.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0481, sandbox reported $0.0000 (total $0.0481; this search; ledger extraction is included only if it shared the search's router)
