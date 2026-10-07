# Gap Report: RusKey (SIGMOD 2024), Figure 6

Artifact `ruskey-fig6` · generated 2026-10-07 16:29 · 78 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C5 (balanced_ratio_k10_k5) | Fits but unsupported | -44.1% | -11.0% | ±2.7% | `block_cache_mb=256`, `zero_result_ratio=0.5` |
| C5b (balanced_ratio_k1_k5) | Unexplained | -33.1% | -33.1% | ±5.2% | — |

## C5: balanced_ratio_k10_k5 (paper 1.56)
**Fits but unsupported** · gap -44.1% → -11.0% · 13 hypotheses tested

Evidence:
- `block_cache_mb=256`: UNSUPPORTED, no evidence mentions '256'; it fits, but nothing says the authors used it
- `zero_result_ratio=0.5`: UNSUPPORTED, no evidence mentions '0.5'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `block_cache_mb`: gap -50.0% (ok)
- without `zero_result_ratio`: gap -45.6% (ok)

Held-out claims (must not get worse beyond noise):
- C5b: -33.1% → -33.1% (ok)
- C3: -68.4% → -63.9% (ok)

Replay: fork checkpoint `56cac700-3c0f-43c6-add8-a498cb399b59` and run
```
RUN_TAG=8efba02d75d4 bash /work/harness/fig6_cell.sh db=/work/db workloads=balanced:0.5,writeheavy:0.1 missions=10 ops_per_mission=10000 num_keys=500000 key_size=128 value_size=896 logical_levels=6 size_ratio=10 write_buffer=2097152 target_file_size_mb=2 bits_per_key=8 monkey=false direct_io=true background_jobs=4 rate_limit_mb=0 block_cache_mb=256 zero_result_ratio=0.5
```
(result checkpoint `e502dd4c-11a5-4d64-8df3-b0b194d00af2`; 1 repeat(s) recorded)

Notes:
- stopped early: run budget of 78 reached
- verified from runs already made, after the budget ran out

## C5b: balanced_ratio_k1_k5 (paper 1.3)
**Unexplained** · gap -33.1% → -33.1% · 13 hypotheses tested

Notes:
- stopped early: run budget of 78 reached
- {'num_keys': '2000000'} (gap -1.7%) was verified from existing runs and rejected: {'num_keys': '2000000'} closes this claim but makes held-out claims worse; rejected
- {'monkey': 'true'} (gap -14.9%) was verified from existing runs and rejected: {'monkey': 'true'} closes this claim but makes held-out claims worse; rejected
- {'block_cache_mb': '0'} (gap -16.0%) was verified from existing runs and rejected: {'block_cache_mb': '0'} closes this claim but makes held-out claims worse; rejected

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `ops_per_mission=50000`, `ops_per_mission=40000`, `missions=2000`, `missions=1000`, `missions=260`, `missions=300`, `num_keys=100000000`, `num_keys=20000000`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--lookup_ratio`, `--shuffle_load`, `--gamma`, `--action_hold`, `--settle_missions`, `--alpha`, `level_compaction_dynamic_level_bytes`, `--max_background_compactions`, `hardware_environment`, `--lookup_schedule`, `--warmup_frac`, `flsm_intra_level_merge`, `CXXFLAGS`, `--no_propagate_during_learning`
