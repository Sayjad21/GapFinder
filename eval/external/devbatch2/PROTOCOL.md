# devbatch-2: protocol (written before any run)

A fresh frozen batch: plan item 6 of docs/CONTEXT_v11.md section 7. It measures the changes of 2026-10-18
(paper reading, early confirmation, the constant matcher, the environment builder) on repositories none of
them was built or judged on.

## Freeze

- Code: git tag `devbatch-2`, at the commit that adds this file. Runs use a worktree at that tag, with
  `python -P` so the main checkout is never imported, and the worktree's own `.env`.
- Nothing in `gapfinder/` changes until every run below is committed. A bug found on the way is written
  down here and fixed after the batch, never in it.

## Papers (dev-set cases 7, 8 and 10 in `eval/external/devset/CANDIDATES.md`, unused before)

| Id | Paper | Repository at commit |
|---|---|---|
| at | Anomaly Transformer (ICLR 2022) | thuml/Anomaly-Transformer `b0ee470c` |
| ncf | Neural Collaborative Filtering (WWW 2017) | hexiangnan/neural_collaborative_filtering `4aab159e` |
| pyg | GAT vs GCN, PyG `benchmark/citation` (Pitfalls of GNN Evaluation, 2018) | pyg-team/pytorch_geometric `ff9fb3d7` (2.3.1) |

All three must fit a Sandboxes VM (4 vCPU, 3.9 GB, no swap, at most 3600 s a run). A case that can't is
reported as "harness failed", not moved to Docker.

## Stage 1: the environment builder, unseen (a measurement on its own)

`gapfinder env-build <repo> --commit <sha> --local <checkout>`, frozen code, no hand help, no goal command.
Recorded in `<id>/env_build.json`: whether every third-party import loads, the image, and the recipe. This is
the builder's first number on repositories it has never seen (the first env bench, 1/7, was on dev-set
repos, and the image-switch change came from it).

## Stage 2: the harness

Written by a harness agent from a brief that does **not** contain the documented cause. The agent:
- uses the stage-1 image when it works, and otherwise its own pins (recorded as hand-built);
- writes `HARNESS.md`, `case.json`, `<id>.yaml` and `targets.json`.

Every harness must have **at least two claims: one target and at least one held-out** whose metric the run
prints. With one number, different causes are rarely distinguishable (planted pygcn: 4 of 8 misses).
- at: SMD precision, recall and F1 from the main table;
- ncf: ML-1M HR@10 and NDCG@10 of NeuMF (GMF and MLP as further held-outs if the time allows);
- pyg: GAT and GCN accuracy on Cora (target: GAT), with CiteSeer as held-out.

## Stage 3: the search

`gapfinder ledger` (Nemotron Ultra, the paper PDF), then `gapfinder search` with that ledger, in Sandboxes,
from the frozen worktree.

## Scoring (fixed now)

The documented causes are the CANDIDATES.md entries. For these three they are evaluation protocol or noise,
not a setting. So running the repo may well reproduce the paper's number.

- **at:** the point adjustment, which uses ground-truth labels, and validation on the test loader in
  `solver.py`. Correct means one of:
  - the report names the adjustment, or test-set use in evaluation, as a lead, a difference or a
    selection-in-code finding;
  - or it reports "Reproduced" and names it.

  "Reproduced" without naming it is a correct abstention, scored as a miss of the cause.
- **ncf:** the best epoch is picked by test HR (`if hr > best_hr`). Same rule as at.
- **pyg:** the GAT-over-GCN margin is within split noise and flips with random splits. Correct means one of:
  - "Reproduced" or "Inconclusive" with the margin inside the noise band;
  - or `random_splits` found to move the claims.
- **Confidently wrong** (any case): "Explained" or "Paper-artifact inconsistency" naming a setting that is not
  among the documented causes.
- The batch is reported as found / correct abstention / missed / confidently wrong, next to devbatch-1
  (1/5 correct, 0 confidently wrong).

## After the batch (not in it)

If the stage-2 harnesses work, planted causes (`eval/planted/plant.py`) are drawn on them too. Their several
claims make planted causes identifiable, unlike pygcn. These are measurement only.
