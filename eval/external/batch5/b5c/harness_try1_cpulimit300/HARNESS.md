# HARNESS.md (written by `gapfinder harness`)

**Status:** stopped at env: the model gave up: The benchmark script is being killed due to out-of-memory (OOM) even after adding 2GB swap; the environment likely lacks sufficient memory to run the model.

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

Image `python:3.8-slim`; checkpoint `958ea454-3f04-4ae6-b2eb-de4e61c5202a`; recipe:

```
pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir -r benchmark/requirements.txt && pip install --no-cache-dir -r docs/requirements.txt
cd /work && pip install --no-cache-dir .
pip install --no-cache-dir --force-reinstall torch_geometric==2.0.4
pip install --no-cache-dir --upgrade torch_geometric==2.3.1
```

## Notes

- command given by the runner: `cd benchmark && python main.py --model dominant --dataset inj_cora --gpu -1`

Model spend: $0.0150
