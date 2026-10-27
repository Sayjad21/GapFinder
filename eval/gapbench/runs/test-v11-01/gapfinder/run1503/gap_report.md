# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 19:18 · 97 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -45.2% | -13.1% | ±2.9% | `max_steps=1000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -45.2% → -13.1% · 50 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0034`, `B0035`, `B0052` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `a9f6fd14-57f3-4798-b5ed-4480d39f4d09` and run
  ```
  RUN_TAG=f794de1a57a6 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 247, 500.4, 307.5, 306.6; gap after -13.1%; result checkpoint `cc46cc9c-3c38-4c2f-b64d-e75bf3c2f8a5`
- Effect: candidate 307.1 minus naive 193.7 = +113.4, 95% bootstrap interval [+109.4, +317.1] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 193.7 over 5 runs; repeats: 194.9, 193.7, 198.8, 175.6, 186.8
- Spread: range 175.6 to 198.8, noise band ±10.19 (2 x MAD), CV 4.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -45.2% (noise band ±2.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -45.2% (it comes back)
- PASS · Held-out claim: C2: +287.1% to -26.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +113.4 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (13.17 noise units, gap -7.2%); `max_steps=500` (10.52 noise units, gap -14.9%); `max_steps=2000` (7.42 noise units, gap -23.8%)
- Near alternatives (closest across all claims):
  - `init_q=1.0`, `max_steps=500`: this claim +0.3%, mean |gap| 13.2% (3 runs)
  - `init_q=1.0`, `max_steps=400`: this claim -18.4%, mean |gap| 15.5% (2 runs)
  - `max_steps=2000`: this claim +15.2%, mean |gap| 17.8% (4 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=1000` (reported)
- `max_steps=2000`
- `max_steps=400`
- `max_steps=500`
- `init_q=1.0, max_steps=500`
- `gamma=1.0, max_steps=400`
- `gamma=0.995, max_steps=500`
- `init_q=-1.0, max_steps=500`

### History matching (every measured configuration, all claims together)
- 6 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `init_q, max_steps`: init_q=1.0, max_steps=500 (max I 0.54); init_q=-1.0, max_steps=500 (max I 2.88)
  - `max_steps`: max_steps=1000 (max I 0.7); max_steps=2000 (max I 2.5); max_steps=500 (max I 2.93)
  - `gamma, max_steps`: gamma=0.995, max_steps=500 (max I 1.61)
- Equally good values: `max_steps` in {400, 1000, 2000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=1000; max_steps=2000; max_steps=400; max_steps=500; init_q=1.0, max_steps=500; gamma=1.0, max_steps=400; gamma=0.995, max_steps=500; init_q=-1.0, max_steps=500
- equally good values within one noise band (measured): max_steps in {400, 1000, 2000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `init_q=1.0`, `max_steps=500` | 3 | +0.3% | -26.2% | 13.2% |
| `init_q=1.0`, `max_steps=400` | 2 | -18.4% | -12.6% | 15.5% |
| `max_steps=2000` | 4 | +15.2% | -20.5% | 17.8% |
| `max_steps=400`, `gamma=0.995` | 2 | -17.1% | +19.0% | 18.1% |
| `max_steps=1000` | 4 | -13.1% | -26.0% | 19.6% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The argument --init_q expects a floating‑point number, but the supplied value 'zero' cannot be parsed as a float, causing the program to reject it; retried as `init_q=0`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
