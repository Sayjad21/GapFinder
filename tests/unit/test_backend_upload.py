from gapfinder.sandbox.backend import _empty_dirs, _folder_files


def test_empty_directories_are_listed_for_creation(tmp_path):
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "x.txt").write_text("1")
    (tmp_path / "results").mkdir()  # empty: an upload of files alone would drop it
    (tmp_path / "a" / "b").mkdir(parents=True)
    (tmp_path / ".git" / "objects").mkdir(parents=True)
    assert set(_folder_files(tmp_path)) == {"data/x.txt"}
    assert _empty_dirs(tmp_path) == ["a", "a/b", "results"]
