"""Plan F1: the code that computes the printed metric ranks above sites that are merely near a knob.

A new instance of the class the planted curriculum found (an aggregation defect in a function not named like a
metric, ranked below a hundred knob-slice sites): the summary is computed in `report()`, printed as
"final ndcg", in a file that sorts after the model and data code, whose many arithmetic sites read the knobs."""

import textwrap

from gapfinder.search.mutation import find_mutants, metric_words

AAA_MODEL = textwrap.dedent('''\
    def build(args):
        w = args.width * 2
        h = args.depth + 3
        s = w * h / 4
        t = s - args.width
        u = (t + h) * args.depth
        return w, h, s, t, u
    ''')
BBB_DATA = textwrap.dedent('''\
    def load(args):
        n = args.n_items * 10
        m = n / args.batch + 1
        k = m * args.n_items - 2
        return list(range(int(n))), m, k
    ''')
ZZZ_RUN = textwrap.dedent('''\
    import argparse
    import numpy as np
    from aaa_model import build
    from bbb_data import load

    def report(scores):
        per_query = [s * 1.0 for s in scores]
        return np.mean(per_query)

    def main():
        p = argparse.ArgumentParser()
        for name in ("width", "depth", "n_items", "batch"):
            p.add_argument("--" + name, type=int, default=4)
        args = p.parse_args()
        w, h, s, t, u = build(args)
        items, m, k = load(args)
        scores = [(i % 5) / 5.0 for i in items]
        final = report(scores)
        train_loss = np.mean([abs(s - 0.5) for s in scores])
        print("final ndcg: %.4f" % final)
        print("train loss: %.4f" % train_loss)
        print("epoch time", w + h)

    main()
    ''')


def _repo(tmp_path):
    for name, src in (("aaa_model.py", AAA_MODEL), ("bbb_data.py", BBB_DATA), ("zzz_run.py", ZZZ_RUN)):
        (tmp_path / name).write_text(src, encoding="utf-8")
    return tmp_path


def test_the_reduction_behind_the_printed_metric_ranks_first(tmp_path):
    root = _repo(tmp_path)
    knobs = ["width", "depth", "n_items", "batch"]
    ms = find_mutants(root, knobs, limit=10 ** 6, files=sorted(root.glob("*.py")), metrics=["c1_ndcg"])
    order = [m.describe() for m in ms]
    def at(ms_, text):
        return next((i for i, m in enumerate(ms_) if text in m.before and m.op.startswith("red.")), None)
    ndcg, loss = at(ms, "mean(per_query)"), at(ms, "abs(s - 0.5)")
    assert ndcg is not None and ndcg < 3, order[:6]  # the reduction behind the claim's metric, among 100 knob sites
    assert loss is None or loss > ndcg + 10, (loss, order[:12])  # another printed number gets no bonus
    assert "metric output" in ms[ndcg].tags
    as_loss = find_mutants(root, knobs, limit=10 ** 6, files=sorted(root.glob("*.py")), metrics=["c1_loss"])
    assert at(as_loss, "abs(s - 0.5)") is not None and at(as_loss, "abs(s - 0.5)") < 3  # the claim's metric decides


def test_metric_words_come_from_the_claims_names():
    assert metric_words(["book_auc", "c18_acc"]).search("test auc: 0.71")
    assert not metric_words(["book_auc"]).search("epoch time 3.2")
    assert metric_words([]).search("mse 0.31")  # no claim names: every common metric word


def test_a_reduction_inside_the_print_is_a_mutant_that_applies(tmp_path):
    """The printed expression itself (`print("test auc", np.mean(aucs))`) is part of the output slice, and the hook
    applies the edit there."""
    from gapfinder.sandbox.ast_patch import apply_source

    src = "import numpy as np\naucs = [0.7, 0.8]\nprint('test auc: %.4f' % np.mean(aucs))\n"
    (tmp_path / "run.py").write_text(src, encoding="utf-8")
    ms = find_mutants(tmp_path, [], limit=50, files=[tmp_path / "run.py"], metrics=["c1_auc"])
    m = next(m for m in ms if m.op == "red.sum")
    assert m.line == 3 and "metric output" in m.tags
    out = apply_source(src, m.line, f"@mut.{m.col}.{m.kind}.{m.op}", "1").splitlines()[2]
    assert "np.sum(aucs)" in out
