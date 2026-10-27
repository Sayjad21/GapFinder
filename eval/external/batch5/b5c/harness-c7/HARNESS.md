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
cd benchmark && PYTHONPATH="$OLDPWD${PYTHONPATH:+${GF_PATHSEP:-:}$PYTHONPATH}" "${PYTHON:-python}" main.py --model dominant --dataset inj_cora --gpu -1
```

### Knobs

| knob | default | declared at |
|---|---|---|

### Fixed (not knobs)

- `model`: its value 'dominant' is one of the claim's conditions: defines the claim
- `dataset`: dataset: defines the claim
- `gpu`: how to run (paths, devices, logging), not the method

## Environment

Image `(given)`; checkpoint `c6dd9389-eb85-4995-abc1-c3fb1d08e44a`; recipe:

```
(none needed)
```

## Data kept in the base checkpoint

0 files, 0.0 MB (new since the environment: downloads, preprocessing, dataset loaders' caches). 41 other new files deleted (outputs, logs, model checkpoints).


## Smoke run

1 run(s) in parallel; exit 0 after 1068.0 s; peak memory 708 MB a run, 1 at a time in the cell

- `c_auc`: 76.52
- `c_ap`: 17.93
- `c_rec_recall`: 27.17

Seeds vary: unknown (one copy)

## Metric binding

Test before unqualified before validation before train; final before best; on the paper's scale. A tie is a refusal.

| claim | printed label | value | scale | alternatives |
|---|---|---|---|---|
| C_auc | `inj_cora DOMINANT AUC` | 0.7652 | 100 |  |
| C_ap | `AP` | 0.1793 | 100 |  |
| C_rec | `Recall` | 0.2717 | 100 |  |

## Paper-year environment (knob `gf_paper_year_env`)

Packages as of 2022-07-01 (Python 3.8.20), each in its own directory under `/opt/gf_py`: `pygod==0.3.0` (the repository's own package), `pyod==1.0.2`, `scikit-learn==1.1.1`, `torch-geometric==2.0.4`, `tqdm==4.64.0`. Used: yes.

Values: `0` (as installed), `all`, one directory, a comma list, or `dist==version` (installed on demand by the run). The runtime shim imports those packages from there whatever sys.path says.

- torch: not installed (part of another package, or not needed)

## Paper-era code (knob `gf_paper_era_code`)

The repository's last commit before the paper's date: `7de5d925ef59` (2022-06-25: Merge pull request #36 from pygod-team/dev); 59 code files in `/opt/gf_paper_era`, copied over the checkout when the knob is 1. 109 commits from it to the given one (history before the given commit only) for the binary search.

## Fit in one Sandboxes operation (3600 s)

as is: about 1068 s fits one operation

## Notes

- command given by the runner: `cd benchmark && python main.py --model dominant --dataset inj_cora --gpu -1`
- the script exposes 0 flag(s): 12 named literal(s) it runs became patch knobs (in memory, no file edited): weight_decay, batch_size, epoch, batch_size, epoch, hid_dim, num_layers, dropout, weight_decay, lr, epoch, batch_size

Model spend: $0.0000
