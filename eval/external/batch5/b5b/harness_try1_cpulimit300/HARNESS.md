# HARNESS.md (written by `gapfinder harness`)

**Status:** stopped at env: the model gave up: The code attempts to move tensors to GPU via .cuda() calls, but the VM has no GPU or NVIDIA driver, causing an AssertionError. Without modifying the repository source, we cannot make it run on CPU.

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

Image `python:3.7-slim`; checkpoint `00681266-da61-4737-954e-86e2c91abd84`; recipe:

```
apt-get update && apt-get install -y --no-install-recommends gcc libhdf5-dev libopenblas-dev liblapack-dev && pip install --no-cache-dir -r requirements.txt
```

## Notes

- C_z_acc bound to the printed label `Z acc` by the runner
- C_z_nmi bound to the printed label `Z nmi` by the runner
- C_z_ari bound to the printed label `Z ari` by the runner
- C_z_f1 bound to the printed label `Z f1` by the runner
- C_q_acc bound to the printed label `Q acc` by the runner
- C_q_nmi bound to the printed label `Q nmi` by the runner
- C_q_ari bound to the printed label `Q ari` by the runner
- C_q_f1 bound to the printed label `Q f1` by the runner

Model spend: $0.0140
