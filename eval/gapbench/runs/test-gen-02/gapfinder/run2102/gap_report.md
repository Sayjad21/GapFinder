# Gap Report: test-gen-02

Artifact `rlbench` · generated 2026-10-15 20:52 · 17 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +201.0% | +201.0% | ±18.0% | — |

## C1: mean_reward (paper 59.35)
**Unexplained** · gap +201.0% → +201.0% · 2 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (2 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 59.4 on CartPole; the worst of its seeds reaches 9.8.

- p. 1; value used: `mean_reward` = 59.35 reward (headline claim)

### What did we measure?
- Naive median 178.6 over 5 runs; repeats: 178.6, 167.3, 164.4, 184, 182.5
- Spread: range 164.4 to 184, noise band ±10.71 (2 x MAD), CV 5.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +201.0% (noise band ±18.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `--eps_start`, `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (3.47 noise units, gap +138.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +132.8%, mean |gap| 300.4% (6 runs)
  - `lr_schedule=linear`: this claim +183.3%, mean |gap| 741.5% (6 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, C2, among 2 tested

Notes:
- closest configuration tried: {'lr_schedule': 'inv'} (gap +132.8%); it did not pass verification
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C1, C2, among 2 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 6 | +132.8% | +468.0% | 300.4% |
| naive (reproduction as run) | 5 | +201.0% | +423.4% | 312.2% |
| `lr_schedule=linear` | 6 | +183.3% | +1299.7% | 741.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--eps_start`, `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `1a857c206acd3466452a9528e9062b12b02985097be7506b73503e6215db6beb`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
