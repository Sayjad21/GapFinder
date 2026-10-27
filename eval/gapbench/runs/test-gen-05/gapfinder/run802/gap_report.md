# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-14 23:25 · 112 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +995.4% | +49.6% | ±42.3% | `eps_start=0.02` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +995.4% → +49.6% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0014`, `B0034`, `B0035`, `B0043` (4 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.02`
- Command:

  Replay: fork checkpoint `342f082c-b6d7-43fd-a28c-1e6130041e2d` and run
  ```
  RUN_TAG=e5ff655ef8ba "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.02 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 37.24, 17.96, 33.84, 16.52; gap after +49.6%; result checkpoint `4ee83d5d-5ae1-4606-9461-6e7af34ccaa3`
- Effect: candidate 25.9 minus naive 189.6 = -163.7, 95% bootstrap interval [-175.9, -152.6] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 189.6 over 5 runs; repeats: 181.9, 189.6, 193.3, 193.4, 188.8
- Spread: range 181.9 to 193.4, noise band ±7.32 (2 x MAD), CV 2.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +995.4% (noise band ±42.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +995.4% (it comes back)
- PASS · Held-out claim: C2: +1370.9% to +0.3% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.02`: no evidence mentions '0.02'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -163.7 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.0` (22.79 noise units, gap -31.9%); `eps_start=0.1` (18.89 noise units, gap +196.6%); `eps_start=0.2` (16.61 noise units, gap +293.0%); `lr_schedule=inv` (9.14 noise units, gap +609.0%); `eps_start=0.8` (7.14 noise units, gap +693.6%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_start=0.0`: this claim -2.9%, mean |gap| 1.5% (3 runs)
  - `lr_schedule=inv`, `eps_start=0.02`: this claim +4.2%, mean |gap| 2.4% (3 runs)
  - `eps_start=0.1`, `lr_schedule=linear`: this claim +6.0%, mean |gap| 3.0% (3 runs)

### Equally good configurations
The target claim can't tell these 10 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.02` (reported)
- `eps_start=0.0`
- `eps_start=0.1`
- `eps_start=0.1, lr_schedule=linear`
- `eps_start=0.0, lr_schedule=inv`
- `eps_start=0.02, lr_schedule=inv`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.2, lr_schedule=linear`
- `eps_start=0.2, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 7 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `eps_start, lr_schedule`: eps_start=0.02, lr_schedule=inv (max I 0.23); eps_start=0.0, lr_schedule=inv (max I 0.33); eps_start=0.1, lr_schedule=inv (max I 0.41); eps_start=0.1, lr_schedule=linear (max I 0.41); +2 more
  - `eps_start`: eps_start=0.02 (max I 2.73)
- Equally good values: `eps_start` in {0.0, 0.02}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.02; eps_start=0.0; eps_start=0.1; eps_start=0.1, lr_schedule=linear; eps_start=0.0, lr_schedule=inv; eps_start=0.02, lr_schedule=inv; eps_start=0.1, lr_schedule=inv; eps_start=0.02, lr_schedule=linear; eps_start=0.2, lr_schedule=linear; eps_start=0.2, lr_schedule=inv
- equally good values within one noise band (measured): eps_start in {0.0, 0.02}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_start=0.0` | 3 | -2.9% | +0.0% | 1.5% |
| `lr_schedule=inv`, `eps_start=0.02` | 3 | +4.2% | -0.5% | 2.4% |
| `eps_start=0.1`, `lr_schedule=linear` | 3 | +6.0% | +0.0% | 3.0% |
| `eps_start=0.1`, `lr_schedule=inv` | 3 | +26.5% | +1.6% | 14.1% |
| `eps_start=0.0`, `lr_schedule=linear` | 3 | -43.4% | -1.1% | 22.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
