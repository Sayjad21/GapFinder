# Gap Report: test-gen-02

Artifact `rlbench` · generated 2026-10-12 23:11 · 19 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +180.7% | +180.7% | ±74.2% | — |

## C1: mean_reward (paper 59.35)
**Unexplained** · gap +180.7% → +180.7% · 6 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (6 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 59.4 on CartPole; the worst of its seeds reaches 9.8.

- p. 1; value used: `mean_reward` = 59.35 reward (headline claim)

### What did we measure?
- Naive median 166.6 over 5 runs; repeats: 144.6, 166.6, 178.8, 136.8, 198.2
- Spread: range 136.8 to 198.2, noise band ±44.04 (2 x MAD), CV 15.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +180.7% (noise band ±74.2% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `eps_start`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (1.09 noise units, gap +100.1%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `init_q=0`: this claim +105.4%, mean |gap| 179.6% (5 runs)
  - `lr_schedule=inv`: this claim +121.2%, mean |gap| 239.8% (5 runs)

Notes:
- closest configuration tried: {'lr_schedule': 'inv', 'init_q': '0'} (gap +105.4%); it did not pass verification

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | +180.7% | +123.4% | 152.0% |
| `lr_schedule=inv`, `init_q=0` | 5 | +105.4% | +253.8% | 179.6% |
| `lr_schedule=inv` | 5 | +121.2% | +358.4% | 239.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The argument --init_q expects a numeric float; 'zero' is not a valid float literal. Using '0' (or '0.0') provides the same intent of initializing Q-values to zero, and '0' is a distinct valid value from the default '0.0' already measured; retried as `init_q=0`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `eps_start`

## Provenance
- GapFinder commit: `56779a9cc2cef642dbf91ede59da97a848c305cd` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `16ad3c4a71eefac5fc45f4c9a201b3fc6f51a0c3cef30e8c3ea67682f56fab21`
- Cost: Nemotron billed $0.0376, sandbox reported $0.0000 (total $0.0376; this search; ledger extraction is included only if it shared the search's router)
