# devbatch-2: results (protocol in PROTOCOL.md; code frozen at tag `devbatch-2`, `e0117a2`)

## Stage 1: environment builder on three unseen repos

| Id | Imports load | Image | Recipe | Could it run the experiment? |
|---|---|---|---|---|
| at | yes | python:3.6-slim | 1 command (torch 1.4.0 and friends) | **no**: `model/attn.py` calls `.cuda()` unconditionally (no GPU in the VM), and the paper's batch 256 runs out of memory. The harness layered a CPU shim, jemalloc and batch 32 on top of it |
| ncf | yes | python:3.7-slim | 2 commands (gcc, BLAS, Theano 0.8, Keras 1.0.7, h5py) | **no**: Python 2 code (`layers[0]/2` is a float, `xrange`, `has_key`). The harness hand-built python:2.7 |
| pyg | yes | python:3.8-slim | 1 of 2 commands kept (torch 1.9 CPU, `pip install -e .`) | **yes** (the harness reused the recipe), but the naive scale doesn't fit 3600 s |

- Imports load on 3/3; the experiment runs on 1/3.
- Model cost $0.014.
- The gap between the two is the import-only goal: an image whose imports load is not a runnable image.

## Stage 3: searches

| Id | Default runs vs paper | GapFinder | Score (PROTOCOL.md) |
|---|---|---|---|
| ncf | NeuMF HR@10 0.6825 (5 runs, CV 0.4%) vs 0.688; NDCG -0.8%; MLP/GMF within 0.6% | **Reproduced** after 5 runs | **correct abstention, cause missed**: the test-set epoch selection was not named |
| at | 5 naive runs: F1 91.9 (paper 92.33, -0.5%), P -0.0%, R -1.0%; CV 0.4% | **Reproduced** after 5 runs | **correct abstention, cause missed.** The ledger extracted the paper's own statement of the point adjustment ("We adopt the widely-used adjustment strategy ...", p. 6) as assumption `adjustment_strategy` (prior 0.8), but the report lists it only under "not settable with this harness", not as a lead |
| pyg | 5 naive runs: GAT Cora 83.0 (paper 83.0); GAT CiteSeer 70.8 (72.5, -2.3%); GCN Cora 81.3 (81.5); GCN CiteSeer 71.1 (70.3, +1.1%) | **Reproduced** (target) after 5 runs | **correct abstention, cause missed.** The Cora margin (1.7 points) is outside the noise band, so the pre-registered "margin within noise" is not met. On CiteSeer the paper's ranking already flips in the naive runs (GCN 71.1 > GAT 70.8), which is the documented finding's direction, but the report doesn't say so; `random_splits` was never tested |

## The batch

**0 of 3 causes found, 3 correct abstentions, 0 confidently wrong** (devbatch-1: 1/5 correct, 0 confidently
wrong).

- Every target reproduced within noise on the first 5 runs, so no search ran: NCF -0.8%, PyG 0.0%, AT -0.5%.
- The pre-registered causes are protocol and noise findings that the paper's number already contains:
  - NCF: test-set epoch selection;
  - AT: label-based point adjustment, which the paper states;
  - PyG: the ranking depends on the split.

  A tool that explains gaps between paper and code has no gap to explain here. It was right not to invent
  one, and it said nothing about the flaw.
- What the three share (bugs 2 and 5 below, seen on all three): a reproduced number is not audited.
  - Static leakage checks are not reported;
  - held-out misses and broken comparisons are not reported (PyG CiteSeer: GCN beats GAT);
  - the paper's own stated protocol is buried under "not settable" (AT).

  This is the class to fix next, measured on a fresh batch.

## Bugs and gaps found during the batch (fixed only after it)

1. **GapFinder's hooks shadow an existing `sitecustomize`.** The trace and patch hooks are a
   `sitecustomize.py` on PYTHONPATH and don't chain to the environment's own. at's CPU shim lived there.
   Worked around in the harness (the shim moved to a `.pth` file). The class: any environment that customises
   startup through sitecustomize breaks under tracing and patching.
2. **Nothing static is reported when a number reproduces.** ncf's loop `if hr > best_hr: best_hr, best_ndcg,
   best_iter = ...` over test-set evaluations is what `code_checks` calls selection on test data (leakage).
   The report lists leads only when a claim is out of space or unsupported, so a reproduced but leaky number
   gets no warning. The class: protocol flaws that the paper's number depends on.
3. **env-build's default goal is too weak.** Imports loaded on all three repos, but two didn't run. A short run
   of the entry script (or the README's command) should be the default goal; the `--goal` option exists, but
   stage 1 ran without it, by protocol.
5. **A reproduced target ends the analysis** (seen on ncf and pyg, so a class). When the target is inside
   noise, GapFinder stops, even when a held-out claim misses (pyg: GAT CiteSeer -2.3%), and it never checks
   the paper's comparison between methods (GAT beats GCN). Relation claims (`Target.relation`) exist but no
   harness declared one. Fix after the batch: report held-out claims outside noise and violated relations
   even when the target reproduces, and derive relation claims from the paper's tables.
4. **`build_case.py`'s fetch is Python 3 only** (the ncf harness fetched with curl instead). `env_build.fetch`
   already works on Python 2 and 3.
