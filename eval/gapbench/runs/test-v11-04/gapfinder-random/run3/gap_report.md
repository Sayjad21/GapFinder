# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 12:36 · 92 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +89.0% | +1.6% | ±17.4% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +89.0% → +1.6% · 47 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0019`, `B0035`, `B0036`, `B0037` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `b06da866-3a51-4de9-a312-8283bdbc826b` and run
  ```
  RUN_TAG=88c937d977c0 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 94.25, 97.36, 98.94, 95.62; gap after +1.6%; result checkpoint `7a87b708-b87f-413b-87f9-ca59cde81e3c`
- Effect: candidate 96.49 minus naive 179.4 = -82.96, 95% bootstrap interval [-90.84, -75.04] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 179.4 over 5 runs; repeats: 179.4, 170.6, 187.7, 188.7, 176.9
- Spread: range 170.6 to 188.7, noise band ±16.51 (2 x MAD), CV 4.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +89.0% (noise band ±17.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +89.0% (it comes back)
- PASS · Held-out claim: C2: +34.2% to +14.4% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -82.96 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (2.47 noise units, gap +46.1%); `lr_schedule=inv` (2.25 noise units, gap +49.9%); `lr_schedule=linear` (1.61 noise units, gap +61.0%); `eps_start=0.1` (1.47 noise units, gap -63.4%); `eps_start=10` (1.41 noise units, gap +64.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +4.1%, mean |gap| 27.0% (3 runs)
  - `eps_start=10`, `max_steps=100`: this claim +5.0%, mean |gap| 28.5% (3 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -8.0%, mean |gap| 30.1% (3 runs)

### History matching (every measured configuration, all claims together)
- 6 of 47 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `max_steps`: max_steps=100 (max I 0.28)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.4); lr_schedule=inv, max_steps=100 (max I 1.17)
  - `eps_start, max_steps`: eps_start=10, max_steps=100 (max I 0.56); eps_start=0.5, max_steps=100 (max I 1.82)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.09)
- 2 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; eps_start=10, max_steps=100 | eps_start=0.5, lr_schedule=linear

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 4 | +1.6% | +14.4% | 8.0% |
| `lr_schedule=linear`, `max_steps=100` | 3 | +4.1% | +50.0% | 27.0% |
| `eps_start=10`, `max_steps=100` | 3 | +5.0% | +52.0% | 28.5% |
| `lr_schedule=inv`, `max_steps=100` | 3 | -8.0% | -52.2% | 30.1% |
| `lr_schedule=inv`, `max_steps=1000` | 3 | +65.8% | -14.1% | 40.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
