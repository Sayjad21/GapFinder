# Gap Report: test-v12-05

Artifact `rlbench` · generated 2026-10-15 19:03 · 17 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +90.9% | +40.2% | ±17.6% | `lr_schedule=inv` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +90.9% → +40.2% · 2 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0013`, `B0014`, `B0015`, `B0016`, `B0017` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `a7d7a552-1b69-4117-8850-f16a13a81358` and run
  ```
  RUN_TAG=a3d7698730cb "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 105.5, 152.9, 121.7, 138.1, 159.1, 138.7; gap after +40.2%; result checkpoint `0bbf3621-d7ea-4c11-9afa-28ce977b563f`
- Effect: candidate 138.4 minus naive 188.4 = -50, 95% bootstrap interval [-57.95, -5.324] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1; value used: `mean_reward` = 98.685 reward (headline claim)

### What did we measure?
- Naive median 188.4 over 5 runs; repeats: 197.1, 166.5, 188.4, 134.4, 192.5
- Spread: range 134.4 to 197.1, noise band ±17.36 (2 x MAD), CV 14.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +90.9% (noise band ±17.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +90.9% (it comes back)
- PASS · Held-out claim: C2: +41.5% to -66.5% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -50 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `--max_steps`, `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (2.6 noise units, gap +45.1%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`: this claim +53.6%, mean |gap| 37.7% (6 runs)

### History matching (every measured configuration, all claims together)
- 1 of 2 tested configurations fit every claim within 3 sigma
- Equally good values: `lr_schedule` in {inv, linear}

Notes:
- equally good values within one noise band (measured): lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear` | 6 | +53.6% | -21.9% | 37.7% |
| `lr_schedule=inv` | 6 | +40.2% | -66.5% | 53.4% |
| naive (reproduction as run) | 5 | +90.9% | +41.5% | 66.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--max_steps`, `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
