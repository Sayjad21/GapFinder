# Gap Report: planted L1-b3a-s5-2

Artifact `b3a` · generated 2026-10-23 01:44 · 128 branch runs (0 build/load setups) · sandbox $105.5795

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_km_syn_obj (kmeans_synthetic_objective) | Fits but unsupported | +88.3% | -0.0% | ±1.9% | `@ast:src/utils.py:79:@mut.32.num.mul2=1` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: kmedian_synthetic_balance 0.64 > kmeans_synthetic_balance 0.52; measured: kmedian_synthetic_balance 0.437 < kmeans_synthetic_balance 0.505 (margin -0.068, noise 0.00668)
- **Held-out claims outside noise:**
  - C_km_syn_bal (`kmeans_synthetic_balance`): paper 0.52, measured 0.505 (-2.9%, band ±1.0%)
  - C_km_uneq_obj (`kmeans_unequal_objective`): paper 97.1, measured 159.8 (+64.5%, band ±1.6%)
  - C_kmd_syn_obj (`kmedian_synthetic_objective`): paper 206.95, measured 288.5 (+39.4%, band ±1.4%)
  - C_kmd_syn_bal (`kmedian_synthetic_balance`): paper 0.64, measured 0.437 (-31.7%, band ±0.7%)
  - C_kmd_uneq_obj (`kmedian_unequal_objective`): paper 151.81, measured 174.8 (+15.2%, band ±1.2%)

## C_km_syn_obj: kmeans_synthetic_objective (paper 108.88)
**Fits but unsupported** · gap +88.3% → -0.0% · 63 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0050`, `B0127`, `B0128` (3 run(s) of the same config)
- Config: `@ast:src/utils.py:79:@mut.32.num.mul2` naive `0`, changed to `1`
- Command:

  Replay: fork checkpoint `507a8c7f-af37-4a64-ac24-1f373177be7d` and run
  ```
  @ast:src/utils.py:139:target_precision=0.9 @ast:src/bound_update.py:32:parallel=True @ast:src/utils.py:109:@mut.26.Call.red.sum=0 @ast:src/utils.py:122:@mut.11.Call.red.mean=0 @ast:src/utils.py:79:@mut.32.num.add1=0 @ast:src/utils.py:79:@mut.32.num.div2=0 @ast:src/utils.py:79:@mut.32.num.mul2=1 @ast:src/utils.py:79:@mut.32.num.sub1=0 RUN_TAG=7a449a56e8ec export PYTHONPATH="${WORK:-$PWD}/.gf_patch${PYTHONPATH:+${GF_PATHSEP:-:}$PYTHONPATH}"; cd /work; mkdir -p out; export OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1 MPLBACKEND=Agg; n=0; for c in kmeans kmedian; do for d in Synthetic Synthetic-unequal; do case "$c-$d" in kmeans-Synthetic) L=10;; kmeans-Synthetic-unequal) L=10;; kmedian-Synthetic) L=10;; *) L=10;; esac; for s in 0 1 2 3 4 5 6 7 8 9; do dd=/tmp/gfdata/$c-$d-$s; mkdir -p $dd; python test_fair_clustering.py -d $d --cluster_option $c --lmbda $L --lmbda-tune False --seed $s --data_dir $dd > out/${c}_${d}_s${s}.log 2>&1 & n=$((n+1)); if [ $((n % 4)) -eq 0 ]; then wait; fi; done; done; done; wait; bash gf_harness/emit.sh
  ```
- Output: `kmeans_synthetic_objective` 108.9, 108.9, 108.9; gap after -0.0%; result checkpoint `5fac8a07-5869-4d76-8ca7-0624b6184e27`
- Effect: candidate 108.9 minus naive 205 = -96.12, 95% bootstrap interval [-96.12, -96.12] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `kmeans_synthetic_objective` = 108.88.

### What did we measure?
- Naive median 205 over 5 runs; repeats: 205, 205, 205, 205, 205
- Spread: range 205 to 205, noise band ±2.05 (2 x MAD), CV 0.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +88.3% (noise band ±1.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `@ast:src/utils.py:79:@mut.32.num.mul2` the gap is +88.3% (it comes back)
- PASS · Held-out claim: C_km_syn_bal: -2.9% to -1.0% (not worse beyond noise)
- PASS · Held-out claim: C_km_uneq_obj: +64.5% to -0.0% (not worse beyond noise)
- PASS · Held-out claim: C_km_uneq_bal: +0.0% to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_kmd_syn_obj: +39.4% to -0.0% (not worse beyond noise)
- PASS · Held-out claim: C_kmd_syn_bal: -31.7% to +0.2% (not worse beyond noise)
- PASS · Held-out claim: C_kmd_uneq_obj: +15.2% to +0.0% (not worse beyond noise)
- PASS · Held-out claim: C_kmd_uneq_bal: +0.0% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `@ast:src/utils.py:79:@mut.32.num.mul2=1`: no assumption record for this knob, so no evidence
- PASS · Effect vs noise: candidate minus naive is -96.12 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `kmeans_synthetic_lmbda=2` (2.12 noise units, gap +84.3%); `kmeans_synthetic_lmbda=1` (2.12 noise units, gap +84.3%); `kmeans_synthetic_lmbda=5` (1.25 noise units, gap +85.9%)
- Near alternatives (closest across all claims):
  - `kmeans_synthetic_lmbda=2`, `kmedian_synthetic_lmbda=20`: this claim +84.3%, mean |gap| 31.0% (3 runs)
  - `kmedian_synthetic_lmbda=20`, `kmeans_synthetic_lmbda=1`: this claim +84.3%, mean |gap| 31.0% (3 runs)
  - `kmeans_synthetic_lmbda=2`: this claim +84.3%, mean |gap| 32.3% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a code change: @ast:src/utils.py:79:@mut.32.num.mul2=1 | code | 100% | 0.6 sigma (fits every claim) | run with @ast:src/utils.py:79:@mut.32.num.mul2=1 (an in-memory code patch) |
| 2 | a cause outside every class tested | outside | 0% |  | look for code, data or evaluation differences the classes don't cover |
| 3 | no difference in reporting: the numbers as printed at the end of the run | settings | 0% | 59.5 sigma | the settings search and the other classes |

### History matching (every measured configuration, all claims together)
- 1 of 76 tested configurations fit every claim within 3 sigma
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
- {'kmeans_synthetic_lmbda': '2'} closes this claim but makes held-out claims worse; rejected
- kmeans_unequal_lmbda dropped: with repeats, {'kmeans_synthetic_lmbda': '2', 'kmeans_unequal_lmbda': '20'} fits {'kmeans_synthetic_lmbda': '2'}'s gap by less than one noise band, so it is not needed
- closest configuration tried: {'kmeans_synthetic_lmbda': '2'} (gap +84.3%); it did not pass verification
- history matching: 1 of 76 tested configurations fit every claim within 3 sigma
- explained with a code patch (tested in memory, no file edited): src/utils.py line 79: @mut.32.num.mul2 = 0 -> 1

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_km_syn_obj | C_km_syn_bal | C_km_uneq_obj | C_km_uneq_bal | C_kmd_syn_obj | C_kmd_syn_bal | C_kmd_uneq_obj | C_kmd_uneq_bal | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `@ast:src/utils.py:79:@mut.32.num.mul2=1` | 3 | -0.0% | -1.0% | -0.0% | +0.0% | -0.0% | +0.2% | +0.0% | +0.0% | 0.1% |
| naive (reproduction as run) | 5 | +88.3% | -2.9% | +64.5% | +0.0% | +39.4% | -31.7% | +15.2% | +0.0% | 30.2% |
| `kmeans_synthetic_lmbda=2`, `kmedian_synthetic_lmbda=20` | 3 | +84.3% | -23.1% | +64.5% | +0.0% | +40.9% | -20.3% | +15.2% | +0.0% | 31.0% |
| `kmedian_synthetic_lmbda=20`, `kmeans_synthetic_lmbda=1` | 3 | +84.3% | -23.1% | +64.5% | +0.0% | +40.9% | -20.3% | +15.2% | +0.0% | 31.0% |
| `kmeans_synthetic_lmbda=2` | 4 | +84.3% | -23.1% | +64.5% | +0.0% | +39.4% | -31.7% | +15.2% | +0.0% | 32.3% |

## Knob names
- Code defaults read from the code instead of the ledger: `lmbda_tune` True at test_fair_clustering.py:218 (ledger said False)

## Runtime trace (one dry run)
41 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Provenance
- GapFinder commit: `96f43d9d872690442737d0ad342eeb7d86352416` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `04d9d4f0f0e15850557b3db9b1e7bb7f561151e4eda41f15f89d331c6b1adb64`
- Cost: Nemotron billed $0.0000, sandbox reported $105.5795 (total $105.5795; this search; ledger extraction is included only if it shared the search's router)
