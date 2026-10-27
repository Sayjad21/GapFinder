# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-16 01:50 · 137 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -46.3% | +4.8% | ±2.0% | `max_steps=10000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -46.3% → +4.8% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0027`, `B0066`, `B0067`, `B0068` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `10000`
- Command:

  Replay: fork checkpoint `1de69b8a-744b-41d5-9d1e-18f08efdda00` and run
  ```
  RUN_TAG=a7393626e2a7 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 10000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 441, 385.7, 355.3, 262.8; gap after +4.8%; result checkpoint `ee6271ae-5a2a-42fc-972d-e6d4268c738e`
- Effect: candidate 370.5 minus naive 189.7 = +180.9, 95% bootstrap interval [+70.7, +201.5] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 189.7 over 5 runs; repeats: 189.7, 192.5, 193.1, 180.8, 184.9
- Spread: range 180.8 to 193.1, noise band ±6.93 (2 x MAD), CV 2.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -46.3% (noise band ±2.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -46.3% (it comes back)
- PASS · Held-out claim: C2: +199.2% to -60.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=10000`: no evidence mentions '10000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +180.9 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (17.35 noise units, gap -12.3%); `max_steps=2000` (14.07 noise units, gap -18.8%); `max_steps=400` (12.32 noise units, gap -22.2%); `gamma=0.995` (1.49 noise units, gap -43.4%); `gamma=0.999` (1.27 noise units, gap -43.9%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim +5.7%, mean |gap| 8.2% (4 runs)
  - `max_steps=500`: this claim -12.1%, mean |gap| 8.5% (4 runs)
  - `gamma=0.995`, `max_steps=10000`: this claim -2.0%, mean |gap| 15.6% (3 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=10000` (reported)
- `max_steps=1000`
- `max_steps=500`
- `gamma=1.0, max_steps=500`
- `gamma=1.0, max_steps=400`
- `gamma=0.995, max_steps=500`
- `gamma=0.998, max_steps=500`
- `gamma=0.995, max_steps=10000`

### History matching (every measured configuration, all claims together)
- 10 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=10000 (max I 0.43); max_steps=2000 (max I 1.03); max_steps=1000 (max I 2.7)
  - `gamma, max_steps`: gamma=1.0, max_steps=400 (max I 1.37); gamma=1.0, max_steps=500 (max I 1.51); gamma=0.999, max_steps=500 (max I 2.21); gamma=0.998, max_steps=500 (max I 2.56); +3 more
- Equally good values: `max_steps` in {1000, 10000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=10000; max_steps=1000; max_steps=500; gamma=1.0, max_steps=500; gamma=1.0, max_steps=400; gamma=0.995, max_steps=500; gamma=0.998, max_steps=500; gamma=0.995, max_steps=10000
- equally good values within one noise band (measured): max_steps in {1000, 10000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 4 | +5.7% | -10.7% | 8.2% |
| `max_steps=500` | 4 | -12.1% | -4.9% | 8.5% |
| `gamma=0.995`, `max_steps=10000` | 3 | -2.0% | -29.3% | 15.6% |
| `gamma=1.0`, `max_steps=500` | 3 | +0.5% | +40.5% | 20.5% |
| `max_steps=2000` | 4 | -18.6% | +23.7% | 21.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
