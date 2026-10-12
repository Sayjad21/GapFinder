# Gap Report: test-gen-02

Artifact `rlbench` · generated 2026-10-12 23:43 · 15 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +209.3% | +209.3% | ±22.2% | — |

## C1: mean_reward (paper 59.35)
**Unexplained** · gap +209.3% → +209.3% · 2 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (2 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 59.4 on CartPole; the worst of its seeds reaches 9.8.

- p. 1; value used: `mean_reward` = 59.35 (headline claim)

### What did we measure?
- Naive median 183.5 over 5 runs; repeats: 164.9, 181.6, 183.5, 190.1, 200
- Spread: range 164.9 to 200, noise band ±13.17 (2 x MAD), CV 7.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +209.3% (noise band ±22.2% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `eps_start`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (2.63 noise units, gap +150.9%); `lr_schedule=linear` (2.04 noise units, gap +164.0%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +129.5%, mean |gap| 123.4% (5 runs)
  - `lr_schedule=linear`: this claim +169.5%, mean |gap| 456.8% (5 runs)

Notes:
- closest configuration tried: {'lr_schedule': 'inv'} (gap +129.5%); it did not pass verification

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 5 | +129.5% | +117.3% | 123.4% |
| `lr_schedule=linear` | 5 | +169.5% | +744.2% | 456.8% |
| naive (reproduction as run) | 5 | +209.3% | +925.9% | 567.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `eps_start`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `16ad3c4a71eefac5fc45f4c9a201b3fc6f51a0c3cef30e8c3ea67682f56fab21`
- Cost: Nemotron billed $0.0458, sandbox reported $0.0000 (total $0.0458; this search; ledger extraction is included only if it shared the search's router)
