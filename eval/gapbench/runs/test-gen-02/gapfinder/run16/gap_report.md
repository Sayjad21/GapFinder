# Gap Report: test-gen-02

Artifact `rlbench` · generated 2026-10-14 00:29 · 28 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +218.3% | +218.3% | ±21.2% | — |

## C1: mean_reward (paper 59.35)
**Unexplained** · gap +218.3% → +218.3% · 5 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (5 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 59.4 on CartPole; the worst of its seeds reaches 9.8.

- p. 1; value used: `mean_reward` = 59.35 reward (headline claim)

### What did we measure?
- Naive median 188.9 over 5 runs; repeats: 187.2, 188.9, 195.5, 153.8, 195.2
- Spread: range 153.8 to 195.5, noise band ±12.58 (2 x MAD), CV 9.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +218.3% (noise band ±21.2% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `eps_start`, `hardware_cpu`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (5.33 noise units, gap +105.3%); `lr_schedule=linear` (1.41 noise units, gap +188.5%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `reward_norm=on`: this claim +129.8%, mean |gap| 170.0% (5 runs)
  - `lr_schedule=inv`: this claim +121.8%, mean |gap| 214.8% (6 runs)
  - `lr_schedule=linear`: this claim +178.9%, mean |gap| 734.1% (6 runs)

Notes:
- closest configuration tried: {'lr_schedule': 'inv'} (gap +121.8%); it did not pass verification

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `reward_norm=on` | 5 | +129.8% | +210.2% | 170.0% |
| `lr_schedule=inv` | 6 | +121.8% | +307.9% | 214.8% |
| `lr_schedule=linear` | 6 | +178.9% | +1289.3% | 734.1% |
| `lr_schedule=linear`, `reward_norm=on` | 5 | +183.3% | +1351.3% | 767.3% |
| naive (reproduction as run) | 5 | +218.3% | +1387.3% | 802.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `eps_start`, `hardware_cpu`

## Provenance
- GapFinder commit: `ab5d0e01d517ea012f76706719410d70d422f3f9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `e323442c06dc23e2a59acc0ba37f900485ab760e6844bc4ffbd19ace981376ca`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
