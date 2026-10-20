# HARNESS.md (written by `gapfinder harness`)

**Status:** ready for approval

A person reads the commands below and approves them (about 5 minutes). The knobs are mechanical: every flag of the script at its default, so they need no approval.

## Claims

Rule: the target, then every other cell of its table row (same conditions, another metric) as held-outs.

| claim | role | metric | paper | spec metric |
|---|---|---|---|---|
| C_z_acc | target | SDCN ACC | 90.45 | `c_z_acc` |
| C_z_nmi | held-out | SDCN NMI | 68.31 | `c_z_nmi` |
| C_z_ari | held-out | SDCN ARI | 73.91 | `c_z_ari` |
| C_z_f1 | held-out | SDCN F1 | 90.42 | `c_z_f1` |
| C_q_acc | held-out | SDCN_Q ACC | 86.95 | `c_q_acc` |
| C_q_nmi | held-out | SDCN_Q NMI | 58.9 | `c_q_nmi` |
| C_q_ari | held-out | SDCN_Q ARI | 65.25 | `c_q_ari` |
| C_q_f1 | held-out | SDCN_Q F1 | 86.84 | `c_q_f1` |

## Command

Picked by the claims' words in the command's arguments (README and shell scripts):

**picked** `python sdcn.py --name [usps|hhar|reut|acm|dblp|cite]` (README.md:18; matched acm, sdcn)

One run, at every default:

```
"${PYTHON:-python}" sdcn.py --name acm --k 3 --lr 1e-3 --n_clusters 3 --n_z 10
```

Note: the README lists ['usps', 'hhar', 'reut', 'acm', 'dblp', 'cite'] for --name; the claim's is 'acm'

### Knobs

| knob | default | declared at |
|---|---|---|
| k | `3` | sdcn.py:170 |
| lr | `1e-3` | sdcn.py:171 |
| n_clusters | `3` | sdcn.py:172 |
| n_z | `10` | sdcn.py:173 |

### Fixed (not knobs)

- `name`: one of the README's alternatives: the claim's
- `pretrain_path`: how to run (paths, devices, logging), not the method

## Environment

Image `python:3.7-slim`; checkpoint `e0f609c0-1071-4bd7-8382-342a0fc1c689`; recipe:

```
apt-get update && apt-get install -y --no-install-recommends gcc libhdf5-dev libopenblas-dev liblapack-dev && pip install --no-cache-dir -r requirements.txt
```

## Data kept in the base checkpoint

0 files, 0.0 MB (new since the environment: downloads, preprocessing, dataset loaders' caches). 7 other new files deleted (outputs, logs, model checkpoints).


## Smoke run

4 run(s) in parallel; exit 0 after 798.0 s

- `c_z_acc`: 88.5, 89.42, 88.4, 88.76
- `c_z_nmi`: 63.63, 65.31, 63.55, 64.17
- `c_z_ari`: 69.21, 71.27, 68.99, 69.83
- `c_z_f1`: 88.43, 89.44, 88.31, 88.72
- `c_q_acc`: 86.68, 86.81, 86.45, 86.71
- `c_q_nmi`: 58.34, 58.76, 57.88, 58.76
- `c_q_ari`: 64.62, 64.96, 64.08, 64.8
- `c_q_f1`: 86.57, 86.74, 86.34, 86.61

Seeds vary: yes

## Metric binding

Test before unqualified before validation before train; final before best; on the paper's scale. A tie is a refusal.

| claim | printed label | value | scale | alternatives |
|---|---|---|---|---|
| C_z_acc | `Z acc` | 0.885 | 100 | `P acc`, `Q acc`, `Z acc` |
| C_z_nmi | `Z nmi` | 0.6363 | 100 | `P nmi`, `Q nmi`, `Z nmi` |
| C_z_ari | `Z ari` | 0.6921 | 100 | `P ari`, `Q ari`, `Z ari` |
| C_z_f1 | `Z f1` | 0.8843 | 100 | `P f1`, `Q f1`, `Z f1` |
| C_q_acc | `Q acc` | 0.8668 | 100 | `P acc`, `Q acc`, `Z acc` |
| C_q_nmi | `Q nmi` | 0.5834 | 100 | `P nmi`, `Q nmi`, `Z nmi` |
| C_q_ari | `Q ari` | 0.6462 | 100 | `P ari`, `Q ari`, `Z ari` |
| C_q_f1 | `Q f1` | 0.8657 | 100 | `P f1`, `Q f1`, `Z f1` |

## Paper-year environment (knob `gf_paper_year_env`)

Packages as of 2020-03-01 (Python 3.7.17): none older than installed.

- h5py: installed 2.9.0 is already from then
- munkres: installed 1.0.12 is already from then
- numpy: installed 1.17.2 is already from then
- scikit-learn: installed 0.22.1 is already from then
- scipy: installed 1.3.1 is already from then
- torch: installed 1.3.1 is already from then

## Fit in one Sandboxes operation (3600 s)

as is: about 2394 s fits one operation

## Notes

- C_z_acc bound to the printed label `Z acc` by the runner
- C_z_nmi bound to the printed label `Z nmi` by the runner
- C_z_ari bound to the printed label `Z ari` by the runner
- C_z_f1 bound to the printed label `Z f1` by the runner
- C_q_acc bound to the printed label `Q acc` by the runner
- C_q_nmi bound to the printed label `Q nmi` by the runner
- C_q_ari bound to the printed label `Q ari` by the runner
- C_q_f1 bound to the printed label `Q f1` by the runner

Model spend: $0.0000
