"""MC Dropout harness: repeats of one configuration must see different data splits.

run_cell.sh turns RUN_TAG into a seeded draw of n_splits distinct splits (without replacement). These
tests run the real script against a fake `python` (no Theano, no dataset), so they check the split
bookkeeping only.
"""

import os
import shutil
import subprocess
import uuid
from pathlib import Path

import pytest

from gapfinder.sandbox.backend import _find_bash

CELL = Path(__file__).resolve().parents[2] / "eval" / "external" / "mc-dropout" / "harness" / "run_cell.sh"
try:
    BASH = _find_bash()
except RuntimeError:
    BASH = None
pytestmark = pytest.mark.skipif(BASH is None, reason="needs bash")

N_SPLITS = 3
TOTAL = 20


def run(args, tag=None, cwd=None):
    env = {**os.environ}
    env.pop("RUN_TAG", None)
    if tag is not None:
        env["RUN_TAG"] = tag
    env["PATH"] = f"{Path(BASH).parent}{os.pathsep}{env['PATH']}"  # coreutils next to a Windows Git bash
    if cwd is not None:
        env["PATH"] = f"{cwd}{os.pathsep}{env['PATH']}"
    return subprocess.run([BASH, str(cwd / "run_cell.sh") if cwd else str(CELL), *args], capture_output=True,
                          text=True, env=env, cwd=cwd, timeout=60)


def draw(tag, n=N_SPLITS, total=TOTAL):
    out = run(["print_splits=1", f"n_splits={n}", f"total_splits={total}"], tag=tag)
    assert out.returncode == 0, out.stderr
    return [int(x) for x in out.stdout.split()]


def real_tags(k):
    """Tags like the orchestrator's: 12 hex characters of a uuid."""
    return [uuid.UUID(int=i * 7919 + 12345).hex[-12:] for i in range(k)]


def test_draw_is_in_range_without_duplicates_and_deterministic_per_tag():
    for tag in real_tags(25) + ["not-a-hex-tag", ""]:
        d = draw(tag)
        assert len(d) == N_SPLITS and len(set(d)) == N_SPLITS
        assert all(0 <= x < TOTAL for x in d)
        assert draw(tag) == d  # same tag, same draw


def test_different_tags_give_different_sets_with_high_probability():
    sets = [frozenset(draw(t)) for t in real_tags(30)]
    assert len(set(sets)) >= 27  # 1140 possible sets of 3 from 20; a few coincidences at most
    used = {x for s in sets for x in s}
    assert len(used) >= 18  # every split gets used, not just a block of them
    # overlap between repeats is allowed (and expected), identical draws are rare
    assert any(a & b for a in sets for b in sets if a != b)


def test_draw_covers_all_splits_when_asked_for_all_and_caps_at_the_total():
    assert sorted(draw("00ff00ff00ff", n=20)) == list(range(20))
    assert sorted(draw("00ff00ff00ff", n=25)) == list(range(20))


@pytest.fixture
def fake_artifact(tmp_path):
    """A copy of run_cell.sh next to a fake UCI_Datasets/toy with 20 splits, and a stub `python`.

    Split k's index files hold the number k; the stub `python` records which splits it finds as splits
    0..n-1, and writes them as the metrics, so the run shows which splits it used."""
    shutil.copy(CELL, tmp_path / "run_cell.sh")
    fresh_data(tmp_path)
    stub = tmp_path / "python"
    stub.write_text(
        "#!/usr/bin/env bash\n"
        "d=UCI_Datasets/toy; mkdir -p $d/results; sfx=500_xepochs_2_hidden_layers.txt\n"
        "n=$(cat $d/data/n_splits.txt)\n"
        "for f in test_MC_rmse test_rmse test_ll test_tau; do : > $d/results/${f}_$sfx; done\n"
        "for i in $(seq 0 $((n - 1))); do for f in test_MC_rmse test_rmse test_ll test_tau; do\n"
        "  cat $d/data/index_train_$i.txt >> $d/results/${f}_$sfx; done\n"
        "  cat $d/data/index_test_$i.txt >> out/seen_test.txt; cat $d/data/index_train_$i.txt >> out/seen_train.txt; done\n",
        newline="\n")
    stub.chmod(0o755)
    return tmp_path


def fresh_data(art):
    """A fresh checkpoint: the orchestrator forks one per run."""
    data = art / "UCI_Datasets" / "toy" / "data"
    data.mkdir(parents=True, exist_ok=True)
    for k in range(TOTAL):
        for kind in ("train", "test"):
            (data / f"index_{kind}_{k}.txt").write_text(f"{k}\n")
    (data / "n_splits.txt").write_text("20\n")
    shutil.rmtree(art / "out", ignore_errors=True)


def kv(out):
    return dict(line.split("=", 1) for line in out.stdout.splitlines() if "=" in line)


def used_splits(art, tag, extra=()):
    fresh_data(art)
    out = run(["dir=toy", "n_splits=3", *extra], tag=tag, cwd=art)
    assert out.returncode == 0, out.stderr
    reported = [int(x) for x in kv(out)["splits_used"].split(",")]
    seen_train = [int(x) for x in (art / "out" / "seen_train.txt").read_text().split()]
    seen_test = [int(x) for x in (art / "out" / "seen_test.txt").read_text().split()]
    assert seen_train == seen_test == reported  # the data files really were swapped in, train and test alike
    return reported


def test_run_uses_the_tags_draw(fake_artifact):
    tag = real_tags(5)[3]
    assert used_splits(fake_artifact, tag) == draw(tag)


def test_repeats_with_different_tags_get_different_splits(fake_artifact):
    sets = {frozenset(used_splits(fake_artifact, t)) for t in real_tags(8)}
    assert len(sets) >= 6


def test_no_tag_keeps_the_old_behaviour(fake_artifact):
    assert used_splits(fake_artifact, None) == [0, 1, 2]


def test_explicit_split_offset_wins_over_the_tag(fake_artifact):
    assert used_splits(fake_artifact, real_tags(1)[0], extra=["split_offset=9"]) == [9, 10, 11]
