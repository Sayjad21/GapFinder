"""Differential trace (gapfinder/search/difftrace.py): reproduction vs reference, setting by setting."""

from gapfinder.sandbox.spec import Knob
from gapfinder.search.difftrace import diff, hypotheses, report_markdown


def _rec(lr, wd, p, bs, opt="Adam", widths=(16,)):
    return {"config": [{"src": "argparse", "where": None, "values": {"lr": lr, "weight_decay": wd}}],
            "sinks": [{"kind": "optimizer", "cls": opt, "args": {"lr": lr, "weight_decay": wd}, "site": ["train.py", 40]},
                      {"kind": "dropout", "cls": "Dropout", "args": {"p": p}, "site": ["model.py", 9]},
                      {"kind": "batch", "cls": "DataLoader", "args": {"batch_size": bs}, "site": ["data.py", 12]},
                      {"kind": "seed", "cls": "manual_seed", "args": {"seed": 7}, "site": ["train.py", 3]}]
                     + [{"kind": "width", "cls": "Linear", "args": {"out_features": w}, "site": ["model.py", 5]} for w in widths],
            "ranges": {}, "steps": 3}


def test_value_differences_become_hypotheses_on_the_knob_or_the_literal(tmp_path):
    (tmp_path / "model.py").write_text("import torch\n\n\n\n\n\n\n\nd = torch.nn.Dropout(p=0.2)\n", encoding="utf-8")
    ref = [_rec(0.01, 5e-4, 0.5, 64, widths=(16, 7))]
    mine = [_rec(0.05, 5e-4, 0.2, 64, opt="Adam", widths=(32, 7))]
    diffs = diff(ref, mine)
    keys = {d.key: d for d in diffs}
    assert set(keys) == {"optimizer.lr", "dropout.p", "width.out_features"}  # seeds and equal values are skipped
    assert keys["optimizer.lr"].kind == "value" and keys["width.out_features"].kind == "several"
    knobs = {"lr": Knob(layer="config", default="0.05"), "weight_decay": Knob(layer="config", default="5e-4")}
    plan = hypotheses(diffs, mine, knobs, tmp_path)
    by_knob = {a.knob: a for a in plan.assumptions}
    assert by_knob["lr"].candidate_values == ["0.01"] and by_knob["lr"].evidence[0].kind == "measurement"
    assert plan.patch_knobs == {"@ast:model.py:9:p": "0.2"}
    assert by_knob["@ast:model.py:9:p"].candidate_values == ["0.5"]
    assert [d.key for d in plan.untestable] == ["width.out_features"]
    md = report_markdown(diffs, plan)
    assert "`lr` = 0.01" in md and "not tested (several)" in md


def test_a_different_optimizer_is_structural():
    d = diff([_rec(0.01, 0, 0.5, 64, opt="Adam")], [_rec(0.01, 0, 0.5, 64, opt="SGD")])
    assert [(x.key, x.kind, x.reference, x.mine) for x in d] == [("optimizer class", "structural", ["Adam"], ["SGD"])]
