# Gap Report: RusKey Figure 6 ablation (nofork)

Artifact `ruskey-fig6-final` · generated 2026-10-09 12:32 · 30 branch runs (44 build/load setups) · sandbox $8.0667

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C5 (balanced_ratio_k10_k5) | Unexplained | -37.9% | -37.9% | ±6.2% | — |
| C5b (balanced_ratio_k1_k5) | Fits but unsupported | -9.0% | +0.5% | ±1.4% | `target_file_size_mb=64` |

## C5: balanced_ratio_k10_k5 (paper 1.48)
**Unexplained** · gap -37.9% → -37.9% · 17 hypotheses tested

Notes:
- stopped early: run budget of 30 reached (wanted 4 more run(s) of {'block_cache_mb': '32'} for 'confirm')
- {'monkey': 'false'} (gap -0.0%) was verified from existing runs and rejected: {'monkey': 'false'} closes this claim but makes held-out claims worse; rejected
- {'background_jobs': '8'} (gap -22.2%) was verified from existing runs and rejected: {'background_jobs': '8'} closes this claim but makes held-out claims worse; rejected
- {'bits_per_key': '8'} (gap -25.9%) was verified from existing runs and rejected: {'bits_per_key': '8'} closes this claim but makes held-out claims worse; rejected

## C5b: balanced_ratio_k1_k5 (paper 1.341)
**Fits but unsupported** · gap -9.0% → +0.5% · 17 hypotheses tested

Evidence:
- `target_file_size_mb=64`: UNSUPPORTED, no evidence mentions '64'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `target_file_size_mb`: gap -9.0% (ok)

Held-out claims (must not get worse beyond noise):
- C5: -37.9% → -31.4% (ok)
- C3: -42.8% → -41.5% (ok)

Replay: fork checkpoint `f8a76dc0-6a5c-4e75-bf40-abd16101656a` and run
```
RUN_TAG=b7e37348ce5e bash /work/harness/fig6_cell.sh db=/work/db workloads=balanced:0.5,writeheavy:0.1 missions=10 ops_per_mission=20000 num_keys=2000000 key_size=128 value_size=896 logical_levels=6 size_ratio=10 write_buffer=2097152 target_file_size_mb=64 bits_per_key=4 monkey=true direct_io=true background_jobs=4 rate_limit_mb=0 block_cache_mb=256 zero_result_ratio=1.0
```
(result checkpoint `0e74108a-dfd6-440c-9ae3-23517e5e9592`; 1 repeat(s) recorded)

Notes:
- stopped early: run budget of 30 reached (wanted 4 more run(s) of {'target_file_size_mb': '64'} for 'confirm')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C5 | C5b | C3 | Mean |gap| |
|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | -37.9% | -9.0% | -42.8% | 29.9% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `num_keys=100000000`, `num_keys=20000000`, `missions=2000`, `missions=260`, `missions=300`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--no_propagate_during_learning`, `--horizon`, `--lookup_schedule`, `--per_level_stats`, `--action_hold`, `--gamma`, `--settle_missions`, `--stable_missions`, `--no_greedy_critic`, `--warmup_frac`, `--shuffle_load`, `--flex`, `--seed`, `--zipfian`, `--zipf_theta`
