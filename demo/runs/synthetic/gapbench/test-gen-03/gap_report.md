# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-23 17:43 · 178 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -44.2% | +0.8% | ±7.2% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -44.2% → +0.8% · 73 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0038`, `B0039`, `B0040` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `8ef5c575-f4d4-46cf-beef-c0b23d77c127` and run
  ```
  RUN_TAG=0710d638d4ee export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 318.7, 265.2, 323.7, 290.2, 258.2, 371.6; gap after +0.8%; result checkpoint `fd82637b-776e-407c-baaf-4edb4428d833`
- Effect: candidate 304.4 minus naive 168.6 = +135.9, 95% bootstrap interval [+82.72, +191.9] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 168.6 over 5 runs; repeats: 149.2, 168.6, 162.5, 187.1, 179.4
- Spread: range 149.2 to 187.1, noise band ±21.6 (2 x MAD), CV 8.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -44.2% (noise band ±7.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -44.2% (it comes back)
- PASS · Held-out claim: C2: +31.4% to +12.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +135.9 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=10000` (5.4 noise units, gap -5.5%); `max_steps=400` (5.3 noise units, gap -6.3%); `max_steps=2000` (4.57 noise units, gap -11.5%); `max_steps=1000` (1.63 noise units, gap -32.5%)
- Near alternatives (closest across all claims):
  - `max_steps=400`: this claim -21.2%, mean |gap| 15.9% (6 runs)
  - `max_steps=1000`: this claim +7.7%, mean |gap| 26.3% (6 runs)
  - `omega_bins=8`: this claim -43.6%, mean |gap| 27.8% (6 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=500` (reported)
- `max_steps=1000`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting max_steps=500 | settings | 73% | 0.5 sigma (fits every claim) | run with max_steps=500 |
| 2 | the setting max_steps=1000 | settings | 13% | 0.4 sigma (fits every claim) | run with max_steps=1000 |
| 3 | the setting max_steps=10000 | settings | 10% | 0.7 sigma (fits every claim) | run with max_steps=10000 |

### History matching (every measured configuration, all claims together)
- 4 of 73 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `max_steps`: max_steps=500 (max I 0.51); max_steps=1000 (max I 0.99); max_steps=10000 (max I 2.63); max_steps=400 (max I 2.93)
- Equally good values: `max_steps` in {500, 1000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=500; max_steps=1000
- equally good values within one noise band (measured): max_steps in {500, 1000}
- spec knobs no ledger assumption names (episodes, eps_decay, eps_end, eps_start, eval_episodes, gamma, init_q, lr, omega_bins, reward_norm, seeds, theta_bins) were screened too; no better answer
- max_steps: values from 500 to 545 fit every claim (a bisection, 3 runs a side, one run a value: approximate)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 6 | +0.8% | +12.1% | 6.5% |
| `max_steps=400` | 6 | -21.2% | +10.7% | 15.9% |
| `max_steps=1000` | 6 | +7.7% | -44.9% | 26.3% |
| `omega_bins=8` | 6 | -43.6% | +11.9% | 27.8% |
| `max_steps=10000` | 6 | -9.7% | -55.8% | 32.7% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `28b211d810d1b9d96fc05d215b47c832dfb18c6d18bc5a8b475d528ad9c3b24a`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
