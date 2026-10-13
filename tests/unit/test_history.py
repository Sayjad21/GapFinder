from gapfinder.search.history import diagnose

CLAIMS = [("T", "a", 10.0), ("H", "b", 5.0)]


def runs(**cfgs):
    return {tuple(sorted(c.items())): [{"a": a, "b": b} for a, b in vals] for c, vals in cfgs.items()}


def _r(cfg, vals):
    return (tuple(sorted(cfg.items())), [{"a": a, "b": b} for a, b in vals])


def test_conflicting_claims_are_out_of_space_suspected():
    data = dict([_r({}, [(20, 5.0), (20.5, 5.1), (19.5, 4.9)]),     # naive: target off, held-out fine
                 _r({"k": "1"}, [(10, 9.0), (10.2, 9.1), (9.8, 8.9)]),  # fixes the target, breaks the held-out
                 _r({"k": "2"}, [(20, 5.0), (20.1, 5.0)])])           # matches the held-out only
    d = diagnose(data, CLAIMS, "T", disc=0.0)
    assert d.kind == "out_of_space_suspected" and d.per_claim["T"][0]["config"] == {"k": "1"}


def test_a_joint_fit_is_in_space_and_the_naive_one_is_reproduced():
    data = dict([_r({}, [(20, 5.0), (20.5, 5.1), (19.5, 4.9)]), _r({"k": "1"}, [(10, 5.0), (10.1, 5.05)])])
    assert diagnose(data, CLAIMS, "T", disc=0.0).kind == "in_space"
    near = dict([_r({}, [(10, 5.0), (10.5, 5.1), (9.5, 4.9)])])
    assert diagnose(near, CLAIMS, "T", disc=0.0).kind == "reproduced"


def test_nothing_reaching_the_target_is_out_of_space_likely():
    data = dict([_r({}, [(20, 5.0), (20.5, 5.1), (19.5, 4.9)]), _r({"k": "1"}, [(18, 5.0), (18.2, 5.0)])])
    assert diagnose(data, CLAIMS, "T", disc=0.0).kind == "out_of_space_likely"


def test_islands_join_single_knob_neighbours_only():
    from gapfinder.search.history import islands

    cfgs = [{"a": "1"}, {"a": "2"}, {"a": "2", "b": "x"}, {"c": "9", "d": "9"}]
    got = islands(cfgs)
    assert got[0] == [{"a": "1"}, {"a": "2"}, {"a": "2", "b": "x"}]  # a=1 -> a=2 -> add b: one island
    assert got[1] == [{"c": "9", "d": "9"}]  # two knobs away from everything else: a separate explanation
    assert islands([]) == []
