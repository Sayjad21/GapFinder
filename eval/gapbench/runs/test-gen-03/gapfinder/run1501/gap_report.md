# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-15 19:13 · 99 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -40.8% | +6.6% | ±5.5% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -40.8% → +6.6% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0038`, `B0039`, `B0040` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `8f20c315-2a16-47e4-ac02-74cfa1380d03` and run
  ```
  RUN_TAG=faf95c8b6c68 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 342.9, 260.7, 290.3, 363.7, 301.2, 352.1; gap after +6.6%; result checkpoint `179d228a-6ab0-476e-b824-93171e05f911`
- Effect: candidate 322 minus naive 178.7 = +143.3, 95% bootstrap interval [+83.94, +175.6] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 178.7 over 5 runs; repeats: 178.7, 170.4, 196.3, 193.1, 178.2
- Spread: range 170.4 to 196.3, noise band ±16.6 (2 x MAD), CV 6.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -40.8% (noise band ±5.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -40.8% (it comes back)
- PASS · Held-out claim: C2: +171.3% to +26.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +143.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (7.27 noise units, gap +0.9%); `max_steps=2000` (6.18 noise units, gap -6.9%); `max_steps=400` (2.86 noise units, gap -25.1%)
- Near alternatives (closest across all claims):
  - `max_steps=2000`: this claim -7.9%, mean |gap| 4.4% (6 runs)
  - `max_steps=1000`: this claim +1.7%, mean |gap| 13.4% (6 runs)
  - `max_steps=400`: this claim -15.2%, mean |gap| 15.6% (6 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=500` (reported)
- `max_steps=400`
- `max_steps=1000`

### History matching (every measured configuration, all claims together)
- 4 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `max_steps`: max_steps=500 (max I 0.99); max_steps=2000 (max I 1.73); max_steps=400 (max I 1.92)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=2000 (max I 2.78)
- Equally good values: `max_steps` in {500, 1000, 2000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=500; max_steps=400; max_steps=1000
- equally good values within one noise band (measured): max_steps in {500, 1000, 2000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=2000` | 6 | -7.9% | +0.8% | 4.4% |
| `max_steps=1000` | 6 | +1.7% | -25.1% | 13.4% |
| `max_steps=400` | 6 | -15.2% | -16.0% | 15.6% |
| `max_steps=500` | 6 | +6.6% | +26.0% | 16.3% |
| `max_steps=10000` | 6 | +22.2% | -17.7% | 19.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
