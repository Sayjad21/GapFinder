# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 01:02 · 128 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +52.2% | +2.7% | ±3.5% | `lr_schedule=inv` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +52.2% → +2.7% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0026`, `B0049`, `B0050`, `B0052` (4 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `fd3933fe-3aaa-4f8d-87f3-e32a2dd18dd6` and run
  ```
  RUN_TAG=89f40a037619 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 144.2, 132.8, 111.5, 103.9; gap after +2.7%; result checkpoint `09ba2a6a-5666-43a8-8f1b-13bf4d6f29b8`
- Effect: candidate 122.1 minus naive 181 = -58.86, 95% bootstrap interval [-85.4, -47.25] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 181 over 5 runs; repeats: 195.1, 180.2, 185.5, 178.9, 181
- Spread: range 178.9 to 195.1, noise band ±4.11 (2 x MAD), CV 3.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +52.2% (noise band ±3.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +52.2% (it comes back)
- PASS · Held-out claim: C2: -19.1% to -54.9% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -58.86 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=1` (14.37 noise units, gap -2.5%); `theta_bins=30` (12.41 noise units, gap -9.3%); `eps_end=0.01` (1.34 noise units, gap +47.5%); `eps_end=0.81` (1.12 noise units, gap +48.3%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `theta_bins=12`: this claim +15.5%, mean |gap| 18.9% (3 runs)
  - `lr_schedule=inv`, `theta_bins=8`: this claim +7.7%, mean |gap| 23.7% (3 runs)
  - `lr_schedule=inv`, `eps_end=0.01`: this claim +30.2%, mean |gap| 23.8% (3 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=inv` (reported)
- `theta_bins=30`
- `eps_end=0.905, theta_bins=1`
- `eps_end=0.01, theta_bins=30`
- `lr_schedule=inv, theta_bins=8`
- `eps_end=0.01, theta_bins=1`
- `eps_end=0.81, theta_bins=1`
- `eps_end=0.01, lr_schedule=inv`
- `lr_schedule=inv, theta_bins=12`

### History matching (every measured configuration, all claims together)
- 7 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 0.29)
  - `lr_schedule`: lr_schedule=inv (max I 0.75)
  - `eps_end, theta_bins`: eps_end=0.81, theta_bins=1 (max I 1.03); eps_end=0.905, theta_bins=1 (max I 1.04); eps_end=0.01, theta_bins=30 (max I 1.41); eps_end=0.01, theta_bins=1 (max I 1.74)
  - `theta_bins`: theta_bins=30 (max I 2.11)
- 2 separate islands (no single-knob move joins them): eps_end=0.81, theta_bins=1; eps_end=0.905, theta_bins=1; eps_end=0.01, theta_bins=30 | lr_schedule=inv, theta_bins=8; lr_schedule=inv

Notes:
- configurations the target claim can't tell apart from the answer: lr_schedule=inv; theta_bins=30; eps_end=0.905, theta_bins=1; eps_end=0.01, theta_bins=30; lr_schedule=inv, theta_bins=8; eps_end=0.01, theta_bins=1; eps_end=0.81, theta_bins=1; eps_end=0.01, lr_schedule=inv; lr_schedule=inv, theta_bins=12

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `theta_bins=12` | 3 | +15.5% | +22.2% | 18.9% |
| `lr_schedule=inv`, `theta_bins=8` | 3 | +7.7% | -39.6% | 23.7% |
| `lr_schedule=inv`, `eps_end=0.01` | 3 | +30.2% | -17.5% | 23.8% |
| `theta_bins=12` | 4 | +46.4% | +10.2% | 28.3% |
| `lr_schedule=inv` | 4 | +2.7% | -54.9% | 28.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
