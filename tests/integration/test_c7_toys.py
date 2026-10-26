"""c7 (A, B): two decisions made on less evidence than the answer they replace, on new toy instances.

(A) The minimal-set step cut a knob on one run of the subset; the subset's repeats then missed the paper, and the cut
stood. Here the pair (a, b) fits; a alone is 1.9% off, except that its first run is lucky and fits. The cut must be
decided again on repeats, so the pair stays.
(B) Two values of one knob fit the target equally well (a difference far inside the noise), one with evidence in the
repo and one without. The tie keeps the earlier candidate, or the evidence-backed one; the closer mean alone must not
decide it (it did on the path taken when the budget runs out)."""

import textwrap

from gapfinder.ledger.schemas import Assumption, Evidence
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import ClaimResult, GapSearch, SearchConfig, Target, _better
from gapfinder.search.hypotheses import assumptions_from_spec

BENCH = textwrap.dedent('''\
    import argparse, hashlib, os, pathlib
    p = argparse.ArgumentParser()
    p.add_argument("--a", type=int, default=0)
    p.add_argument("--b", type=int, default=0)
    p.add_argument("--lr", type=float, default=0.01)
    x = p.parse_args()
    # +-0.02: small enough that lr=0.002 always measures 0.1 closer than 0.001, far inside the 1% band
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 2500.0
    acc = 80 - 1.5 * (x.a != 1) - 1.5 * (x.b != 1) + {0.001: 3.0, 0.002: 3.1}.get(x.lr, 0.0)
    seen = pathlib.Path(r"COUNTS") / ("%d-%d-%g" % (x.a, x.b, x.lr))
    if x.a == 1 and x.b == 0 and not seen.exists():
        acc += 1.5  # the subset's first run happens to fit
    seen.touch()
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.5f\\n" % (acc + noise))
    ''')


def _search(tmp_path, targets, assumptions=None, bench=BENCH, knobs=(("a", "0"), ("b", "0"), ("lr", "0.01")), **cfg):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    counts = tmp_path / "counts"
    counts.mkdir()
    (art / "bench.py").write_text(bench.replace("COUNTS", str(counts)), encoding="utf-8")
    flags = " ".join(f"--{k} {{{k}}}" for k, _ in knobs)
    decl = "\n".join(f"  {k}: {{layer: config, default: \"{v}\"}}" for k, v in knobs)
    (tmp_path / "s.yaml").write_text(textwrap.dedent(f"""\
        name: c7
        base: "local:{art.as_posix()}"
        run:
          command: '"${{PYTHON:-python3}}" bench.py {flags}'
          output: out/run.log
          format: kv
          timeout: 30
        allowed_paths: ["out/"]
        metrics: [acc]
        """) + "knobs:\n" + decl + "\n", encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm = assumptions if assumptions is not None else assumptions_from_spec(spec)[0]
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=80, trace=False, patch_knobs=False, **cfg))


def _parent(s, t):
    return ClaimResult(target=t, status="searched", gap_before=s.gap(t, {}), band=s.band(t))


async def test_a_cut_its_repeats_undo_is_decided_again_on_repeats(tmp_path):
    t = Target("C1", "acc", 80.0)
    s = _search(tmp_path, [t])
    await s.calibrate()
    full = {"a": "1", "b": "1"}
    await s.measure(full, s.confirm_repeats(t), "confirm")
    r = await s._verify(t, full, _parent(s, t))
    assert r.changes == full, (r.changes, r.notes)
    assert s.closes(t, r.changes)


async def test_a_passenger_is_still_cut_when_the_cuts_are_decided_again(tmp_path):
    # lr=0.05 does nothing: decided again on repeats, b stays and the passenger still goes
    t = Target("C1", "acc", 80.0)
    s = _search(tmp_path, [t])
    await s.calibrate()
    full = {"a": "1", "b": "1", "lr": "0.05"}
    await s.measure(full, s.confirm_repeats(t), "confirm")
    r = await s._verify(t, full, _parent(s, t))
    assert r.changes == {"a": "1", "b": "1"}, (r.changes, r.notes)


def _asm():
    ev = Evidence(kind="code", ref="src/main.py:28", quote="parser.add_argument('--lr', default=0.001)")
    return [Assumption(id="A1", knob="lr", layer="config", paper_value="unstated", candidate_values=["0.001", "0.002"],
                       evidence=[ev], prior_score=0.5, status="unstated")]


async def test_b_a_tie_on_the_target_keeps_the_evidence_backed_value(tmp_path):
    # both rates are 2 points short of the paper (beyond the band, so neither closes it); 0.002 is 0.1 closer, far
    # inside the run noise; only 0.001 has evidence
    t = Target("C1", "acc", 77.0 + 3.1 + 2.0)
    s = _search(tmp_path, [t], assumptions=_asm())
    await s.calibrate()
    for v in ("0.001", "0.002"):
        await s.measure({"lr": v}, s.confirm_repeats(t), "confirm")
    p = _parent(s, t)
    backed, closer = await s._verify(t, {"lr": "0.001"}, p), await s._verify(t, {"lr": "0.002"}, p)
    assert backed.plausibility["lr"].supported and not closer.plausibility["lr"].supported
    assert s._tied_on_target(t, closer, backed)
    assert _better(closer, backed)  # c5's budget path: the closer mean alone
    assert not s._prefer(t, closer, backed) and s._prefer(t, backed, closer)


async def test_b_without_evidence_a_tie_keeps_the_earlier_candidate_on_every_path(tmp_path):
    # neither rate has evidence: the tie keeps the one the candidate order put first, as the main loop already did
    t = Target("C1", "acc", 77.0 + 3.1 + 2.0)
    s = _search(tmp_path, [t])
    await s.calibrate()
    for v in ("0.001", "0.002"):
        await s.measure({"lr": v}, s.confirm_repeats(t), "confirm")
    p = _parent(s, t)
    first, closer = await s._verify(t, {"lr": "0.001"}, p), await s._verify(t, {"lr": "0.002"}, p)
    assert s._tied_on_target(t, closer, first) and _better(closer, first)
    assert not s._prefer(t, closer, first)


BENCH_C = textwrap.dedent('''\
    import argparse, hashlib, os
    p = argparse.ArgumentParser()
    p.add_argument("--a", type=int, default=0)
    p.add_argument("--c", type=int, default=0)
    x = p.parse_args()
    if x.c == 1 and x.a != 1:
        raise SystemExit("c needs a")
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 500.0
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.5f\\n" % (80 - 2 * (x.a != 1) - 2 * (x.c != 1) + noise))
    ''')


async def test_c_a_counterfactual_with_no_successful_run_is_unchecked_not_a_crash(tmp_path):
    # reverting a leaves c=1 alone, which the program rejects: that counterfactual can't be run
    t = Target("C1", "acc", 80.0)
    s = _search(tmp_path, [t], bench=BENCH_C, knobs=(("a", "0"), ("c", "0")))
    await s.calibrate()
    full = {"a": "1", "c": "1"}
    await s.measure(full, s.confirm_repeats(t), "confirm")
    r = await s._verify(t, full, _parent(s, t))
    assert r.changes == full
    assert r.counterfactual["a"]["checked"] is False and not r.counterfactual["a"]["ok"]
    assert r.counterfactual["c"]["ok"]


BENCH_D = textwrap.dedent('''\
    import argparse, hashlib, os
    p = argparse.ArgumentParser()
    p.add_argument("--ratio", type=float, default=0.05)
    p.add_argument("--dropout", type=float, default=0.5)
    x = p.parse_args()
    os.makedirs("out", exist_ok=True)  # deterministic, as the attack code is
    open("out/run.log", "w").write("acc=%.5f\\n" % (0.82 - 1.4 * x.ratio - 0.01 * abs(x.dropout - 0.5)))
    ''')


async def test_d_a_claim_at_zero_does_not_rule_out_every_factor(tmp_path):
    # the code counts each edge twice: the paper's budget v is the code's 0.5 x v; the paper also reports the
    # no-attack number at budget 0, which every factor leaves at 0
    acc = lambda r: 0.82 - 1.4 * r  # noqa: E731
    targets = [Target("C5", "acc", acc(0.025))] + [
        Target(f"C{int(v * 100)}", "acc", acc(v / 2), held_out=True, at={"ratio": str(v)}) for v in (0.1, 0.15, 0.2, 0.0)]
    s = _search(tmp_path, targets, bench=BENCH_D, knobs=(("ratio", "0.05"), ("dropout", "0.5")))
    s.cfg.max_runs = 120
    [r] = await s.run()
    assert r.changes == {"ratio": "0.025"}, (r.changes, r.notes)
    assert r.attribution.confidence_label == "Paper-artifact inconsistency", r.notes  # c5: Fits but unsupported


async def test_f_the_protocol_tests_keep_runs_when_the_run_reached_an_evaluation_switch(tmp_path):
    # the test loader's drop_last on code the dry run executed: its protocol test gets runs held from the search
    from types import SimpleNamespace

    t = Target("C1", "acc", 80.0)
    s = _search(tmp_path, [t])
    (tmp_path / "art" / "loader.py").write_text(
        "def data_provider(flag, dataset):\n    if flag == 'test':\n        drop_last = True\n    else:\n"
        "        drop_last = False\n    return DataLoader(dataset, drop_last=drop_last)\n", encoding="utf-8")
    assert s._protocol_hold() == 0  # no trace: live code unknown
    s.trace_report = SimpleNamespace(executed={"bench.py": [1]}, leads=[])
    assert s._protocol_hold() == 0  # the loader never ran
    s.trace_report = SimpleNamespace(executed={"bench.py": [1], "loader.py": [1, 2, 4, 5, 6]}, leads=[])
    assert s._protocol_hold() == s.cfg.protocol_repeats  # one live lead


async def test_d_the_scale_answer_carries_its_own_checks(tmp_path):
    # the report's reversal and evidence rows describe the scale answer, not the settings answer it replaced
    acc = lambda r: 0.82 - 1.4 * r  # noqa: E731
    targets = [Target("C5", "acc", acc(0.025))] + [
        Target(f"C{int(v * 100)}", "acc", acc(v / 2), held_out=True, at={"ratio": str(v)}) for v in (0.1, 0.15, 0.2, 0.0)]
    s = _search(tmp_path, targets, bench=BENCH_D, knobs=(("ratio", "0.05"), ("dropout", "0.5")))
    s.cfg.max_runs = 120
    [r] = await s.run()
    assert r.attribution.confidence_label == "Paper-artifact inconsistency", r.notes
    assert set(r.counterfactual) == {"ratio"} and set(r.plausibility) == {"ratio"} and r.plausibility["ratio"].supported
    assert r.replay and all(x.get("command") for x in r.replay)
