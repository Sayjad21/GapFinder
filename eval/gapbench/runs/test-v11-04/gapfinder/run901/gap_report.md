# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 23:47 · 99 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +86.7% | +1.7% | ±32.5% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +86.7% → +1.7% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0028`, `B0029`, `B0030`, `B0031`, `B0032` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `0ab5b594-db47-42a0-a110-cf68b4188246` and run
  ```
  RUN_TAG=ae9996d06b98 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.83, 98.99, 93.36, 96.4, 96.62, 91.73; gap after +1.7%; result checkpoint `cefb8497-e5f0-43e6-98f5-b12a7a472144`
- Effect: candidate 96.51 minus naive 177.2 = -80.69, 95% bootstrap interval [-93.24, -45.77] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 (headline claim)

### What did we measure?
- Naive median 177.2 over 5 runs; repeats: 192.6, 128.7, 177.2, 157.6, 184.1
- Spread: range 128.7 to 192.6, noise band ±30.87 (2 x MAD), CV 15.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +86.7% (noise band ±32.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +86.7% (it comes back)
- PASS · Held-out claim: C2: -74.0% to +4.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -80.69 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (2.15 noise units, gap +16.8%); `eps_start=0.1` (2.1 noise units, gap -18.5%); `eps_start=0.2` (1.77 noise units, gap -29.1%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.7%, mean |gap| 23.2% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -6.5%, mean |gap| 23.5% (5 runs)
  - `lr_schedule=linear`, `eps_start=0.5`: this claim -11.9%, mean |gap| 44.8% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`
- `lr_schedule=inv, max_steps=100`

### History matching (every measured configuration, all claims together)
- 39 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=100 (max I 0.19); max_steps=40 (max I 1.93)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.43); lr_schedule=inv, max_steps=100 (max I 0.49); lr_schedule=linear, max_steps=40 (max I 1.93)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.18); eps_start=0.5, lr_schedule=inv (max I 1.81)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.39)
  - `eps_start`: eps_start=0.2 (max I 1.64); eps_start=0.0 (max I 1.83)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +1.7% | +4.0% | 2.8% |
| `max_steps=100`, `lr_schedule=linear` | 5 | +2.7% | +43.6% | 23.2% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -6.5% | -40.5% | 23.5% |
| `lr_schedule=linear`, `eps_start=0.5` | 5 | -11.9% | -77.6% | 44.8% |
| `max_steps=100`, `eps_start=0.5` | 5 | -20.0% | -74.9% | 47.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
