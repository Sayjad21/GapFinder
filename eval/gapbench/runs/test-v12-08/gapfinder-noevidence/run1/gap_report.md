# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 07:34 · 192 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +90.1% | +3.0% | ±21.2% | `lr=0.05`, `lr_schedule=inv` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +90.1% → +3.0% · 55 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0104`, `B0165`, `B0166`, `B0167`, `B0168` (5 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `0.05`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `d91e81e7-6e01-4bbe-a487-1dc54b8b66ad` and run
  ```
  RUN_TAG=06faf58e1eb8 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.05 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 101.7, 121.9, 87.85, 99.53, 117; gap after +3.0%; result checkpoint `649ff9cd-a8f2-45d8-970b-7d28514057b6`
- Effect: candidate 101.7 minus naive 187.6 = -85.87, 95% bootstrap interval [-98.49, -60.78] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 187.6 over 5 runs; repeats: 174.4, 187.6, 175.4, 198, 191.1
- Spread: range 174.4 to 198, noise band ±20.88 (2 x MAD), CV 5.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +90.1% (noise band ±21.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +30.8% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +42.3% (it comes back)
- PASS · Held-out claim: C2: +49.5% to -86.7% (not worse beyond noise)
- FAIL · Evidence: `lr=0.05`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `lr_schedule=inv`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -85.87 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (4.13 noise units, gap -2.7%); `lr=0.02` (3.82 noise units, gap -9.3%); `lr=0.002` (2.52 noise units, gap -36.7%); `lr=0.001` (2.52 noise units, gap -36.7%); `lr=1` (2.29 noise units, gap -41.7%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim +1.2%, mean |gap| 2.1% (6 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim -1.4%, mean |gap| 2.4% (5 runs)
  - `lr=0.05`, `max_steps=100`: this claim -13.3%, mean |gap| 39.0% (5 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=0.05, lr_schedule=inv` (reported)
- `max_steps=100`
- `lr=0.02`
- `lr=0.01`
- `lr_schedule=linear, max_steps=100`
- `lr=0.02, lr_schedule=linear`
- `lr=0.02, lr_schedule=inv`
- `lr=0.05, lr_schedule=linear`

### History matching (every measured configuration, all claims together)
- 9 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `max_steps`: max_steps=100 (max I 0.23)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.33); lr_schedule=inv, max_steps=100 (max I 1.67)
  - `lr, lr_schedule`: lr=0.05, lr_schedule=inv (max I 1.7); lr=0.02, lr_schedule=linear (max I 1.95); lr=0.02, lr_schedule=inv (max I 2.11); lr=0.05, lr_schedule=linear (max I 2.2)
  - `lr`: lr=0.02 (max I 1.85)
  - `lr, max_steps`: lr=0.05, max_steps=100 (max I 1.99)
- 2 separate islands (no single-knob move joins them): lr=0.05, lr_schedule=inv; lr=0.02; lr=0.02, lr_schedule=linear | max_steps=100; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100
- Equally good values: `lr` in {0.02, 0.05}; `lr_schedule` in {inv, linear}

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- configurations the target claim can't tell apart from the answer: lr=0.05, lr_schedule=inv; max_steps=100; lr=0.02; lr=0.01; lr_schedule=linear, max_steps=100; lr=0.02, lr_schedule=linear; lr=0.02, lr_schedule=inv; lr=0.05, lr_schedule=linear
- equally good values within one noise band (measured): lr in {0.02, 0.05}; lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +1.2% | +3.1% | 2.1% |
| `max_steps=100`, `lr_schedule=linear` | 5 | -1.4% | -3.5% | 2.4% |
| `lr=0.05`, `max_steps=100` | 5 | -13.3% | -64.7% | 39.0% |
| `lr=0.2` | 6 | +72.8% | -6.6% | 39.7% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -15.6% | -66.9% | 41.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
