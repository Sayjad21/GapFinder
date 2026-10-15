# Gap Report: test-v13-09

Artifact `rlbench` · generated 2026-10-16 01:02 · 116 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +80.7% | +0.2% | ±18.3% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Fits but unsupported** · gap +80.7% → +0.2% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0040`, `B0041`, `B0042` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `92775c6f-5dfd-448e-b012-14252e26bee3` and run
  ```
  RUN_TAG=ee7927045564 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 89.31, 99.96, 99.31, 99.97, 99.75, 99.73; gap after +0.2%; result checkpoint `2ea4a8fa-0d99-49be-9c96-b2476f0b11ce`
- Effect: candidate 99.74 minus naive 179.8 = -80.04, 95% bootstrap interval [-95.8, -64.94] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 179.8 over 5 runs; repeats: 175.6, 161.8, 188.9, 197.4, 179.8
- Spread: range 161.8 to 197.4, noise band ±18.19 (2 x MAD), CV 7.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +80.7% (noise band ±18.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +80.7% (it comes back)
- PASS · Held-out claim: C2: +11.0% to +0.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -80.04 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `theta_clip_low`, `theta_clip_high`, `omega_clip_low`, `omega_clip_high`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `init_state_low`, `init_state_high`, `theta_range`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (2.31 noise units, gap +38.5%); `max_steps=150` (1.7 noise units, gap +49.7%); `max_steps=40` (1.14 noise units, gap -59.8%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -3.8%, mean |gap| 17.6% (5 runs)
  - `max_steps=150`, `lr_schedule=linear`: this claim +41.3%, mean |gap| 34.7% (2 runs)
  - `lr_schedule=inv`, `max_steps=150`: this claim +17.1%, mean |gap| 36.9% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 5 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `max_steps`: max_steps=100 (max I 0.19)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.58); lr_schedule=inv, max_steps=150 (max I 1.44); lr_schedule=inv, max_steps=100 (max I 1.47); lr_schedule=inv, max_steps=2000 (max I 2.86)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +0.2% | +0.6% | 0.4% |
| `max_steps=100`, `lr_schedule=linear` | 5 | -3.8% | -31.4% | 17.6% |
| `max_steps=150`, `lr_schedule=linear` | 2 | +41.3% | +28.0% | 34.7% |
| `lr_schedule=inv`, `max_steps=150` | 5 | +17.1% | -56.7% | 36.9% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -11.9% | -65.7% | 38.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `theta_clip_low`, `theta_clip_high`, `omega_clip_low`, `omega_clip_high`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `init_state_low`, `init_state_high`, `theta_range`, `--out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
