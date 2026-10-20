# HARNESS.md (written by `gapfinder harness`)

**Status:** ready for approval

A person reads the commands below and approves them (about 5 minutes). The knobs are mechanical: every flag of the script at its default, so they need no approval.

## Claims

Rule: the target, then every other cell of its table row (same conditions, another metric) as held-outs.

| claim | role | metric | paper | spec metric |
|---|---|---|---|---|
| C_auc | target | ROC-AUC | 82.7 | `c_auc` |
| C_ap | held-out | Average Precision | 20 | `c_ap` |
| C_rec | held-out | Recall@k | 23.8 | `c_rec_recall` |

## Command

Picked by the claims' words in the command's arguments (README and shell scripts):

**picked** `cd benchmark && python main.py --model dominant --dataset inj_cora --gpu -1` (given by the runner; matched nothing)

One run, at every default:

```
cd benchmark && "${PYTHON:-python}" main.py --model dominant --dataset inj_cora --gpu -1
```

### Knobs

| knob | default | declared at |
|---|---|---|

### Fixed (not knobs)

- `model`: its value 'dominant' is one of the claim's conditions: defines the claim
- `dataset`: dataset: defines the claim
- `gpu`: how to run (paths, devices, logging), not the method

## Environment

Image `python:3.8-slim`; checkpoint `cd3e9ea9-1933-474a-9264-e5ad4d18e677`; recipe:

```
cd /work && pip install --no-cache-dir https://download.pytorch.org/whl/cpu/torch-2.0.0%2Bcpu-cp38-cp38-linux_x86_64.whl https://data.pyg.org/whl/torch-2.0.0%2Bcpu/pyg_lib-0.2.0%2Bpt20cpu-cp38-cp38-linux_x86_64.whl https://data.pyg.org/whl/torch-2.0.0%2Bcpu/torch_cluster-1.6.1%2Bpt20cpu-cp38-cp38-linux_x86_64.whl https://data.pyg.org/whl/torch-2.0.0%2Bcpu/torch_scatter-2.1.1%2Bpt20cpu-cp38-cp38-linux_x86_64.whl https://data.pyg.org/whl/torch-2.0.0%2Bcpu/torch_sparse-0.6.17%2Bpt20cpu-cp38-cp38-linux_x86_64.whl https://data.pyg.org/whl/torch-2.0.0%2Bcpu/torch_spline_conv-1.2.2%2Bpt20cpu-cp38-cp38-linux_x86_64.whl torch_geometric tqdm pyod scikit-learn numpy scipy networkx setuptools
cd /work && pip install -e . --no-cache-dir
pip install --no-cache-dir torch_geometric==2.3.0
```

## Data kept in the base checkpoint

0 files, 0.0 MB (new since the environment: downloads, preprocessing, dataset loaders' caches). 41 other new files deleted (outputs, logs, model checkpoints).


## Smoke run

1 run(s) in parallel; exit 0 after 1075.0 s

- `c_auc`: 76.64
- `c_ap`: 18.25
- `c_rec_recall`: 28.12

Seeds vary: unknown (one copy)

## Metric binding

Test before unqualified before validation before train; final before best; on the paper's scale. A tie is a refusal.

| claim | printed label | value | scale | alternatives |
|---|---|---|---|---|
| C_auc | `inj_cora DOMINANT AUC` | 0.7664 | 100 |  |
| C_ap | `AP` | 0.1825 | 100 |  |
| C_rec | `Recall` | 0.2812 | 100 |  |

## Paper-year environment (knob `gf_paper_year_env`)

Packages as of 2022-07-01 (Python 3.8.20): `pyod==1.0.2`, `scikit-learn==1.1.1`, `torch-geometric==2.0.4`, `tqdm==4.64.0`. Used: yes.

- torch: not installed (part of another package, or not needed)

## Fit in one Sandboxes operation (3600 s)

as is: about 1075 s fits one operation

## Notes

- command given by the runner: `cd benchmark && python main.py --model dominant --dataset inj_cora --gpu -1`

Model spend: $0.0072
