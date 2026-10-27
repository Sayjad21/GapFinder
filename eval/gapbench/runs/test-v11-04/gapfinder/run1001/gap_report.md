# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 00:22 · 165 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +92.8% | +1.2% | ±7.5% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +92.8% → +1.2% · 67 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0030`, `B0031`, `B0054` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `3c03bae9-b048-4c86-ae99-d18715d67e6c` and run
  ```
  RUN_TAG=3624daa0fad5 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 92.08, 95.71, 96.52, 99.8; gap after +1.2%; result checkpoint `7e4f5d94-ed16-4b13-bb81-9bca7d0d416c`
- Effect: candidate 96.11 minus naive 183 = -86.92, 95% bootstrap interval [-99.15, -81.67] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 (headline claim)

### What did we measure?
- Naive median 183 over 5 runs; repeats: 196.6, 181.1, 183, 193.6, 179.5
- Spread: range 179.5 to 196.6, noise band ±7.15 (2 x MAD), CV 4.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +92.8% (noise band ±7.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +92.8% (it comes back)
- PASS · Held-out claim: C2: +25.7% to -1.7% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -86.92 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.2` (12.21 noise units, gap +0.9%); `lr_schedule=inv` (6.46 noise units, gap +44.1%); `eps_start=0.0` (6 noise units, gap -47.6%); `max_steps=40` (4.64 noise units, gap -57.9%); `eps_start=0.5` (4.01 noise units, gap +62.6%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +1.2%, mean |gap| 22.8% (3 runs)
  - `max_steps=100`, `eps_start=5`: this claim +5.1%, mean |gap| 28.9% (3 runs)
  - `max_steps=100`, `eps_start=2`: this claim +5.0%, mean |gap| 29.0% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`
- `eps_start=2, max_steps=100`

### History matching (every measured configuration, all claims together)
- 12 of 67 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=100 (max I 0.15)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.44); lr_schedule=inv, max_steps=100 (max I 1.48)
  - `eps_start, max_steps`: eps_start=2, max_steps=100 (max I 0.54); eps_start=5, max_steps=100 (max I 0.7); eps_start=50, max_steps=100 (max I 0.85); eps_start=10, max_steps=100 (max I 0.88); +2 more
  - `eps_start`: eps_start=0.2 (max I 1.43)
- 3 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; eps_start=2, max_steps=100 | eps_start=0.2, max_steps=500; eps_start=0.2, max_steps=400; eps_start=0.2 | eps_start=0.5, lr_schedule=inv

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100; eps_start=2, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 4 | +1.2% | -1.7% | 1.5% |
| `max_steps=100`, `lr_schedule=linear` | 3 | +1.2% | +44.4% | 22.8% |
| `max_steps=100`, `eps_start=5` | 3 | +5.1% | +52.7% | 28.9% |
| `max_steps=100`, `eps_start=2` | 3 | +5.0% | +52.9% | 29.0% |
| `max_steps=100`, `eps_start=50` | 3 | +5.3% | +56.4% | 30.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
