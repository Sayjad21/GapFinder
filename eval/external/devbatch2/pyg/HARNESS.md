# devbatch-2 `pyg` harness: GAT vs GCN, PyG `benchmark/citation`

Paper: Veličković et al., "Graph Attention Networks", ICLR 2018, Table 2 (transductive, fixed Planetoid split).
Code: pyg-team/pytorch_geometric at `ff9fb3d7cdbaa2f2b8a848fb6cc5f4c3f465118c` (release 2.3.1),
`benchmark/citation/gcn.py` and `gat.py`. No repository file is changed.

The harness agent wrote `case.json`, `pyg.yaml`, `targets.json` and `harness/emit.sh`, built the image and ran
two smoke runs. It stopped (an API session limit) before writing this file and before the search. The
orchestrator wrote this file and set the run count below, by a mechanical rule; nothing else changed.

## Image

The automatic image worked. `case.json`'s `setup` reproduces stage 1's recipe (`env_build.json`):
- python:3.8-slim, torch 1.9.0+cpu, the repo installed with `pip install -e .`;
- then the Planetoid datasets (Cora, CiteSeer, PubMed) downloaded at build time.

Build checkpoint: `3a358250-f2ee-4694-8872-aa858cac0734`.

## Claims (paper Table 2)

| Claim | Metric | Paper | Role |
|---|---|---|---|
| C34 | gat_cora_acc | 83.0 | target |
| C35 | gat_citeseer_acc | 72.5 | held-out |
| C_gcn_cora | gcn_cora_acc | 81.5 | held-out |
| C_gcn_citeseer | gcn_citeseer_acc | 70.3 | held-out |

One shared setting should fit all four: one protocol, the fixed split, as Table 2's caption states. PubMed is
left out for time.

## What a run is

One cell runs four processes at once, one per vCPU (`OMP_NUM_THREADS=1`): `gcn.py` and `gat.py`, each on Cora
and CiteSeer. Each process trains `--runs` models and prints the mean ± std of the test accuracy, which
`emit.sh` reports in percent.

The naive commands are run.sh's fixed-split lines (`python gcn.py --dataset=X`, `python gat.py --dataset=X`),
so every flag is at the script's default. The code sets no seed, so its own randomness is the noise.

## Knobs

Every argparse flag of gcn.py and gat.py, model-prefixed (`gcn_*`, `gat_*`), at each script's default, plus
the two shared protocol flags as 0/1 knobs passed to both scripts: `random_splits` and `no_normalize_features`.
Left out:
- `--dataset`: it defines the claim;
- `--runs`: the scale (below);
- `--inference`, `--profile`, `--bf16`: how to run (inference timing, the profiler, bf16 only on the inference
  path).

## Deviation: the number of GAT runs (discrepancy 0.05)

- run.sh's naive count is 100 runs for each script; GCN keeps it.
- For GAT, 100 runs do not fit 3600 s. The agent's 20-run smoke runs both timed out at 3600 s, under heavy
  Sandboxes load from other searches.
- Rule (the same one the `at` harness used): halve until a run fits. So **GAT runs 10**.
- Timing measured with 2 GAT and 10 GCN runs per dataset, four processes at once (the cell's layout), under
  less load:

  | Model | CiteSeer | Cora |
  |---|---|---|
  | GAT | 51 s per run | 21 s per run |
  | GCN | 5 s per run | 1.7 s per run |

  Peak memory 0.7 GB.
- The count was set by the rule, not toward any expected result. Fewer runs make each mean noisier; the
  scripts' printed std is kept as a metric.

## Smoke run at 10 GAT runs (the spec's naive command, as rendered)

509 s wall, 0.7 GB peak. gat_cora_acc 83.40 ± 0.40, gat_citeseer_acc 70.70 ± 0.30, gcn_cora_acc 81.30 ± 0.60,
gcn_citeseer_acc 71.00 ± 0.70. Search base: the build checkpoint `3a358250`; code source: the repo root (the run
command's paths are relative to /work).
