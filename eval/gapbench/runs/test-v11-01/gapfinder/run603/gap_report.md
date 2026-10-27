# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 22:31 · 196 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -51.5% | -1.4% | ±1.9% | `max_steps=1000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -51.5% → -1.4% · 51 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0037`, `B0038`, `B0039`, `B0040`, `B0041` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `35ac3a5d-644b-4fbb-beb4-341d419d3eee` and run
  ```
  RUN_TAG=bf48c2a31718 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 466.5, 327.8, 276, 208, 394.7, 368.9; gap after -1.4%; result checkpoint `4fee3df7-cd8d-4241-8723-718c857dac3c`
- Effect: candidate 348.4 minus naive 171.3 = +177.1, 95% bootstrap interval [+54.82, +221.5] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 171.3 over 5 runs; repeats: 167.9, 174.1, 186.6, 171.3, 153.6
- Spread: range 153.6 to 186.6, noise band ±6.86 (2 x MAD), CV 7.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -51.5% (noise band ±1.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -51.5% (it comes back)
- PASS · Held-out claim: C2: +30.4% to -20.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +177.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (24.53 noise units, gap -3.9%); `max_steps=400` (17.78 noise units, gap -17.0%); `max_steps=2000` (4.09 noise units, gap -43.6%); `init_q=0` (2.98 noise units, gap -45.8%); `gamma=1.0` (2.96 noise units, gap -45.8%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=500`, `gamma=0.995`: this claim -2.7%, mean |gap| 11.4% (5 runs)
  - `init_q=-1.0`, `max_steps=500`: this claim -23.5%, mean |gap| 12.4% (5 runs)
  - `max_steps=400`, `gamma=0.995`: this claim -21.1%, mean |gap| 12.9% (5 runs)

### Equally good configurations
The target claim can't tell these 7 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=1000` (reported)
- `max_steps=500`
- `max_steps=2000`
- `max_steps=10000`
- `gamma=0.995, max_steps=500`
- `init_q=0, max_steps=500`
- `init_q=-1.0, max_steps=500`

### History matching (every measured configuration, all claims together)
- 9 of 50 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `max_steps`: max_steps=1000 (max I 0.68); max_steps=2000 (max I 1.3); max_steps=10000 (max I 1.64); max_steps=400 (max I 2.3); +1 more
  - `init_q, max_steps`: init_q=0, max_steps=500 (max I 2.23)
  - `gamma, max_steps`: gamma=1.0, max_steps=400 (max I 2.28); gamma=0.999, max_steps=1000 (max I 2.56); gamma=0.995, max_steps=500 (max I 2.59)
- Equally good values: `max_steps` in {1000, 2000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=1000; max_steps=500; max_steps=2000; max_steps=10000; gamma=0.995, max_steps=500; init_q=0, max_steps=500; init_q=-1.0, max_steps=500
- equally good values within one noise band (measured): max_steps in {1000, 2000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 6 | -1.4% | -20.1% | 10.7% |
| `max_steps=500`, `gamma=0.995` | 5 | -2.7% | +20.2% | 11.4% |
| `init_q=-1.0`, `max_steps=500` | 5 | -23.5% | -1.3% | 12.4% |
| `max_steps=400`, `gamma=0.995` | 5 | -21.1% | +4.6% | 12.9% |
| `max_steps=2000` | 6 | -2.3% | +26.8% | 14.5% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The argument --init_q expects a floating‑point number, but the supplied value 'zero' cannot be parsed as a float, causing the program to reject it; retried as `init_q=0`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
