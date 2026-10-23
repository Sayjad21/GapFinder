"""Plans G6 and H3: the code proposer's prompt pieces and its grounding of the model's edits."""

from gapfinder.sandbox import ast_patch
from gapfinder.search.proposer import Edit, code_listing, ground, ratio_lines


def test_a_ratio_near_a_count_the_run_used_is_pointed_out():
    rows = ratio_lines([("C1", "loss", 12.8, 0.4), ("C2", "acc", 0.81, 0.80)], {"num_batches": 32, "epochs": 100})
    assert "paper / code = 32" in rows[0] and "num_batches (32)" in rows[0]
    assert "near" not in rows[1]  # 1.0125: nothing


def _apply(tmp_path, knob):
    rel, line, name = ast_patch.parse(knob)
    return ast_patch.apply_source((tmp_path / rel).read_text(), line, name, "1")


def test_edits_are_grounded_on_the_expression_they_change(tmp_path):
    (tmp_path / "m.py").write_text("def agg(xs):\n    return max(xs) * 1\n", encoding="utf-8")
    kept, refused = ground([Edit(file="m.py", line=2, old="max(xs)", new="sum(xs) / len(xs)"),
                            Edit(file="m.py", line=2, old="min(xs)", new="xs[0]"),
                            Edit(file="m.py", line=2, old="max(xs)", new="0.7"),
                            Edit(file="m.py", line=2, old="max(xs)", new="min(xs)")], tmp_path, [0.7])
    assert len(kept) == 1 and len(refused) == 2  # at most 3 edits are read: the fourth is not
    knob, desc = kept[0]
    assert ast_patch.parse(knob)[:2] == ("m.py", 2) and "sum(xs) / len(xs)" in desc
    out = _apply(tmp_path, knob)
    assert "sum(xs) / len(xs)" in out and "max(xs)" not in out
    assert any("writes a reported number" in r for r in refused) and any("not on that line" in r for r in refused)
    assert ground([Edit(file="nope.py", line=1, old="a", new="b")], tmp_path, []) == ([], ["nope.py: no such file"])


def test_a_statement_and_a_piece_of_a_long_expression_are_grounded(tmp_path):
    """Plan H3: the forms the model wrote on seed 5 (a whole statement; the first line of a multi-line call)."""
    (tmp_path / "d.py").write_text("def load(X_org):\n    X = X_org\n    kl = (0.5 / 4) * sum(1 + x -\n"
                                   "        x * x for x in X)\n    return X, kl\n", encoding="utf-8")
    kept, refused = ground([Edit(file="d.py", line=2, old="X = X_org", new="X = X_org[: len(X_org) // 2]"),
                            Edit(file="d.py", line=3, old="(0.5 / 4)", new="(1.0 / 4)"),
                            Edit(file="d.py", line=3, old="kl = (0.5", new="kl = ((0.5")], tmp_path, [])
    assert len(kept) == 2, refused
    assert "X_org[:len(X_org) // 2]" in _apply(tmp_path, kept[0][0])
    assert "1.0 / 4" in _apply(tmp_path, kept[1][0])
    assert refused and "doesn't parse" in refused[0]


def test_the_listing_keeps_executed_lines_only(tmp_path):
    (tmp_path / "a.py").write_text("x = 1\n# note\ny = 2\nz = 3\n", encoding="utf-8")
    assert code_listing(tmp_path, {"a.py": [1, 4]}, ["a.py"]) == "a.py:1: x = 1\na.py:4: z = 3"
    assert "a.py:3: y = 2" in code_listing(tmp_path, {}, ["a.py"])  # no trace: the file's lines
