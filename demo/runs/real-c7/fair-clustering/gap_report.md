# Gap Report: Variational Fair Clustering (batch-3)

Artifact `b3a` · generated 2026-10-26 17:47 · 170 branch runs (0 build/load setups) · sandbox $134.1042

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_km_syn_obj (kmeans_synthetic_objective) | Fits but unsupported | -1.3% | +0.0% | ±1.0% | `kmeans_synthetic_lmbda=100` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_km_syn_bal (`kmeans_synthetic_balance`): paper 1, measured 0.505 (-49.5%, band ±0.5%)
  - C_kmd_syn_obj (`kmedian_synthetic_objective`): paper 292.4, measured 288.5 (-1.3%, band ±1.0%)
  - C_kmd_syn_bal (`kmedian_synthetic_balance`): paper 1, measured 0.437 (-56.3%, band ±0.4%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `--cluster_option`: "including both prototype-based (e.g., K-means/K-median) and graph-based (e.g., Normalized Cut or Ratio Cut)" (p.2)
  - `knn (affinity matrix neighbors)`: "For Ncut, we use 20-nearest neighbor affinity matrix" (p.5)
  - `fairness (boolean flag)`: "We report comprehensive evaluations and comparisons with state-of-the-art methods over various fair-clustering benchmarks" (p.1)

## C_km_syn_obj: kmeans_synthetic_objective (paper 207.8)
**Fits but unsupported** · gap -1.3% → +0.0% · 30 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0043`, `B0044`, `B0101` (4 run(s) of the same config)
- Config: `kmeans_synthetic_lmbda` naive `10`, changed to `100`
- Command:

  Replay: fork checkpoint `507a8c7f-af37-4a64-ac24-1f373177be7d` and run
  ```
  @ast:src/bound_update.py:32:parallel=True @ast:src/utils.py:109:@mut.26.Call.red.sum=0 @ast:src/utils.py:122:@mut.11.Call.red.mean=0 @ast:src/utils.py:79:@mut.32.num.add1=0 @ast:src/utils.py:79:@mut.32.num.div2=0 @ast:src/utils.py:79:@mut.32.num.mul2=0 @ast:src/utils.py:79:@mut.32.num.sub1=0 RUN_TAG=4366ca4cee9e export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; cd /work; mkdir -p out; export OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1 MPLBACKEND=Agg; n=0; for c in kmeans kmedian; do for d in Synthetic Synthetic-unequal; do case "$c-$d" in kmeans-Synthetic) L=100;; kmeans-Synthetic-unequal) L=10;; kmedian-Synthetic) L=10;; *) L=10;; esac; for s in 0 1 2 3 4 5 6 7 8 9; do dd=/tmp/gfdata/$c-$d-$s; mkdir -p $dd; python test_fair_clustering.py -d $d --cluster_option $c --lmbda $L --lmbda-tune False --seed $s --data_dir $dd > out/${c}_${d}_s${s}.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; done; done; wait; bash gf_harness/emit.sh
  ```
- Output: `kmeans_synthetic_objective` 207.8, 207.8, 207.8, 207.8; gap after +0.0%; result checkpoint `a54231dc-33c5-4bab-8b47-f04bc2b89267`
- Effect: candidate 207.8 minus naive 205 = +2.808, 95% bootstrap interval [+2.808, +2.808] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `kmeans_synthetic_objective` = 207.8.

### What did we measure?
- Naive median 205 over 5 runs; repeats: 205, 205, 205, 205, 205
- Spread: range 205 to 205, noise band ±2.05 (2 x MAD), CV 0.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -1.3% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `kmeans_synthetic_lmbda` the gap is -1.3% (it comes back)
- PASS · Held-out claim: C_km_syn_bal: -49.5% to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_km_uneq_obj: +0.0% to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_km_uneq_bal: +0.0% to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_kmd_syn_obj: -1.3% to -1.3% (not worse beyond noise)
- PASS · Held-out claim: C_kmd_syn_bal: -56.3% to -56.3% (not worse beyond noise)
- PASS · Held-out claim: C_kmd_uneq_obj: +0.0% to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_kmd_uneq_bal: +0.0% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `kmeans_synthetic_lmbda=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +2.808 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `--cluster_option`, `knn (affinity matrix neighbors)`, `--seed`, `fairness (boolean flag)`, `plot options (--plot_option_*)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `kmeans_synthetic_lmbda=15` (1.06 noise units, gap -0.3%)
- Near alternatives (closest across all claims):
  - `kmedian_synthetic_lmbda=100`: this claim -1.3%, mean |gap| 9.3% (4 runs)
  - `kmeans_synthetic_lmbda=40`: this claim +2.5%, mean |gap| 9.9% (4 runs)
  - `kmeans_synthetic_lmbda=50`: this claim +3.9%, mean |gap| 9.9% (4 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `kmeans_synthetic_lmbda=100` (reported)
- `kmeans_synthetic_lmbda=15`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 100% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | the setting kmeans_synthetic_lmbda=100 | settings | 0% | 37.5 sigma | run with kmeans_synthetic_lmbda=100 |
| 3 | no difference in reporting: the numbers as printed at the end of the run | settings | 0% | 38.0 sigma | the settings search and the other classes |

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C_kmd_syn_bal, among 37 tested
- Fit C_km_syn_obj alone (9; worst claim's implausibility in brackets, lowest is the least inconsistent): kmeans_synthetic_lmbda=100 (56.3); kmeans_synthetic_lmbda=15 (56.3); kmeans_synthetic_lmbda=20 (56.3); kmeans_unequal_lmbda=40 (56.3); kmeans_unequal_lmbda=100 (56.3); kmeans_unequal_lmbda=6000 (56.3)
- Leads outside the settings (static code checks, nothing run; check these first):
  - selection in code: the code selects best_avg_balance, best_lambda_avg_balance by comparing avg_balance > best_avg_balance over (count, lmbda) in enumerate(lmbdas): a tuning protocol the paper may describe differently (e.g. a different search, grid or budget) (`test_fair_clustering.py:149`)
  - selection in code: the code selects best_min_balance, best_lambda_min_balance by comparing min_balance > best_min_balance over (count, lmbda) in enumerate(lmbdas): a tuning protocol the paper may describe differently (e.g. a different search, grid or budget) (`test_fair_clustering.py:153`)
  - selection in code: the code selects bestacc, best_lambda_acc by comparing fairness_error < bestacc over (count, lmbda) in enumerate(lmbdas): a tuning protocol the paper may describe differently (e.g. a different search, grid or budget) (`test_fair_clustering.py:157`)
  - unexposed setting: `bound_iterations = 5000` is fixed in the code; no flag sets it (`src/fair_clustering.py:298`)
  - unexposed setting: `jit(..., parallel=True)`: a switch fixed in the call; no flag sets it (`src/bound_update.py:32`)
  - unexposed setting: `n_samples = 400` is fixed in the code; no flag sets it (`src/dataset_load.py:25`)
  - unexposed setting: `make_blobs(..., shuffle=False)`: a switch fixed in the call; no flag sets it (`src/dataset_load.py:28`)
  - fixed seed: random_state fixed to 1 (`src/dataset_load.py:28`)
- Equally good values: `kmeans_synthetic_lmbda` in {15, 20, 100}

Notes:
- configurations the target claim can't tell apart from the answer: kmeans_synthetic_lmbda=100; kmeans_synthetic_lmbda=15
- equally good values within one noise band (measured): kmeans_synthetic_lmbda in {15, 20, 100}
- patch round: none of 2 code-patch configurations fits every claim
- mutation round: none of 21 mutants moved C_km_syn_obj toward the paper
- value interval stopped early: run budget of 200 reached (wanted 1 more run(s) of {'kmeans_synthetic_lmbda': '278'} for 'interval kmeans_synthetic_lmbda=278')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_km_syn_obj | C_km_syn_bal | C_km_uneq_obj | C_km_uneq_bal | C_kmd_syn_obj | C_kmd_syn_bal | C_kmd_uneq_obj | C_kmd_uneq_bal | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `kmeans_synthetic_lmbda=100` | 4 | +0.0% | +0.0% | +0.0% | +0.0% | -1.3% | -56.3% | +0.0% | +0.0% | 7.2% |
| `kmedian_synthetic_lmbda=100` | 4 | -1.3% | -49.5% | +0.0% | +0.0% | +1.7% | -22.2% | +0.0% | +0.0% | 9.3% |
| `kmeans_synthetic_lmbda=40` | 4 | +2.5% | -18.8% | +0.0% | +0.0% | -1.3% | -56.3% | +0.0% | +0.0% | 9.9% |
| `kmeans_synthetic_lmbda=50` | 4 | +3.9% | -18.0% | +0.0% | +0.0% | -1.3% | -56.3% | +0.0% | +0.0% | 9.9% |
| `kmedian_synthetic_lmbda=40` | 4 | -1.3% | -49.5% | +0.0% | +0.0% | -0.7% | -36.3% | +0.0% | +0.0% | 11.0% |

## Knob names
- Ledger names mapped to spec knobs: `--lmbda` → `kmeans_synthetic_lmbda, kmeans_unequal_lmbda, kmedian_synthetic_lmbda, kmedian_unequal_lmbda`

## Runtime trace (one dry run)
41 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--cluster_option`, `knn (affinity matrix neighbors)`, `--seed`, `fairness (boolean flag)`, `plot options (--plot_option_*)`

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `2906138b3a7bc197dbefe6db4ea661cefb92e1d89155ff05ca75966bd7f75f97`
- Cost: Nemotron billed $0.0011, sandbox reported $134.1042 (total $134.1054; this search; ledger extraction is included only if it shared the search's router)
