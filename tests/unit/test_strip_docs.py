import importlib.util
from pathlib import Path

import pytest

from gapfinder.ingest.repo_map import build_repo_map

_spec = importlib.util.spec_from_file_location("strip_docs", Path(__file__).resolve().parents[2] / "scripts" / "strip_docs.py")
sd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sd)


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    (r / "docs" / "img").mkdir(parents=True)
    (r / "sub").mkdir()
    (r / ".git").mkdir()
    (r / ".git" / "HEAD").write_text("ref: x")
    (r / "README.md").write_text("the README explains the flags")
    (r / "sub" / "readme.txt").write_text("notes")
    (r / "docs" / "guide.md").write_text("guide")
    (r / "docs" / "img" / "a.png").write_bytes(b"x")
    (r / "CHANGELOG.md").write_text("changes")
    (r / "experiment.py").write_text('p.add_argument("--epochx", default=500)\n')
    return r


def test_strips_readmes_and_docs_and_reports(repo, tmp_path):
    out = tmp_path / "out"
    r = sd.strip_docs(repo, out)
    assert sorted(r["removed_files"]) == ["README.md", "sub/readme.txt"]
    assert r["removed_dirs"] == ["docs/"]
    assert r["remaining_prose"] == ["CHANGELOG.md"]  # reported so the person can decide
    assert (out / "experiment.py").exists() and not (out / "docs").exists() and not (out / ".git").exists()
    assert (repo / "README.md").exists()  # the original is untouched
    rm = build_repo_map(out)
    assert rm.readme == "" and rm.find_flag("epochx")[0].default == "500"  # the ledger sees code, not the README


def test_refuses_existing_or_nested_output(repo, tmp_path):
    with pytest.raises(SystemExit):
        sd.strip_docs(repo, repo / "inside")
    (tmp_path / "taken").mkdir()
    with pytest.raises(SystemExit):
        sd.strip_docs(repo, tmp_path / "taken")


def test_cli_prints_what_it_removed(repo, tmp_path, capsys):
    assert sd.main([str(repo), str(tmp_path / "o2")]) == 0
    out = capsys.readouterr().out
    assert "removed docs/" in out and "removed README.md" in out and "CHANGELOG.md" in out
