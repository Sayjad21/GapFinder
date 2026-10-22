"""Plan G6: the code proposer's prompt pieces and its grounding of the model's edits."""

from gapfinder.sandbox import ast_patch
from gapfinder.search.proposer import Edit, code_listing, ground, ratio_lines


def test_a_ratio_near_a_count_the_run_used_is_pointed_out():
    rows = ratio_lines([("C1", "loss", 12.8, 0.4), ("C2", "acc", 0.81, 0.80)], {"num_batches": 32, "epochs": 100})
    assert "paper / code = 32" in rows[0] and "num_batches (32)" in rows[0]
    assert "near" not in rows[1]  # 1.0125: nothing


def test_edits_are_grounded_on_an_expression_of_that_line(tmp_path):
    (tmp_path / "m.py").write_text("def agg(xs):\n    return max(xs) * 1\n", encoding="utf-8")
    kept, refused = ground([Edit(file="m.py", line=2, old="max(xs)", new="sum(xs) / len(xs)"),
                            Edit(file="m.py", line=2, old="min(xs)", new="xs[0]"),
                            Edit(file="m.py", line=2, old="max(xs)", new="0.7"),
                            Edit(file="m.py", line=2, old="max(xs)", new="min(xs)")], tmp_path, [0.7])
    assert len(kept) == 1 and len(refused) == 2  # at most 3 edits are read: the fourth is not
    knob, desc = kept[0]
    rel, line, name = ast_patch.parse(knob)
    assert (rel, line) == ("m.py", 2) and "sum(xs) / len(xs)" in desc
    out = ast_patch.apply_source((tmp_path / "m.py").read_text(), line, name, "1")
    assert "sum(xs) / len(xs)" in out and "max(xs)" not in out
    assert any("writes a reported number" in r for r in refused) and any("not an expression" in r for r in refused)
    assert ground([Edit(file="nope.py", line=1, old="a", new="b")], tmp_path, []) == ([], ["nope.py: no such file"])


def test_the_listing_keeps_executed_lines_only(tmp_path):
    (tmp_path / "a.py").write_text("x = 1\n# note\ny = 2\nz = 3\n", encoding="utf-8")
    assert code_listing(tmp_path, {"a.py": [1, 4]}, ["a.py"]) == "a.py:1: x = 1\na.py:4: z = 3"
    assert "a.py:3: y = 2" in code_listing(tmp_path, {}, ["a.py"])  # no trace: the file's lines
