# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 19:11 · 136 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +47.9% | +47.9% | ±32.7% | — |

## C1: mean_reward (paper 118.924)
**Unexplained** · gap +47.9% → +47.9% · 53 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (53 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 175.8 over 5 runs; repeats: 175.5, 198.1, 175.8, 195.3, 147.8
- Spread: range 147.8 to 198.1, noise band ±38.89 (2 x MAD), CV 11.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +47.9% (noise band ±32.7% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (1.08 noise units, gap +12.5%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +21.6%, mean |gap| 19.7% (6 runs)
  - `eps_end=0.005`, `lr_schedule=inv`: this claim +11.7%, mean |gap| 30.4% (5 runs)
  - `eps_end=0.0`, `lr_schedule=inv`: this claim +20.4%, mean |gap| 31.2% (5 runs)

### History matching (every measured configuration, all claims together)
- 37 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, theta_bins`: eps_end=0.0, theta_bins=30 (max I 0.91); eps_end=0.81, theta_bins=60 (max I 1.02); eps_end=0.525, theta_bins=1 (max I 1.24); eps_end=0.525, theta_bins=60 (max I 1.53); +1 more
  - `lr_schedule, theta_bins`: lr_schedule=linear, theta_bins=12 (max I 0.98); lr_schedule=inv, theta_bins=1 (max I 1.27); lr_schedule=inv, theta_bins=12 (max I 1.32)
  - `eps_end, lr_schedule`: eps_end=0.005, lr_schedule=inv (max I 1.16); eps_end=0.0, lr_schedule=inv (max I 1.37)

Notes:
- closest configuration tried: {'theta_bins': '1'} (gap -30.3%); it did not pass verification
- history matching: 37 of 53 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 6 | +21.6% | -17.7% | 19.7% |
| `eps_end=0.005`, `lr_schedule=inv` | 5 | +11.7% | -49.1% | 30.4% |
| `eps_end=0.0`, `lr_schedule=inv` | 5 | +20.4% | -42.0% | 31.2% |
| `theta_bins=60`, `eps_end=0.525` | 5 | +21.1% | -43.2% | 32.2% |
| `lr_schedule=linear`, `theta_bins=12` | 5 | +16.5% | -49.4% | 32.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
