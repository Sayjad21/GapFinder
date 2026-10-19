"""Cells longer than one Sandboxes operation (3600 s at most): shards run in parallel VMs and their outputs are
joined; segments run in sequence, each from the previous one's checkpoint (training that resumes from disk)."""

import textwrap

from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec

JOB = textwrap.dedent('''\
    import os, sys
    shard, seg = sys.argv[1], int(sys.argv[2])
    # "training" that resumes: each segment adds its epochs to what the previous one saved
    done = int(open("state.txt").read()) if os.path.exists("state.txt") else 0
    done += 10
    open("state.txt", "w").write(str(done))
    if seg == 2:
        print("%s_epochs_trained=%d" % (shard, done))
        print("%s_score=%.1f" % (shard, {"cora": 81.0, "citeseer": 70.5}[shard] + done / 100))
    ''')

SPEC = """name: pieces
base: "local:{base}"
run:
  command: '"${{PYTHON:-python3}}" job.py {{shard}} {{segment}}'
  output: stdout
  format: kv
  timeout: 60
{extra}knobs:
  lr: {{layer: config, default: "0.01"}}
allowed_paths: ["out/"]
"""


def _spec(tmp_path, extra: str):
    art = tmp_path / "art"
    art.mkdir()
    (art / "job.py").write_text(JOB, encoding="utf-8")
    p = tmp_path / "spec.yaml"
    p.write_text(SPEC.format(base=art.as_posix(), extra=extra), encoding="utf-8")
    return HarnessSpec.load_yaml(p)


async def test_shards_run_in_parallel_and_segments_continue_from_the_previous_checkpoint(tmp_path):
    spec = _spec(tmp_path, '  shards: ["cora", "citeseer"]\n  segments: 2\n')
    assert spec.run.shards == ["cora", "citeseer"] and spec.run.segments == 2
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    b = await orch.run_branch({})
    assert b.status == "succeeded", b.note
    # both shards' metrics in one branch; each shard's second segment saw the first segment's saved state
    assert b.parsed_metrics == {"cora_epochs_trained": 20.0, "cora_score": 81.2,
                                "citeseer_epochs_trained": 20.0, "citeseer_score": 70.7}


async def test_a_failed_piece_fails_the_cell(tmp_path):
    spec = _spec(tmp_path, '  shards: ["cora", "pubmed"]\n  segments: 2\n')  # pubmed: KeyError in the job
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    b = await orch.run_branch({})
    assert b.status == "failed" and "KeyError" in (b.note or ""), b.note


def test_a_spec_without_pieces_is_unchanged(tmp_path):
    spec = _spec(tmp_path, "")
    assert spec.run.shards == [] and spec.run.segments == 1
