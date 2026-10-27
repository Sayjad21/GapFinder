# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 18:57 · 150 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +82.8% | +82.8% | ±11.3% | — |

## C1: mean_reward (paper 94.93)
**Unexplained** · gap +82.8% → +82.8% · 57 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (57 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 173.5 over 5 runs; repeats: 179.9, 178.8, 173.5, 172.5, 167.2
- Spread: range 167.2 to 179.9, noise band ±10.7 (2 x MAD), CV 2.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +82.8% (noise band ±11.3% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (6.93 noise units, gap +4.6%); `lr=0.002` (6.4 noise units, gap -10.6%); `lr=0.02` (6.13 noise units, gap -13.6%); `lr=1` (6.1 noise units, gap +14.0%); `lr=0.01` (5.62 noise units, gap -19.4%) (and 9 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=inv`: this claim -6.6%, mean |gap| 18.4% (3 runs)
  - `lr_schedule=linear`, `max_steps=100`: this claim +1.6%, mean |gap| 22.3% (3 runs)
  - `max_steps=100`: this claim +4.8%, mean |gap| 27.1% (4 runs)

### History matching (every measured configuration, all claims together)
- 4 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.94); lr_schedule=inv, max_steps=100 (max I 1.59)
  - `eps_start, lr, lr_schedule, max_steps`: eps_start=0.2, lr=1, lr_schedule=inv, max_steps=100 (max I 2.01)
  - `max_steps`: max_steps=100 (max I 2.16)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100; max_steps=100 | eps_start=0.2, lr=1, lr_schedule=inv, max_steps=100

Notes:
- {'lr': '1'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr': '1'} (gap +2.8%); it did not pass verification
- history matching: 4 of 57 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=inv` | 3 | -6.6% | -30.1% | 18.4% |
| `lr_schedule=linear`, `max_steps=100` | 3 | +1.6% | +43.1% | 22.3% |
| `max_steps=100` | 4 | +4.8% | +49.3% | 27.1% |
| `lr=1`, `max_steps=100`, `eps_start=0.2`, `lr_schedule=inv` | 3 | +5.0% | +51.4% | 28.2% |
| `lr_schedule=inv` | 4 | +42.4% | -24.3% | 33.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
