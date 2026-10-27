# Gap Report: test-v12-05

Artifact `rlbench` · generated 2026-10-16 01:28 · 13 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +86.4% | +35.5% | ±7.0% | `lr_schedule=inv` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +86.4% → +35.5% · 2 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0011`, `B0012`, `B0013` (4 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `1df8dff3-5d2f-4daf-9518-e7c26055218f` and run
  ```
  RUN_TAG=817768491855 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 134.9, 132.4, 144, 129.9; gap after +35.5%; result checkpoint `fae97fb0-107e-4633-b7f1-ab97beb2739e`
- Effect: candidate 133.7 minus naive 184 = -50.32, 95% bootstrap interval [-54.34, -37.58] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1; value used: `mean_reward` = 98.685 reward (headline claim)

### What did we measure?
- Naive median 184 over 5 runs; repeats: 184.6, 177, 187.4, 178, 184
- Spread: range 177 to 187.4, noise band ±6.86 (2 x MAD), CV 2.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +86.4% (noise band ±7.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +86.4% (it comes back)
- PASS · Held-out claim: C2: +9.8% to -74.7% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -50.32 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `--max_steps`, `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (2.01 noise units, gap +72.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`: this claim +74.8%, mean |gap| 60.9% (4 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, among 2 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | +86.4% | +9.8% | 48.1% |
| `lr_schedule=inv` | 4 | +35.5% | -74.7% | 55.1% |
| `lr_schedule=linear` | 4 | +74.8% | +47.0% | 60.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--max_steps`, `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
