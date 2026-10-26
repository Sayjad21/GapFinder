# Gap Report: test-v13-07

Artifact `rlbench` · generated 2026-10-23 18:10 · 153 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +114.5% | -24.3% | ±2.1% | `eps_decay=0.0` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`min_reward`): paper 69.8625, measured 165.9 (+137.5%, band ±24.3%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `learning_rate_schedule_constant`: "Q-values are updated with a constant learning rate of 0.1." (p.1)

## C1: mean_reward (paper 89.7375)
**Fits but unsupported** · gap +114.5% → -24.3% · 36 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0031`, `B0032`, `B0054`, `B0055`, `B0056` (6 run(s) of the same config)
- Config: `eps_decay` naive `0.99`, changed to `0.0`
- Command:

  Replay: fork checkpoint `a6edebb6-d312-4938-85ed-ae2eaedf74a2` and run
  ```
  RUN_TAG=7a0970c8cd86 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.0 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 63.41, 29.86, 80.07, 90.31, 52.58, 72.4; gap after -24.3%; result checkpoint `f3e79fd5-2ff7-4c86-9a68-c899a2e3b48d`
- Effect: candidate 67.91 minus naive 192.5 = -124.6, 95% bootstrap interval [-154.1, -94.33] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 89.7 on CartPole; the worst of its seeds reaches 69.9.

- p. 1; value used: `mean_reward` = 89.7375 reward (headline claim)

### What did we measure?
- Naive median 192.5 over 5 runs; repeats: 193.9, 191.9, 192.5, 193.4, 166.5
- Spread: range 166.5 to 193.9, noise band ±1.925 (2 x MAD), CV 6.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +114.5% (noise band ±2.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_decay` the gap is +114.5% (it comes back)
- PASS · Held-out claim: C2: +137.5% to -85.7% (not worse beyond noise)
- FAIL · Evidence: `eps_decay=0.0`: no evidence mentions '0.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -124.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `termination_angle`, `termination_position`, `reward_per_step`, `learning_rate_schedule_constant`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_decay=0.6` (47.01 noise units, gap +13.6%); `eps_decay=0.0198` (40.93 noise units, gap -26.7%); `eps_decay=0.099` (37.62 noise units, gap -33.8%); `eps_decay=0.495` (34.63 noise units, gap -40.2%); `lr_schedule=inv` (26.28 noise units, gap +58.1%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +47.8%, mean |gap| 45.2% (3 runs)
  - `eps_decay=0.6`: this claim -6.3%, mean |gap| 45.5% (6 runs)
  - `lr_schedule=linear`, `eps_decay=0.495`: this claim -9.9%, mean |gap| 47.5% (5 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_decay=0.0` (reported)
- `eps_decay=0.6`
- `eps_decay=0.099`
- `eps_decay=0.495`
- `eps_decay=0.198`
- `eps_decay=0.495, lr_schedule=linear`
- `eps_decay=0.6, lr_schedule=linear`
- `eps_decay=0.98, lr_schedule=inv`
- `eps_decay=0.495, lr_schedule=inv`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting eps_decay=0.6 | settings | 16% | 1.8 sigma (fits every claim) | run with eps_decay=0.6 |
| 2 | the setting eps_decay=0.0 | settings | 16% | 1.8 sigma (fits every claim) | run with eps_decay=0.0 |
| 3 | the setting eps_decay=0.495, lr_schedule=linear | settings | 13% | 1.7 sigma (fits every claim) | run with eps_decay=0.495, lr_schedule=linear |

### History matching (every measured configuration, all claims together)
- 10 of 36 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_decay`: eps_decay=0.6 (max I 1.75); eps_decay=0.099 (max I 1.79); eps_decay=0.495 (max I 1.99); eps_decay=0.0 (max I 2.89); +1 more
  - `eps_decay, lr_schedule`: eps_decay=0.495, lr_schedule=linear (max I 1.91); eps_decay=0.6, lr_schedule=linear (max I 2.06); eps_decay=0.495, lr_schedule=inv (max I 2.53); eps_decay=0.98, lr_schedule=inv (max I 2.6); +1 more
- Equally good values: `eps_decay` in {0.0, 0.6}

Notes:
- configurations the target claim can't tell apart from the answer: eps_decay=0.0; eps_decay=0.6; eps_decay=0.099; eps_decay=0.495; eps_decay=0.198; eps_decay=0.495, lr_schedule=linear; eps_decay=0.6, lr_schedule=linear; eps_decay=0.98, lr_schedule=inv; eps_decay=0.495, lr_schedule=inv
- equally good values within one noise band (measured): eps_decay in {0.0, 0.6}
- spec knobs no ledger assumption names (episodes, eps_end, eps_start, eval_episodes, gamma, init_q, lr, max_steps, omega_bins, reward_norm, seeds, theta_bins) were screened too; no better answer
- eps_decay: values from 0 to 0 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- not identifiable from the paper's numbers: 8 configuration(s) of other knobs fit every claim as well as the answer (eps_decay=0.0: eps_decay=0.099; eps_decay=0.198; eps_decay=0.495; eps_decay=0.495, lr_schedule=inv; eps_decay=0.495, lr_schedule=linear; eps_decay=0.6), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 3 | +47.8% | -42.6% | 45.2% |
| `eps_decay=0.6` | 6 | -6.3% | -84.6% | 45.5% |
| `lr_schedule=linear`, `eps_decay=0.495` | 5 | -9.9% | -85.0% | 47.5% |
| `eps_decay=0.6`, `lr_schedule=linear` | 5 | -13.8% | -86.2% | 50.0% |
| `eps_decay=0.98`, `lr_schedule=inv` | 5 | +17.7% | -82.8% | 50.2% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `termination_angle`, `termination_position`, `reward_per_step`, `learning_rate_schedule_constant`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `28b211d810d1b9d96fc05d215b47c832dfb18c6d18bc5a8b475d528ad9c3b24a`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
