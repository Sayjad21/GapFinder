# Gap Report: test-gen-02

Artifact `rlbench` · generated 2026-10-15 19:36 · 23 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +227.3% | +227.3% | ±7.7% | — |

## C1: mean_reward (paper 59.35)
**Unexplained** · gap +227.3% → +227.3% · 5 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (5 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 59.4 on CartPole; the worst of its seeds reaches 9.8.

- p. 1; value used: `mean_reward` = 59.35 reward (headline claim)

### What did we measure?
- Naive median 194.2 over 5 runs; repeats: 187.4, 196.5, 196, 194.2, 180.1
- Spread: range 180.1 to 196.5, noise band ±4.56 (2 x MAD), CV 3.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +227.3% (noise band ±7.7% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `eps_start`, `hardware_cpu`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (12.79 noise units, gap +129.0%); `reward_norm=on` (9.63 noise units, gap +153.2%); `lr_schedule=linear` (7.4 noise units, gap +170.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +143.6%, mean |gap| 177.9% (4 runs)
  - `lr_schedule=inv`, `reward_norm=on`: this claim +121.6%, mean |gap| 225.8% (3 runs)
  - `reward_norm=on`: this claim +207.0%, mean |gap| 359.8% (4 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, among 5 tested

Notes:
- closest configuration tried: {'lr_schedule': 'inv', 'reward_norm': 'on'} (gap +121.6%); it did not pass verification
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C1, among 5 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 4 | +143.6% | +212.2% | 177.9% |
| `lr_schedule=inv`, `reward_norm=on` | 3 | +121.6% | +329.9% | 225.8% |
| `reward_norm=on` | 4 | +207.0% | +512.7% | 359.8% |
| `lr_schedule=linear` | 4 | +170.6% | +1273.6% | 722.1% |
| naive (reproduction as run) | 5 | +227.3% | +1525.9% | 876.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `eps_start`, `hardware_cpu`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `1a857c206acd3466452a9528e9062b12b02985097be7506b73503e6215db6beb`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
