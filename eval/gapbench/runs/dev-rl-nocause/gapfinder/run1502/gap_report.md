# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 19:11 · 140 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +50.2% | -16.9% | ±17.1% | `theta_bins=30` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +50.2% → -16.9% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0039`, `B0040`, `B0050`, `B0051`, `B0052` (6 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `30`
- Command:

  Replay: fork checkpoint `0ae27e1e-48cb-4b45-9161-90badb4a38be` and run
  ```
  RUN_TAG=8fdea63e06a1 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 30 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 123.8, 65.14, 100, 83.53, 113.2, 97.53; gap after -16.9%; result checkpoint `698836c1-7137-4b40-a822-2eb1f240fccc`
- Effect: candidate 98.78 minus naive 178.6 = -79.82, 95% bootstrap interval [-114.9, -61.27] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 178.6 over 5 runs; repeats: 187.2, 156.2, 168.4, 178.6, 198.4
- Spread: range 156.2 to 198.4, noise band ±20.33 (2 x MAD), CV 9.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +50.2% (noise band ±17.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +50.2% (it comes back)
- PASS · Held-out claim: C2: -7.3% to -78.0% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=30`: no evidence mentions '30'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -79.82 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (2.64 noise units, gap +5.1%)
- Near alternatives (closest across all claims):
  - `theta_bins=4`, `lr_schedule=inv`: this claim +35.1%, mean |gap| 18.7% (5 runs)
  - `lr_schedule=inv`, `eps_end=0.1`: this claim +7.3%, mean |gap| 28.0% (5 runs)
  - `lr_schedule=inv`, `eps_end=0.025`: this claim -1.8%, mean |gap| 28.9% (5 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `theta_bins=30` (reported)
- `lr_schedule=inv`
- `eps_end=0.025, theta_bins=1`
- `eps_end=0.1, theta_bins=30`
- `eps_end=0.025, lr_schedule=inv`
- `eps_end=0.1, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 29 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, lr_schedule`: eps_end=0.025, lr_schedule=inv (max I 0.85); eps_end=0.1, lr_schedule=inv (max I 0.92); eps_end=0.905, lr_schedule=inv (max I 2.1); eps_end=0.025, lr_schedule=linear (max I 2.1)
  - `lr_schedule`: lr_schedule=inv (max I 0.94)
  - `eps_end, theta_bins`: eps_end=0.1, theta_bins=30 (max I 1.03); eps_end=0.025, theta_bins=1 (max I 1.22); eps_end=0.025, theta_bins=30 (max I 2.12)
  - `theta_bins`: theta_bins=30 (max I 1.84)
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=3 (max I 2.14)
- Equally good values: `theta_bins` in {1, 30}

Notes:
- configurations the target claim can't tell apart from the answer: theta_bins=30; lr_schedule=inv; eps_end=0.025, theta_bins=1; eps_end=0.1, theta_bins=30; eps_end=0.025, lr_schedule=inv; eps_end=0.1, lr_schedule=inv
- equally good values within one noise band (measured): theta_bins in {1, 30}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `theta_bins=4`, `lr_schedule=inv` | 5 | +35.1% | -2.2% | 18.7% |
| `lr_schedule=inv`, `eps_end=0.1` | 5 | +7.3% | -48.7% | 28.0% |
| naive (reproduction as run) | 5 | +50.2% | -7.3% | 28.7% |
| `lr_schedule=inv`, `eps_end=0.025` | 5 | -1.8% | -56.1% | 28.9% |
| `theta_bins=8` | 6 | +55.1% | +17.5% | 36.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
