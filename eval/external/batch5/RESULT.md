# batch-5: results (code frozen at tag `batch-5`, `0586e5c`; protocol in PROTOCOL.md)

The first blind cases whose harness was built by `gapfinder harness`. Each run was committed before its key
was opened; each key matched its sealed hash.

| Case | Documented cause | GapFinder | Score (the key's pre-registered rule) |
|---|---|---|---|
| **b5a** Topology Attack and Defense for GNNs (IJCAI 2019), Cora, CE-PGD | `attack.py` counts each undirected edge twice (`total_edges = adj.data.shape[0]`), so the attack budget is twice the paper's. Flag equivalent: `--perturb_ratio` at half the paper's value (0.025 for the 5% target). Owner confirmed in issue #6 | **Fits but unsupported, `dropout = 0.5`** (gap -5.1% -> +0.0%). The true value `perturb_ratio = 0.03` was measured, fit the target (+1.1%), and is listed as a lead and in the 14-configuration equivalence set | **miss** (not confidently wrong): the equivalence set is larger than 3, and the reported answer is a decoy |
| **b5b** Structural Deep Clustering Network (WWW 2020), ACM | The paper reports each run's **best epoch** by the label-based metrics (the code evaluates against the true labels every epoch); the README run read at its last epoch is about 2 ACC / 4 NMI points lower. Not a flag (issue #23) | **Unexplained**, out-of-space likely (134 runs, 18 code patches); leads: unexposed constants and the paper's 50 epochs (a decoy) | **miss** (not confidently wrong): out of space, but it did not point at the evaluation/reporting protocol |
| **b5c** BOND (NeurIPS 2022 D&B), DOMINANT on inj_cora | **Library API drift:** PyGOD 0.3.1's `alpha=None` auto-balanced DOMINANT's attribute/structure weight (about 0.84); in PyGOD 1.0 it is `weight`, default 0.5, and the benchmark's `alpha` is silently dropped. Fix: weight about 0.84, or PyGOD 0.3.1 (author, issue #83) | **Unexplained**, out-of-space likely (17 runs); Adam->SGD fit every claim on one run, not after repeats; structural leads: grid averaging, early stopping | **miss** (not confidently wrong): out of space, but not attributed to a library version change |

Runs committed before their keys were opened: b5a in `6c9e89c` (hash `9022bd01...`), b5b and b5c in `1b7d102` (hashes `f8252f52...`, `9b25aaef...`); all three match.

**Batch-5 in one line: 3 papers searched, 0 correct, 0 partial, 0 confidently wrong.** Each miss has a different, specific reason (below), and in each the run already held the information the answer needed.

## b5a: why it missed (each is a class; fixed after the batch, measured on the next one)

1. **A setting whose meaning in the code differs from the paper's by a factor.**
   - The code's accuracy-against-budget curve is the paper's curve squeezed by 2: the paper's 10% (0.673) is the
     code's 0.05 (0.684), the paper's 20% (0.598) is the code's 0.10 (0.611). GapFinder had measured all of
     these.
   - The claims at fixed settings (plan item 14) set `perturb_ratio` to the paper's 0.10/0.15/0.20 on top of each
     candidate. That overwrites the very setting that is wrong, so "the code's knob means twice the paper's"
     can't be expressed as any value.
   - The class: units and scales (a fraction against a percent, an edge counted twice, a rate per sample against
     per batch). When claims sweep a knob, a scale hypothesis (the paper's v is the code's c x v, c fitted on the
     target and checked on every point) is testable and identifiable.
2. **A decoy that hits the target exactly wins the tie.**
   - `dropout = 0.5` (the value `train.py` trains with; `attack.py` defaults to 0) gives exactly 0.721. At the
     other budgets it is 2.8-8.9% off, so history matching ruled it out ("doesn't fit C_t3_15, C_t3_20"), but no
     tested configuration fit every claim (because of 1), so it stayed the answer, capped at "Fits but
     unsupported".
3. **A deterministic program.** All 5 naive runs gave 0.684, so the noise band is the floor and 14
   configurations are statistically indistinguishable on the target alone.

## b5b: the harness could not be built (two formats it does not read)

Run on the frozen code's own deterministic steps (claims, command, template, binder), locally, at no cost:
- **The README lists the datasets as alternatives:** `python sdcn.py --name [usps|hhar|reut|acm|dblp|cite]`. The
  dataset flag is called `--name`, which the harness treats as how-to-run, so the whole bracket was kept as the
  value (`--name '[usps|hhar|reut|acm|dblp|cite]'`). Class: README placeholders and alternatives (`[a|b|c]`,
  `{a,b}`, `<dataset>`), and dataset flags with other names.
- **The program prints `199Z :acc 0.9045 , nmi 0.6831 , ari 0.7391 , f1 0.9042`:** a label then a space then the
  number. The binder reads `label: value` and `label = value` only, so it finds no number. Class: metrics printed
  without a separator.
- Env-build would have spent Super calls on a goal command that can't work, so the case was not run in Sandboxes.
  Per the protocol it is not built by hand. Its key is still sealed: once the harness reads both formats, b5b can
  be run blind in a later batch.

## b5c: the harness could not be built either

- **The experiment's README is in a subfolder** (`benchmark/README.md`; the repository is the PyGOD library). The
  command picker reads the top-level README and shell scripts only, so it found no command.
- **Its usage line is help syntax:** `python main.py [-h] [--model MODEL] [--gpu GPU] [--dataset DATASET]`, the same
  placeholder class as b5b.
- **The settings are in code:** `main.py` has `--model`, `--gpu` and `--dataset` only; the trial count (20) and the
  hyperparameter grid are in `main.py` and `benchmark/utils.py`. Only the patch round could reach them.
- **"AP" is not a known metric name** to the binder (its average-precision claim would not bind).
- Key still sealed.

## batch-5b (harness fixes, engine unchanged): b5b and b5c again

- **A setting of mine, not the harness, killed the first attempts.** The Sandboxes backend puts a 300-second
  CPU-time limit (`ulimit -t`, `GF_SANDBOX_CPU_LIMIT_S`) on every process unless it is raised; earlier batches
  raised it (6000-60000), batch-5 did not. SDCN's 4-thread training was killed (SIGKILL, exit 137) at epoch 45
  after 95 s with 3.4 GB free; env-build's model then blamed `.cuda()` (its own test step runs without the CPU
  shim; under the shim the code runs) and gave up. b5c's "out of memory" report was probably the same kill. b5a's
  runs used less than 300 CPU-seconds and are unaffected. Re-run with `GF_SANDBOX_CPU_LIMIT_S=20000` (an
  infrastructure setting; allowed by the protocol).
- **b5b:** the harness was built (8 claims bound with `--bind`, case.md's Z/Q mapping; 10 repeats; one cell about
  40 minutes). Naive SDCN ACC about 88.8 against the paper's 90.45. Ledger $0.29. Search: see below.
- **b5c:** env-build passed; the smoke run's Sandboxes operation then failed twice at the same point with HTTP 500.
  Out of memory is suspected (env-build's model reported it even with 2 GB of swap) but not shown: the harness
  crashed on the API error without writing HARNESS.md, so that environment was lost. **Harness failed at smoke;**
  not run further, no ledger spent, key kept sealed.

Harness bugs found on the way (fixed after the batch): env-build's own test steps run without the CPU shim; on
failure env-build reports its starting checkpoint instead of the last good one; an infrastructure error in the
smoke run crashes the harness without writing HARNESS.md; the default CPU-time limit (300 s) should follow the
run's timeout instead.

## b5b: why it missed

- **Best-epoch reporting with the labels.** SDCN prints its Z metrics after every epoch; the paper's numbers are
  each run's maximum over epochs (selected with the true labels), the harness bound the last epoch ("final before
  best"). The per-run maximum was in every run's log: comparing the paper's number with the final value and with the
  best epoch costs no run. GapFinder's protocol tests look for selection by test score inside the code; here the
  selection happened when the authors read the output.
- The 50-epoch difference it reported is the key's listed decoy (epoch 49 is still far off).

## b5c: why it missed

- **The library under test is the repository itself.** The paper-year knob (item 19) pins the imported packages to
  their releases before the paper's date, but PyGOD is installed from the checkout, so it was not pinned; PyGOD 0.3.1
  (the paper's version, and the author's stated fix) was never tried.
- **A keyword argument silently swallowed after an API rename.** `benchmark/utils.py` passes `alpha=` to `DOMINANT`,
  whose signature now names `weight` and forwards the rest into `**kwargs`. A static check for keyword arguments a
  callee does not name (and only forwards) would point at it; none exists.
- Only 17 runs: the script exposes no settings, so the search had the paper-year knob and the patch round only.

## Lessons for after the batch (each seen once here; proposals, not implemented)

| Case | Class | A test that would have caught it |
|---|---|---|
| b5a | A setting's unit or scale differs between paper and code (an edge counted twice) | When claims sweep a knob, fit a scale c (paper v = code c x v) on the target and check it on every point |
| b5b | The paper's number is the best epoch chosen with the labels | From the per-epoch log of the same runs: does the paper's number match the best epoch rather than the last? (no extra runs) |
| b5c | Library API drift in the code's own package | The paper-year knob also installs the repository's own package as released before the paper (when it is on PyPI); a static check for swallowed keyword arguments |

## The automatic harness on its first unseen repo

- It got to a spec with one recorded change: `--repeats 5` (the paper's 5 splits) ran 4 copies in parallel and
  the smoke run failed (exit 120, apparently memory: one copy runs fine); `--repeats 1` passed. The harness has
  no memory-aware parallelism (a gap).
- The experiment needs two commands (`train.py`, then `attack.py`). The harness templated only `attack.py`;
  env-build ran `train.py` itself to satisfy its goal, so the natural model is fixed in the environment and
  `train.py`'s settings are not knobs. Here the cause was in `attack.py`, so this did not decide the case.
- HARNESS.md printed "Seeds vary: no" for a single copy, where it can't know (a display bug).
- The ledger dropped 57 of 67 claims as ungrounded (to look at); the claims came from `case.md` anyway.
- Two Table 1 claims were not used: one repeats the target's setting, the other needs `--method CW`, which the
  harness takes only as a number.
- Order: the harness ran before the ledger, to save the ledger's cost if the harness failed.

## Cost

| Case | Ledger | Environment | Search | Total |
|---|---|---|---|---|
| b5a | $0.159 | $0.015 | $0.002 | $0.18 |
| b5b | $0.292 | $0.014 | $0.003 | $0.31 |
| b5c | $0.199 | $0.022 | $0.001 | $0.22 |
| **batch** | | | | **$0.71** |

Sandboxes: 150 search runs, unbilled.
