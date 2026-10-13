# RusKey: honest noise model and multi-claim history matching (offline, post-hoc)

Inputs: every final-regime RusKey run (the 127-branch search, both ablation arms, the 5-load search).
That is 20 naive runs on 12 loads plus every measured configuration. No new runs.

## Variance components (`eval/noise_model.py`, `noise_model_ruskey.json`)

| Claim | Paper | Naive mean (gap) | SD within a load | SD between loads | Minimum detectable effect, n=5 (fork SD / total SD) | Verdict |
|---|---|---|---|---|---|---|
| C5 balanced K10/K5 | 1.48 | 0.905 (-38.9%) | 0.066 | 0.082 | 0.13 / 0.21 | **detectable** |
| C5b balanced K1/K5 | 1.341 | 1.013 (-24.5%) | 0.084 | **0.311** | 0.17 / 0.65 | below the MDE: **Inconclusive** |
| C3 write-heavy K1/K10 | 3.051 | 1.714 (-43.8%) | 0.847 | 0.342 | 1.71 / 1.85 | below the MDE: **Inconclusive** |

For C5b, forked repeats see a quarter of the real spread (Hurlbert's pseudo-replication). Only C5 is a
gap these runs can measure.

## History matching over all claims together (`eval/history_match.py`, `history_match_ruskey.json`)

- 44 tested configurations; **11 jointly not ruled out** at discrepancy 0 (17 at 0.05).
- The best supported is `target_file_size_mb=64`, the driver's own default (the reproduction's scripts
  use 8 MB): 10 runs, I = 0.27 (C5), 0.06 (C5b), 1.28 (C3).
- `block_cache_mb=32` + `target_file_size_mb=2` also fits (3 runs; I = 0.03, 0.07, 1.12).

**Reading.** RusKey's balanced claims are not "unexplained" so much as **non-identifiable at this noise**:
several settings fit every claim within the load-to-load noise. SST file size, already flagged as a
large unstated factor in the first run, is the strongest lead. To turn it into an attribution, it
needs confirmation runs on fresh loads (`--noise-setups 5` for `target_file_size_mb=64` and for the
naive configuration), which is a sandbox run and needs S's OK.
