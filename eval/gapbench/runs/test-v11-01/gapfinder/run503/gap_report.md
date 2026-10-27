# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 22:17 · 128 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -50.7% | -2.7% | ±4.3% | `max_steps=2000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -50.7% → -2.7% · 51 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0009`, `B0047`, `B0048`, `B0049`, `B0050`, `B0051` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `2000`
- Command:

  Replay: fork checkpoint `28556824-c16d-44fc-b17c-6b0fed0da24c` and run
  ```
  RUN_TAG=e9ef98120a7e "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 2000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 405.7, 262.8, 378.4, 377.8, 310, 293.1; gap after -2.7%; result checkpoint `473915ab-7dda-4cf8-8594-356ecd141864`
- Effect: candidate 343.9 minus naive 174.3 = +169.6, 95% bootstrap interval [+86.16, +202.1] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 174.3 over 5 runs; repeats: 166.6, 193.4, 174.1, 174.3, 185.8
- Spread: range 166.6 to 193.4, noise band ±15.32 (2 x MAD), CV 6.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -50.7% (noise band ±4.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -50.7% (it comes back)
- PASS · Held-out claim: C2: +9.5% to -57.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=2000`: no evidence mentions '2000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +169.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (9 noise units, gap -11.7%); `max_steps=1000` (7.74 noise units, gap -17.1%); `max_steps=500` (2.65 noise units, gap -39.2%); `gamma=1.0` (1.68 noise units, gap -43.4%); `gamma=0.998` (1.68 noise units, gap -43.4%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`, `init_q=1.0`: this claim -6.6%, mean |gap| 4.4% (5 runs)
  - `max_steps=10000`: this claim -4.5%, mean |gap| 10.2% (6 runs)
  - `max_steps=500`: this claim -23.1%, mean |gap| 16.0% (6 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=2000` (reported)
- `max_steps=1000`
- `init_q=1.0, max_steps=1000`
- `gamma=0.998, max_steps=2000`

### History matching (every measured configuration, all claims together)
- 4 of 50 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `max_steps`: max_steps=2000 (max I 0.82); max_steps=10000 (max I 1.26); max_steps=1000 (max I 2.83)
  - `init_q, max_steps`: init_q=1.0, max_steps=1000 (max I 2.82)
- Equally good values: `max_steps` in {2000, 10000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=2000; max_steps=1000; init_q=1.0, max_steps=1000; gamma=0.998, max_steps=2000
- equally good values within one noise band (measured): max_steps in {2000, 10000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000`, `init_q=1.0` | 5 | -6.6% | +2.2% | 4.4% |
| `max_steps=10000` | 6 | -4.5% | -15.9% | 10.2% |
| `max_steps=500` | 6 | -23.1% | -8.9% | 16.0% |
| `max_steps=400` | 6 | -13.5% | +24.5% | 19.0% |
| `max_steps=1000` | 6 | +23.4% | +31.7% | 27.5% |

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
