# Gap Report: test-gen-02

Artifact `rlbench` · generated 2026-10-14 21:41 · 17 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +194.7% | +194.7% | ±36.7% | — |

## C1: mean_reward (paper 59.35)
**Unexplained** · gap +194.7% → +194.7% · 2 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (2 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 59.4 on CartPole; the worst of its seeds reaches 9.8.

- p. 1; value used: `mean_reward` = 59.35 reward (headline claim)

### What did we measure?
- Naive median 174.9 over 5 runs; repeats: 189.4, 162.5, 174.9, 185.8, 168
- Spread: range 162.5 to 189.4, noise band ±21.78 (2 x MAD), CV 6.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +194.7% (noise band ±36.7% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `--eps_start`, `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +119.8%, mean |gap| 227.8% (6 runs)
  - `lr_schedule=linear`: this claim +185.0%, mean |gap| 761.9% (6 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, among 2 tested

Notes:
- closest configuration tried: {'lr_schedule': 'inv'} (gap +119.8%); it did not pass verification
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C1, among 2 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 6 | +119.8% | +335.8% | 227.8% |
| naive (reproduction as run) | 5 | +194.7% | +561.9% | 378.3% |
| `lr_schedule=linear` | 6 | +185.0% | +1338.8% | 761.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--eps_start`, `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `634d827f07d6659ff82f6ea0924c8ba487e9d02a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `1a857c206acd3466452a9528e9062b12b02985097be7506b73503e6215db6beb`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
