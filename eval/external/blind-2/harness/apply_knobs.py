"""blind-2 harness: apply GapFinder's knob values to GraphMAE's configs.yml for one cell (see ../HARNESS.md).

    python gf_harness/apply_knobs.py --datasets COLLAB,IMDB-BINARY -- lr=0.00015 max_epoch=20 ...
    python gf_harness/apply_knobs.py --print-defaults        # the target's effective settings, for the spec

The README's command (scripts/run_graph.sh) passes flags and then --use_cfg, and load_best_configs() then
overwrites every flag the dataset's configs.yml entry names. A knob passed as a flag would be ignored, so
a changed knob is written into configs.yml instead, for every dataset of the cell, and load_best_configs()
applies it as it applies the repo's own entries.

A knob whose value equals the TARGET's (COLLAB's) effective setting is left alone, so every dataset keeps its
own configuration unless the branch changes that knob. The effective setting is what the README command
gives COLLAB: argparse defaults, then run_graph.sh's flags, then configs.yml["COLLAB"], computed with the
repo's own build_args() and load_best_configs(). configs.yml is a configuration file, not algorithm code;
the change is local to the branch's sandbox.
"""
import argparse
import os
import sys

import yaml

TARGET = "COLLAB"
# scripts/run_graph.sh at 1be5941, minus --device/--dataset/--seeds (set per run by the cell)
RUN_GRAPH_FLAGS = ["--mask_rate", "0.5", "--encoder", "gin", "--decoder", "gin", "--in_drop", "0.2",
                   "--attn_drop", "0.1", "--num_layers", "2", "--num_hidden", "512", "--num_heads", "2",
                   "--max_epoch", "100", "--max_epoch_f", "0", "--lr", "0.00015", "--weight_decay", "0.0",
                   "--activation", "prelu", "--optimizer", "adam", "--drop_edge_rate", "0.0", "--loss_fn", "sce",
                   "--linear_prob", "--use_cfg"]
# flags that say how to run, not what is computed (or that would load a model from disk)
OPERATIONAL = {"seeds", "dataset", "device", "use_cfg", "logging", "load_model", "save_model"}


def effective(dataset):
    sys.path.insert(0, os.getcwd())  # the repo root (/work), where graphmae/ lives
    from graphmae.utils import build_args, load_best_configs

    argv = sys.argv
    sys.argv = ["main_graph.py", "--dataset", dataset, "--device", "-1"] + RUN_GRAPH_FLAGS
    try:
        args = load_best_configs(build_args(), "configs.yml")
    finally:
        sys.argv = argv
    return vars(args)


def text(v):
    """One spelling per value: booleans lowercase, None as none, floats as Python prints them."""
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "none"
    return str(v)


def same(a, b):
    a, b = str(a).strip().lower(), str(b).strip().lower()
    if a == b:
        return True
    try:
        return float(a) == float(b)
    except ValueError:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", default=TARGET)
    ap.add_argument("--print-defaults", action="store_true")
    ap.add_argument("pairs", nargs="*")
    a = ap.parse_args()
    eff = effective(TARGET)
    if a.print_defaults:
        for k in sorted(eff):
            if k not in OPERATIONAL and k != "num_features":
                print(f"{k}={text(eff[k])}")
        return
    with open("configs.yml") as f:
        cfg = yaml.load(f, yaml.FullLoader)
    changed = {}
    for pair in a.pairs:
        k, _, v = pair.partition("=")
        if k in OPERATIONAL or k not in eff:
            sys.exit(f"apply_knobs: unknown or operational knob {k!r}")
        if same(v, text(eff[k])):
            continue
        val = yaml.safe_load(v) if v.lower() != "none" else None
        changed[k] = val
    for ds in a.datasets.split(","):
        cfg.setdefault(ds, {}).update(changed)
    with open("configs.yml", "w") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)
    print("gf_knobs_changed=" + (",".join(f"{k}:{v}" for k, v in changed.items()) or "none"), file=sys.stderr)


if __name__ == "__main__":
    main()
