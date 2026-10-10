# MC Dropout feasibility scripts

The two throwaway scripts behind [../FEASIBILITY.md](../FEASIBILITY.md), kept so nobody has to redo
that work. They read keys from `.env` and record every sandbox run in the spend ledger. Run them
with `GF_SPEND_TAG=mcdropout-feasibility`, and only after the money safety checks in TODO.md
section 0.

| Script | What it does | Reported cost when run |
|---|---|---|
| `mcd_probe.py` | Starts `python:3.6-slim` in a sandbox; prints the Python version, CPUs, and whether pip and PyPI are reachable | $0.016 |
| `mcd_build.py <artifact folder>` | Uploads the artifact, installs the 2018 stack (numpy 1.13.3, scipy 1.1.0, Theano 0.8.2, Keras 2.2.0, h5py 2.8.0, g++) and checkpoints it, then times `experiment.py --dir yacht --epochx 1 --hidden 1` on 2 splits | build $0.12; the timing run crashed after $6.58 |

**Before re-running `mcd_build.py`:**
- the timing step is the expensive one: about 650 CPU-seconds per grid setting with the code's
  `T = 10000`;
- either set `GF_SANDBOX_CPU_LIMIT_S` low, or apply the `T = 100` patch from the TODO's
  recommended option;
- the artifact folder is the repo's `experiment.py`, `net/` and the `UCI_Datasets/` folders for
  yacht, energy and concrete, each with an empty `results/` folder (uploads now keep empty
  folders).
