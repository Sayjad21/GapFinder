"""MC Dropout harness, sharded execution (procs=<N|auto>, FROZEN.md Deviation 3).

One experiment.py process per (dataset, split), each in its own copy of the dataset and net folders,
then one aggregation. The real run_cell.sh runs against a stub `python` (no Theano, no dataset): for
every split it is given, the stub writes metrics that depend on the split's index file, and it can log
which split it saw and how many stubs ran at once.
"""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

from gapfinder.sandbox.backend import _find_bash

CELL = Path(__file__).resolve().parents[2] / "eval" / "external" / "mc-dropout" / "harness" / "run_cell.sh"
try:
    BASH = _find_bash()
except RuntimeError:
    BASH = None
pytestmark = pytest.mark.skipif(BASH is None, reason="needs bash")

TOTAL = 20
TAG = "abc123def456"

STUB = r"""#!/usr/bin/env bash
# fake `python experiment.py --dir <d> --epochx <e> --hidden <h>`: $3=d $5=e $7=h
d=$3; res=UCI_Datasets/$d/results; mkdir -p $res; sfx=$5_xepochs_$7_hidden_layers.txt
n=$(cat UCI_Datasets/$d/data/n_splits.txt)
first=$(cat UCI_Datasets/$d/data/index_train_0.txt)
[ -f "UCI_Datasets/$d/data/fail_$first.txt" ] && { echo boom >&2; exit 3; }
if [ -n "${CONC_DIR:-}" ]; then
  touch "$CONC_DIR/run_$$"; ls "$CONC_DIR" | grep -c '^run_' >> "$CONC_DIR/count.log"; sleep 0.4
fi
for f in test_MC_rmse test_rmse test_ll test_tau; do : > $res/${f}_$sfx; done
for i in $(seq 0 $((n - 1))); do
  k=$(cat UCI_Datasets/$d/data/index_train_$i.txt)
  echo "$k.5" >> $res/test_MC_rmse_$sfx; echo "$k.25" >> $res/test_rmse_$sfx
  echo "-$k" >> $res/test_ll_$sfx; echo "0.5" >> $res/test_tau_$sfx
  echo "$d $k $(basename "$PWD")" >> "${SEEN_LOG:-/dev/null}"
done
[ -n "${CONC_DIR:-}" ] && rm -f "$CONC_DIR/run_$$"
exit 0
"""


def make_artifact(root):
    root.mkdir(parents=True)
    shutil.copy(CELL, root / "run_cell.sh")
    for name, rows in (("small", 5), ("big", 9)):
        data = root / "UCI_Datasets" / name / "data"
        data.mkdir(parents=True)
        (data / "data.txt").write_text("1 2\n" * rows)
        for k in range(TOTAL):
            for kind in ("train", "test"):
                (data / f"index_{kind}_{k}.txt").write_text(f"{k}\n")
        (data / "n_splits.txt").write_text("20\n")
    (root / "experiment.py").write_text("# fake\n")
    (root / "net").mkdir()
    (root / "net" / "net.py").write_text("# fake\n")
    stub = root / "python"
    stub.write_text(STUB, newline="\n")
    stub.chmod(0o755)
    return root


@pytest.fixture
def art(tmp_path):
    return make_artifact(tmp_path / "a")


def run(art, args, tag=TAG, env_extra=None):
    env = {**os.environ, **(env_extra or {})}
    env.pop("RUN_TAG", None)
    if tag:
        env["RUN_TAG"] = tag
    env["PATH"] = f"{art}{os.pathsep}{Path(BASH).parent}{os.pathsep}{env['PATH']}"
    return subprocess.run([BASH, str(art / "run_cell.sh"), *args], capture_output=True, text=True, env=env,
                          cwd=art, timeout=120)


def kv(out):
    return dict(line.split("=", 1) for line in out.stdout.splitlines() if "=" in line)


def draw(n):
    env = {**os.environ, "RUN_TAG": TAG}
    env["PATH"] = f"{Path(BASH).parent}{os.pathsep}{env['PATH']}"
    out = subprocess.run([BASH, str(CELL), "print_splits=1", f"n_splits={n}", "total_splits=20"],
                         capture_output=True, text=True, env=env, timeout=60)
    return [int(x) for x in out.stdout.split()]


def test_sharded_run_prints_what_the_unsharded_aggregation_prints(art, tmp_path):
    args = ["dir=big,small", "epochx=500", "hidden=2", "n_splits=4"]
    plain = kv(run(art, args))
    other = make_artifact(tmp_path / "b")
    out = run(other, [*args, "procs=3"])
    assert out.returncode == 0, out.stderr
    sharded = kv(out)
    for d in ("big", "small"):
        for key in ("rmse", "rmse_sd", "rmse_single", "rmse_single_sd", "ll", "ll_sd", "mean_tau", "splits_done",
                    "splits_used"):
            assert sharded[f"{d}_{key}"] == plain[f"{d}_{key}"], (d, key)
        assert sharded[f"{d}_shards"] == "4" and sharded[f"{d}_splits_done"] == "4"
        assert f"{d}_wall_s" in sharded
    assert plain["big_splits_used"] == ",".join(map(str, draw(4)))
    assert sharded["procs"] == "3" and "shards_wall_s" in sharded


def test_each_shard_sees_exactly_one_split_in_its_own_folder(art, tmp_path):
    seen = tmp_path / "seen.log"
    out = run(art, ["dir=big", "n_splits=3", "procs=2"], env_extra={"SEEN_LOG": str(seen)})
    assert out.returncode == 0, out.stderr
    rows = [line.split() for line in seen.read_text().splitlines()]
    want = draw(3)
    assert sorted(int(r[1]) for r in rows) == sorted(want)  # each split once
    assert sorted(r[2] for r in rows) == [f"big_{i}" for i in range(3)]  # one folder per shard
    got = kv(out)
    assert got["splits_used"] == ",".join(map(str, want))  # draw order, not finishing order
    assert float(got["rmse"]) == pytest.approx(sum(want) / 3 + 0.5, abs=1e-5)
    assert got["shards"] == "3"


def test_sharded_run_never_exceeds_procs_and_does_use_them(art, tmp_path):
    conc = tmp_path / "conc"
    conc.mkdir()
    out = run(art, ["dir=big,small", "n_splits=4", "procs=2"], env_extra={"CONC_DIR": str(conc)})
    assert out.returncode == 0, out.stderr
    counts = [int(x) for x in (conc / "count.log").read_text().split()]
    assert len(counts) == 8 and max(counts) == 2
    # auto means the machine's cores even though the spec caps every BLAS library at one thread
    # through OMP_NUM_THREADS (which plain `nproc` would obey, giving 1)
    env = {k: v for k, v in os.environ.items() if k not in ("OMP_NUM_THREADS", "OMP_THREAD_LIMIT")}
    env["PATH"] = f"{Path(BASH).parent}{os.pathsep}{env['PATH']}"
    cores = int(subprocess.run(["nproc"], capture_output=True, text=True, env=env).stdout)
    out = run(art, ["dir=big,small", "n_splits=4", "procs=auto"], env_extra={"OMP_NUM_THREADS": "1"})
    assert out.returncode == 0 and int(kv(out)["procs"]) == cores


def test_the_bigger_dataset_goes_first_and_output_keeps_dir_order(art, tmp_path):
    seen = tmp_path / "seen.log"
    out = run(art, ["dir=small,big", "n_splits=2", "procs=1"], env_extra={"SEEN_LOG": str(seen)})
    assert out.returncode == 0, out.stderr
    assert [line.split()[0] for line in seen.read_text().splitlines()] == ["big", "big", "small", "small"]
    assert [k for k in kv(out) if k.endswith("_rmse")] == ["small_rmse", "big_rmse"]


def test_a_failed_shard_fails_the_cell_and_drops_that_datasets_metrics(art):
    # the stub fails for a shard whose split index is 7, in dataset "big" only
    (art / "UCI_Datasets" / "big" / "data" / "fail_7.txt").write_text("")
    out = run(art, ["dir=big,small", "n_splits=3", "split_offset=6", "procs=2"], tag="")
    assert out.returncode != 0
    got = kv(out)
    assert "boom" in out.stderr and "shard 1 of big exited with status 3" in out.stderr
    assert not any(key.startswith("big_") for key in got)
    assert got["small_splits_used"] == "6,7,8" and got["small_splits_done"] == "3"


def test_procs_must_be_a_positive_integer_or_auto_and_the_dataset_must_exist(art):
    for bad in ("0", "x", "-1"):
        out = run(art, ["dir=big", "n_splits=2", f"procs={bad}"])
        assert out.returncode == 2 and "procs must be" in out.stderr, bad
    assert run(art, ["dir=nope", "n_splits=2", "procs=2"]).returncode == 2


def test_default_procs_keeps_the_unsharded_path(art):
    out = run(art, ["dir=big", "n_splits=2", "procs=default"])
    assert out.returncode == 0, out.stderr
    got = kv(out)
    assert "procs" not in got and "shards" not in got
    assert not (art / "out" / "shards").exists()


# ----------------------------------------------------------------- the spec and the launcher
ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "eval" / "external" / "mc-dropout"


def test_sandbox_spec_differs_from_the_frozen_one_only_in_base_env_procs_and_timeout(monkeypatch):
    from gapfinder.sandbox.spec import HarnessSpec

    monkeypatch.setenv("GF_MCD_SANDBOX_BASE", "76b71887-d3e7-48ff-96d5-f16cefcf6779")
    frozen = HarnessSpec.load_yaml(CASE / "mcd.yaml")
    sbx = HarnessSpec.load_yaml(CASE / "mcd_sandbox.yaml")
    assert sbx.knobs == frozen.knobs  # same knobs, defaults, candidates and caps
    assert (sbx.build, sbx.load, sbx.allowed_paths, sbx.metrics) == (frozen.build, frozen.load,
                                                                      frozen.allowed_paths, frozen.metrics)
    assert (sbx.run.output, sbx.run.format) == (frozen.run.output, frozen.run.format)
    assert sbx.run.timeout == 3600  # the Sandboxes API maximum
    cmd = sbx.run.command.split("; ", 1)[1]  # drop the environment export (Deviation 2)
    assert cmd == frozen.run.command + " procs=auto"
    rendered, _ = sbx.render(sbx.run, {})
    assert "bash run_cell.sh dir=energy,yacht epochx=500 hidden=2 n_splits=3" in rendered
    assert rendered.endswith(" procs=auto") and "{" not in rendered


def test_launcher_defaults_to_two_arms_and_keeps_total_concurrency_within_50():
    def plan(*args, env=None):
        e = {k: v for k, v in os.environ.items() if k != "GF_MAX_CONCURRENCY"}  # .env may export one; the launcher honours it
        e.update({"MCD_ARMS_DRY_RUN": "1", **(env or {})})
        e["PATH"] = f"{Path(BASH).parent}{os.pathsep}{e['PATH']}"
        return subprocess.run([BASH, str(ROOT / "scripts" / "run_mcd_sandbox_arms.sh"), *args], capture_output=True,
                              text=True, env=e, timeout=60)

    out = plan()
    assert out.returncode == 0, out.stderr
    lines = out.stdout.splitlines()
    assert "GF_MAX_CONCURRENCY=24 each" in lines[0] and "no-README all-flags-random" in lines[0]
    assert len(lines) == 3
    assert "run-no-README" in lines[1] and "--no-evidence-gate" in lines[1] and "mcd-ledger-nodocs" in lines[1]
    assert "run-all-flags-random" in lines[2] and "--hypotheses repomap --rank random --seed 0" in lines[2]
    assert all("mcd_sandbox.yaml" in line and "--backend contree" in line for line in lines[1:])
    four = plan("all")
    assert "GF_MAX_CONCURRENCY=12 each" in four.stdout.splitlines()[0] and len(four.stdout.splitlines()) == 5
    one = plan("normal")
    assert "--assumptions runs/mcd-ledger/assumptions.json" in one.stdout and "GF_MAX_CONCURRENCY=48" in one.stdout
    over = plan("normal", "evidence-off", env={"GF_MAX_CONCURRENCY": "30"})
    assert over.returncode == 2 and "over the Beta limit of 50" in over.stderr
    assert plan("nonsense").returncode == 2 and plan("normal", "normal").returncode == 2
