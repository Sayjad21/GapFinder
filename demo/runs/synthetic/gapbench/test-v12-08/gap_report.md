# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-23 18:03 · 160 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +79.0% | -3.5% | ±5.7% | `max_steps=100` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`min_reward`): paper 95.4, measured 50.75 (-46.8%, band ±46.3%)

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +79.0% → -3.5% · 34 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0023`, `B0028`, `B0029`, `B0070`, `B0071`, `B0072` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `03c104ac-d8cc-4dec-8934-01df1d551f1d` and run
  ```
  RUN_TAG=ecaa1ff126c1 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 94.41, 99.72, 99.73, 95.19, 95.32, 94.3; gap after -3.5%; result checkpoint `ba2ccbe4-abf3-4beb-b93d-bfcfb3ff75a7`
- Effect: candidate 95.26 minus naive 176.7 = -81.43, 95% bootstrap interval [-96.81, -67.75] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 176.7 over 5 runs; repeats: 176.7, 173.9, 197.9, 162.1, 176.7
- Spread: range 162.1 to 197.9, noise band ±5.62 (2 x MAD), CV 7.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +79.0% (noise band ±5.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +79.0% (it comes back)
- PASS · Held-out claim: C2: -46.8% to -39.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -81.43 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.01` (11.9 noise units, gap -11.3%); `lr=1` (10.05 noise units, gap -21.8%); `lr=0.5` (9.06 noise units, gap +27.5%); `lr_schedule=inv` (8.52 noise units, gap +30.5%); `max_steps=10000` (7.69 noise units, gap +35.3%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=0.5`, `max_steps=100`: this claim +1.3%, mean |gap| 3.1% (6 runs)
  - `lr_schedule=inv`: this claim +30.3%, mean |gap| 42.9% (6 runs)
  - `lr=0.02`: this claim -9.5%, mean |gap| 48.3% (6 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr=1`
- `lr=0.5, max_steps=100`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting max_steps=100 | settings | 59% | 0.7 sigma (fits every claim) | run with max_steps=100 |
| 2 | the setting lr=0.5, max_steps=100 | settings | 25% | 0.1 sigma (fits every claim) | run with lr=0.5, max_steps=100 |
| 3 | the setting lr=1, max_steps=10000 | settings | 4% | 1.1 sigma (fits every claim) | run with lr=1, max_steps=10000 |

### History matching (every measured configuration, all claims together)
- 12 of 34 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.14); lr=1, max_steps=100 (max I 1.05); lr=1, max_steps=10000 (max I 1.15); lr=0.5, max_steps=10000 (max I 1.2)
  - `max_steps`: max_steps=100 (max I 0.66)
  - `lr_schedule, max_steps`: lr_schedule=inv, max_steps=100 (max I 1.32)
  - `lr, lr_schedule`: lr=0.01, lr_schedule=inv (max I 2.12)
  - `lr`: lr=1 (max I 2.13); lr=0.02 (max I 2.13); lr=0.01 (max I 2.14)

Notes:
- its runs spread 0.3x the naive run's noise band (reported, not used to judge)
- configurations the target claim can't tell apart from the answer: max_steps=100; lr=1; lr=0.5, max_steps=100
- spec knobs no ledger assumption names (episodes, eps_decay, eps_end, eps_start, eval_episodes, gamma, init_q, omega_bins, reward_norm, seeds, theta_bins) were screened too; no better answer
- max_steps: values from 100 to 100 fit every claim (a bisection, 3 runs a side, one run a value: approximate)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=0.5`, `max_steps=100` | 6 | +1.3% | +4.8% | 3.1% |
| `max_steps=100` | 6 | -3.5% | -39.1% | 21.3% |
| `lr_schedule=inv` | 6 | +30.3% | -55.5% | 42.9% |
| `lr=0.02` | 6 | -9.5% | -87.1% | 48.3% |
| `lr=0.01`, `lr_schedule=inv` | 6 | -12.1% | -86.7% | 49.4% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `28b211d810d1b9d96fc05d215b47c832dfb18c6d18bc5a8b475d528ad9c3b24a`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
