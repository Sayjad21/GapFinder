# Gap Report: test-v12-05

Artifact `rlbench` · generated 2026-10-23 17:59 · 200 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +91.1% | +91.1% | ±4.9% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`min_reward`): paper 95.4, measured 136.1 (+42.7%, band ±14.5%)

## C1: mean_reward (paper 98.685)
**Unexplained** · gap +91.1% → +91.1% · 71 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (71 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1; value used: `mean_reward` = 98.685 reward (headline claim)

### What did we measure?
- Naive median 188.6 over 5 runs; repeats: 196.6, 188.6, 190.1, 171.1, 186.2
- Spread: range 171.1 to 196.6, noise band ±4.88 (2 x MAD), CV 5.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +91.1% (noise band ±4.9% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `--max_steps`, `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (9.64 noise units, gap +43.4%); `lr_schedule=linear` (4.76 noise units, gap +67.6%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`: this claim +64.6%, mean |gap| 39.4% (6 runs)
  - `lr=0.05`: this claim +28.9%, mean |gap| 41.4% (6 runs)
  - `omega_bins=4`: this claim +82.6%, mean |gap| 43.7% (3 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting theta_bins=30 | settings | 26% | 2.1 sigma (fits every claim) | run with theta_bins=30 |
| 2 | the setting lr=1 | settings | 23% | 2.4 sigma (fits every claim) | run with lr=1 |
| 3 | a cause outside every class tested | outside | 14% |  | look for code, data or evaluation differences the classes don't cover |

### History matching (every measured configuration, all claims together)
- 10 of 71 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `theta_bins`: theta_bins=30 (max I 2.1); theta_bins=1 (max I 2.93)
  - `lr`: lr=1 (max I 2.44)
  - `omega_bins`: omega_bins=2 (max I 2.53)
  - `eps_start`: eps_start=0.5 (max I 2.69)
  - `episodes`: episodes=20 (max I 2.79)
  - `eps_decay`: eps_decay=0.8 (max I 2.81); eps_decay=0.9 (max I 2.83); eps_decay=0.0 (max I 2.88)
  - `gamma`: gamma=0.8 (max I 2.98)
- 7 separate islands (no single-knob move joins them): eps_decay=0.8; eps_decay=0.9; eps_decay=0.0 | theta_bins=30; theta_bins=1 | lr=1 | omega_bins=2

Notes:
- closest configuration tried: {'lr_schedule': 'inv'} (gap +48.6%); it did not pass verification
- spec knobs no ledger assumption names (episodes, eps_decay, eps_end, eps_start, eval_episodes, gamma, init_q, lr, omega_bins, reward_norm, seeds, theta_bins) were screened too; no better answer
- history matching: 10 of 71 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear` | 6 | +64.6% | -14.2% | 39.4% |
| `lr=0.05` | 6 | +28.9% | -53.9% | 41.4% |
| `omega_bins=4` | 3 | +82.6% | +4.9% | 43.7% |
| `lr=1` | 6 | -7.8% | -80.2% | 44.0% |
| `omega_bins=2` | 6 | -11.4% | -78.0% | 44.7% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--max_steps`, `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `628b5c73850e927a9f4a60a62df08223407f68c2742e658344952145d44bf832`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
