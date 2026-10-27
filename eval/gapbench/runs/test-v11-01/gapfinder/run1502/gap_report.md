# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 19:19 · 127 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -45.1% | -4.0% | ±1.4% | `max_steps=1000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -45.1% → -4.0% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0017`, `B0050`, `B0051`, `B0058` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `81d5266b-08ac-4945-937c-69146ac1bccc` and run
  ```
  RUN_TAG=cced70d97455 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 379, 226.1, 424.7, 299.9; gap after -4.0%; result checkpoint `4535e525-9897-4c62-b3ee-bc4faa28f441`
- Effect: candidate 339.4 minus naive 194 = +145.5, 95% bootstrap interval [+30.74, +240] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 194 over 5 runs; repeats: 183.1, 194, 180.8, 195.5, 196.5
- Spread: range 180.8 to 196.5, noise band ±4.97 (2 x MAD), CV 3.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -45.1% (noise band ±1.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -45.1% (it comes back)
- PASS · Held-out claim: C2: +279.9% to +44.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +145.5 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=2000` (23.24 noise units, gap -12.4%); `max_steps=400` (19.77 noise units, gap -17.3%); `max_steps=10000` (12.7 noise units, gap +27.2%); `max_steps=500` (12.58 noise units, gap -27.4%)
- Near alternatives (closest across all claims):
  - `max_steps=10000`: this claim -1.5%, mean |gap| 4.4% (4 runs)
  - `max_steps=1000`, `gamma=0.995`: this claim +5.6%, mean |gap| 4.7% (3 runs)
  - `max_steps=400`: this claim -27.3%, mean |gap| 13.8% (4 runs)

### Equally good configurations
The target claim can't tell these 10 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=1000` (reported)
- `max_steps=500`
- `max_steps=10000`
- `max_steps=2000`
- `gamma=0.995, max_steps=400`
- `gamma=0.995, max_steps=1000`
- `gamma=0.998, max_steps=2000`
- `gamma=1.0, max_steps=400`
- `gamma=0.999, max_steps=1000`
- `gamma=0.999, max_steps=2000`

### History matching (every measured configuration, all claims together)
- 7 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `gamma, max_steps`: gamma=0.995, max_steps=1000 (max I 0.56); gamma=0.995, max_steps=400 (max I 1.42); gamma=1.0, max_steps=400 (max I 1.54); gamma=0.999, max_steps=400 (max I 1.77); +2 more
  - `max_steps`: max_steps=1000 (max I 1.14)
- Equally good values: `max_steps` in {1000, 10000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=1000; max_steps=500; max_steps=10000; max_steps=2000; gamma=0.995, max_steps=400; gamma=0.995, max_steps=1000; gamma=0.998, max_steps=2000; gamma=1.0, max_steps=400; gamma=0.999, max_steps=1000; gamma=0.999, max_steps=2000
- equally good values within one noise band (measured): max_steps in {1000, 10000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=10000` | 4 | -1.5% | +7.3% | 4.4% |
| `max_steps=1000`, `gamma=0.995` | 3 | +5.6% | +3.8% | 4.7% |
| `max_steps=400` | 4 | -27.3% | -0.4% | 13.8% |
| `gamma=0.999`, `max_steps=10000` | 2 | -20.7% | -10.8% | 15.8% |
| `gamma=0.999`, `max_steps=400` | 3 | -11.2% | -22.0% | 16.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
