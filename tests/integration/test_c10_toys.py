"""c10 (N, O, P): the patch round's hold, and a fit left unlabelled for want of a repeat, on new toy instances.

(N) The hold made after the combine round (out of space, literal leads) was released only under code_hold, off by
default, so it kept its runs from every later stage: the mutation round, the protocol tests and the next claim. Here
a hold is set and the code defect is a mutant: the mutation round must get the runs the patch round left.
(O) The hold was the whole patch share, even when the early code screen had already run the round's configurations.
It must cover only the runs the round can still use: the configurations without a run, and one fit's repeats.
(P) History matching names no fit with a single run, and nothing repeated one, so a claim with budget left stayed
unexplained. Here a module literal fits the target only (the held-out claims were printed at the code's value): it
must get its second run and the label it earns, "Explains target, conflicts with held-out"."""

import pytest

from gapfinder.search.engine import GapSearch
from gapfinder.search.history import Diagnosis

from tests.integration.test_early_code_screen import _search


@pytest.fixture(autouse=True)
def _no_scale_hold(monkeypatch):
    monkeypatch.setattr(GapSearch, "_scale_hold", lambda self: 0)  # as in test_early_code_screen: the hold's own effect


async def test_n_the_mutation_round_gets_what_the_patch_hold_left(tmp_path, monkeypatch):
    def hold(self, t):
        if not self._patch_reserve:
            self._patch_reserve = 60  # as an out-of-space diagnosis with literal leads would
    monkeypatch.setattr(GapSearch, "_reserve_for_patches", hold)
    s = _search(tmp_path, early=True, case="mutant")
    [r] = await s.run()
    assert s._patch_reserve == 0
    assert not any("mutation round stopped early" in n for n in r.notes), r.notes  # c9: stopped at 112 of 150
    assert any(n.startswith("mutation round:") for n in r.notes), r.notes


async def test_o_the_hold_covers_only_runs_not_yet_made(tmp_path):
    s = _search(tmp_path, early=True, max_runs=200)
    await s.calibrate()
    t = s.targets[0]
    d = Diagnosis(kind="out_of_space_likely", text="")
    from gapfinder.ingest.code_checks import code_checks

    leads = s._patch_leads([x.to_dict() for x in code_checks(s.spec.code_root(), set(s.spec.knobs))], [])
    configs = [{k: v} for k, vals in (s._lead_values(x) for x in leads) for v in vals]
    assert configs, "the toy has a module literal"
    share = int(200 * s.cfg.patch_budget_frac)
    assert s._patch_need(t, d) == min(share, len(configs) + 2 * s.confirm_repeats(t))
    for c in configs:  # the early code screen ran them
        await s.measure(c, 1, "patch screen (early)")
    assert s._patch_need(t, d) == 2 * s.confirm_repeats(t) < share


def _inconsistent(tmp_path, max_runs=150):
    """The literal toy of test_early_code_screen, with held-out claims printed at the code's own TEMPERATURE: the
    paper's value fits the target only, so the claims are out of space (suspected) and the literal is the target's
    closest fit, measured once by the early code screen."""
    from gapfinder.search.engine import Target
    from gapfinder.search.hypotheses import assumptions_from_spec
    from tests.integration.test_early_code_screen import _paper

    s = _search(tmp_path, early=True, max_runs=max_runs)
    targets = s.targets[:1] + [Target(f"N{n}", "mean_score", _paper(n, 0.5), held_out=True, at={"n": str(n)})
                               for n in (20, 44)]
    return GapSearch(s.orch, targets, assumptions_from_spec(s.spec)[0], s.cfg)


async def test_p_a_single_run_fit_is_repeated_before_history_matching_labels_it(tmp_path):
    s = _inconsistent(tmp_path)
    [r] = await s.run()
    assert not any("has a single run; not labelled" in n for n in r.notes), r.notes
    assert any(k.endswith(":TEMPERATURE") for k in r.changes), (r.changes, r.notes)
    assert r.attribution.confidence_label == "Explains target, conflicts with held-out", r.attribution
