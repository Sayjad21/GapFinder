# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 12:35 · 161 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | +94.8% | +7.9% | ±23.9% | `eps_start=0.5`, `lr_schedule=linear` |

## C1: mean_reward (paper 94.93)
**Explained** · gap +94.8% → +7.9% · 47 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0096`, `B0142`, `B0143`, `B0144`, `B0145` (5 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.5`
- Config: `lr_schedule` naive `const`, changed to `linear`
- Command:

  Replay: fork checkpoint `54b715cd-2bfd-4880-8450-ea0fecc2ae05` and run
  ```
  RUN_TAG=60a9211a6eaa "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule linear --eps_start 0.5 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 55.4, 107.2, 111.6, 102.4, 77.62; gap after +7.9%; result checkpoint `02dde18c-89b7-4dc2-8f94-25d77a83ce7f`
- Effect: candidate 102.4 minus naive 184.9 = -82.48, 95% bootstrap interval [-124.8, -66.37] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 184.9 over 5 runs; repeats: 193.4, 184.9, 172.8, 164, 196.2
- Spread: range 164 to 196.2, noise band ±22.71 (2 x MAD), CV 7.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +94.8% (noise band ±23.9% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -82.48 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (3.87 noise units, gap -2.3%); `lr_schedule=inv` (1.91 noise units, gap +49.2%); `eps_start=0.02` (1.28 noise units, gap -64.2%)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim +3.7%, mean |gap| 19.8% (6 runs)
  - `lr_schedule=linear`, `max_steps=100`: this claim +2.7%, mean |gap| 23.6% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -13.4%, mean |gap| 30.2% (5 runs)

### History matching (every measured configuration, all claims together)
- 7 of 47 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `max_steps`: max_steps=100 (max I 0.27)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.81); lr_schedule=inv, max_steps=100 (max I 1)
  - `eps_start, max_steps`: eps_start=10, max_steps=100 (max I 0.99); eps_start=0.5, max_steps=100 (max I 1.24)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=inv (max I 1.48); eps_start=0.5, lr_schedule=linear (max I 1.48)
- 2 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; eps_start=10, max_steps=100 | eps_start=0.5, lr_schedule=inv; eps_start=0.5, lr_schedule=linear
- Equally good values: `lr_schedule` in {inv, linear}

Notes:
- equally good values within one noise band (measured): lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +3.7% | +36.0% | 19.8% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +2.7% | +44.5% | 23.6% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -13.4% | -46.9% | 30.2% |
| `eps_start=10`, `max_steps=100` | 5 | +5.3% | +55.2% | 30.2% |
| `eps_start=0.5`, `lr_schedule=linear` | 5 | +7.9% | -83.3% | 45.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
