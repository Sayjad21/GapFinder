# batch-5: results (code frozen at tag `batch-5`, `0586e5c`; protocol in PROTOCOL.md)

The first blind cases whose harness was built by `gapfinder harness`. Each run was committed before its key
was opened; each key matched its sealed hash.

| Case | Documented cause | GapFinder | Score (the key's pre-registered rule) |
|---|---|---|---|
| **b5a** Topology Attack and Defense for GNNs (IJCAI 2019), Cora, CE-PGD | `attack.py` counts each undirected edge twice (`total_edges = adj.data.shape[0]`), so the attack budget is twice the paper's. Flag equivalent: `--perturb_ratio` at half the paper's value (0.025 for the 5% target). Owner confirmed in issue #6 | **Fits but unsupported, `dropout = 0.5`** (gap -5.1% -> +0.0%). The true value `perturb_ratio = 0.03` was measured, fit the target (+1.1%), and is listed as a lead and in the 14-configuration equivalence set | **miss** (not confidently wrong): the equivalence set is larger than 3, and the reported answer is a decoy |
| **b5b** Structural Deep Clustering Network (WWW 2020), ACM | (sealed: key not opened) | **harness failed at the command step** (the frozen harness's own steps, run locally; not run in Sandboxes) | not scored; the key stays sealed so the case can be run blind once the harness reads these formats |

Run committed in `6c9e89c` before the key was opened (hash `9022bd01...88e9`, matches).

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

Sandboxes: 150 search runs, unbilled.
