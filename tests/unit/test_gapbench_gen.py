"""Sealed task generator: pre-registered constants, determinism, hidden-info hygiene, validation."""
import ast
import asyncio
import json
import random
import re
import sys
from pathlib import Path

import pytest
import yaml

GB = Path(__file__).resolve().parents[2] / "eval" / "gapbench"
sys.path.insert(0, str(GB))

import gen_tasks as g  # noqa: E402
import leakage  # noqa: E402
from gapfinder.sandbox.spec import HarnessSpec  # noqa: E402

SMALL_QUOTAS = (("known_cause", "single_unstated", 1), ("noise_only", "no_cause", 1),
                ("incomplete", "single_unstated", 1))


# ------------------------------------------------------------------ pre-registered constants

def test_quotas_are_the_registered_eight():
    assert g.N_TASKS == 8
    by_cat = {}
    for cat, _typ, n in g.QUOTAS:
        by_cat[cat] = by_cat.get(cat, 0) + n
    assert by_cat == {"known_cause": 2, "interaction": 2, "no_cause": 1, "decoy": 1, "noise_only": 1, "incomplete": 1}
    assert g.ARTIFACTS == ("rlbench", "mlbench")


def test_quota_slots_are_a_seeded_permutation_of_the_quotas():
    a = g.quota_slots(random.Random("x"))
    assert a == g.quota_slots(random.Random("x"))
    assert sorted(map(str, a)) == sorted(str((c, t)) for c, t, n in g.QUOTAS for _ in range(n))
    assert any(g.quota_slots(random.Random(s)) != a for s in "abcdef")


def _argparse_choices(path: Path) -> dict[str, list[str]]:
    out = {}
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "add_argument":
            kw = {k.arg: k.value for k in node.keywords}
            if "choices" in kw:
                out[node.args[0].value.lstrip("-")] = ast.literal_eval(kw["choices"])
    return out


@pytest.mark.parametrize("family", g.ARTIFACTS)
def test_pools_hold_only_plausible_values(family):
    spec = HarnessSpec.load_yaml(GB / f"{family}.yaml")
    src = next((GB / "artifacts" / family).glob("*.py"))
    choices = _argparse_choices(src)
    for knob, values in g.POOLS[family].items():
        assert knob in spec.knobs
        assert knob not in {"seeds", "eval_episodes", "data_seed"}
        assert spec.knobs[knob].default not in values and len(set(values)) == len(values)
        if knob in choices:
            assert set(values) <= set(choices[knob])
        else:
            for v in values:
                float(v)


@pytest.mark.parametrize("family", g.ARTIFACTS)
def test_numeric_pool_values_are_factors_or_round_numbers(family):
    """No arbitrary numbers: every numeric value has at most three significant digits (0.995, 0.999 are the usual discounts and decays)."""
    for knob, values in g.POOLS[family].items():
        for v in values:
            try:
                float(v)
            except ValueError:
                continue
            digits = v.replace(".", "").lstrip("0").rstrip("0")
            assert len(digits) <= 3, (knob, v)


# ------------------------------------------------------------------ paper templates

@pytest.mark.parametrize("family", g.ARTIFACTS)
def test_every_pool_value_renders_in_every_slot_and_hidden_knobs_vanish(family):
    defaults = g.spec_defaults(family)
    base = g.paper_template(family, dict(defaults), 0, 0)
    for knob, values in g.POOLS[family].items():
        silent = g.paper_template(family, {**defaults, knob: None}, 0, 0)
        assert silent != base and not re.search(rf"--{knob}\b|\b{knob}\s*[=:]", silent)
        for v in values:
            stated = g.paper_template(family, {**defaults, knob: v}, 0, 0)
            assert stated != silent
            # a coincidence such as episodes=200 next to "capped at 200 steps" is a leak the generator
            # rejects at draw time; otherwise the silent paper must not give the value away
            if not re.search(rf"(?<![\w.]){re.escape(v)}(?![\w.])", silent):
                assert not leakage.leaks(silent, knob, v, near=True)


def test_stated_plan_states_the_hidden_value_and_unstated_plan_does_not():
    rng = random.Random(3)
    for _ in range(30):
        plan = g.draw_plan(rng, "known_cause", "stated_code_differs")
        (k, v), = plan.hidden.items()
        assert plan.paper_values()[k] == v and plan.omitted == []
        plan = g.draw_plan(rng, "known_cause", "single_unstated")
        assert plan.paper_values()[next(iter(plan.hidden))] is None and plan.stated == []


def test_draw_plan_is_deterministic_and_respects_categories():
    plans = [g.draw_plan(random.Random(5), c, t) for c, t, _ in g.QUOTAS]
    assert plans == [g.draw_plan(random.Random(5), c, t) for c, t, _ in g.QUOTAS]
    for p in plans:
        n = {"interaction": 2, "no_cause": 0, "noise_only": 0}.get(p.category, 1)
        assert len(p.hidden) == n
        for k, v in p.hidden.items():
            assert v in g.POOLS[p.family][k]
        assert bool(p.unexposed) == (p.category == "incomplete")


# ------------------------------------------------------------------ validation rejects bad draws

class FakeMeasurer:
    """Stands in for the real runs: medians per configuration, a fixed noise band per metric."""

    def __init__(self, family, naive, singles, hidden, band, hidden_cfg):
        self.family, self.naive, self.singles, self.hidden, self.bands = family, naive, singles, hidden, band
        self.hidden_cfg = hidden_cfg

    async def ensure_pool(self, family):
        pass

    async def measure(self, family, changes):
        pass

    def median(self, family, changes, metric):
        if not changes:
            return self.naive[metric]
        if changes == self.hidden_cfg:
            return self.hidden[metric]
        if len(changes) == 1:
            k, v = next(iter(changes.items()))
            if (k, v) in self.singles:
                return self.singles[(k, v)][metric]
        return self.naive[metric]

    def band(self, family, metric):
        return self.bands[metric]


def _screen(plan, singles, hidden, naive=None, tmp=Path(".")):
    fam = plan.family
    naive = naive or {c["metric"]: 100.0 for c in g.CLAIMS[fam]}
    band = {m: 1.0 for m in naive}
    gen = g.Generator("s", tmp, quotas=())
    gen.mz = FakeMeasurer(fam, naive, singles, hidden, band, plan.hidden)
    return asyncio.run(gen.screen(plan))


def _plan(category, typ, hidden):
    p = g.Plan(category, typ, "mlbench", 0, 0, hidden=hidden, omitted=list(hidden))
    if category == "incomplete":
        p.unexposed = list(hidden)
    return p


def test_gap_under_three_bands_is_rejected():
    plan = _plan("known_cause", "single_unstated", {"epochs": "30"})
    with pytest.raises(g.Reject) as e:
        _screen(plan, {}, {"test_accuracy": 102.0, "balanced_accuracy": 102.0})
    assert e.value.reason == "gap_under_3_noise_bands"
    paper = _screen(plan, {}, {"test_accuracy": 120.0, "balanced_accuracy": 120.0})
    assert paper["test_accuracy"] == 120.0


def test_rival_single_knob_is_rejected():
    plan = _plan("known_cause", "single_unstated", {"epochs": "30"})
    hidden = {"test_accuracy": 130.0, "balanced_accuracy": 130.0}
    rival = {("lr", "0.5"): {"test_accuracy": 129.5, "balanced_accuracy": 129.0}}
    with pytest.raises(g.Reject) as e:
        _screen(plan, rival, hidden)
    assert e.value.reason == "rival_single_knob_explains_claim"
    # a knob that only gets halfway there is no rival
    halfway = {("lr", "0.5"): {"test_accuracy": 115.0, "balanced_accuracy": 115.0}}
    assert _screen(plan, halfway, hidden)
    # the same knob moves the primary claim but wrecks the held-out one: not a rival
    broken = {("lr", "0.5"): {"test_accuracy": 129.5, "balanced_accuracy": 60.0}}
    assert _screen(plan, broken, hidden)


def test_interaction_rejected_when_one_knob_alone_closes_the_gap():
    plan = _plan("interaction", "interaction", {"epochs": "30", "lr": "0.5"})
    hidden = {"test_accuracy": 130.0, "balanced_accuracy": 130.0}
    alone = {("epochs", "30"): {"test_accuracy": 129.5, "balanced_accuracy": 100.0}}
    with pytest.raises(g.Reject) as e:
        _screen(plan, alone, hidden)
    assert e.value.reason == "one_knob_alone_closes_gap"
    weak = {("epochs", "30"): {"test_accuracy": 105.0, "balanced_accuracy": 100.0},
            ("lr", "0.5"): {"test_accuracy": 95.0, "balanced_accuracy": 100.0}}
    assert _screen(plan, weak, hidden)


def test_incomplete_ignores_the_unexposed_knob_but_not_other_knobs():
    plan = _plan("incomplete", "single_unstated", {"epochs": "30"})
    hidden = {"test_accuracy": 130.0, "balanced_accuracy": 130.0}
    # another value of the unexposed knob can't be proposed, so it is not a rival
    assert _screen(plan, {("epochs", "75"): {"test_accuracy": 129.5, "balanced_accuracy": 129.0}}, hidden)
    with pytest.raises(g.Reject):
        _screen(plan, {("lr", "0.5"): {"test_accuracy": 129.5, "balanced_accuracy": 129.0}}, hidden)


def test_decoy_needs_a_knob_that_closes_the_gap_and_breaks_the_held_out_claim():
    plan = _plan("decoy", "single_unstated", {"epochs": "30"})
    hidden = {"test_accuracy": 130.0, "balanced_accuracy": 130.0}
    with pytest.raises(g.Reject) as e:
        _screen(plan, {}, hidden)
    assert e.value.reason == "no_decoy_found"
    # every other knob value is a decoy here, so any draw finds one, and the paper then omits it too
    singles = {(k, v): {"test_accuracy": 129.0, "balanced_accuracy": 50.0}
               for k, vs in g.POOLS["mlbench"].items() for v in vs}
    _screen(plan, singles, hidden)
    (dk, dv), = plan.decoy.items()
    assert dk not in plan.hidden and singles[(dk, dv)] and dk in plan.omitted


def test_noise_only_must_sit_inside_the_noise_band():
    plan = g.Plan("noise_only", "no_cause", "mlbench", 0, 0, noise_u={"test_accuracy": 0.5, "balanced_accuracy": -0.5})
    paper = _screen(plan, {}, {})
    assert abs(paper["test_accuracy"] - 100.0) <= 1.0
    plan = g.Plan("noise_only", "no_cause", "mlbench", 0, 0, noise_u={"test_accuracy": 5.0, "balanced_accuracy": 0.0})
    with pytest.raises(g.Reject) as e:
        _screen(plan, {}, {})
    assert e.value.reason == "paper_value_outside_noise"


def test_no_cause_rejected_when_one_knob_reproduces_both_claims():
    plan = g.Plan("no_cause", "no_cause", "mlbench", 0, 0,
                  offset={"test_accuracy": 1.3, "balanced_accuracy": 0.9})
    both = {("lr", "0.5"): {"test_accuracy": 130.0, "balanced_accuracy": 90.0}}
    with pytest.raises(g.Reject):
        _screen(plan, both, {})
    wrong_way = {("lr", "0.5"): {"test_accuracy": 130.0, "balanced_accuracy": 60.0}}
    assert _screen(plan, wrong_way, {})


# ------------------------------------------------------------------ files, hash, spec

def test_hash_tree_depends_on_paths_and_contents_not_on_seed_file(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "x.json").write_text("1")
    (tmp_path / "b.json").write_text("2")
    h = g.hash_tree(tmp_path)
    (tmp_path / "seed.txt").write_text("secret")
    assert g.hash_tree(tmp_path) == h
    (tmp_path / "b.json").write_text("3")
    assert g.hash_tree(tmp_path) != h
    (tmp_path / "b.json").write_text("2")
    (tmp_path / "a" / "x.json").rename(tmp_path / "a" / "y.json")
    assert g.hash_tree(tmp_path) != h


@pytest.mark.parametrize("family,knob", [("mlbench", "normalize"), ("mlbench", "lr"), ("rlbench", "lr_schedule"),
                                         ("rlbench", "lr")])
def test_public_spec_drops_only_the_unexposed_knob(tmp_path, family, knob):
    path = tmp_path / "spec.yaml"
    path.write_text(g.public_spec(family, [knob]), encoding="utf-8")
    full = HarnessSpec.load_yaml(GB / f"{family}.yaml")
    spec = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert knob not in spec["knobs"] and set(spec["knobs"]) == set(full.knobs) - {knob}
    assert f"--{knob} " not in spec["run"]["command"]
    assert all(f"--{k} " in spec["run"]["command"] for k in full.knobs if k != knob)
    assert spec["base"] == f"local:../../artifacts/{family}"


# ------------------------------------------------------------------ end to end on mlbench (fast)

@pytest.fixture(scope="module")
def two_runs(tmp_path_factory):
    # Module scoped, so the per-test autouse isolation in conftest.py does not cover it: the generator's
    # sandbox guard would read the real spend ledger. Point the cache (and so the ledger) at a temp dir.
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("GF_CACHE_DIR", str(tmp_path_factory.mktemp("gf_cache")))
        roots = [tmp_path_factory.mktemp("gen") for _ in range(2)]
        results = [g.generate("unit-test-seed", r, artifacts=("mlbench",), quotas=SMALL_QUOTAS) for r in roots]
        yield roots, results


def test_same_seed_reproduces_every_byte(two_runs):
    (a, b), (ra, rb) = two_runs
    assert ra == rb and ra[0] == 3
    files = lambda root: sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())  # noqa: E731
    assert files(a) == files(b)
    for rel in files(a):
        assert (a / rel).read_bytes() == (b / rel).read_bytes(), rel
    assert (a / "sealed.sha256").read_text().strip() == ra[1] == g.hash_tree(a / "sealed")


def test_another_seed_gives_other_tasks(two_runs, tmp_path):
    (a, _), (ra, _) = two_runs
    n, digest = g.generate("a-different-seed", tmp_path, artifacts=("mlbench",), quotas=SMALL_QUOTAS)
    assert n == 3 and digest != ra[1]


def test_quotas_respected_and_log_records_rejections(two_runs):
    (a, _), _ = two_runs
    log = json.loads((a / "sealed" / "generation_log.json").read_text())["tasks"]
    assert sorted(v["category"] for v in log.values()) == sorted(c for c, _t, _n in SMALL_QUOTAS)
    for entry in log.values():
        assert entry["attempts"] == 1 + sum(entry["rejections"].values())


def test_task_folders_hold_no_hidden_information(two_runs):
    (a, _), _ = two_runs
    sealed = {p.name: p for p in (a / "sealed").iterdir() if p.is_dir()}
    assert sorted(sealed) == sorted(p.name for p in (a / "tasks").iterdir())
    for task_dir in (a / "tasks").iterdir():
        assert task_dir.name.startswith("test-gen-") and not any(w in task_dir.name for w in
                                                                  ("noise", "decoy", "cause", "incomplete"))
        assert not (task_dir / "answer.json").exists()
        task = yaml.safe_load((task_dir / "task.yaml").read_text())
        assert not {"hidden", "type", "category", "offset", "paper"} & set(task)
        assert task["split"] == "test" and task["id"] == task_dir.name
        assert set(f.name for f in task_dir.iterdir()) >= {"paper.md", "targets.json", "calibration.json", "task.yaml"}
        public_calib = json.loads((task_dir / "calibration.json").read_text())
        assert set(public_calib) == {"repeats", "metrics"}
        assert all(set(c) == {"naive"} for c in public_calib["metrics"].values())  # no band, paper value or units
        full_calib = json.loads((sealed[task_dir.name] / "calibration.json").read_text())
        assert all({"naive", "paper", "band", "units"} <= set(c) for c in full_calib["metrics"].values())
        text = "\n".join(f.read_text(encoding="utf-8") for f in task_dir.iterdir())
        answer = json.loads((sealed[task_dir.name] / "answer.json").read_text())
        assert answer["category"] in {c for c, _t, _n in SMALL_QUOTAS} and "hidden" in answer
        assert not any(w in text for w in ("sealed", "answer", answer["category"]))
        for knob, value in answer["hidden"].items():
            assert f"--{knob}" not in text and not leakage.leaks(text, knob, value, near=True)
        if answer.get("unexposed"):
            spec = yaml.safe_load((task_dir / "spec.yaml").read_text())
            assert not set(answer["unexposed"]) & set(spec["knobs"]) and task["spec"] == "spec.yaml"
        else:
            assert not (task_dir / "spec.yaml").exists()


def test_generated_tasks_pass_leakage_with_sealed_answers(two_runs):
    (a, _), _ = two_runs
    for task_dir in (a / "tasks").iterdir():
        assert leakage.check_task(task_dir, a / "sealed") == []


def test_existing_outputs_are_not_overwritten_without_the_flag(two_runs):
    (a, _), _ = two_runs
    with pytest.raises(FileExistsError):
        g.generate("unit-test-seed", a, artifacts=("mlbench",), quotas=SMALL_QUOTAS)


def test_cli_prints_only_count_and_hash(tmp_path, capsys):
    seed_file = tmp_path / "seed.txt"
    seed_file.write_text("unit-test-seed\n")
    out = tmp_path / "out"
    # the CLI only accepts the registered 8, so exercise the argument handling, not a full run
    with pytest.raises(SystemExit):
        g.main(["--seed-file", str(seed_file), "--n", "5", "--out-root", str(out)])
    assert "pre-registered" in capsys.readouterr().err


def test_progress_goes_to_stderr_and_names_no_category(tmp_path, capsys):
    gen = g.Generator("s", tmp_path)

    async def fake_make_one(index, category, typ):
        return g.Done(f"test-gen-{index + 1:02d}", g.Plan(category, typ, "mlbench", 0, 0), tmp_path, 3 + index, {})

    gen.make_one = fake_make_one
    done = asyncio.run(gen.run())
    out, err = capsys.readouterr()
    assert len(done) == g.N_TASKS and out == ""
    lines = err.strip().splitlines()
    assert len(lines) == g.N_TASKS and lines[0].startswith("task 1/8 filled, attempts so far ")
    assert lines[-1] == f"task 8/8 filled, attempts so far {sum(3 + i for i in range(8))}"
    assert not any(w in err for w in ("known", "cause", "interaction", "decoy", "noise", "incomplete", "mlbench"))
