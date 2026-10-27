# Gap Report: test-gen-02

Artifact `rlbench` · generated 2026-10-15 19:12 · 18 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +200.4% | +200.4% | ±28.7% | — |

## C1: mean_reward (paper 59.35)
**Unexplained** · gap +200.4% → +200.4% · 5 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (5 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 59.4 on CartPole; the worst of its seeds reaches 9.8.

- p. 1; value used: `mean_reward` = 59.35 reward (headline claim)

### What did we measure?
- Naive median 178.3 over 5 runs; repeats: 177.3, 169.8, 188.1, 190.6, 178.3
- Spread: range 169.8 to 190.6, noise band ±17.03 (2 x MAD), CV 4.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +200.4% (noise band ±28.7% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `eps_start`, `hardware_cpu`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (1.25 noise units, gap +164.5%); `lr_schedule=linear` (1.02 noise units, gap +171.1%)
- Near alternatives (closest across all claims):
  - `reward_norm=on`, `lr_schedule=inv`: this claim +157.3%, mean |gap| 241.1% (3 runs)
  - `lr_schedule=inv`: this claim +165.2%, mean |gap| 675.6% (4 runs)
  - `lr_schedule=linear`: this claim +174.8%, mean |gap| 716.2% (4 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, among 5 tested

Notes:
- closest configuration tried: {'lr_schedule': 'inv'} (gap +165.2%); it did not pass verification
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C1, among 5 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `reward_norm=on`, `lr_schedule=inv` | 3 | +157.3% | +324.9% | 241.1% |
| naive (reproduction as run) | 5 | +200.4% | +499.5% | 350.0% |
| `lr_schedule=inv` | 4 | +165.2% | +1186.0% | 675.6% |
| `lr_schedule=linear` | 4 | +174.8% | +1257.6% | 716.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `eps_start`, `hardware_cpu`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `1a857c206acd3466452a9528e9062b12b02985097be7506b73503e6215db6beb`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
