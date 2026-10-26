# Gap Report: planted L1-b3a-s2-2

Artifact `b3a` · generated 2026-10-21 02:34 · 114 branch runs (0 build/load setups) · sandbox $90.1328

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_km_syn_obj (kmeans_synthetic_objective) | Paper-artifact inconsistency | -2.0% | -0.0% | ±1.0% | `kmeans_synthetic_lmbda=20` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_km_syn_bal (`kmeans_synthetic_balance`): paper 0.61, measured 0.505 (-17.2%, band ±0.8%)

## C_km_syn_obj: kmeans_synthetic_objective (paper 209.17)
**Paper-artifact inconsistency** · gap -2.0% → -0.0% · 57 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0007`, `B0039`, `B0040`, `B0041` (4 run(s) of the same config)
- Config: `kmeans_synthetic_lmbda` naive `10`, changed to `20`
- Command:

  Replay: fork checkpoint `507a8c7f-af37-4a64-ac24-1f373177be7d` and run
  ```
  RUN_TAG=898e1c53acbb export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out; export OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1 MPLBACKEND=Agg; n=0; for c in kmeans kmedian; do for d in Synthetic Synthetic-unequal; do case "$c-$d" in kmeans-Synthetic) L=20;; kmeans-Synthetic-unequal) L=10;; kmedian-Synthetic) L=10;; *) L=10;; esac; for s in 0 1 2 3 4 5 6 7 8 9; do dd=/tmp/gfdata/$c-$d-$s; mkdir -p $dd; python test_fair_clustering.py -d $d --cluster_option $c --lmbda $L --lmbda-tune False --seed $s --data_dir $dd > out/${c}_${d}_s${s}.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; done; done; wait; bash gf_harness/emit.sh
  ```
- Output: `kmeans_synthetic_objective` 209.2, 209.2, 209.2, 209.2; gap after -0.0%; result checkpoint `f1ff2346-eeb8-4508-ad0f-201c26e45d72`
- Effect: candidate 209.2 minus naive 205 = +4.173, 95% bootstrap interval [+4.173, +4.173] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `kmeans_synthetic_objective` = 209.17.

### What did we measure?
- Naive median 205 over 5 runs; repeats: 205, 205, 205, 205, 205
- Spread: range 205 to 205, noise band ±2.05 (2 x MAD), CV 0.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.0% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `kmeans_synthetic_lmbda` the gap is -2.0% (it comes back)
- PASS · Held-out claim: C_km_syn_obj@kmeans_synthetic_lmbda=5 at kmeans_synthetic_lmbda=10: n/a to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_km_syn_obj@kmeans_synthetic_lmbda=20 at kmeans_synthetic_lmbda=40: n/a to +0.0% (not worse beyond noise)
- FAIL · Evidence: `kmeans_synthetic_lmbda=20`: no evidence mentions '20'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +4.173 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `kmeans_synthetic_lmbda=100` (1.37 noise units, gap -0.7%)
- Near alternatives (closest across all claims):
  - `kmeans_unequal_lmbda=5`, `kmeans_synthetic_lmbda=20`: this claim -0.0%, mean |gap| 0.1% (4 runs)
  - `kmeans_unequal_lmbda=20`, `kmeans_synthetic_lmbda=20`: this claim -0.0%, mean |gap| 0.1% (4 runs)
  - `kmedian_unequal_lmbda=5`, `kmeans_synthetic_lmbda=20`: this claim -0.0%, mean |gap| 0.1% (4 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `kmeans_synthetic_lmbda=20` (reported)
- `kmeans_synthetic_lmbda=20, kmeans_unequal_lmbda=20`
- `kmeans_synthetic_lmbda=20, kmeans_unequal_lmbda=5`
- `kmeans_synthetic_lmbda=20, kmedian_unequal_lmbda=20`
- `kmeans_synthetic_lmbda=20, kmedian_unequal_lmbda=5`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting kmeans_synthetic_lmbda=20 | settings | 43% | 1.2 sigma (fits every claim) | run with kmeans_synthetic_lmbda=20 |
| 2 | the setting kmeans_synthetic_lmbda=20, kmeans_unequal_lmbda=20 | settings | 14% | 1.2 sigma (fits every claim) | run with kmeans_synthetic_lmbda=20, kmeans_unequal_lmbda=20 |
| 3 | the setting kmeans_synthetic_lmbda=20, kmeans_unequal_lmbda=5 | settings | 14% | 1.2 sigma (fits every claim) | run with kmeans_synthetic_lmbda=20, kmeans_unequal_lmbda=5 |

### History matching (every measured configuration, all claims together)
- 5 of 60 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `kmeans_synthetic_lmbda`: kmeans_synthetic_lmbda=20 (max I 1.79)
  - `kmeans_synthetic_lmbda, kmeans_unequal_lmbda`: kmeans_synthetic_lmbda=20, kmeans_unequal_lmbda=5 (max I 1.79); kmeans_synthetic_lmbda=20, kmeans_unequal_lmbda=20 (max I 1.79)
  - `kmeans_synthetic_lmbda, kmedian_unequal_lmbda`: kmeans_synthetic_lmbda=20, kmedian_unequal_lmbda=5 (max I 1.79); kmeans_synthetic_lmbda=20, kmedian_unequal_lmbda=20 (max I 1.79)
- Leads outside the settings (static code checks, nothing run; check these first):
  - selection in code: the code selects best_avg_balance, best_lambda_avg_balance by comparing avg_balance > best_avg_balance over (count, lmbda) in enumerate(lmbdas): a tuning protocol the paper may describe differently (e.g. a different search, grid or budget) (`test_fair_clustering.py:149`)
  - selection in code: the code selects best_min_balance, best_lambda_min_balance by comparing min_balance > best_min_balance over (count, lmbda) in enumerate(lmbdas): a tuning protocol the paper may describe differently (e.g. a different search, grid or budget) (`test_fair_clustering.py:153`)
  - selection in code: the code selects bestacc, best_lambda_acc by comparing fairness_error < bestacc over (count, lmbda) in enumerate(lmbdas): a tuning protocol the paper may describe differently (e.g. a different search, grid or budget) (`test_fair_clustering.py:157`)
  - unexposed setting: `bound_iterations = 5000` is fixed in the code; no flag sets it (`src/fair_clustering.py:298`)
  - unexposed setting: `nn(..., target_precision=0.9)`: fixed in the call; no flag sets it (`src/utils.py:139`)
  - unexposed setting: `jit(..., parallel=True)`: a switch fixed in the call; no flag sets it (`src/bound_update.py:32`)
  - unexposed setting: `n_samples = 400` is fixed in the code; no flag sets it (`src/dataset_load.py:25`)
  - unexposed setting: `make_blobs(..., shuffle=False)`: a switch fixed in the call; no flag sets it (`src/dataset_load.py:28`)

Notes:
- configurations the target claim can't tell apart from the answer: kmeans_synthetic_lmbda=20; kmeans_synthetic_lmbda=20, kmeans_unequal_lmbda=20; kmeans_synthetic_lmbda=20, kmeans_unequal_lmbda=5; kmeans_synthetic_lmbda=20, kmedian_unequal_lmbda=20; kmeans_synthetic_lmbda=20, kmedian_unequal_lmbda=5
- scale probe: the code's kmeans_synthetic_lmbda as 2 x the paper's fits every swept claim after 11 runs at g(v) (C_km_syn_obj at kmeans_synthetic_lmbda=20, C_km_syn_obj@kmeans_synthetic_lmbda=5 at kmeans_synthetic_lmbda=10, C_km_syn_obj@kmeans_synthetic_lmbda=20 at kmeans_synthetic_lmbda=40)
- labelled Paper-artifact inconsistency: one factor (2 x the paper's) makes every one of the 3 swept claims fit
- mutation round: none of 1 mutants moved C_km_syn_obj toward the paper

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_km_syn_obj | C_km_syn_bal | C_km_uneq_obj | C_km_uneq_bal | C_kmd_syn_obj | C_kmd_syn_bal | C_kmd_uneq_obj | C_kmd_uneq_bal | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `kmeans_synthetic_lmbda=20` | 4 | -0.0% | +0.3% | +0.0% | +0.0% | -0.0% | -0.7% | -0.0% | +0.0% | 0.1% |
| `kmeans_unequal_lmbda=5`, `kmeans_synthetic_lmbda=20` | 4 | -0.0% | +0.3% | +0.0% | +0.0% | -0.0% | -0.7% | -0.0% | +0.0% | 0.1% |
| `kmeans_unequal_lmbda=20`, `kmeans_synthetic_lmbda=20` | 4 | -0.0% | +0.3% | +0.0% | +0.0% | -0.0% | -0.7% | -0.0% | +0.0% | 0.1% |
| `kmedian_unequal_lmbda=5`, `kmeans_synthetic_lmbda=20` | 4 | -0.0% | +0.3% | +0.0% | +0.0% | -0.0% | -0.7% | -0.0% | +0.0% | 0.1% |
| `kmedian_unequal_lmbda=20`, `kmeans_synthetic_lmbda=20` | 4 | -0.0% | +0.3% | +0.0% | +0.0% | -0.0% | -0.7% | -0.0% | +0.0% | 0.1% |

## Knob names
- Code defaults read from the code instead of the ledger: `lmbda_tune` True at test_fair_clustering.py:218 (ledger said False)

## Runtime trace (one dry run)
41 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Provenance
- GapFinder commit: `1c8f0f8b4a997137c12c0ee6716ab6adeed88fc3`
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `cddf344cd7f6cfd7f898eaba78d747c71689031cf1e09c8d012cbe104db4f1fb`
- Cost: Nemotron billed $0.0000, sandbox reported $90.1328 (total $90.1328; this search; ledger extraction is included only if it shared the search's router)
