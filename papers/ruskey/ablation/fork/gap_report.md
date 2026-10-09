# Gap Report: RusKey Figure 6 ablation (fork)

Artifact `ruskey-fig6-final` · generated 2026-10-09 12:27 · 30 branch runs (8 build/load setups) · sandbox $4.4757

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C5 (balanced_ratio_k10_k5) | Fits but unsupported | -44.7% | -2.7% | ±6.7% | `background_jobs=8` |
| C5b (balanced_ratio_k1_k5) | Fits but unsupported | -18.5% | -2.2% | ±3.0% | `background_jobs=8` |

## C5: balanced_ratio_k10_k5 (paper 1.48)
**Fits but unsupported** · gap -44.7% → -2.7% · 17 hypotheses tested

Evidence:
- `background_jobs=8`: UNSUPPORTED, no evidence mentions '8'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `background_jobs`: gap -44.7% (ok)

Held-out claims (must not get worse beyond noise):
- C5b: -18.5% → -2.2% (ok)
- C3: -75.0% → -36.1% (ok)

Replay: fork checkpoint `35943598-18ee-459d-b588-fdc0eb181f27` and run
```
RUN_TAG=3bac6420911b bash /work/harness/fig6_cell.sh db=/work/db workloads=balanced:0.5,writeheavy:0.1 missions=10 ops_per_mission=20000 num_keys=2000000 key_size=128 value_size=896 logical_levels=6 size_ratio=10 write_buffer=2097152 target_file_size_mb=8 bits_per_key=4 monkey=true direct_io=true background_jobs=8 rate_limit_mb=0 block_cache_mb=256 zero_result_ratio=1.0
```
(result checkpoint `10560bca-8a83-4149-91f7-e7534d0f73b3`; 1 repeat(s) recorded)

Notes:
- stopped early: run budget of 30 reached (wanted 4 more run(s) of {'block_cache_mb': '32'} for 'confirm')
- verified from runs already made, after the budget ran out

## C5b: balanced_ratio_k1_k5 (paper 1.341)
**Fits but unsupported** · gap -18.5% → -2.2% · 17 hypotheses tested

Evidence:
- `background_jobs=8`: UNSUPPORTED, no evidence mentions '8'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `background_jobs`: gap -18.5% (ok)

Held-out claims (must not get worse beyond noise):
- C5: -44.7% → -2.7% (ok)
- C3: -75.0% → -36.1% (ok)

Replay: fork checkpoint `35943598-18ee-459d-b588-fdc0eb181f27` and run
```
RUN_TAG=3bac6420911b bash /work/harness/fig6_cell.sh db=/work/db workloads=balanced:0.5,writeheavy:0.1 missions=10 ops_per_mission=20000 num_keys=2000000 key_size=128 value_size=896 logical_levels=6 size_ratio=10 write_buffer=2097152 target_file_size_mb=8 bits_per_key=4 monkey=true direct_io=true background_jobs=8 rate_limit_mb=0 block_cache_mb=256 zero_result_ratio=1.0
```
(result checkpoint `10560bca-8a83-4149-91f7-e7534d0f73b3`; 1 repeat(s) recorded)

Notes:
- stopped early: run budget of 30 reached (wanted 4 more run(s) of {'target_file_size_mb': '64'} for 'confirm')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C5 | C5b | C3 | Mean |gap| |
|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | -44.7% | -18.5% | -75.0% | 46.1% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `num_keys=100000000`, `num_keys=20000000`, `missions=2000`, `missions=260`, `missions=300`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--no_propagate_during_learning`, `--horizon`, `--lookup_schedule`, `--per_level_stats`, `--action_hold`, `--gamma`, `--settle_missions`, `--stable_missions`, `--no_greedy_critic`, `--warmup_frac`, `--shuffle_load`, `--flex`, `--seed`, `--zipfian`, `--zipf_theta`
