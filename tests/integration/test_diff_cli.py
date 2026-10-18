"""`gapfinder diff` end to end on the local backend: two programs that differ in a flag default and in a
literal at a dropout call; the reference's numbers are the target, and both differences are found."""

import os
import textwrap

from tests.unit.test_trace import FAKE_TORCH

TRAIN = textwrap.dedent("""\
    import argparse, hashlib, os
    import torch
    p = argparse.ArgumentParser()
    p.add_argument("--lr", type=float, default={lr})
    a = p.parse_args()
    opt = torch.optim.Adam([], lr=a.lr)
    opt.zero_grad()
    d = torch.nn.Dropout(p={p})
    noise = int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 1000 / 5e4
    print("score=%.4f" % (90 - abs(a.lr - 0.01) * 200 - abs(d.p - 0.5) * 40 + noise))
    """)

SPEC = textwrap.dedent("""\
    name: {name}
    base: "local:{base}"
    run:
      command: '"${{PYTHON:-python3}}" train.py --lr {{lr}}'
      output: stdout
      format: kv
      timeout: 120
    knobs:
      lr: {{layer: config, default: "{lr}"}}
    allowed_paths: ["out/"]
    metrics: [score]
    """)


def _artifact(root, name, lr, p):
    d = root / name
    for rel, src in FAKE_TORCH.items():
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        (d / rel).write_text(src, encoding="utf-8")
    (d / "train.py").write_text(TRAIN.format(lr=lr, p=p), encoding="utf-8")
    spec = root / f"{name}.yaml"
    spec.write_text(SPEC.format(name=name, base=d.as_posix(), lr=lr), encoding="utf-8")
    return spec


def test_diff_finds_and_confirms_both_differences(tmp_path, monkeypatch, capsys):
    from gapfinder import config
    from gapfinder.cli import main

    monkeypatch.setenv("GF_LOCAL_SANDBOX_DIR", str(tmp_path / "sbx"))
    monkeypatch.setenv("GF_SANDBOX_GUARD_USD", "1000000")
    config.settings.cache_clear() if hasattr(config.settings, "cache_clear") else None
    ref = _artifact(tmp_path, "ref", "0.01", "0.5")
    mine = _artifact(tmp_path, "mine", "0.05", "0.2")
    out = tmp_path / "diff"
    rc = main(["diff", "--spec", str(mine), "--ref-spec", str(ref), "--backend", "local", "--max-runs", "60",
               "--concurrency", "4", "--out", str(out)])
    text = capsys.readouterr().out
    assert rc == 0, text
    assert "optimizer.lr: reference 0.01; yours 0.05" in text and "dropout.p: reference 0.5; yours 0.2" in text
    md = (out / "differences.md").read_text(encoding="utf-8")
    assert "`lr` = 0.01" in md and "`@ast:train.py:8:p` = 0.5" in md
    assert "R_score:" in text and "'lr': '0.01'" in text and "'@ast:train.py:8:p': '0.5'" in text
