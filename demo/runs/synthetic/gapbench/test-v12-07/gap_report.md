# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-23 18:01 · 158 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +89.5% | +3.8% | ±18.5% | `lr=0.02` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `evaluation_policy`: "evaluate the greedy policy for 20 episodes" (p.1)
  - `seed_generation_logic`: "averaging over 10 random seeds" (p.1)

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +89.5% → +3.8% · 67 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0075`, `B0107`, `B0108`, `B0119`, `B0120`, `B0121` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `0.02`
- Command:

  Replay: fork checkpoint `866c80ee-c2ed-44af-8a79-70d1a2af2fb0` and run
  ```
  RUN_TAG=5ed7438c97c5 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.02 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 111.1, 102.1, 102.8, 100.8, 87.89, 107.7; gap after +3.8%; result checkpoint `6ce62ad5-bb34-47a2-8d45-9c403365d232`
- Effect: candidate 102.5 minus naive 187 = -84.53, 95% bootstrap interval [-99.58, -68.85] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 187 over 5 runs; repeats: 196.1, 171.5, 187, 170.3, 195.7
- Spread: range 170.3 to 196.1, noise band ±18.27 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +89.5% (noise band ±18.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +89.5% (it comes back)
- PASS · Held-out claim: C2: +41.2% to -88.3% (not worse beyond noise)
- FAIL · Evidence: `lr=0.02`: no evidence mentions '0.02'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -84.53 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=1` (4.57 noise units, gap -4.9%); `episodes=40` (4.12 noise units, gap +13.2%); `lr=0.01` (3.99 noise units, gap -15.5%); `eps_decay=0.0` (3.99 noise units, gap +15.7%); `eps_decay=0.099` (3.34 noise units, gap -27.7%) (and 22 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=1`, `episodes=40`: this claim +10.8%, mean |gap| 42.7% (5 runs)
  - `lr=1`: this claim -9.0%, mean |gap| 46.4% (6 runs)
  - `lr_schedule=inv`: this claim +52.3%, mean |gap| 48.5% (6 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=0.02` (reported)
- `theta_bins=1`
- `episodes=40, lr=1`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting lr=0.02 | settings | 56% | 1.8 sigma (fits every claim) | run with lr=0.02 |
| 2 | the setting episodes=40, lr=1 | settings | 15% | 1.1 sigma (fits every claim) | run with episodes=40, lr=1 |
| 3 | the setting lr=0.01 | settings | 12% | 1.0 sigma (fits every claim) | run with lr=0.01 |

### History matching (every measured configuration, all claims together)
- 7 of 67 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `lr`: lr=0.01 (max I 1.04); lr=0.02 (max I 1.78); lr=1 (max I 1.79)
  - `episodes, lr`: episodes=40, lr=1 (max I 1.95)
  - `eps_decay`: eps_decay=0.495 (max I 2.11)
  - `theta_bins`: theta_bins=1 (max I 2.3)
  - `episodes`: episodes=200 (max I 2.77)
- 4 separate islands (no single-knob move joins them): lr=0.01; lr=0.02; lr=1 | eps_decay=0.495 | theta_bins=1 | episodes=200
- Equally good values: `lr` in {0.01, 0.02, 1}

Notes:
- configurations the target claim can't tell apart from the answer: lr=0.02; theta_bins=1; episodes=40, lr=1
- equally good values within one noise band (measured): lr in {0.01, 0.02, 1}
- found after adding spec knobs no ledger assumption names (episodes, eps_decay, eps_end, eps_start, eval_episodes, gamma, init_q, lr, omega_bins, seeds, theta_bins)
- lr: values from 0.02 to 0.03162 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- not identifiable from the paper's numbers: 2 configuration(s) of other knobs fit every claim as well as the answer (lr=0.02: episodes=40, lr=1; theta_bins=1), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause
- the paper states lr = 0.1 ("Q-values are updated with a constant learning rate of 0.1"), but 0.1 leaves the gap at +89.5% (beyond noise); 0.02 closes it: the stated value is likely not the one behind the paper's numbers

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=1`, `episodes=40` | 5 | +10.8% | -74.7% | 42.7% |
| `lr=0.02` | 6 | +3.8% | -88.3% | 46.0% |
| `lr=1` | 6 | -9.0% | -83.8% | 46.4% |
| `lr_schedule=inv` | 6 | +52.3% | -44.6% | 48.5% |
| `init_q=-1.0` | 3 | +79.5% | -24.2% | 51.9% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `628b5c73850e927a9f4a60a62df08223407f68c2742e658344952145d44bf832`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
