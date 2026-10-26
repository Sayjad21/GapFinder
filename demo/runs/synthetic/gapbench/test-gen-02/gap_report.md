# Gap Report: test-gen-02

Artifact `rlbench` · generated 2026-10-23 17:41 · 158 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +202.6% | -16.3% | ±21.6% | `theta_bins=1` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`min_reward`): paper 9.85, measured 58.05 (+489.3%, band ±134.0%)

## C1: mean_reward (paper 59.35)
**Fits but unsupported** · gap +202.6% → -16.3% · 72 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0040`, `B0087`, `B0088`, `B0120`, `B0121`, `B0122` (6 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `1`
- Command:

  Replay: fork checkpoint `bef39d22-8a27-4af9-b098-d9027a3a32e1` and run
  ```
  RUN_TAG=58429d8bdf35 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_end 0.05 --eps_decay 0.99 --theta_bins 1 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 82.98, 82.66, 49.71, 33.84, 32.38, 49.62; gap after -16.3%; result checkpoint `b0664243-8bf9-44ed-a14d-7e092b52fa31`
- Effect: candidate 49.67 minus naive 179.6 = -129.9, 95% bootstrap interval [-152.4, -97.83] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 59.4 on CartPole; the worst of its seeds reaches 9.8.

- p. 1; value used: `mean_reward` = 59.35 reward (headline claim)

### What did we measure?
- Naive median 179.6 over 5 runs; repeats: 191.2, 162.1, 179.6, 177.4, 186
- Spread: range 162.1 to 191.2, noise band ±12.83 (2 x MAD), CV 6.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +202.6% (noise band ±21.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +202.6% (it comes back)
- PASS · Held-out claim: C2: +489.3% to +59.9% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -129.9 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `--eps_start`, `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `omega_bins=60` (9.04 noise units, gap -7.2%); `eps_decay=0.099` (9.02 noise units, gap -7.6%); `lr=0.01` (8.94 noise units, gap -9.3%); `eps_decay=0.0` (8.82 noise units, gap -12.0%); `lr=0.02` (8.36 noise units, gap +21.8%) (and 26 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_decay=0.099`: this claim -5.9%, mean |gap| 5.7% (6 runs)
  - `eps_decay=0.0`, `lr=0.01`: this claim -21.4%, mean |gap| 11.2% (6 runs)
  - `eps_decay=0.0`: this claim +25.1%, mean |gap| 13.2% (6 runs)

### Equally good configurations
The target claim can't tell these 7 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `theta_bins=1` (reported)
- `omega_bins=60`
- `lr=0.01`
- `eps_decay=0.0`
- `eps_decay=0.099`
- `theta_bins=60`
- `eps_decay=0.0, lr=0.01`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting theta_bins=1 | settings | 40% | 0.3 sigma (fits every claim) | run with theta_bins=1 |
| 2 | the setting omega_bins=60 | settings | 20% | 0.4 sigma (fits every claim) | run with omega_bins=60 |
| 3 | the setting lr=0.01 | settings | 11% | 0.5 sigma (fits every claim) | run with lr=0.01 |

### History matching (every measured configuration, all claims together)
- 12 of 72 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `omega_bins`: omega_bins=60 (max I 0.48)
  - `theta_bins`: theta_bins=1 (max I 0.55); theta_bins=60 (max I 2.45)
  - `lr`: lr=0.01 (max I 1.12)
  - `eps_decay`: eps_decay=0.099 (max I 1.36); eps_decay=0.0 (max I 1.7)
  - `eps_decay, lr`: eps_decay=0.0, lr=0.01 (max I 2.11)
  - `episodes`: episodes=1 (max I 2.41)
  - `lr, omega_bins`: lr=0.02, omega_bins=60 (max I 2.66); lr=0.01, omega_bins=60 (max I 2.68)
- 4 separate islands (no single-knob move joins them): omega_bins=60; lr=0.01; eps_decay=0.099 | theta_bins=1; theta_bins=60 | episodes=1 | gamma=0.0
- Equally good values: `theta_bins` in {1, 60}

Notes:
- configurations the target claim can't tell apart from the answer: theta_bins=1; omega_bins=60; lr=0.01; eps_decay=0.0; eps_decay=0.099; theta_bins=60; eps_decay=0.0, lr=0.01
- equally good values within one noise band (measured): theta_bins in {1, 60}
- found after adding spec knobs no ledger assumption names (episodes, eps_decay, eps_end, eval_episodes, gamma, init_q, lr, max_steps, omega_bins, reward_norm, seeds, theta_bins)
- theta_bins: values from 1 to 1 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- not identifiable from the paper's numbers: 6 configuration(s) of other knobs fit every claim as well as the answer (theta_bins=1: eps_decay=0.0; eps_decay=0.0, lr=0.01; eps_decay=0.099; lr=0.01; omega_bins=60; theta_bins=60), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause
- the paper states theta_bins = 6 ("6 pole-angle bins"), but 6 leaves the gap at +202.6% (beyond noise); 1 closes it: the stated value is likely not the one behind the paper's numbers

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_decay=0.099` | 6 | -5.9% | -5.6% | 5.7% |
| `eps_decay=0.0`, `lr=0.01` | 6 | -21.4% | -1.0% | 11.2% |
| `eps_decay=0.0` | 6 | +25.1% | +1.3% | 13.2% |
| `lr=0.01` | 6 | +2.0% | +25.9% | 14.0% |
| `episodes=1` | 6 | -27.2% | -2.8% | 15.0% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--eps_start`, `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `5b529fe059a1d25f5c30f84a36b28953ae9555656cfbfaa1af42ab228d75cdaf`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
