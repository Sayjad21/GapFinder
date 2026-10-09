# Gap Report: RusKey Figure 6 (5 independent loads)

Artifact `ruskey-fig6-final` · generated 2026-10-09 12:52 · 30 branch runs (12 build/load setups) · sandbox $6.0042

> **Partial report:** the run or dollar budget ran out before every claim was verified.

> **Setup check:** setup is NOT reproducible: 5 identical setups gave 5 different checkpoints, so the noise band includes setup-to-setup variation.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C5 (balanced_ratio_k10_k5) | Unexplained | -30.8% | -30.8% | ±8.6% | — |
| C5b (balanced_ratio_k1_k5) | Reproduced | -12.4% | n/a | ±15.9% | — |

## C5: balanced_ratio_k10_k5 (paper 1.48)
**Unexplained** · gap -30.8% → -30.8% · 17 hypotheses tested

Notes:
- stopped early: run budget of 30 reached (wanted 4 more run(s) of {'bits_per_key': '8'} for 'confirm')
- {'target_file_size_mb': '64'} (gap -30.3%) was verified from existing runs and rejected: did not pass verification
- closest configuration not verified: {'bits_per_key': '8'} (gap -16.8%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made

## C5b: balanced_ratio_k1_k5 (paper 1.341)
Reproduces: naive gap -12.4% is inside the noise band ±15.9%.

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C5 | C5b | C3 | Mean |gap| |
|---|---|---|---|---|---|
| `target_file_size_mb=64` | 5 | -30.3% | -9.7% | -32.4% | 24.1% |
| naive (reproduction as run) | 5 | -30.8% | -12.4% | -43.3% | 28.8% |
| `target_file_size_mb=2` | 5 | -66.3% | -29.6% | -45.4% | 47.1% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `num_keys=100000000`, `num_keys=20000000`, `missions=2000`, `missions=260`, `missions=300`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--no_propagate_during_learning`, `--horizon`, `--lookup_schedule`, `--per_level_stats`, `--action_hold`, `--gamma`, `--settle_missions`, `--stable_missions`, `--no_greedy_critic`, `--warmup_frac`, `--shuffle_load`, `--flex`, `--seed`, `--zipfian`, `--zipf_theta`
