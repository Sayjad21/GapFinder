# Spike S6 — RusKey gap check (draft)

**Status: draft, pre-S4.** The pass condition is "at least 2 claims differ by
more than twice the S4 noise band". S4 hasn't run in a sandbox yet, so the
noise used below is the reproduction's own 95% CIs (from `scripts/stats.py`, local
WSL2 machine). Every measured number is copied from the RusKey reproduction's
committed docs. The source is cited on each row.

Two measurement regimes exist in the reproduction, and they disagree. That
disagreement is itself the kind of gap GapFinder is meant to explain:

- **R-20M:** 20M entries (20 GB), direct I/O, no rate limit, 1 seed
  (`RESULTS.md`, Figure 6 table, generated 2026-09-29).
- **R-regime:** the corrected regime from `RESULTS_LOG.md` (fixed-K arms at
  50/50 over 150 missions, second half measured, ±95% CI; tuner over 480
  missions).

| Claim | Paper | Measured | Regime / source | Gap beyond noise? |
|---|---|---|---|---|
| C5: Moderate (K=5) is the best fixed policy on balanced | K=5 best | K=1 best: 150.0 vs K=5 160.3 vs K=10 166.1 us/op | R-20M, `RESULTS.md` | Probably (single seed, no CI) |
| C5 (same) | K=5 best | K=5 42.3±4.2 and K=10 40.9±4.0 tie; K=1 57.1±6.7 is worst | R-regime, `results_bal` | **Yes:** no interior minimum; K=1 minus K=5 = +14.8, CI +6.9 to +22.7 |
| C4: RusKey settles at K=4 on balanced | K=4 | K=2 (R-20M); K=10 (R-regime, 70/100 final missions) | both | **Yes** (policy is discrete; K=10 vs 4 is far outside the tuner's ±1 action) |
| C3: RusKey picks lazy (K=10) on write-heavy | K=10 | K=1, 70.8 vs best fixed K=10 62.0 (R-20M); K=10 held 100/100 (R-regime) | both | **Yes in R-20M**, no in R-regime |
| C2: Aggressive (K=1) best on read-heavy | K=1 | K=1 best, 218.5 us/op (R-20M) | R-20M | No gap (reproduces) |
| C7: no single fixed policy wins everywhere | holds | holds in R-20M (K=10 wins write-heavy, K=1 wins the others); invisible without a compaction cap at 0.5–2 GB | R-20M; `WHERE_WE_ARE.md` | Reproduces at 20 GB; gap at small scale |
| Absolute read-heavy latency (Fig. 6a, read by eye) | ~0.027 ms/query at K=1 | 218.5 us/op = 0.2185 ms (R-20M) | R-20M | ~8× slower. Different hardware, so this belongs in "Unexplained (hardware)" unless a knob moves it |

**Tentative verdict: S6 passes.** C4 and C5 differ beyond the reproduction's
own noise in R-regime, and C3 differs in R-20M. RusKey can be the live case.

**Candidate explanations already on the reproduction's record, ready to be the
first knobs GapFinder tests** (see `gold_assumptions.json`):

1. `num_keys` 20M vs the paper's 100M. Tree depth is 4 levels vs 5–6, which
   makes reads ~10× cheaper than writes and removes the interior minimum.
   `[INFERENCE]` in RESULTS_LOG, never tested at 100M.
2. `rate_limit_mb`. A 30 MB/s compaction cap recovers the K trade-off. The
   paper says nothing about device headroom.
3. `direct_io`: the paper says it's enabled, the driver default is `false`
   (a paper–artifact inconsistency in the reproduction's own driver; every
   script passes it explicitly).
4. Tuner defaults that aren't in the paper: `propagate_during_learning=True`,
   `greedy_critic=True`, `move_margin=0.4`.

**Limit to state in the report:** 100M entries × 1 KB ≈ 100 GB. That doesn't
fit the 12 GiB sandbox writable layer, so A1 can't be tested at full scale in
a sandbox. The scaled-down protocol (keep the ratios, state the scaling) from
S3's fallback applies.
