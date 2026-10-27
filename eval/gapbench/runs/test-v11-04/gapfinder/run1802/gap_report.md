# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 19:46 · 200 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +80.4% | +1.9% | ±16.8% | `lr=1` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +80.4% → +1.9% · 57 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0019`, `B0062`, `B0063`, `B0077`, `B0078`, `B0079` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `1`
- Command:

  Replay: fork checkpoint `e0d4625f-1539-4f4a-af7c-99db8caaf95f` and run
  ```
  RUN_TAG=c2de02b960ca "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 98.88, 59.05, 94.54, 100.7, 64.07, 109.8; gap after +1.9%; result checkpoint `c34b6cb7-691d-4019-a937-ec7ece9fcdd9`
- Effect: candidate 96.71 minus naive 171.2 = -74.54, 95% bootstrap interval [-119.1, -65.27] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 171.2 over 5 runs; repeats: 189.2, 163.3, 189.3, 168.5, 171.2
- Spread: range 163.3 to 189.3, noise band ±15.95 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +80.4% (noise band ±16.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +80.4% (it comes back)
- PASS · Held-out claim: C2: +0.5% to -76.9% (not worse beyond noise)
- FAIL · Evidence: `lr=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -74.54 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.05` (4.72 noise units, gap -1.1%); `max_steps=100` (4.47 noise units, gap +5.2%); `eps_start=0.5` (3.89 noise units, gap +15.0%); `lr=0.002` (3.54 noise units, gap -21.0%); `lr=0.02` (3.13 noise units, gap -27.8%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim -2.2%, mean |gap| 17.1% (6 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -8.5%, mean |gap| 22.8% (5 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.4%, mean |gap| 23.4% (5 runs)

### Equally good configurations
The target claim can't tell these 16 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=1` (reported)
- `max_steps=100`
- `lr=0.05`
- `eps_start=0.2`
- `lr=0.02`
- `eps_start=0.5`
- `lr_schedule=linear, max_steps=100`
- `lr_schedule=inv, max_steps=100`
- `lr=0.05, lr_schedule=inv`
- `eps_start=0.5, lr=1`
- `eps_start=0.5, lr_schedule=linear`
- `eps_start=0.5, lr_schedule=inv`
- `eps_start=0.2, lr=1`
- `eps_start=0.5, lr=0.05`
- `lr=0.05, lr_schedule=linear`
- `lr=0.05, max_steps=100`

### History matching (every measured configuration, all claims together)
- 18 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=100 (max I 0.29)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.31); lr_schedule=inv, max_steps=100 (max I 0.63)
  - `lr, lr_schedule`: lr=0.05, lr_schedule=inv (max I 1.17)
  - `eps_start, lr`: eps_start=0.5, lr=1 (max I 1.22); eps_start=0.2, lr=1 (max I 1.4); eps_start=0.5, lr=0.05 (max I 1.6)
  - `lr`: lr=1 (max I 1.26)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=inv (max I 1.28); eps_start=0.5, lr_schedule=linear (max I 1.28)
- 2 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100 | eps_start=0.5, lr_schedule=inv; eps_start=0.5, lr_schedule=linear

Notes:
- configurations the target claim can't tell apart from the answer: lr=1; max_steps=100; lr=0.05; eps_start=0.2; lr=0.02; eps_start=0.5; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100; lr=0.05, lr_schedule=inv; eps_start=0.5, lr=1; eps_start=0.5, lr_schedule=linear; eps_start=0.5, lr_schedule=inv; eps_start=0.2, lr=1; eps_start=0.5, lr=0.05; lr=0.05, lr_schedule=linear; lr=0.05, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | -2.2% | -32.0% | 17.1% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -8.5% | -37.2% | 22.8% |
| `max_steps=100`, `lr_schedule=linear` | 5 | +2.4% | +44.5% | 23.4% |
| `max_steps=100`, `lr=0.05` | 5 | -16.6% | -52.3% | 34.5% |
| `lr=1` | 6 | +1.9% | -76.9% | 39.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
