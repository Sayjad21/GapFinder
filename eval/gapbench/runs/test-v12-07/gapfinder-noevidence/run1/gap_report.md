# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 07:31 · 23 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +85.9% | +37.0% | ±5.7% | `lr_schedule=inv` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +85.9% → +37.0% · 5 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0012`, `B0013`, `B0014` (4 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `bc5d9619-acd0-4dd7-97b2-b6324f1131f3` and run
  ```
  RUN_TAG=28ef06a59e6d "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 140.1, 135.2, 135.3, 120.9; gap after +37.0%; result checkpoint `559e9e50-4cae-4777-803d-812549cc6569`
- Effect: candidate 135.2 minus naive 183.5 = -48.28, 95% bootstrap interval [-62.37, -41.76] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 183.5 over 5 runs; repeats: 176.6, 174.2, 185.4, 183.5, 186.3
- Spread: range 174.2 to 186.3, noise band ±5.58 (2 x MAD), CV 3.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +85.9% (noise band ±5.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +85.9% (it comes back)
- PASS · Held-out claim: C2: -43.1% to -82.5% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -48.28 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (5.25 noise units, gap +56.2%); `reward_norm=on` (2.51 noise units, gap +71.7%)
- Near alternatives (closest across all claims):
  - `reward_norm=on`: this claim +70.2%, mean |gap| 43.3% (4 runs)
  - `reward_norm=on`, `lr_schedule=inv`: this claim +32.9%, mean |gap| 52.1% (3 runs)
  - `lr_schedule=linear`: this claim +73.1%, mean |gap| 59.9% (4 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=inv` (reported)
- `lr_schedule=inv, reward_norm=on`

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, among 5 tested

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- configurations the target claim can't tell apart from the answer: lr_schedule=inv; lr_schedule=inv, reward_norm=on

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `reward_norm=on` | 4 | +70.2% | -16.3% | 43.3% |
| `reward_norm=on`, `lr_schedule=inv` | 3 | +32.9% | -71.4% | 52.1% |
| `lr_schedule=inv` | 4 | +37.0% | -82.5% | 59.8% |
| `lr_schedule=linear` | 4 | +73.1% | +46.6% | 59.9% |
| `lr_schedule=linear`, `reward_norm=on` | 3 | +70.6% | +49.3% | 59.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
