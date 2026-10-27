# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-16 02:02 · 186 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +70.2% | -4.7% | ±18.4% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +70.2% → -4.7% · 45 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0023`, `B0058`, `B0059`, `B0068`, `B0069`, `B0070` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `53c8d400-a49c-4e65-80c6-176f65ed6836` and run
  ```
  RUN_TAG=df794a52bd79 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 92.04, 95.08, 99.54, 91.52, 93.03, 96.58; gap after -4.7%; result checkpoint `74b859cd-ee45-4c98-a385-14eed1567858`
- Effect: candidate 94.06 minus naive 168 = -73.92, 95% bootstrap interval [-95.35, -62.83] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 168 over 5 runs; repeats: 193.3, 157.3, 177, 160.1, 168
- Spread: range 157.3 to 193.3, noise band ±18.14 (2 x MAD), CV 8.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +70.2% (noise band ±18.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +70.2% (it comes back)
- PASS · Held-out claim: C2: -45.8% to -44.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -73.92 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.05` (3.77 noise units, gap +0.8%); `lr=1` (2.84 noise units, gap -18.0%); `lr=0.02` (2.39 noise units, gap -26.4%); `lr=0.01` (2.31 noise units, gap -27.8%); `lr=0.5` (2.06 noise units, gap +32.3%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -1.6%, mean |gap| 3.2% (5 runs)
  - `lr=0.05`: this claim +18.1%, mean |gap| 40.9% (6 runs)
  - `lr_schedule=linear`, `lr=0.05`: this claim +5.0%, mean |gap| 43.7% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 15 of 45 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.69); lr_schedule=inv, max_steps=100 (max I 2.48)
  - `max_steps`: max_steps=100 (max I 1.42)
  - `lr, max_steps`: lr=1, max_steps=100 (max I 1.98)
  - `lr`: lr=0.05 (max I 2.26); lr=0.5 (max I 2.67); lr=1 (max I 2.72)
  - `lr, lr_schedule`: lr=0.05, lr_schedule=linear (max I 2.49); lr=0.02, lr_schedule=inv (max I 2.7); lr=0.05, lr_schedule=inv (max I 2.71)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | -1.6% | -4.9% | 3.2% |
| `max_steps=100` | 6 | -4.7% | -44.1% | 24.4% |
| `lr=0.05` | 6 | +18.1% | -63.8% | 40.9% |
| `lr_schedule=linear`, `lr=0.05` | 5 | +5.0% | -82.4% | 43.7% |
| `lr=0.2` | 6 | +70.5% | -17.5% | 44.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
