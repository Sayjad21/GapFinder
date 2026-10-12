# MC Dropout external case (ext-eval-1): result

Paper: Gal and Ghahramani, "Dropout as a Bayesian Approximation" (ICML 2016). Code:
`yaringal/DropoutUncertaintyExps` at `6eb4497`, scaled down (T = 100, 3 splits). Targets: Energy
test RMSE 1.66 (the target claim) and Yacht test RMSE 1.11 (held out), both from ICML Table 1
([targets_mcd.json](targets_mcd.json)). The answer key was sealed before any run
([answer_key.sha256](answer_key.sha256)), revealed after all four arms finished, and checked
(`sha256sum -c answer_key.sha256` gives OK). Rules, setup and every deviation are in
[FROZEN.md](FROZEN.md); the feasibility work is in [FEASIBILITY.md](FEASIBILITY.md).

## Short version

- All four pre-registered arms ended **Unexplained**. None named `epochx` or `hidden` as the cause,
  and none made a false attribution. By the answer key's rules no arm earns full or partial credit.
- The answer key's documented cause (`epochx=10` and `hidden=1` together) **does** close the Energy
  gap when we run it ourselves: median 1.716 against the paper's 1.66 (+3.4%), where the defaults
  give 0.364. Neither setting alone does (0.533 and 0.427). So the cause was findable, and the search
  missed it. It is "documented and confirmed here" for Energy.
- The same setting **overshoots the held-out Yacht claim**: median 2.996 against 1.11 (+170%), where
  the defaults give 0.831 (-25%). GapFinder's held-out check would have rejected it as a cause.
  So "Unexplained" is a miss on search coverage, and the final label would probably not have been
  "Explained" even with a perfect search.
- The best partial lead was `hidden=1` in the random arm. Confirmation shows it moves Energy only
  5% of the way to the paper, so it is a name match with a weak effect, not a cause.

## Verdict per arm

All arms: same spec, targets, budget (`--max-runs 40 --candidates-per-knob 2 --cap 0.5`) and seed 0
([FROZEN.md](FROZEN.md), "Arms"). Naive = `epochx=500 hidden=2`. Noise band = 2 x MAD of the five
naive repeats of that arm. Energy gap = naive median against 1.66.

| # | Arm | Where it ran | Branch runs | Label (C_energy_rmse) | Naive median, band | Gap to paper | Score | Report |
|---|---|---|---|---|---|---|---|---|
| 1 | normal | local Docker, unsharded | 26 (25 ok, 1 timeout at 14,400 s) | Unexplained | 0.3692, +-0.0569 | -77.8% | no credit | [gap_report.md](attempt2-local/run-normal/gap_report.md) |
| 2 | evidence off | local Docker, unsharded | 26 (25 ok, 1 killed, exit 137) | Unexplained | 0.3611, +-0.0337 | -78.2% | no credit | [gap_report.md](attempt2-local/run-evidence-off/gap_report.md) |
| 3 | no README | Sandboxes, sharded | 22 (17 ok, 5 timeouts at 3,600 s) | Unexplained | 0.3828, +-0.0225 | -76.9% | no credit | [gap_report.md](run-no-README/gap_report.md) |
| 4 | all flags, random | Sandboxes, sharded | 26 (all ok) | Unexplained | 0.3903, +-0.0099 | -76.5% | no credit (lead: `hidden=1`) | [gap_report.md](run-all-flags-random/gap_report.md) |

Each arm also has `events.jsonl`, `gap_report.json` and `search.log` in its folder. The run counts
and statuses above come from the `branch_finished` events in each `events.jsonl`.

### Scoring rules, quoted, and how each arm fits

From [answer_key.md](answer_key.md), section 3:

> **Full credit.** The report names **both** `epochx` (lower, towards 10; any value that closes the
> gap in the same direction counts, 10 is the documented value) and `hidden` = 1 as the confirmed
> cause of at least one target claim, with a confirmed label ("Explained" or "Paper-artifact
> inconsistency"), where the closing run's effect exceeds the noise band. [...]

> **Partial credit.** Any one of: names exactly one of `epochx` / `hidden`, correctly confirmed;
> names both but only as "Partially explained" or "Fits but unsupported"; names `epochx` or `hidden`
> in the right direction with a closing run but a different value; flags the grid-search vs BO
> difference as a likely, untestable contributor while also finding one of the two knobs. [...]

> **Failure.** Names no relevant knob; names only an irrelevant knob (`n_splits`, `n_hidden` alone,
> `dropout_rates` or `tau_values` alone) as the cause; labels a claim "Reproduced" when the defaults
> are outside the noise band of the paper value; or confirms a cause whose re-run shows no effect
> beyond noise (a name match without the effect).

An arm that reports "Unexplained" and names no cause is not described exactly by any of the three
bullets. We score it as no credit, closest to the first failure bullet (no relevant knob named as a
cause). None hit the false-attribution bullets: no arm said "Reproduced", and no arm confirmed a
cause.

| Arm | What it tested | Strongest leads | Why it ended Unexplained |
|---|---|---|---|
| 1 normal | The ledger's hypotheses ([ledgers/normal/assumptions.json](ledgers/normal/assumptions.json)): `epochx` in {500, 1000, 2000}, `hidden` in {2, 4, 5}. The ledger recorded both as "unstated" in the paper, although the README describes the effect. Evidence gate on, but nothing reached it. | None. `epochx=1000` moved Energy by -0.49 noise units, `hidden=5` by +0.66; the report lists `hidden=5`, `hidden=4` and `epochx=1000` only as near alternatives. | Every proposed value was larger than the default, so the paper's setting (a smaller `epochx` and `hidden=1`) was never in the candidate set. Nothing moved Energy beyond the band. The combine run (`epochx=2000`, `hidden=5`) hit the 14,400 s timeout. |
| 2 | Same ledger, evidence check off. | None. Screen survivors moved Energy by -0.55, +0.20, -0.68 and -0.70 units; none was confirmed (the confirm round kept 0; the one logged test, `hidden=5`, had a bootstrap interval that includes 0). | Same candidate set as arm 1, so the same blind spot. The last run (`epochx=2000`, `hidden=4`) was killed (exit 137) when the runner was stopped. |
| 3 no README | The ledger from the clone without README or docs ([ledgers/no-README/assumptions.json](ledgers/no-README/assumptions.json)): `epochx` {500, 2000, 1000000}, `hidden` {2, 4, 5}, `n_splits` {10, 20}, plus others it could not set. | `hidden=4` (4.19 noise units) and `hidden=5` (4.02), both in the wrong direction for the paper's setting (deeper, not shallower). | Candidates again only larger than default. `hidden=4` closed the gap by the search's own test but made held-out Yacht worse and was rejected in verification. Five of 22 runs timed out at 3,600 s (`n_splits=20`, `epochx=1000000` and all three combine cells), so the combine round gave no information. |
| 4 all flags, random | Every spec knob with generated candidate values and uniform priors, no ledger, random order: `epochx` {250, 1000}, `hidden` {1, 4}, `n_splits` {2, 6} and combinations. | **`hidden=1`**: Energy 0.481 against 0.390 naive (9.79 noise units, gap -70.7%). Also `n_splits=2` (3.4 units) and `hidden=4` (1.18). | The generic grid cannot reach the documented `epochx` (the lowest value tried was 250; the paper's is 10). The best combination (`hidden=1`, `epochx=250`) reached 0.523, gap -68.5%, and held-out Yacht got worse, so verification rejected it. Nothing tested was near 1.66. |

Why arm 4 is not partial credit. Its report lists `hidden=1` under "Unconfirmed leads", not as an
explanation. The first partial bullet needs a knob "correctly confirmed", and the third needs a
closing run. The confirmation runs below show `hidden=1` alone closes about 5% of the Energy gap,
so crediting it would be crediting "a name match without the effect", which the key lists as a
failure. It is a lead worth reporting, not a cause.

Note that no arm could earn full credit under the frozen candidate sets: the key's full-credit
condition needs `epochx` lower, but the ledger arms only proposed higher values and the random arm's
smallest value was 250.

## Confirmation runs (TODO Step 5)

The key's rule: "after the search, the predicted setting is re-run (3 repeats on disjoint split
sets, since identical splits are bit-identical) and must move the metric toward the paper beyond the
noise band." Run on Sandboxes in one fan-out on the same checkpoint and spec as arms 3 and 4
(`mcd_sandbox.yaml`, base `gf/mcd/base-v2`, sharded cells, `--noise 0`, `GF_CACHE_ONLY=1`, so no
model calls). Each of the 12 runs gets its own `RUN_TAG`, so each draws its own 3 splits. Naive
defaults were run again in the same batch as the control. All 12 runs succeeded.

Raw: [confirm/run.json](confirm/run.json), [confirm/events.jsonl](confirm/events.jsonl),
[confirm/knobs.json](confirm/knobs.json) (the change sets), [confirm/fanout.log](confirm/fanout.log).
Table by [confirm/summarize.py](confirm/summarize.py), output in [confirm/summary.json](confirm/summary.json).

| Configuration | Energy RMSE, 3 runs | Median | Gap to 1.66 | Yacht RMSE, 3 runs | Median | Gap to 1.11 |
|---|---|---|---|---|---|---|
| **a. documented cause: `epochx=10 hidden=1`** | 1.821, 1.716, 1.712 | **1.716** | **+0.056 (+3.4%)** | 2.753, 2.996, 3.284 | **2.996** | **+1.886 (+170%)** |
| b1. `epochx=10` alone | 0.499, 0.605, 0.533 | 0.533 | -1.127 (-68%) | 1.815, 2.566, 1.510 | 1.815 | +0.705 (+64%) |
| b2. `hidden=1` alone | 0.427, 0.418, 0.431 | 0.427 | -1.233 (-74%) | 0.438, 0.603, 0.597 | 0.597 | -0.513 (-46%) |
| c. naive defaults (control) | 0.364, 0.345, 0.428 | 0.364 | -1.296 (-78%) | 0.831, 1.079, 0.776 | 0.831 | -0.279 (-25%) |

Repeats are listed in the order they finished; read the table by the medians.

Noise. The naive band in this batch (2 x MAD, GapFinder's definition) is +-0.038 for Energy and
+-0.111 for Yacht. The five-run bands of the four arms were +-0.057, +-0.034, +-0.022 and +-0.010 for
Energy. Pooling all 23 naive runs (4 arms and this batch): Energy median 0.381, sd 0.032, band
+-0.034; Yacht median 0.994, sd 0.174, band +-0.240 (`naive_pooled_all_arms_plus_this_batch` in
[confirm/summary.json](confirm/summary.json); the local arms are unsharded, so the pool mixes two
seeding schemes, see Deviation 3). The paper's own listed spread is +-0.19 (Energy) and +-0.38 (Yacht)
over 20 splits ([answer_key.md](answer_key.md), section 1).

What this shows.
- **The documented setting closes the Energy gap.** The median moves from 0.364 to 1.716, a shift of
  +1.352, which is 36 times the naive band and 104% of the 1.296 gap. The final value is 0.056 above
  the paper, well inside the paper's own spread of 0.19. All three repeats (1.71 to 1.82) sit within
  0.16 of 1.66. It is a confirmed effect on the target claim.
- **It needs both settings together.** `epochx=10` alone moves Energy +0.169 (13% of the gap),
  `hidden=1` alone +0.063 (5%, 1.7 naive bands in this batch). The sum of the two single effects is
  0.232; together they give 1.352. The effect is strongly non-additive, which is why a one-knob-at-a-time
  screen finds almost nothing and only a combine round with the right values could.
- **It overshoots the held-out claim.** Yacht goes from 0.831 (-25% against the paper) to 2.996
  (+170%). That is 2.7 times the paper and far outside Yacht's noise band (+-0.11 here, +-0.24 pooled).
  By GapFinder's rule (a closing change must not make a held-out claim worse) this setting would be
  rejected as a cause for Energy. This is the same rule that rejected `hidden=4` in arm 3 and
  `hidden=1, epochx=250` in arm 4. Even `epochx=10` alone worsens Yacht (+64%).
- We do not know why Yacht overshoots. Plausible candidates are the changes the key says GapFinder
  cannot test (Bayesian optimisation of dropout and tau instead of the code's grid, batch size 32
  instead of 128), and that a 308-row dataset may need a different budget than the 768-row Energy
  set. That is speculation; we did not test it.

## Was "Unexplained" a miss or justified?

Both, for different reasons, and the two should not be mixed up.

1. **A miss on search coverage.** The cause was findable. The documented setting closes the target
   gap with a large effect. All four arms failed to try a value anywhere near it: the three ledger
   arms proposed only `epochx` of 1000 or more and `hidden` of 4 or 5 (the ledger recorded the paper's
   values as "unstated"; the paper's "10x more iterations" and its single hidden layer were not
   extracted), and the random arm's generic values were 250 and 1000 for `epochx` and 1 and 4 for
   `hidden`. The only place the right direction appeared was `hidden=1` in arm 4, and combining it with
   `epochx=250` gives 0.523, not 1.7. The README text about the effect did not rescue the normal arm:
   its candidate list is the same as the no-README arm's in direction.
2. **Not an Explained label either way.** Even if a search had tried `epochx=10 hidden=1`, the held-out
   Yacht claim would have gone from -25% to +170% against the paper, and the verification step
   rejects a change that makes a held-out claim worse. The most likely label would have been
   "Unexplained", with the closest configuration reported. That is the product doing what it
   is designed to do. It is also a limit: the held-out guard cannot tell "a cause that over-explains
   one dataset" from "a wrong cause", so on this case it errs towards silence.

We did not rerun the search with `epochx=10` added to the candidates to test the second point; that
would be a new, unfrozen experiment. It is stated here as an expectation, not a result.
(Run afterwards as a post-hoc diagnostic, see "Post-hoc diagnostic" below.)

## Honest conclusion

- GapFinder made no false attribution on this case in any arm (0 of 4 confidently wrong), and the
  abstentions were honest: each report says nothing moved the gap beyond noise.
- It did not find the cause. Recall on this case is 0 of 4 arms. The failure sits upstream of the
  search logic: the candidate values (from the ledger's "unstated" reading of the paper, or from a
  generic grid around the defaults) never included the paper's smaller `epochx`.
- Nothing here supports "the README leaked the answer": the normal arm had the README and got the
  same Unexplained as the arm without it.
- The documented cause is now "documented and confirmed here" for Energy (both settings together,
  3 repeats, effect 36 noise bands, gap closed to +3.4%), and **not confirmed for Yacht**, where it
  overshoots. We cannot say the pair is the whole story of the Yacht discrepancy.
- Partial lead: `hidden=1` in the random arm (9.79 noise units). It is a correct knob and value, but
  alone it explains about 5% of the Energy gap, and the arm labelled it only as an unconfirmed lead.

## What went wrong and the deviations

All are written up in [FROZEN.md](FROZEN.md); none changed a knob, a candidate, a prompt, a model or
the search logic.

1. **Attempt 1 (Sandboxes, T = 10000) was a no-go on cost**, about 650 CPU-seconds per grid setting
   ([FEASIBILITY.md](FEASIBILITY.md)). We moved to local Docker with T = 100.
2. **Deviation 1, Docker thread fix.** In attempt 1 of the arms, all four stopped in calibration:
   the five naive cells of each arm hit the 14,400 s timeout (20 cells, no result,
   [attempt1-timeout/](attempt1-timeout/)). Cause: OpenBLAS started one thread per visible core in
   every container and 12 processes with 12 threads each fought over 12 cores. Fix: one BLAS thread per
   container in `LocalBackend` (infrastructure only). Six default cells then ran in 52 to 53 minutes.
3. **Arms split across two backends.** Attempt 2 ran locally: arm 1 took 13.8 hours (11 Oct 14:37 to
   12 Oct 04:25) and arm 2 10.9 hours ([attempt2-local/arms.log](attempt2-local/arms.log)). Arms 3 and 4
   were too slow on a teammate's laptop and were stopped; two stray local runs that started after the
   stop were killed in calibration and have no verdict
   ([attempt2-local/README.md](attempt2-local/README.md)).
4. **Deviation 2, switch to Sandboxes.** The team moved arms 3 and 4 to Token Factory Sandboxes after
   checking that Sandboxes were not billed in the Beta. The API caps any operation at 3,600 s, so the
   spec's timeout dropped from 14,400 s to 3,600 s ([mcd_sandbox.yaml](mcd_sandbox.yaml)). We first
   misread a Sandboxes VM as one core; it has four.
5. **Deviation 3, sharding.** To fit slow cells under 3,600 s, `run_cell.sh` runs every
   (dataset, split) as its own process, four at a time (`procs=auto`). The default cell fell from
   about 1,910 s of wall time to 805 s. Side effect: the first split of each dataset is bit-identical
   to an unsharded run, other splits get different random numbers. So arms 1 and 2 (unsharded) and
   arms 3 and 4 (sharded) are the same experiment in distribution, not run for run. Arms 3 and 4 and
   the confirmation runs share the sharded scheme, so the confirmation is directly comparable to them.
6. **Timeouts still lost information in arm 3**: 5 of its 22 runs (`n_splits=20`, `epochx=1000000`,
   `hidden=4` with `n_splits=10`, `epochx=2000` with `n_splits=10`, `epochx=2000` with `hidden=4`)
   ended at 3,600 s, so its combine round returned nothing. FROZEN.md predicted `n_splits=20` and large
   combined cells would time out. Arm 4 had no timeouts. Arm 1 lost its combine cell to the 14,400 s
   limit locally.
7. **No arm used its 40-run budget.** The searches ended after 22 to 26 branch runs, when their screen,
   confirm and combine rounds finished (`branch_finished` events in each `events.jsonl`).

## Caveats from the answer key

From [answer_key.md](answer_key.md), section 4, plus what this run adds.

- **Semi-blind.** The TODO stated the documented cause in the repository, and the repo's results
  filenames mention epochs and hidden layers. Sealing, the frozen system and a spec generated from the
  repo map keep it honest, but a truly blind case is a separate, later one (TODO Step 6).
- **Grid search vs Bayesian optimisation, and batch size 32 vs 128, are untestable here.** The key
  predicted a closure might stay partial; in fact Energy closed to +3.4% without them, and the open
  question is Yacht.
- **Scaled reproduction.** T = 100 Monte Carlo passes and 3 splits per cell, not 20. RMSE of the mean
  prediction is barely affected by T; the log-likelihood is more so (not used as a target).
  Each confirmation run covers only 3 splits, and the per-split sd is large on Yacht (0.3), so Yacht
  medians of three runs are rough.
- **Which numbers are "the paper's":** ICML Table 1 (Energy 1.66, Yacht 1.11), not the README column
  (Energy 1.08, Yacht 0.70), which is a later re-run.
- **The defaults are better than the paper, not worse** (key, caveat 2). The documented direction is
  confirmed: a smaller budget and a shallower net give a higher RMSE, and on Energy by about the amount
  the paper reports.
- **Repeats of identical settings and splits are bit-identical**, so noise is measured over different
  splits. The naive band is the repeat noise of 3-split cells, not the paper's 20-split spread.

## Post-hoc diagnostic (not blind, not scored)

Run after the key was revealed; it changes no arm's score or label above. One extra search on
Sandboxes with the documented values written into the hypothesis set by hand: the normal ledger plus
`epochx=10` and `hidden=1` as candidates (with the paper's "10x more iterations" and the authors'
README "10x epochs one layer" as their evidence), everything else as pre-registered. Details, the
exact edits and the gap report are in [posthoc/README.md](posthoc/README.md).

- **Label: Unexplained.** The search tested `epochx=10`, `hidden=1` and the pair. The pair gave
  Energy 1.723 against 1.66 (+3.8%, naive 0.387) but held-out Yacht 1.987 against 1.11 (+79%, naive
  1.041). Verification found it plausible with the counterfactual passing, then rejected it:
  "closes this claim but makes held-out claims worse; rejected". The pair is reported only as the
  closest configuration.
- So GapFinder's verification confirms the Energy effect and declines to call it the explanation
  because of Yacht. The probable reason Yacht's paper value cannot be matched by any setting is in
  the authors' README ("Update (2018)"): the paper-era code tuned hyperparameters by Bayesian
  optimisation shared across all splits, which caused test-set contamination and was replaced by
  per-split grid search. That is a code change, not a knob. Not tested here.
- The result of the blind evaluation stays 0 of 4 arms.

## Cost

- **Nemotron, billed:** about **$0.28**, all of it ledger extraction: $0.1538 (normal ledger) and
  $0.1253 (no-README ledger), from [ledgers/normal/cost.json](ledgers/normal/cost.json) and
  [ledgers/no-README/cost.json](ledgers/no-README/cost.json) (Ultra and Super tokens priced as in the
  config). The searches themselves cost $0 in model calls, except $0.0009 for arm 3's failed-run triage
  ([run-no-README/gap_report.md](run-no-README/gap_report.md)); arms 1, 2 and 4 report $0.
- **Sandboxes, reported (diagnostic, not billed in the Beta):** arm 3 $1,043.03, arm 4 $584.66
  (their gap reports), confirmation runs $134.56 ([confirm/fanout.log](confirm/fanout.log)). Arms 1 and 2
  ran locally ($0). The reported figure is about $0.01 per CPU-second and is counted by GapFinder's own
  guard, which is why `GF_SANDBOX_GUARD_USD` was raised for these runs; no GapFinder code changed.
  The Nebius billing console showed no Sandboxes charge ([FROZEN.md](FROZEN.md), Deviation 2).
- **Wall time:** arm 4 took 1 h 18 min and arm 3 3 h 05 min on Sandboxes, running together
  ([sandbox-arms.log](sandbox-arms.log)); the confirmation batch took about 14 minutes of wall time (12 cells at once; the naive cells set its
  length, the documented-setting cells took about 1.6 minutes of reported time each).

## Files

| What | Where |
|---|---|
| Pre-registration, deviations | [FROZEN.md](FROZEN.md) |
| Sealed key (revealed) and hash | [answer_key.md](answer_key.md), [answer_key.sha256](answer_key.sha256) |
| Arm 1 and 2 (local) | [attempt2-local/run-normal/](attempt2-local/run-normal/), [attempt2-local/run-evidence-off/](attempt2-local/run-evidence-off/) |
| Arm 3 and 4 (Sandboxes) | [run-no-README/](run-no-README/), [run-all-flags-random/](run-all-flags-random/), [sandbox-arms.log](sandbox-arms.log) |
| Ledgers the arms used | [ledgers/](ledgers/) |
| Confirmation runs | [confirm/](confirm/) |
| Post-hoc diagnostic (not blind) | [posthoc/](posthoc/) |
| Gap check before sealing (defaults only) | [gapcheck/](gapcheck/) |
