# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 20:59 · 122 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -50.5% | -2.6% | ±2.4% | `max_steps=500` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -50.5% → -2.6% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0010`, `B0036`, `B0037`, `B0054` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `8925f41e-cde0-45c7-b015-7a92f23d1575` and run
  ```
  RUN_TAG=61adc2884194 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 380.2, 352.5, 335.7, 266.8; gap after -2.6%; result checkpoint `6b4867aa-756d-4f4e-a314-fb54b96004b6`
- Effect: candidate 344.1 minus naive 175 = +169.1, 95% bootstrap interval [+89.55, +183.6] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 175 over 5 runs; repeats: 177.6, 166.4, 179.3, 175, 166.4
- Spread: range 166.4 to 179.3, noise band ±8.47 (2 x MAD), CV 3.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -50.5% (noise band ±2.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -50.5% (it comes back)
- PASS · Held-out claim: C2: +20.3% to +8.7% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +169.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (17.69 noise units, gap +8.1%); `max_steps=400` (10.44 noise units, gap -25.4%); `gamma=0.999` (2.56 noise units, gap -44.3%); `gamma=0.995` (1.39 noise units, gap -47.2%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim -5.5%, mean |gap| 8.7% (4 runs)
  - `max_steps=1000`, `gamma=0.995`: this claim -10.3%, mean |gap| 9.9% (2 runs)
  - `max_steps=1000`, `gamma=0.999`: this claim +11.2%, mean |gap| 12.3% (2 runs)

### Equally good configurations
The target claim can't tell these 7 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=500` (reported)
- `max_steps=1000`
- `gamma=0.999, max_steps=500`
- `gamma=0.995, max_steps=500`
- `gamma=0.998, max_steps=1000`
- `gamma=0.999, max_steps=400`
- `gamma=0.998, max_steps=400`

### History matching (every measured configuration, all claims together)
- 10 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=1000 (max I 0.4); max_steps=500 (max I 1.08)
  - `gamma, max_steps`: gamma=0.998, max_steps=1000 (max I 1.25); gamma=0.999, max_steps=500 (max I 1.4); gamma=0.995, max_steps=500 (max I 1.56); gamma=0.998, max_steps=500 (max I 1.81); +4 more

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=500; max_steps=1000; gamma=0.999, max_steps=500; gamma=0.995, max_steps=500; gamma=0.998, max_steps=1000; gamma=0.999, max_steps=400; gamma=0.998, max_steps=400

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 4 | -2.6% | +8.7% | 5.6% |
| `max_steps=1000` | 4 | -5.5% | -12.0% | 8.7% |
| `max_steps=1000`, `gamma=0.995` | 2 | -10.3% | -9.4% | 9.9% |
| `max_steps=1000`, `gamma=0.999` | 2 | +11.2% | -13.4% | 12.3% |
| `max_steps=500`, `gamma=0.995` | 3 | -12.6% | +22.5% | 17.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
