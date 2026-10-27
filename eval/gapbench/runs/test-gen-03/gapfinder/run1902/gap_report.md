# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-15 19:37 · 91 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -40.8% | +4.4% | ±11.3% | `max_steps=1000` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -40.8% → +4.4% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0020`, `B0021`, `B0047`, `B0048`, `B0049` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `9a18c687-67c5-4d11-aa90-70d6a22b70b5` and run
  ```
  RUN_TAG=7f9ebcfc525c "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 375.6, 397.5, 301.1, 280.6, 287.6, 329.3; gap after +4.4%; result checkpoint `7e3c5cfc-5100-4735-b235-b2387986e730`
- Effect: candidate 315.2 minus naive 178.8 = +136.5, 95% bootstrap interval [+98.78, +207.8] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 178.8 over 5 runs; repeats: 197.2, 182.8, 157.2, 178.8, 161.7
- Spread: range 157.2 to 197.2, noise band ±34.02 (2 x MAD), CV 9.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -40.8% (noise band ±11.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -40.8% (it comes back)
- PASS · Held-out claim: C2: -61.8% to -7.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +136.5 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (2.62 noise units, gap +11.3%); `max_steps=2000` (1.58 noise units, gap +23.0%); `max_steps=400` (1.37 noise units, gap -25.4%)
- Near alternatives (closest across all claims):
  - `max_steps=400`: this claim -15.2%, mean |gap| 14.8% (6 runs)
  - `max_steps=500`: this claim +6.2%, mean |gap| 17.6% (6 runs)
  - `max_steps=2000`: this claim +44.4%, mean |gap| 34.6% (6 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=1000` (reported)
- `max_steps=400`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=500 (max I 0.54); max_steps=1000 (max I 1.46); max_steps=400 (max I 2.6)
- Equally good values: `max_steps` in {400, 500, 1000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=1000; max_steps=400
- equally good values within one noise band (measured): max_steps in {400, 500, 1000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 6 | +4.4% | -7.1% | 5.7% |
| `max_steps=400` | 6 | -15.2% | +14.4% | 14.8% |
| `max_steps=500` | 6 | +6.2% | +28.9% | 17.6% |
| `max_steps=2000` | 6 | +44.4% | +24.9% | 34.6% |
| `max_steps=10000` | 6 | +34.7% | +67.8% | 51.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
