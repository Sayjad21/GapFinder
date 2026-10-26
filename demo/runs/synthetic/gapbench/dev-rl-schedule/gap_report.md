# Gap Report: dev-rl-schedule

Artifact `rlbench` · generated 2026-10-23 17:39 · 151 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +27.0% | +3.6% | ±11.0% | `lr_schedule=inv` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`min_reward`): paper 29.05, measured 49.5 (+70.4%, band ±52.7%)

## C1: mean_reward (paper 139.35)
**Partially explained** · gap +27.0% → +3.6% · 76 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0006`, `B0008`, `B0009`, `B0010` (4 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `2270d7a8-dd9f-43dc-99d9-67d7ed903f6f` and run
  ```
  RUN_TAG=ace1746874e0 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 144.2, 149.1, 141.2, 144.6; gap after +3.6%; result checkpoint `1b138efb-7662-40a3-97c5-1c5d139e0c9d`
- Effect: candidate 144.4 minus naive 177 = -32.56, 95% bootstrap interval [-39.25, -20.13] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over six pole-angle and six angular-velocity bins balances CartPole for a mean of 139.3 steps after 400 training episodes.

- p. 1; value used: `mean_reward` = 139.35 steps (headline claim)

### What did we measure?
- Naive median 177 over 5 runs; repeats: 166, 177, 168.8, 178.5, 184.6
- Spread: range 166 to 184.6, noise band ±15.33 (2 x MAD), CV 4.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +27.0% (noise band ±11.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +27.0% (it comes back)
- PASS · Held-out claim: C2: +70.4% to +103.4% (not worse beyond noise)
- PASS · Evidence: `lr_schedule=inv`: paper states 'inv (0.1 / (1 + t/50))'
- PASS · Effect vs noise: candidate minus naive is -32.56 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `discretise_theta_range`, `discretise_omega_range`, `cartpole_g`, `cartpole_dt`, `reset_uniform_range`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `RUN_TAG`, `greedy_evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (1.05 noise units, gap +15.4%)
- Near alternatives (closest across all claims):
  - `gamma=0.95`: this claim +1.7%, mean |gap| 9.0% (4 runs)
  - `lr=0.05`: this claim -12.0%, mean |gap| 9.0% (4 runs)
  - `omega_bins=3`: this claim +26.2%, mean |gap| 19.5% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting lr_schedule=inv | settings | 25% | 1.4 sigma (fits every claim) | run with lr_schedule=inv |
| 2 | the setting gamma=0.95 | settings | 22% | 0.2 sigma (fits every claim) | run with gamma=0.95 |
| 3 | the setting episodes=40 | settings | 14% | 0.6 sigma (fits every claim) | run with episodes=40 |

### History matching (every measured configuration, all claims together)
- 13 of 76 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `gamma`: gamma=0.95 (max I 0.17)
  - `episodes`: episodes=40 (max I 0.62); episodes=200 (max I 2.54)
  - `gamma, lr_schedule`: gamma=0.95, lr_schedule=inv (max I 0.73)
  - `eps_start`: eps_start=0.5 (max I 1.2)
  - `lr_schedule`: lr_schedule=inv (max I 1.38)
  - `theta_bins`: theta_bins=3 (max I 2.08)
  - `lr`: lr=0.05 (max I 2.11)
  - `eps_end`: eps_end=0.005 (max I 2.25)
  - `omega_bins`: omega_bins=4 (max I 2.69)
- 8 separate islands (no single-knob move joins them): gamma=0.95; gamma=0.95, lr_schedule=inv; lr_schedule=inv | episodes=40; episodes=200 | eps_end=0.005; eps_end=0.1 | eps_start=0.5

Notes:
- its runs spread 0.2x the naive run's noise band (reported, not used to judge)
- spec knobs no ledger assumption names (episodes, eps_decay, eps_end, eps_start, eval_episodes, gamma, init_q, lr, max_steps, omega_bins, reward_norm, seeds, theta_bins) were screened too; no better answer

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `gamma=0.95` | 4 | +1.7% | -16.3% | 9.0% |
| `lr=0.05` | 4 | -12.0% | +6.0% | 9.0% |
| `omega_bins=3` | 4 | +26.2% | +12.8% | 19.5% |
| `gamma=0.95`, `lr_schedule=inv` | 4 | -1.4% | +40.5% | 21.0% |
| `episodes=40` | 4 | -3.0% | +49.0% | 26.0% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `discretise_theta_range`, `discretise_omega_range`, `cartpole_g`, `cartpole_dt`, `reset_uniform_range`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `RUN_TAG`, `greedy_evaluation_policy`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `28b211d810d1b9d96fc05d215b47c832dfb18c6d18bc5a8b475d528ad9c3b24a`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
