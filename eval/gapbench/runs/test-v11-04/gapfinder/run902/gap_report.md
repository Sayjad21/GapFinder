# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 23:49 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +76.9% | +76.9% | ±22.6% | — |

## C1: mean_reward (paper 94.93)
**Unexplained** · gap +76.9% → +76.9% · 57 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (57 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 167.9 over 5 runs; repeats: 183.4, 159.6, 191, 157.2, 167.9
- Spread: range 157.2 to 191, noise band ±21.47 (2 x MAD), CV 8.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +76.9% (noise band ±22.6% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=1` (3.37 noise units, gap -0.6%); `lr=0.02` (3.36 noise units, gap +0.9%); `max_steps=100` (3.33 noise units, gap -1.6%); `lr=0.002` (3.01 noise units, gap -8.9%); `eps_start=0.5` (2.86 noise units, gap +12.2%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -1.3%, mean |gap| 9.5% (5 runs)
  - `max_steps=100`: this claim -1.4%, mean |gap| 21.0% (6 runs)
  - `lr_schedule=inv`: this claim +48.5%, mean |gap| 29.8% (6 runs)

### History matching (every measured configuration, all claims together)
- 16 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.07); lr_schedule=inv, max_steps=100 (max I 1.34)
  - `max_steps`: max_steps=100 (max I 0.28)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 0.96)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.27)
  - `lr`: lr=0.01 (max I 1.5); lr=0.02 (max I 1.6); lr=1 (max I 1.64)
  - `lr, max_steps`: lr=1, max_steps=100 (max I 1.54)
  - `eps_start, lr`: eps_start=0.5, lr=1 (max I 1.58)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; max_steps=100; eps_start=0.5, max_steps=100 | eps_start=0.5, lr_schedule=linear; eps_start=0.5, lr_schedule=inv

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'eps_start': '0.5', 'lr_schedule': 'linear'} for 'confirm-combo')
- {'lr': '0.01'} (gap +0.0%) was verified from existing runs and rejected: {'lr': '0.01'} closes this claim but makes held-out claims worse; rejected
- {'max_steps': '100', 'lr_schedule': 'linear'} (gap -1.3%) was verified from existing runs and rejected: {'max_steps': '100'} closes this claim but makes held-out claims worse; rejected
- {'max_steps': '100'} (gap -1.4%) was verified from existing runs and rejected: {'max_steps': '100'} closes this claim but makes held-out claims worse; rejected
- history matching: 16 of 57 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | -1.3% | -17.8% | 9.5% |
| `max_steps=100` | 6 | -1.4% | -40.7% | 21.0% |
| `lr_schedule=inv` | 6 | +48.5% | -11.0% | 29.8% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -18.8% | -51.7% | 35.3% |
| `lr=0.01` | 6 | +0.0% | -77.0% | 38.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
