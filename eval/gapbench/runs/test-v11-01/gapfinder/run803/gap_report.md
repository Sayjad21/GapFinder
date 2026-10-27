# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 23:32 · 164 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -51.4% | +0.7% | ±3.8% | `max_steps=1000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -51.4% → +0.7% · 50 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0034`, `B0035`, `B0062`, `B0063`, `B0064` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `13654922-c7e2-4fe9-9616-ced2c4bc47a4` and run
  ```
  RUN_TAG=dc0791d38e5c "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 399.4, 254.4, 312.3, 403.1, 273.3, 469.3; gap after +0.7%; result checkpoint `650a545a-1fc3-49c4-9d67-eb3c7881226b`
- Effect: candidate 355.9 minus naive 171.8 = +184.1, 95% bootstrap interval [+82.01, +279.1] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 171.8 over 5 runs; repeats: 165.1, 194.8, 171.8, 167.6, 182
- Spread: range 165.1 to 194.8, noise band ±13.32 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -51.4% (noise band ±3.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -51.4% (it comes back)
- PASS · Held-out claim: C2: +24.2% to -22.3% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +184.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (8.04 noise units, gap +21.1%); `max_steps=2000` (4.29 noise units, gap -35.2%); `max_steps=400` (2.55 noise units, gap -41.8%); `init_q=0` (1.8 noise units, gap -44.6%); `gamma=0.995` (1.67 noise units, gap -45.1%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=1000`, `init_q=-1.0`: this claim +4.4%, mean |gap| 5.3% (5 runs)
  - `max_steps=500`, `init_q=-1.0`: this claim -9.2%, mean |gap| 8.2% (5 runs)
  - `max_steps=2000`: this claim +8.6%, mean |gap| 16.0% (6 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=1000` (reported)
- `max_steps=10000`
- `max_steps=2000`
- `init_q=-1.0, max_steps=1000`
- `init_q=-1.0, max_steps=500`

### History matching (every measured configuration, all claims together)
- 10 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=1000 (max I 0.07); max_steps=10000 (max I 1.02); max_steps=500 (max I 1.57)
  - `init_q, max_steps`: init_q=-1.0, max_steps=1000 (max I 0.16); init_q=0, max_steps=1000 (max I 0.48); init_q=0, max_steps=500 (max I 0.9); init_q=-1.0, max_steps=500 (max I 2.16)
  - `gamma, max_steps`: gamma=0.995, max_steps=1000 (max I 1.53); gamma=0.995, max_steps=500 (max I 1.73); gamma=0.998, max_steps=500 (max I 2.19)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=1000; max_steps=10000; max_steps=2000; init_q=-1.0, max_steps=1000; init_q=-1.0, max_steps=500

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000`, `init_q=-1.0` | 5 | +4.4% | +6.2% | 5.3% |
| `max_steps=500`, `init_q=-1.0` | 5 | -9.2% | -7.2% | 8.2% |
| `max_steps=1000` | 6 | +0.7% | -22.3% | 11.5% |
| `max_steps=2000` | 6 | +8.6% | +23.4% | 16.0% |
| `max_steps=10000` | 6 | -17.5% | -22.7% | 20.1% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The argument --init_q expects a floating‑point number, but the supplied value 'zero' cannot be parsed as a float, causing the program to reject it; retried as `init_q=0`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
