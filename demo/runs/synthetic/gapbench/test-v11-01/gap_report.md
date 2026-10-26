# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-23 17:49 · 184 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -47.5% | -2.7% | ±4.6% | `max_steps=500`, `gamma=0.999` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -47.5% → -2.7% · 34 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0135`, `B0167`, `B0168`, `B0169`, `B0170` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Config: `gamma` naive `0.99`, changed to `0.999`
- Command:

  Replay: fork checkpoint `95975355-8679-46fd-bdff-29834e17399a` and run
  ```
  RUN_TAG=c6aa3ea3d8be export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.999 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 467.5, 344, 245.5, 336.3, 388.3; gap after -2.7%; result checkpoint `565793a3-15ea-416b-a00c-2ddcaaf14e92`
- Effect: candidate 344 minus naive 185.4 = +158.6, 95% bootstrap interval [+83.65, +266.4] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 185.4 over 5 runs; repeats: 173.3, 185.4, 170.2, 192.9, 193.5
- Spread: range 170.2 to 193.5, noise band ±16.21 (2 x MAD), CV 5.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -47.5% (noise band ±4.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -44.2% (it comes back)
- PASS · Counterfactual (reversal test): without `gamma` the gap is -12.8% (it comes back)
- PASS · Held-out claim: C2: +146.5% to +4.4% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- FAIL · Evidence: `gamma=0.999`: no evidence mentions '0.999'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +158.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=2000` (8.42 noise units, gap -8.9%); `max_steps=1000` (7.97 noise units, gap -11.0%)
- Near alternatives (closest across all claims):
  - `max_steps=10000`: this claim -8.7%, mean |gap| 5.3% (6 runs)
  - `gamma=0.998`, `max_steps=500`: this claim +0.6%, mean |gap| 6.5% (5 runs)
  - `max_steps=2000`: this claim -8.9%, mean |gap| 9.9% (6 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `gamma=0.999, max_steps=500` (reported)
- `max_steps=1000`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting gamma=0.999, max_steps=500 | settings | 30% | 0.5 sigma (fits every claim) | run with gamma=0.999, max_steps=500 |
| 2 | the setting max_steps=1500 | settings | 17% | 0.3 sigma (fits every claim) | run with max_steps=1500 |
| 3 | the setting gamma=0.998, max_steps=500 | settings | 16% | 0.9 sigma (fits every claim) | run with gamma=0.998, max_steps=500 |

### History matching (every measured configuration, all claims together)
- 10 of 34 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=2000 (max I 0.39); max_steps=10000 (max I 0.48); max_steps=1500 (max I 0.75); max_steps=1000 (max I 2.28); +1 more
  - `gamma, max_steps`: gamma=0.999, max_steps=500 (max I 0.69); gamma=0.998, max_steps=500 (max I 1.21); gamma=0.998, max_steps=400 (max I 1.77); gamma=0.999, max_steps=400 (max I 1.97); +1 more
- Equally good values: `max_steps` in {400, 500}; `gamma` in {0.998, 0.999}

Notes:
- configurations the target claim can't tell apart from the answer: gamma=0.999, max_steps=500; max_steps=1000
- equally good values within one noise band (measured): max_steps in {400, 500}; gamma in {0.998, 0.999}
- found after adding spec knobs no ledger assumption names (episodes, eps_decay, eps_end, eps_start, eval_episodes, init_q, lr, omega_bins, reward_norm, seeds, theta_bins)
- max_steps: values from 400 to 500 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- gamma: values from 0.9976 to 0.999 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- not identifiable from the paper's numbers: 1 configuration(s) of other knobs fit every claim as well as the answer (gamma=0.999, max_steps=500: max_steps=1000), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `gamma=0.999`, `max_steps=500` | 5 | -2.7% | +4.4% | 3.5% |
| `max_steps=10000` | 6 | -8.7% | -1.9% | 5.3% |
| `gamma=0.998`, `max_steps=500` | 5 | +0.6% | +12.5% | 6.5% |
| `max_steps=2000` | 6 | -8.9% | -10.8% | 9.9% |
| `max_steps=400` | 6 | -18.2% | +16.9% | 17.5% |

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
