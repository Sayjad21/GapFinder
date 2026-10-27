# Gap Report: test-v12-05

Artifact `rlbench` · generated 2026-10-15 19:03 · 17 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +76.6% | +37.1% | ±38.6% | `lr_schedule=inv` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +76.6% → +37.1% · 2 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0013`, `B0014`, `B0015`, `B0016`, `B0017` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `4749f7b4-dea1-43a6-80f3-d470d6f0555f` and run
  ```
  RUN_TAG=9dbd06fff33f "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 124, 146.6, 118.2, 113.2, 148.6, 148; gap after +37.1%; result checkpoint `969bc253-0024-47fc-90cc-08e2f2b82346`
- Effect: candidate 135.3 minus naive 174.3 = -39.05, 95% bootstrap interval [-60.83, -15.17] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 174.3 over 5 runs; repeats: 198.3, 174.3, 152.1, 179.1, 155.3
- Spread: range 152.1 to 198.3, noise band ±38.11 (2 x MAD), CV 11.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +76.6% (noise band ±38.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +76.6% (it comes back)
- PASS · Held-out claim: C2: -52.9% to -62.6% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -39.05 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `max_steps`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`: this claim +76.7%, mean |gap| 69.8% (6 runs)

### History matching (every measured configuration, all claims together)
- 1 of 2 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 6 | +37.1% | -62.6% | 49.8% |
| naive (reproduction as run) | 5 | +76.6% | -52.9% | 64.8% |
| `lr_schedule=linear` | 6 | +76.7% | +62.9% | 69.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `max_steps`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
