# RusKey Figure 6 in Token Factory Sandboxes: first GapFinder run

**Status:** first real run (2026-10-07). It isn't the final result: paper values are by-eye
readings of Figure 6, and the scale is far below the paper's.

## Setup

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

## What the reproduction's defaults give

| Claim | Paper (read off Fig. 6) | Naive (500K keys) |
|---|---|---|
| C5 balanced K10/K5 latency | 1.56 | 0.87 |
| C5b balanced K1/K5 latency | 1.30 | 0.87 |
| C3 write-heavy K1/K10 latency (held out) | 2.94 | 0.93 |

At this scale the compaction-policy trade-off disappears: every K costs about the same, which
matches the reproduction's own finding that the trade-off is invisible below ~20 GB without a
compaction rate limit.

## What moved the ratios (medians of 5 runs)

| Configuration | C5 K10/K5 | C5b K1/K5 | C3 K1/K10 |
|---|---|---|---|
| naive | 0.87 | 0.87 | 0.93 |
| `num_keys=2000000` (4x data) | 0.74 | **1.28** | 1.98 |
| `target_file_size_mb=64` (driver default; scripts use 2) | **2.74** | 1.07 | 1.90 |
| `monkey=true` | 0.63 | 1.11 | 2.01 |
| `block_cache_mb=0` | 0.74 | 1.09 | 1.79 |
| `rate_limit_mb=30` | 0.68 | 0.32 | 1.16 |
| `zero_result_ratio=0.5` | 0.78 | 0.34 | 0.89 |

## Labels (papers/ruskey/search/gap_report.md)

- **C5b: Unexplained.** More data (`num_keys=2M`) closes K1/K5 almost exactly (1.28 vs 1.30), but
  it makes C5 worse (0.74 vs 0.87), so the held-out check rejects it as the explanation.
  `monkey=true` is rejected for the same reason.
- **C5: Fits but unsupported.** `block_cache_mb=256` + `zero_result_ratio=0.5` closes 75% of the
  gap (single run); nothing in the paper or the code backs those values.
- No claim is called Explained. The run budget ran out before combinations could be confirmed.

## What this suggests (to test, not conclusions)

1. **SST file size is a large unstated factor.** The paper never states it; the reproduction's
   scripts use 2 MB against the driver's 64 MB default, and 64 MB swings K10/K5 from 0.87 to
   2.74 (overshooting the paper). This was the first time the reproduction saw it measured.
2. **Scale matters, in a direction-dependent way:** 4x data fixes K1/K5 but not K10/K5. Testing
   larger scales needs more budget or a cheaper machine.
3. **A 30 MB/s rate limit alone doesn't recover the trade-off at 500K keys**, unlike at 20M keys.

## Before treating any of this as a result

- Replace the by-eye Figure 6 readings with values checked by the paper's author/reproducer.
- **Possible batch effect:** for several configurations the single screen run differs from its
  four confirm runs (`target_file_size_mb=64`: 0.76, then 2.95, 2.83, 2.69, 2.74; `num_keys=2M`:
  0.97 vs ~0.74; `block_cache_mb=0`: 0.85 vs ~0.7). Screen runs ran alongside ~13 other sandboxes
  at once; confirm runs came in a later batch. Within-VM ratios cancel machine speed, but not
  contention that changes during a run. Next run: screen with 2 repeats, or interleave configs.
- Rerun with a budget for the combine and bisect rounds.
