# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 20:59 · 180 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -50.6% | +9.1% | ±8.0% | `max_steps=2000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -50.6% → +9.1% · 45 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0013`, `B0042`, `B0043`, `B0074`, `B0075`, `B0076` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `2000`
- Command:

  Replay: fork checkpoint `6be73a1c-b998-428e-8d59-823e9038ba50` and run
  ```
  RUN_TAG=5e9e4989c8dc "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 2000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 398.7, 372.1, 465, 272.7, 239, 617; gap after +9.1%; result checkpoint `45a72fa4-f6ae-47f8-9d58-aaec0c4b872a`
- Effect: candidate 385.4 minus naive 174.6 = +210.8, 95% bootstrap interval [+74.9, +415] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 174.6 over 5 runs; repeats: 174.6, 144.4, 160.4, 189.2, 174.7
- Spread: range 144.4 to 189.2, noise band ±28.42 (2 x MAD), CV 10.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -50.6% (noise band ±8.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -50.6% (it comes back)
- PASS · Held-out claim: C2: +42.7% to -35.8% (not worse beyond noise)
- FAIL · Evidence: `max_steps=2000`: no evidence mentions '2000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +210.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (5.49 noise units, gap -6.4%); `max_steps=10000` (3.6 noise units, gap -21.7%); `max_steps=1000` (3.46 noise units, gap -22.8%)
- Near alternatives (closest across all claims):
  - `max_steps=10000`: this claim +3.5%, mean |gap| 8.3% (6 runs)
  - `gamma=0.995`, `max_steps=10000`: this claim -11.8%, mean |gap| 11.8% (2 runs)
  - `gamma=1.0`, `max_steps=2000`: this claim -15.2%, mean |gap| 21.6% (2 runs)

### Equally good configurations
The target claim can't tell these 7 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=2000` (reported)
- `max_steps=10000`
- `max_steps=1000`
- `max_steps=500`
- `gamma=0.998, max_steps=400`
- `gamma=0.999, max_steps=10000`
- `gamma=1.0, max_steps=10000`

### History matching (every measured configuration, all claims together)
- 14 of 45 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=1000 (max I 1.11); max_steps=10000 (max I 1.31); max_steps=2000 (max I 1.98)
  - `gamma, max_steps`: gamma=0.995, max_steps=10000 (max I 1.83); gamma=0.999, max_steps=1000 (max I 1.87); gamma=1.0, max_steps=400 (max I 1.88); gamma=0.998, max_steps=1000 (max I 1.94); +3 more
- Equally good values: `max_steps` in {500, 1000, 2000, 10000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=2000; max_steps=10000; max_steps=1000; max_steps=500; gamma=0.998, max_steps=400; gamma=0.999, max_steps=10000; gamma=1.0, max_steps=10000
- equally good values within one noise band (measured): max_steps in {500, 1000, 2000, 10000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=10000` | 6 | +3.5% | +13.1% | 8.3% |
| `gamma=0.995`, `max_steps=10000` | 2 | -11.8% | +11.9% | 11.8% |
| `gamma=1.0`, `max_steps=2000` | 2 | -15.2% | -28.0% | 21.6% |
| `max_steps=2000` | 6 | +9.1% | -35.8% | 22.4% |
| `max_steps=400` | 6 | -19.4% | +35.6% | 27.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
