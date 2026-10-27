# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-16 01:45 · 91 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -44.7% | -13.9% | ±9.8% | `max_steps=400` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -44.7% → -13.9% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0014`, `B0030`, `B0031`, `B0047`, `B0048`, `B0049` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Command:

  Replay: fork checkpoint `ad1d9a96-bbc2-41f2-9f72-754b306df3d7` and run
  ```
  RUN_TAG=31ef4e6b2adb "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 272.8, 230.4, 230.4, 247.6, 292, 297.5; gap after -13.9%; result checkpoint `bfe3827c-90eb-4579-b4d9-0fbd744218d9`
- Effect: candidate 260.2 minus naive 167 = +93.19, 95% bootstrap interval [+53.08, +136.8] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 167 over 5 runs; repeats: 152.3, 195.3, 167, 146.4, 174.8
- Spread: range 146.4 to 195.3, noise band ±29.45 (2 x MAD), CV 11.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -44.7% (noise band ±9.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -44.7% (it comes back)
- PASS · Held-out claim: C2: +0.9% to +10.4% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +93.19 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=2000` (3.24 noise units, gap -13.1%); `max_steps=500` (2.23 noise units, gap -22.9%); `max_steps=10000` (1.87 noise units, gap +26.4%); `max_steps=1000` (1.54 noise units, gap -29.7%)
- Near alternatives (closest across all claims):
  - `max_steps=500`: this claim +9.1%, mean |gap| 13.3% (6 runs)
  - `max_steps=2000`: this claim -12.1%, mean |gap| 16.8% (6 runs)
  - `max_steps=10000`: this claim +28.6%, mean |gap| 29.0% (6 runs)

### History matching (every measured configuration, all claims together)
- 4 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `max_steps`: max_steps=500 (max I 1.32); max_steps=1000 (max I 2.08); max_steps=400 (max I 2.08); max_steps=2000 (max I 2.2)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=400` | 6 | -13.9% | +10.4% | 12.1% |
| `max_steps=500` | 6 | +9.1% | +17.6% | 13.3% |
| `max_steps=2000` | 6 | -12.1% | -21.6% | 16.8% |
| naive (reproduction as run) | 5 | -44.7% | +0.9% | 22.8% |
| `max_steps=10000` | 6 | +28.6% | -29.4% | 29.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
