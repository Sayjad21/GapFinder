# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-16 02:01 · 137 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +69.9% | +0.9% | ±29.7% | `lr=1` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +69.9% → +0.9% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0009`, `B0034`, `B0035`, `B0050`, `B0051`, `B0052` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `1`
- Command:

  Replay: fork checkpoint `7ee9b9b2-fd40-4649-b24a-759db7b88392` and run
  ```
  RUN_TAG=c7493c092c5d "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 98.43, 84.2, 117.6, 98.36, 100.6, 125.5; gap after +0.9%; result checkpoint `e9892097-8dc7-4518-ba51-b719549554a3`
- Effect: candidate 99.53 minus naive 167.7 = -68.14, 95% bootstrap interval [-95.16, -42.7] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 167.7 over 5 runs; repeats: 167.7, 197.7, 153, 183.6, 164.4
- Spread: range 153 to 197.7, noise band ±29.35 (2 x MAD), CV 10.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +69.9% (noise band ±29.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +69.9% (it comes back)
- PASS · Held-out claim: C2: -79.9% to -84.5% (not worse beyond noise)
- FAIL · Evidence: `lr=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -68.14 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.001` (2.13 noise units, gap +6.4%); `max_steps=100` (2.02 noise units, gap -9.7%); `lr=0.002` (1.93 noise units, gap -12.5%); `lr=0.5` (1.46 noise units, gap +26.5%); `lr=0.01` (1.4 noise units, gap -28.4%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr=0.5`: this claim +1.3%, mean |gap| 3.1% (5 runs)
  - `max_steps=100`: this claim -2.7%, mean |gap| 16.8% (6 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim -6.3%, mean |gap| 29.6% (5 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=1` (reported)
- `max_steps=100`
- `lr=0.02`
- `lr=0.5, max_steps=100`
- `lr_schedule=linear, max_steps=100`
- `lr_schedule=inv, max_steps=100`

### History matching (every measured configuration, all claims together)
- 17 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.24); lr=1, max_steps=100 (max I 2.07)
  - `max_steps`: max_steps=100 (max I 0.48)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.79); lr_schedule=inv, max_steps=100 (max I 0.98)
  - `lr`: lr=1 (max I 1.6); lr=0.02 (max I 1.7); lr=0.5 (max I 2.08); lr=0.002 (max I 2.45)
  - `lr, lr_schedule`: lr=0.002, lr_schedule=inv (max I 2.24)
- Equally good values: `lr` in {0.02, 0.5, 1}

Notes:
- configurations the target claim can't tell apart from the answer: lr=1; max_steps=100; lr=0.02; lr=0.5, max_steps=100; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100
- equally good values within one noise band (measured): lr in {0.02, 0.5, 1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr=0.5` | 5 | +1.3% | +4.8% | 3.1% |
| `max_steps=100` | 6 | -2.7% | -30.9% | 16.8% |
| `max_steps=100`, `lr_schedule=linear` | 5 | -6.3% | -52.9% | 29.6% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -9.7% | -63.7% | 36.7% |
| `lr=1` | 6 | +0.9% | -84.5% | 42.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
