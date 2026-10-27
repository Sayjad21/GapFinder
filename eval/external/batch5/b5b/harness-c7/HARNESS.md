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

Image `(given)`; checkpoint `8ba556c0-fb7a-4264-8ca1-b371cead9a67`; recipe:

```
(none needed)
```

## Data kept in the base checkpoint

0 files, 0.0 MB (new since the environment: downloads, preprocessing, dataset loaders' caches). 7 other new files deleted (outputs, logs, model checkpoints).


## Smoke run

4 run(s) in parallel; exit 0 after 802.0 s; peak memory 898 MB a run, 3 at a time in the cell

- `c_z_acc`: 87.8, 86.81, 89.32, 89.29
- `c_z_nmi`: 61.62, 60.05, 64.6, 64.71
- `c_z_ari`: 67.34, 65.11, 70.96, 70.94
- `c_z_f1`: 87.69, 86.63, 89.33, 89.26
- `c_q_acc`: 86.55, 86.48, 86.84, 86.58
- `c_q_nmi`: 58.29, 58.18, 58.68, 58.22
- `c_q_ari`: 64.38, 64.22, 65.01, 64.37
- `c_q_f1`: 86.42, 86.35, 86.76, 86.45

Seeds vary: yes

## Metric binding

Test before unqualified before validation before train; final before best; on the paper's scale. A tie is a refusal.

| claim | printed label | value | scale | alternatives |
|---|---|---|---|---|
| C_z_acc | `Z acc` | 0.878 | 100 | `P acc`, `Q acc`, `Z acc` |
| C_z_nmi | `Z nmi` | 0.6162 | 100 | `P nmi`, `Q nmi`, `Z nmi` |
| C_z_ari | `Z ari` | 0.6734 | 100 | `P ari`, `Q ari`, `Z ari` |
| C_z_f1 | `Z f1` | 0.8769 | 100 | `P f1`, `Q f1`, `Z f1` |
| C_q_acc | `Q acc` | 0.8655 | 100 | `P acc`, `Q acc`, `Z acc` |
| C_q_nmi | `Q nmi` | 0.5829 | 100 | `P nmi`, `Q nmi`, `Z nmi` |
| C_q_ari | `Q ari` | 0.6438 | 100 | `P ari`, `Q ari`, `Z ari` |
| C_q_f1 | `Q f1` | 0.8642 | 100 | `P f1`, `Q f1`, `Z f1` |

## Paper-year environment (knob `gf_paper_year_env`)

Packages as of 2020-03-01 (Python 3.7.17), each in its own directory under `/opt/gf_py`: none older than installed.

- h5py: installed 2.9.0 is already from then
- munkres: installed 1.0.12 is already from then
- numpy: installed 1.17.2 is already from then
- scikit-learn: installed 0.22.1 is already from then
- scipy: installed 1.3.1 is already from then
- torch: installed 1.3.1 is already from then

## Paper-era code (knob `gf_paper_era_code`)

The repository's last commit before the paper's date: `0e0af8e10e86` (2020-02-22: Add files via upload); 7 code files in `/opt/gf_paper_era`, copied over the checkout when the knob is 1. 8 commits from it to the given one (history before the given commit only) for the binary search.

## Fit in one Sandboxes operation (3600 s)

shards: 10 independent jobs of about 802 s

## Notes

- C_z_acc bound to the printed label `Z acc` by the runner
- C_z_nmi bound to the printed label `Z nmi` by the runner
- C_z_ari bound to the printed label `Z ari` by the runner
- C_z_f1 bound to the printed label `Z f1` by the runner
- C_q_acc bound to the printed label `Q acc` by the runner
- C_q_nmi bound to the printed label `Q nmi` by the runner
- C_q_ari bound to the printed label `Q ari` by the runner
- C_q_f1 bound to the printed label `Q f1` by the runner
- one run peaks at 898 MB: 3 fit the VM's 3900 MB at once (not 4), so the cell runs its repeats 3 at a time

Model spend: $0.0000
