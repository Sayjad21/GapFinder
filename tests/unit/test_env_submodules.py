"""env-build's fetch brings git submodules at their pinned commits (a tarball has none)."""

import io
import json
import urllib.request

from gapfinder.env_build import fetch, submodule_fetch


def test_submodules_are_fetched_at_the_pinned_commit(tmp_path, monkeypatch):
    (tmp_path / ".gitmodules").write_text(
        '[submodule "third_party/lib"]\n\tpath = third_party/lib\n\turl = https://github.com/someone/lib.git\n'
        '[submodule "other"]\n\tpath = other\n\turl = https://gitlab.com/x/y.git\n', encoding="utf-8")
    seen = []

    def fake(req, timeout=0):
        seen.append(req.full_url)
        return io.BytesIO(json.dumps({"type": "submodule", "sha": "abc123"}).encode())

    monkeypatch.setattr(urllib.request, "urlopen", fake)
    steps = submodule_fetch("https://github.com/me/proj", "deadbeef", tmp_path)
    assert seen == ["https://api.github.com/repos/me/proj/contents/third_party/lib?ref=deadbeef"]  # GitHub only
    assert "codeload.github.com/someone/lib/tar.gz/abc123" in steps and "/work/third_party/lib" in steps
    assert "lib-abc123" in fetch("https://github.com/me/proj", "deadbeef", tmp_path)
    assert submodule_fetch("https://github.com/me/proj", "deadbeef", tmp_path / "none") == ""
