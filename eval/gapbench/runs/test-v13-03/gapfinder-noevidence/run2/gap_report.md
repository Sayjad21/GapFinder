# Gap Report: test-v13-03

Artifact `rlbench` · generated 2026-10-16 00:05 · 179 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +86.2% | -0.2% | ±21.1% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Fits but unsupported** · gap +86.2% → -0.2% · 40 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0017`, `B0048`, `B0049`, `B0070`, `B0071`, `B0072` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `00b8e3bb-1cd2-4496-850b-814c498f501b` and run
  ```
  RUN_TAG=fddb2d7c7d36 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.14, 99.76, 99.95, 99.52, 92.75, 99.05; gap after -0.2%; result checkpoint `7e9bd486-0762-43a0-980d-ddb84a0f0fbd`
- Effect: candidate 99.33 minus naive 185.3 = -85.95, 95% bootstrap interval [-99.57, -70.72] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1, Figure 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 185.3 over 5 runs; repeats: 172.3, 168.7, 185.3, 195.4, 195.7
- Spread: range 168.7 to 195.7, noise band ±20.95 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +86.2% (noise band ±21.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +86.2% (it comes back)
- PASS · Held-out claim: C2: +38.7% to -0.8% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -85.95 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `discretise.theta_clip`, `discretise.omega_clip`, `CartPole.termination_x`, `CartPole.termination_theta`, `RUN_TAG`, `RL_SEED_BASE`, `CartPole.reward_per_step`, `discretise.theta_bin_width`, `discretise.omega_bin_width`, `Q_table.tie_break`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_decay=0.099` (3.67 noise units, gap -9.0%); `lr_schedule=inv` (2.5 noise units, gap +33.6%); `eps_decay=0.0` (2.5 noise units, gap -33.5%); `eps_decay=0.0198` (2.5 noise units, gap -33.5%); `eps_decay=0.495` (2.36 noise units, gap -36.5%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -2.2%, mean |gap| 3.1% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -10.3%, mean |gap| 35.1% (5 runs)
  - `lr_schedule=inv`: this claim +24.4%, mean |gap| 47.9% (6 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 6 of 40 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `max_steps`: max_steps=100 (max I 0.29)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.4); lr_schedule=inv, max_steps=100 (max I 1.38)
  - `eps_decay`: eps_decay=0.495 (max I 2.43); eps_decay=0.198 (max I 2.85)
  - `lr_schedule`: lr_schedule=inv (max I 2.88)
- 2 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100 | eps_decay=0.495; eps_decay=0.198

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | -0.2% | -0.8% | 0.5% |
| `lr_schedule=linear`, `max_steps=100` | 5 | -2.2% | -4.0% | 3.1% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -10.3% | -59.9% | 35.1% |
| `lr_schedule=inv` | 6 | +24.4% | -71.5% | 47.9% |
| `eps_decay=0.995` | 6 | +84.9% | +15.6% | 50.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `discretise.theta_clip`, `discretise.omega_clip`, `CartPole.termination_x`, `CartPole.termination_theta`, `RUN_TAG`, `RL_SEED_BASE`, `CartPole.reward_per_step`, `discretise.theta_bin_width`, `discretise.omega_bin_width`, `Q_table.tie_break`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
