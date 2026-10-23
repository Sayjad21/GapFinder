"""Plans G5 and H2: the mutation round's first mutants. The first `head` stay in priority order (the early code
screen's); after them the operator classes take turns, so no class's best are cut by another class's many sites."""

from gapfinder.search.mutation import Mutant, _stratified


def _m(i, tags):
    return Mutant(file="a.py", line=i, col=0, kind="num", op="mul2", dist=0, knob=None, before="1", after="2",
                  priority=100 - i, tags=tags)


def test_the_head_keeps_priority_order_and_the_rest_take_turns():
    ranked = [_m(i, ["metric output"]) for i in range(10)] + [_m(10 + i, ["data pipeline"]) for i in range(5)]
    out = _stratified(ranked, 8, head=6)
    assert out[:6] == ranked[:6]  # the plain order: nothing displaced from the early screen
    assert [m.line for m in out[6:]] == [6, 10]  # then the classes in turn: metric, data


def test_without_a_head_the_data_class_gets_an_early_slot():
    ranked = [_m(i, ["metric output"]) for i in range(10)] + [_m(10 + i, ["data pipeline"]) for i in range(5)]
    assert [m.line for m in _stratified(ranked, 4, head=0)] == [0, 10, 1, 11]
