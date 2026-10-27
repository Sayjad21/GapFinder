# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 00:34 · 157 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +83.7% | +4.6% | ±25.2% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +83.7% → +4.6% · 66 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0028`, `B0029`, `B0045`, `B0046`, `B0047` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `c8baca30-d20d-439e-bc4e-36dcac57ad68` and run
  ```
  RUN_TAG=a8c193555fff "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.1, 99.77, 99.47, 98.77, 97.16, 99.75; gap after +4.6%; result checkpoint `38ba8051-099e-40bb-9157-18bb69c1e9f4`
- Effect: candidate 99.28 minus naive 174.4 = -75.09, 95% bootstrap interval [-85, -52.94] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 (headline claim)

### What did we measure?
- Naive median 174.4 over 5 runs; repeats: 145.7, 176.2, 174.4, 186.6, 162.4
- Spread: range 145.7 to 186.6, noise band ±23.93 (2 x MAD), CV 9.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +83.7% (noise band ±25.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +83.7% (it comes back)
- PASS · Held-out claim: C2: -43.2% to +50.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -75.09 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (1.83 noise units, gap +37.5%); `lr_schedule=inv` (1.39 noise units, gap +48.6%); `eps_start=0.01` (1.35 noise units, gap -49.7%); `eps_start=0.2` (1.33 noise units, gap -50.2%); `eps_start=0.1` (1.13 noise units, gap -55.1%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +1.9%, mean |gap| 20.7% (5 runs)
  - `lr_schedule=inv`: this claim +48.6%, mean |gap| 38.1% (3 runs)
  - `lr_schedule=linear`, `eps_start=0.5`: this claim +5.4%, mean |gap| 43.1% (5 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `eps_start=0.2`
- `eps_start=0.5`
- `lr_schedule=linear, max_steps=100`
- `eps_start=0.5, lr_schedule=linear`
- `eps_start=0.5, lr_schedule=inv`
- `eps_start=0.2, max_steps=400`
- `eps_start=0.5, max_steps=100`

### History matching (every measured configuration, all claims together)
- 8 of 66 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.49); lr_schedule=inv, max_steps=100 (max I 1.91)
  - `max_steps`: max_steps=100 (max I 0.97)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.59); eps_start=0.5, lr_schedule=inv (max I 1.74)
  - `eps_start, max_steps`: eps_start=0.2, max_steps=400 (max I 1.75); eps_start=0.5, max_steps=100 (max I 2.01)
  - `eps_start`: eps_start=0.2 (max I 1.96)
- 3 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; max_steps=100; lr_schedule=inv, max_steps=100 | eps_start=0.5, lr_schedule=linear; eps_start=0.5, lr_schedule=inv | eps_start=0.2, max_steps=400; eps_start=0.2

Notes:
- lr_schedule dropped: with repeats, {'max_steps': '100', 'lr_schedule': 'linear'} fits {'max_steps': '100'}'s gap by less than one noise band, so it is not needed
- configurations the target claim can't tell apart from the answer: max_steps=100; eps_start=0.2; eps_start=0.5; lr_schedule=linear, max_steps=100; eps_start=0.5, lr_schedule=linear; eps_start=0.5, lr_schedule=inv; eps_start=0.2, max_steps=400; eps_start=0.5, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | +1.9% | +39.4% | 20.7% |
| `max_steps=100` | 6 | +4.6% | +50.1% | 27.4% |
| `lr_schedule=inv` | 3 | +48.6% | -27.5% | 38.1% |
| `lr_schedule=linear`, `eps_start=0.5` | 5 | +5.4% | -80.8% | 43.1% |
| `max_steps=100`, `eps_start=0.5` | 5 | -14.9% | -77.2% | 46.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
