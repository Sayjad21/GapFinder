# RusKey Figure 6 in Token Factory Sandboxes

**Status (2026-10-09):** three runs. The final-regime run (127 branches) is the main search. Read it
together with the correction directly below: the database load turned out not to be reproducible,
which changes two of that run's observations. The first run (further down) used earlier settings
and by-eye paper values.

## Correction (2026-10-09): the database load is not reproducible

The fork vs no-fork ablation reloaded the database for every branch, which exposed this. Every load
runs the same command (`load.sh`, 2M keys) on the same binary (checkpoint `98e3e854`). We then
measured the naive configuration on 12 separate loads, across four runs. The loads gave 12 different
checkpoint IDs, and the Figure 6 ratios moved with them
([load_variance.json](../../eval/results/ruskey_load_variance.json)):

| Naive configuration | C5 K10/K5 | C5b K1/K5 | C3 WH K1/K10 |
|---|---|---|---|
| paper (Figure 6, digitized) | 1.48 | 1.34 | 3.05 |
| the 127-branch run's load (5 runs) | 0.83 | **0.52** | **3.46** |
| 11 other loads: range | 0.82-1.11 | 0.99-1.38 | 0.76-2.27 |
| all 12 loads: median | 0.92 | 1.21 | 1.74 |

The search's noise band came from 5 runs forked from one load, and the spread across loads is far
larger. The 127-branch run happened to get a load that is an outlier on two of the three ratios.
For that run, this means:

1. **Its labels stand.** Both balanced claims are Unexplained; nothing was attributed.
2. **"The reproduction's regime already reproduces the write-heavy ratio (3.46 vs 3.05)" only holds
   for that one load.** Across loads the median is 1.74. The held-out claim is not reproduced in
   general.
3. **"8 bits/key brings both balanced claims to the paper" is withdrawn as stated.** `bits_per_key` is
   a load setting, so its runs came from a different load than the naive runs they were compared
   with. C5b at 8 bits/key (1.28) is inside the naive range across loads (0.99-1.38), so there's no
   evidence of an effect. C5 at 8 bits/key (1.45) is above that range (0.82-1.11), so it remains a
   lead, but it was measured on a single load.

In the final-regime table below, the `bits_per_key` and `monkey` rows (load settings) were each
measured on a load of their own. The `background_jobs` and `zero_result_ratio` rows forked from the
naive row's load, so they compare like with like, but only for that load.

**What changed in GapFinder:** `--noise-setups N` puts N of the naive noise runs on independent
loads. Sandboxes name a checkpoint after its content, so identical loads would dedup to one ID;
different IDs show the load is not reproducible. The noise band then includes the load-to-load
spread, and no candidate is judged against a narrower band than that.

**The search with 5 independent loads** (30 branches; report: [search_setups/gap_report.md](search_setups/gap_report.md);
sandbox cost reported $6.00, billed $0):

| Claim | Gap before | Noise band | Label |
|---|---|---|---|
| C5 balanced K10/K5 | -30.8% | ±8.6% | Unexplained. `bits_per_key=8` came closest (-16.8%) on 1 of the 5 runs a confirmation needs, so no label. |
| C5b balanced K1/K5 | -12.4% | ±15.9% | Reproduced: the gap is inside the noise once load-to-load variation counts. The band is wide, so this means "not distinguishable from the paper at 2M keys", not a tight match. |

The run printed: "setup is NOT reproducible: 5 identical setups gave 5 different checkpoints". The
held-out write-heavy ratio is 43% below the paper (1.73 vs 3.05).

## Fork vs no-fork ablation (2026-10-09)

The same bounded search ran twice (spec, ledger and targets identical; budget 30 runs). Each arm
recorded 22 branches ([ablation_ruskey.json](../../eval/results/ablation_ruskey.json),
[ablation/](ablation/)):

| | With forking | Without (reload per branch) |
|---|---|---|
| Database loads | 8 (the naive one, plus one per load setting tested) | 22 |
| Setup time, summed | 188 s | 519 s |
| Setup cost (reported) | $1.88 | $5.21 |
| Total cost (reported) | $4.48 | $8.07 |
| Wall time | 229 s | 306 s |

Forking cut setup cost by 64% and total cost by 45%. The arms' labels differed (single screen
runs, each on a different database), and both rested on one unconfirmed run. GapFinder now
requires the full confirmation repeats before labelling after the budget runs out. Labelled again
from the recorded runs only, both arms give Unexplained for both claims, as the 127-branch run
did. The ablation also exposed two bugs, both fixed:
- **Unconfirmed labels:** a single screen run could produce a label after the budget ran out.
- **Lost runs:** 8 branches still in flight when the budget stopped the fork arm were never
  recorded. In-flight runs now finish and are recorded first.

## Final-regime run (2026-10-09): the main result

- **Starting point = the reproduction's final Figure 6**, verified in its scripts: `results_fig6_final2`
  links to `results_monkey20` (go20.sh, wsl_monkey.sh): Monkey Bloom filters at 4 bits/key, 256 MB
  block cache, every lookup for an absent key (zero-result ratio 1.0), 8 MB SST files. Scaled to
  2M keys and 10 missions x 20K ops per K. The paper's Figure 6 uses **uniform 8 bits/key** (p.15).
- **Correctness first:** `--verify_mode` under these settings passed (0 stale, 0 missing, 0
  structural violations; papers/ruskey/verify_final_regime.json).
- **Paper values** digitized from Figure 6 (missions 1500-2000): balanced K10/K5 = 1.48,
  K1/K5 = 1.34, write-heavy K1/K10 = 3.05 (held out).
- **Search:** 17 hypotheses from ledger v5, 2 screen runs each, 127 branches, 13 build/load setups;
  sandbox cost reported $21.31, **billed $0**. Report: papers/ruskey/search_final/gap_report.md.

| Configuration (medians, n=3) | C5 K10/K5 | C5b K1/K5 | C3 WH K1/K10 (held out) |
|---|---|---|---|
| paper (Figure 6, digitized) | 1.48 | 1.34 | 3.05 |
| reproduction's final regime (naive) | 0.83 | 0.52 | **3.46** |
| `bits_per_key=8` (the paper's stated value) | **1.45** | **1.28** | 2.09 |
| `background_jobs=2` | 1.51 | 1.13 | 2.24 |
| `monkey=false` (uniform, 4 bits) | 0.85 | 1.13 | 0.92 |
| `monkey=false` + `bits_per_key=8` (the paper's Figure 6 filters) | 1.31 | 1.03 | 0.90 |
| `zero_result_ratio=0.0` (lookups that hit) | 0.47 | 0.99 | 1.58 |

**Labels: both balanced claims Unexplained.** No setting or pair explains all three ratios at this
scale. The reproduction's regime already reproduces the held-out write-heavy ratio (3.46 vs 3.05),
and every change that fixes the balanced claims breaks it, so verification rejects them.

**What it does show:**
1. **The paper's 8 bits/key alone brings both balanced claims to the paper** (within 2% and 4%),
   at the cost of the write-heavy ratio. The reproduction's 4 bits/key (the paper's Figure 8 setting)
   is the single change that moves both balanced Figure 6 claims onto the paper.
2. The paper's full Figure 6 filter setup (uniform, 8 bits) does *not* reproduce at 2M keys: the
   Bloom-filter choice interacts with scale, and the paper's 100M keys aren't testable here.
3. GapFinder reported, rather than hid, that its best single candidate breaks a held-out claim.

## First run (2026-10-07): earlier settings, 500K keys


### Setup

- Engine: the reproduction's RocksDB fork (`ruskey-flsm`, commit `d361675`, uncommitted changes
  present), built locally and uploaded as a stripped binary. Compiling in a sandbox would cost
  thousands of CPU-seconds at the measured price.
- Scale: **500K keys** (496 MB), 10 missions x 10K ops per K. The paper uses **100M keys** and
  2,000 missions x 50K ops. The paper's scale is listed in the report as "not testable within the budget".
- Each branch runs fixed K = 1, 5, 10 on copies of the same loaded database in one VM, for the
  balanced (50% lookups) and write-heavy (10%) workloads. Claims are latency **ratios** within
  one VM, so machine speed cancels.
- Noise (spike S4, 5 identical forks): ratio CV 4-7%.
- Sandbox cost: **$6.76** for 78 branch runs; RusKey total including setup and noise: $7.41 of an $8 cap.

### What the reproduction's defaults give

| Claim | Paper (read off Fig. 6) | Naive (500K keys) |
|---|---|---|
| C5 balanced K10/K5 latency | 1.56 | 0.87 |
| C5b balanced K1/K5 latency | 1.30 | 0.87 |
| C3 write-heavy K1/K10 latency (held out) | 2.94 | 0.93 |

At this scale the compaction-policy trade-off disappears: every K costs about the same, which
matches the reproduction's own finding that the trade-off is invisible below ~20 GB without a
compaction rate limit.

### What moved the ratios (medians of 5 runs)

| Configuration | C5 K10/K5 | C5b K1/K5 | C3 K1/K10 |
|---|---|---|---|
| naive | 0.87 | 0.87 | 0.93 |
| `num_keys=2000000` (4x data) | 0.74 | **1.28** | 1.98 |
| `target_file_size_mb=64` (driver default; scripts use 2) | **2.74** | 1.07 | 1.90 |
| `monkey=true` | 0.63 | 1.11 | 2.01 |
| `block_cache_mb=0` | 0.74 | 1.09 | 1.79 |
| `rate_limit_mb=30` | 0.68 | 0.32 | 1.16 |
| `zero_result_ratio=0.5` | 0.78 | 0.34 | 0.89 |

### Labels (papers/ruskey/search/gap_report.md)

- **C5b: Unexplained.** More data (`num_keys=2M`) closes K1/K5 almost exactly (1.28 vs 1.30), but
  it makes C5 worse (0.74 vs 0.87), so the held-out check rejects it as the explanation.
  `monkey=true` is rejected for the same reason.
- **C5: Fits but unsupported.** `block_cache_mb=256` + `zero_result_ratio=0.5` closes 75% of the
  gap (single run); nothing in the paper or the code backs those values.
- No claim is called Explained. The run budget ran out before combinations could be confirmed.

### What this suggests (to test, not conclusions)

1. **SST file size is a large unstated factor.** The paper never states it; the reproduction's
   scripts use 2 MB against the driver's 64 MB default, and 64 MB swings K10/K5 from 0.87 to
   2.74 (overshooting the paper). This was the first time the reproduction saw it measured.
2. **Scale matters, in a direction-dependent way:** 4x data fixes K1/K5 but not K10/K5. Testing
   larger scales needs more budget or a cheaper machine.
3. **A 30 MB/s rate limit alone doesn't recover the trade-off at 500K keys**, unlike at 20M keys.

### Before treating any of this as a result

- Replace the by-eye Figure 6 readings with values checked by the paper's author/reproducer.
- **Possible batch effect:** for several configurations the single screen run differs from its
  four confirm runs (`target_file_size_mb=64`: 0.76, then 2.95, 2.83, 2.69, 2.74; `num_keys=2M`:
  0.97 vs ~0.74; `block_cache_mb=0`: 0.85 vs ~0.7). Screen runs ran alongside ~13 other sandboxes
  at once; confirm runs came in a later batch. Within-VM ratios cancel machine speed, but not
  contention that changes during a run. Next run: screen with 2 repeats, or interleave configs.
- Rerun with a budget for the combine and bisect rounds.
