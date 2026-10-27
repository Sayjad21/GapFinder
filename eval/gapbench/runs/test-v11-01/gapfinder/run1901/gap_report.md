# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 19:42 · 188 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -50.8% | -6.3% | ±6.5% | `max_steps=400`, `gamma=0.999` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -50.8% → -6.3% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0132`, `B0162`, `B0180`, `B0181`, `B0182` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Config: `gamma` naive `0.99`, changed to `0.999`
- Command:

  Replay: fork checkpoint `5405fc73-d3d5-4aa9-8c11-750d40e875df` and run
  ```
  RUN_TAG=a3e00b2a77c9 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.999 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 327.2, 331.2, 346.8, 365.4, 295.1; gap after -6.3%; result checkpoint `8e787a1d-a577-40b5-a465-b94b04c31eed`
- Effect: candidate 331.2 minus naive 173.9 = +157.3, 95% bootstrap interval [+120.1, +186.4] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 173.9 over 5 runs; repeats: 169, 193.6, 173.9, 188.7, 162.5
- Spread: range 162.5 to 193.6, noise band ±22.88 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -50.8% (noise band ±6.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -46.7% (it comes back)
- PASS · Counterfactual (reversal test): without `gamma` the gap is -15.5% (it comes back)
- PASS · Held-out claim: C2: +12.1% to +119.7% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- FAIL · Evidence: `gamma=0.999`: no evidence mentions '0.999'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +157.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=2000` (6.49 noise units, gap +8.8%); `max_steps=500` (5.07 noise units, gap -17.9%); `max_steps=10000` (3.59 noise units, gap +27.5%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim +10.8%, mean |gap| 11.2% (6 runs)
  - `gamma=1.0`, `max_steps=10000`: this claim -16.9%, mean |gap| 17.4% (5 runs)
  - `gamma=0.995`, `max_steps=400`: this claim -16.6%, mean |gap| 18.3% (2 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `gamma=0.999, max_steps=400` (reported)
- `max_steps=1000`
- `max_steps=500`
- `gamma=0.999, max_steps=500`
- `gamma=1.0, max_steps=500`
- `gamma=1.0, max_steps=10000`

### History matching (every measured configuration, all claims together)
- 11 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `gamma, max_steps`: gamma=0.999, max_steps=500 (max I 1.28); gamma=0.999, max_steps=400 (max I 1.38); gamma=1.0, max_steps=500 (max I 2.02); gamma=1.0, max_steps=10000 (max I 2.12); +3 more
  - `max_steps`: max_steps=10000 (max I 1.33); max_steps=500 (max I 1.45); max_steps=400 (max I 2.48)
- Equally good values: `max_steps` in {400, 500}

Notes:
- configurations the target claim can't tell apart from the answer: gamma=0.999, max_steps=400; max_steps=1000; max_steps=500; gamma=0.999, max_steps=500; gamma=1.0, max_steps=500; gamma=1.0, max_steps=10000
- equally good values within one noise band (measured): max_steps in {400, 500}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 6 | +10.8% | +11.6% | 11.2% |
| `gamma=1.0`, `max_steps=10000` | 5 | -16.9% | +17.9% | 17.4% |
| `gamma=0.995`, `max_steps=400` | 2 | -16.6% | +20.1% | 18.3% |
| `max_steps=400` | 6 | -15.5% | +29.7% | 22.6% |
| `max_steps=2000` | 6 | +26.6% | -18.6% | 22.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
