# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 00:33 · 192 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -48.0% | -3.6% | ±7.7% | `max_steps=1000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -48.0% → -3.6% · 66 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0017`, `B0050`, `B0051`, `B0057`, `B0058`, `B0059` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `37a299a0-a665-4cca-98c9-0e4e0f2100cb` and run
  ```
  RUN_TAG=6672b0a6bc4e "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 365.1, 536.6, 316.4, 294.5, 284.4, 474.1; gap after -3.6%; result checkpoint `b88973f3-58e8-42e3-bc97-c950b41656bb`
- Effect: candidate 340.8 minus naive 183.8 = +157, 95% bootstrap interval [+103.8, +349] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 183.8 over 5 runs; repeats: 188.5, 165, 197.4, 183.8, 150.4
- Spread: range 150.4 to 197.4, noise band ±27.27 (2 x MAD), CV 10.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -48.0% (noise band ±7.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -48.0% (it comes back)
- PASS · Held-out claim: C2: +146.8% to -58.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +157 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (6.12 noise units, gap -0.7%); `max_steps=400` (2.58 noise units, gap -28.1%)
- Near alternatives (closest across all claims):
  - `max_steps=500`, `gamma=0.995`: this claim +1.7%, mean |gap| 6.1% (5 runs)
  - `gamma=0.998`, `max_steps=400`: this claim -7.2%, mean |gap| 8.5% (5 runs)
  - `max_steps=1000`, `gamma=0.995`: this claim -7.2%, mean |gap| 8.9% (5 runs)

### Equally good configurations
The target claim can't tell these 11 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=1000` (reported)
- `max_steps=500`
- `max_steps=400`
- `gamma=0.999, max_steps=400`
- `gamma=0.999, max_steps=500`
- `gamma=0.995, max_steps=500`
- `gamma=0.998, max_steps=400`
- `gamma=1.0, max_steps=500`
- `gamma=0.998, max_steps=500`
- `gamma=0.998, max_steps=1000`
- `gamma=0.999, max_steps=1000`

### History matching (every measured configuration, all claims together)
- 14 of 66 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `gamma, max_steps`: gamma=0.998, max_steps=500 (max I 0.57); gamma=0.995, max_steps=1000 (max I 0.75); gamma=0.999, max_steps=500 (max I 0.79); gamma=0.995, max_steps=500 (max I 0.83); +4 more
  - `max_steps`: max_steps=500 (max I 1.14); max_steps=1000 (max I 1.18)
- Equally good values: `max_steps` in {500, 1000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=1000; max_steps=500; max_steps=400; gamma=0.999, max_steps=400; gamma=0.999, max_steps=500; gamma=0.995, max_steps=500; gamma=0.998, max_steps=400; gamma=1.0, max_steps=500; gamma=0.998, max_steps=500; gamma=0.998, max_steps=1000; gamma=0.999, max_steps=1000
- equally good values within one noise band (measured): max_steps in {500, 1000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500`, `gamma=0.995` | 5 | +1.7% | +10.5% | 6.1% |
| `gamma=0.998`, `max_steps=400` | 5 | -7.2% | +9.7% | 8.5% |
| `max_steps=1000`, `gamma=0.995` | 5 | -7.2% | -10.6% | 8.9% |
| `max_steps=500` | 6 | -5.9% | +21.0% | 13.5% |
| `max_steps=1000`, `gamma=0.95` | 5 | -13.2% | -16.3% | 14.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
