# Gap Report: RusKey Figure 6 ablation (fork, re-labelled from recorded runs)

Artifact `ruskey-fig6-final` · generated 2026-10-09 12:50 · 22 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C5 (balanced_ratio_k10_k5) | Unexplained | -44.7% | -44.7% | ±6.7% | — |
| C5b (balanced_ratio_k1_k5) | Unexplained | -18.5% | -18.5% | ±3.0% | — |

## C5: balanced_ratio_k10_k5 (paper 1.48)
**Unexplained** · gap -44.7% → -44.7% · 17 hypotheses tested

Notes:
- stopped early: run budget of 22 reached (wanted 4 more run(s) of {'target_file_size_mb': '64'} for 'confirm')
- closest configuration not verified: {'background_jobs': '8'} (gap -2.7%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made

## C5b: balanced_ratio_k1_k5 (paper 1.341)
**Unexplained** · gap -18.5% → -18.5% · 17 hypotheses tested

Notes:
- stopped early: run budget of 22 reached (wanted 4 more run(s) of {'target_file_size_mb': '64'} for 'confirm')
- closest configuration not verified: {'background_jobs': '8'} (gap -2.2%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C5 | C5b | C3 | Mean |gap| |
|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | -44.7% | -18.5% | -75.0% | 46.1% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `num_keys=100000000`, `num_keys=20000000`, `missions=2000`, `missions=260`, `missions=300`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--no_propagate_during_learning`, `--horizon`, `--lookup_schedule`, `--per_level_stats`, `--action_hold`, `--gamma`, `--settle_missions`, `--stable_missions`, `--no_greedy_critic`, `--warmup_frac`, `--shuffle_load`, `--flex`, `--seed`, `--zipfian`, `--zipf_theta`
