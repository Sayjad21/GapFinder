# Gap Report: RusKey (SIGMOD 2024), Figure 6, from the reproduction's final regime

Artifact `ruskey-fig6-final` · generated 2026-10-09 00:45 · 127 branch runs (13 build/load setups) · sandbox $21.3147

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C5 (balanced_ratio_k10_k5) | Unexplained | -43.6% | -43.6% | ±1.4% | — |
| C5b (balanced_ratio_k1_k5) | Unexplained | -61.0% | -61.0% | ±2.1% | — |

## C5: balanced_ratio_k10_k5 (paper 1.48)
**Unexplained** · gap -43.6% → -43.6% · 33 hypotheses tested

Notes:
- {'ops_per_mission': '40000'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'ops_per_mission': '40000'} (gap -15.0%); it did not pass verification

## C5b: balanced_ratio_k1_k5 (paper 1.341)
**Unexplained** · gap -61.0% → -61.0% · 33 hypotheses tested

Notes:
- {'monkey': 'false', 'zero_result_ratio': '0.0'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'monkey': 'false', 'zero_result_ratio': '0.0'} (gap +0.1%); it did not pass verification

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C5 | C5b | C3 | Mean |gap| |
|---|---|---|---|---|---|
| `bits_per_key=8` | 3 | -1.8% | -4.3% | -31.6% | 12.6% |
| `background_jobs=2`, `block_cache_mb=32` | 3 | -10.4% | -28.6% | +0.4% | 13.1% |
| `block_cache_mb=64`, `background_jobs=2` | 3 | -0.9% | -30.4% | +10.2% | 13.8% |
| `background_jobs=2` | 3 | +2.0% | -15.4% | -26.6% | 14.7% |
| `target_file_size_mb=2`, `block_cache_mb=32` | 3 | -7.4% | -0.4% | -38.8% | 15.5% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `num_keys=100000000`, `num_keys=20000000`, `missions=2000`, `missions=260`, `missions=300`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--no_propagate_during_learning`, `--horizon`, `--lookup_schedule`, `--per_level_stats`, `--action_hold`, `--gamma`, `--settle_missions`, `--stable_missions`, `--no_greedy_critic`, `--warmup_frac`, `--shuffle_load`, `--flex`, `--seed`, `--zipfian`, `--zipf_theta`
