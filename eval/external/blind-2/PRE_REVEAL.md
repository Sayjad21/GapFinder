# blind-2: the run, and what the runner saw, written before the reveal

Written after the search finished and before `answer_key.md` was opened. `run/` is committed unchanged with
this file.

## Inputs and command

- GapFinder at `v1.4` = `blind-2` (`e0568b6`). The engine is unchanged since the tag.
- Ledger: `ledger/` (Nemotron, $0.20): 165 claims and 29 assumptions. The assumptions use the code's real
  flag names, which is fix 1 at work.
- Spec `graphmae.yaml`, targets `targets.json`, harness `HARNESS.md`, all committed before the search
  (`19d9adf`). Image `docker/Dockerfile` (`gf-graphmae`).
- Command (local Docker backend):
  ```
  gapfinder search --spec eval/external/blind-2/graphmae.yaml --targets eval/external/blind-2/targets.json \
      --assumptions eval/external/blind-2/ledger/assumptions.json --claims eval/external/blind-2/ledger/claim_ledger.json \
      --backend local --concurrency 2 --max-runs 60 --paper "GraphMAE (KDD 2022)" --out eval/external/blind-2/run
  ```
  Environment: `GF_B2_SOURCE` (a local clone at `1be5941`), `GF_SANDBOX_GUARD_USD=1000000`,
  `GF_SPEND_CAP_USD=33`.
- **One false start, listed as the protocol asks (`false-start/`):** the first launch omitted
  `GF_SANDBOX_GUARD_USD`, and the spend guard refused the first run. No branch ran. The relaunch is the
  same command with the guard raised.

## Result (`run/gap_report.md`)

- **Label:** `C_collab` is **Explained** by **`mask_rate=0.5`**. The gap goes from -2.2% to -0.1%, with a
  noise band of ±1.0%.
  - Naive median 78.56 over 5 runs. With `mask_rate=0.5`: 80.52, 80.22, 79.58 (paper 80.32).
  - Counterfactual PASS.
  - Evidence PASS, as code evidence: `graphmae/utils.py:73` sets the argparse default `--mask_rate 0.5`, and
    `scripts/run_graph.sh` also passes `--mask_rate 0.5`. COLLAB's `configs.yml` entry overrides it with
    0.75.
  - Effect interval [+0.87, +1.66].
- **Held-out claims** (all tuned separately, shown as notes): IMDB-B, IMDB-M and MUTAG are not worse
  beyond noise.
- **The run is partial.** The 60-run budget ran out in the confirmation race, just before 2 more runs of
  `mask_rate=0.3`. The label was verified from the runs already made.
- **Unconfirmed leads:** `mask_rate=0.3` (1.93 noise units, gap +0.3%), `encoder=gat` (1.63),
  `in_drop=0.3` (1.04).
- **History matching:** "naive within noise of every claim", with 10 configurations not ruled out.
  `mask_rate=0.5` is the most consistent (max I 0.05).

## What the runner saw, and what went wrong in GapFinder (before the reveal)

1. **The `pool:` key disclosed in HARNESS.md:** `pooling=max` was screened (0.81 noise units, gap -1.4%)
   and did not become a lead. `pooling=sum` made COLLAB much worse (-6.31).
2. **Budget spent on the default under another spelling.** The ledger's candidates included
   `deg4feat=False`, `scheduler=True` and `residual=False`. The defaults are `false`, `true` and `false`.
   GapFinder counted each as a change, so a few screening runs were naive repeats (`apply_knobs` saw no
   change). This is a value-normalisation bug, for after the reveal.
3. **The budget was thin.** 31 knobs and 94 hypotheses: the escrow screened 40, the confirmation race was
   cut short, and the fallback round (`concat_hidden`, `linear_prob`, `lr_f`) never ran.
   `max_epoch` values above the cost cap (60) were reported as untestable.
4. **The evidence for 0.5 is the code's own default and the README script.** That is a legitimate source,
   because the authors' published command says 0.5. But it is code evidence, not a statement in the paper.

**Protocol:** no re-run and no engine change before the reveal.
