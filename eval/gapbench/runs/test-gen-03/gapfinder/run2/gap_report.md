# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-10 21:11 · 22 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | -43.7% | -43.7% | ±7.9% | — |

## C1: mean_reward (paper 302.05)
**Unexplained** · gap -43.7% → -43.7% · 5 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (5 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 169.9 over 5 runs; repeats: 181.8, 164.4, 169.9, 155.1, 183.9
- Spread: range 155.1 to 183.9, noise band ±23.85 (2 x MAD), CV 7.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -43.7% (noise band ±7.9% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (4.54 noise units, gap -7.9%)
- Near alternatives (closest across all claims):
  - `max_steps=500`: this claim -7.9%, mean |gap| 36.8% (5 runs)
  - `max_steps=1000`: this claim +46.1%, mean |gap| 54.6% (5 runs)
  - `lr_schedule=linear`, `max_steps=500`: this claim -35.7%, mean |gap| 133.7% (5 runs)

Notes:
- {'max_steps': '500'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'max_steps': '500'} (gap -7.9%); it did not pass verification

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | -43.7% | +11.2% | 27.5% |
| `max_steps=500` | 5 | -7.9% | -65.8% | 36.8% |
| `max_steps=1000` | 5 | +46.1% | -63.2% | 54.6% |
| `lr_schedule=linear`, `max_steps=500` | 5 | -35.7% | +231.6% | 133.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0672, sandbox reported $0.0000 (total $0.0672; this search; ledger extraction is included only if it shared the search's router)
