# v1.1 value coverage: post-hoc comparison (NOT blind)

**Read this first.** The 8 tasks below were GapBench's blind test set for v1.0. Their answers were
published after both v1.0 test runs, and v1.1 was developed with them in view. So these numbers show
whether the change works; they are **not** blind evidence. v1.1 needs a fresh sealed test (a new seed
after a `v1.1` tag) before any claim about it.

**Setup.** Like for like: v1.1 re-ran only the search, on exactly the claims and assumptions that
v1.0's runs 4-6 recorded (`harness.py --ledger-from`). There were no new model calls and the cost was
$0 (local backend). Scored with `score.py --answers eval/gapbench/sealed`.

| Category (runs) | v1.0, runs 4-6 | v1.1, runs 14-16 |
|---|---|---|
| Confidently wrong (24) | 0 | 0 |
| Correct abstention (9: no cause, noise only, incomplete) | 9 | 9 |
| Correct cause (15) | 7 | 8, plus 1 partial |
| known cause (6) | 5 | 3 |
| decoy (3) | 2 | 3 |
| interaction (6) | 0 | 2, plus 1 partial |

Dev set: v1.0 4/4, v1.1 3/4 (dev-ml-threshold: `normalize=minmax`+... instead of
`normalize=zscore`+`threshold=0.3`).

**What changed.** v1.1 reaches values v1.0 never tested: `normalize=minmax` on the decoy task, and
`n=600` on an interaction task, found twice. **What it costs:** with more candidates, several values
fit about equally (equifinality). On gen-03 `max_steps` 400, 500 and 1000 land within noise of each
other on a noisy RL metric. The parsimony tie-break picks the smallest change (400); the truth is 500.
One target claim can't tell them apart, so the honest output is a range of values not ruled out, not
a point.

Files: `gapbench_v11_posthoc_test.json`, `gapbench_v11_posthoc_dev.json`; run logs under
`eval/gapbench/runs/<task>/gapfinder/run12` (dev) and `run14`-`run16` (former test tasks).
