# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 18:46 · 168 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +50.4% | +50.4% | ±8.5% | — |

## C1: mean_reward (paper 118.924)
**Unexplained** · gap +50.4% → +50.4% · 53 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (53 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 178.9 over 5 runs; repeats: 173.8, 181.3, 178.9, 169.1, 196.9
- Spread: range 169.1 to 196.9, noise band ±10.1 (2 x MAD), CV 5.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +50.4% (noise band ±8.5% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=1` (5.6 noise units, gap -2.9%); `theta_bins=30` (3.75 noise units, gap -18.5%); `eps_end=0.1` (3.63 noise units, gap +19.6%); `lr_schedule=linear` (3.45 noise units, gap +21.1%); `lr_schedule=inv` (2.73 noise units, gap +27.2%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`: this claim +31.4%, mean |gap| 22.5% (6 runs)
  - `eps_end=0.525`, `theta_bins=4`: this claim +36.6%, mean |gap| 25.0% (2 runs)
  - `lr_schedule=inv`, `theta_bins=4`: this claim +6.2%, mean |gap| 27.7% (5 runs)

### History matching (every measured configuration, all claims together)
- 8 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `eps_end, theta_bins`: eps_end=0.1, theta_bins=30 (max I 1.34); eps_end=0.525, theta_bins=1 (max I 1.56); eps_end=0.1, theta_bins=3 (max I 2.1)
  - `theta_bins`: theta_bins=30 (max I 1.43); theta_bins=1 (max I 1.56)
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=4 (max I 1.69)
  - `eps_end, lr_schedule`: eps_end=0.1, lr_schedule=inv (max I 1.7)
  - `lr_schedule`: lr_schedule=inv (max I 2.92)
- 2 separate islands (no single-knob move joins them): eps_end=0.1, theta_bins=30; theta_bins=30; theta_bins=1 | lr_schedule=inv, theta_bins=4; eps_end=0.1, lr_schedule=inv; lr_schedule=inv

Notes:
- {'theta_bins': '30'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'theta_bins': '30'} (gap -6.3%); it did not pass verification
- history matching: 8 of 53 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear` | 6 | +31.4% | +13.6% | 22.5% |
| `eps_end=0.525`, `theta_bins=4` | 2 | +36.6% | -13.3% | 25.0% |
| naive (reproduction as run) | 5 | +50.4% | +1.6% | 26.0% |
| `lr_schedule=inv`, `theta_bins=4` | 5 | +6.2% | -49.2% | 27.7% |
| `eps_end=0.1`, `lr_schedule=inv` | 5 | +14.7% | -42.1% | 28.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
