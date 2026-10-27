# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 20:59 · 191 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -48.0% | -4.4% | ±1.6% | `max_steps=2000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -48.0% → -4.4% · 45 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0013`, `B0042`, `B0043`, `B0074`, `B0075`, `B0076` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `2000`
- Command:

  Replay: fork checkpoint `9caeb0f6-23ca-489a-b9eb-a6f91e9315e1` and run
  ```
  RUN_TAG=c9ddef0830a7 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 2000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 118, 485.3, 294.9, 381.1, 614.7, 242.2; gap after -4.4%; result checkpoint `664025e0-ea44-4317-81cf-1e376adbcd10`
- Effect: candidate 338 minus naive 183.8 = +154.2, 95% bootstrap interval [+80.66, +417.3] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 183.8 over 5 runs; repeats: 185.1, 183.8, 146.4, 155.6, 186.6
- Spread: range 146.4 to 186.6, noise band ±5.56 (2 x MAD), CV 11.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -48.0% (noise band ±1.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -48.0% (it comes back)
- PASS · Held-out claim: C2: +94.7% to -26.9% (not worse beyond noise)
- FAIL · Evidence: `max_steps=2000`: no evidence mentions '2000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +154.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (30.46 noise units, gap +0.1%); `max_steps=500` (25.05 noise units, gap +8.6%); `max_steps=1000` (21.45 noise units, gap -14.2%); `gamma=1.0` (2.55 noise units, gap -44.0%); `gamma=0.998` (2.52 noise units, gap -44.0%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`, `gamma=0.995`: this claim +11.5%, mean |gap| 8.0% (5 runs)
  - `gamma=1.0`, `max_steps=400`: this claim -11.7%, mean |gap| 9.5% (2 runs)
  - `max_steps=1000`: this claim -15.9%, mean |gap| 9.8% (6 runs)

### Equally good configurations
The target claim can't tell these 14 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=2000` (reported)
- `max_steps=500`
- `max_steps=400`
- `max_steps=10000`
- `gamma=0.998, max_steps=500`
- `gamma=0.999, max_steps=500`
- `gamma=1.0, max_steps=500`
- `gamma=0.995, max_steps=1000`
- `gamma=0.999, max_steps=400`
- `gamma=0.998, max_steps=400`
- `gamma=1.0, max_steps=1000`
- `gamma=1.0, max_steps=2000`
- `gamma=0.995, max_steps=500`
- `gamma=1.0, max_steps=400`

### History matching (every measured configuration, all claims together)
- 11 of 45 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=2000 (max I 0.16)
  - `gamma, max_steps`: gamma=1.0, max_steps=500 (max I 0.72); gamma=0.995, max_steps=1000 (max I 0.96); gamma=0.999, max_steps=500 (max I 1.26); gamma=1.0, max_steps=400 (max I 1.73); +5 more

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=2000; max_steps=500; max_steps=400; max_steps=10000; gamma=0.998, max_steps=500; gamma=0.999, max_steps=500; gamma=1.0, max_steps=500; gamma=0.995, max_steps=1000; gamma=0.999, max_steps=400; gamma=0.998, max_steps=400; gamma=1.0, max_steps=1000; gamma=1.0, max_steps=2000; gamma=0.995, max_steps=500; gamma=1.0, max_steps=400

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000`, `gamma=0.995` | 5 | +11.5% | -4.5% | 8.0% |
| `gamma=1.0`, `max_steps=400` | 2 | -11.7% | +7.3% | 9.5% |
| `max_steps=1000` | 6 | -15.9% | +3.6% | 9.8% |
| `max_steps=400` | 6 | -18.1% | -5.5% | 11.8% |
| `max_steps=500`, `gamma=0.995` | 5 | -12.6% | +11.5% | 12.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
