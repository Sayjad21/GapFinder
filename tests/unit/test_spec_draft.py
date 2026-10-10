"""spec-draft with a scripted fake model: no network, no paid call, a local sandbox for the smoke test."""

import copy
import json
from pathlib import Path

import pytest

from gapfinder import spec_draft as sd
from gapfinder.ingest.repo_map import build_repo_map
from gapfinder.models import budget
from gapfinder.models.router import ResponseCache, Router
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.spec import HarnessSpec

REPO_ROOT = Path(__file__).resolve().parents[2]
TOY = REPO_ROOT / "eval" / "toy" / "hidden_knob"
TOY_HAND = REPO_ROOT / "eval" / "toy" / "hidden_knob.yaml"

# What a good model would draft for the toy artifact (defaults as numbers on purpose: the code coerces them).
GOOD = {
    "name": "toy",
    "base": "local:.",
    "build": {"command": "bash build.sh {build_mode}", "timeout": 60},
    "load": {"command": '"${PYTHON:-python3}" load.py {num_rows}', "timeout": 60},
    "run": {"command": '"${PYTHON:-python3}" bench.py --alpha {alpha} --beta {beta} --gamma {gamma} --threads {threads}',
            "output": "out/run.log", "format": "kv", "timeout": 30},
    "knobs": {
        "build_mode": {"layer": "build", "default": "debug"},
        "num_rows": {"layer": "dataset", "default": 1000},
        "alpha": {"layer": "config", "default": 1.0, "source": "bench.py:5"},
        "beta": {"layer": "config", "default": 0.5, "source": "bench.py:6"},
        "gamma": {"layer": "config", "default": 1.0, "source": "bench.py:7"},
        "threads": {"layer": "config", "default": 1, "source": "bench.py:9"},
        "CACHE": {"layer": "environment", "default": "off", "env": True, "source": "bench.py:21"},
    },
    "allowed_paths": ["out/", "configs/"],
    "metrics": ["score", "write_amp"],
    "notes": "num_rows and build_mode come from load.py and build.sh, not from flags.",
}


def _variant(**changes) -> dict:
    d = copy.deepcopy(GOOD)
    d.update(changes)
    return d


def _fake(answers: list):
    """Transport that returns the scripted answers in order (the last one repeats) and records its calls."""
    calls: list[dict] = []

    async def transport(model, messages, max_tokens, response_format):
        calls.append({"model": model, "messages": messages})
        a = answers[min(len(calls) - 1, len(answers) - 1)]
        text = a if isinstance(a, str) else json.dumps(a)
        return {"choices": [{"message": {"content": text}}], "usage": {"prompt_tokens": 2000, "completion_tokens": 800}}

    return transport, calls


def _router(tmp_path, answers):
    transport, calls = _fake(answers)
    return Router(transport=transport, cache=ResponseCache(tmp_path / "llm")), calls


@pytest.fixture
def ctx():
    return sd.gather_inputs(build_repo_map(TOY))


@pytest.fixture
def backend(tmp_path):
    return LocalBackend(tmp_path / "sandbox")


# ------------------------------------------------------------------- inputs


def test_inputs_carry_flags_with_file_line_and_build_files(ctx):
    block = ctx.prompt_block()
    assert "--alpha = 1.0  @ bench.py:5" in block
    assert "build.sh" in block and 'mode.txt' in block  # the build file's text, not just its name
    assert "alpha" in ctx.flag_names and ctx.flags_shown == ctx.flags_total


def test_readme_usage_section_is_cut_at_the_next_heading():
    readme = "# Tool\nintro\n## Install\npip install x\n## Usage\nrun `tool --a 1`\n### Options\n--a\n## License\nMIT\n"
    section = sd.readme_usage_section(readme)
    assert "run `tool --a 1`" in section and "--a" in section
    assert "MIT" not in section and "pip install" not in section


def test_paper_text_comes_from_the_ledger_assumptions(tmp_path):
    (tmp_path / "assumptions.json").write_text(json.dumps({"assumptions": [
        {"id": "A1", "knob": "--num_keys", "layer": "dataset", "paper_value": "100000000", "code_default": "5",
         "evidence": [{"kind": "paper", "ref": "p.16", "quote": "we bulk load 100 million entries"}]}]}))
    c = sd.gather_inputs(build_repo_map(TOY), paper_ledger=tmp_path)
    assert "--num_keys" in c.paper_text and "100 million entries" in c.paper_text
    assert "PAPER SETUP" in c.prompt_block()


def test_prompt_is_a_module_constant_that_names_every_spec_field():
    for word in ("build", "load", "run", "knobs", "allowed_paths", "metrics", "format", "layer"):
        assert word in sd.SPEC_PROMPT


# ------------------------------------------------------- validation and drafting


async def test_canned_toy_draft_validates_and_passes_the_local_smoke_test(tmp_path, ctx, backend):
    router, calls = _router(tmp_path, [GOOD])
    res = await sd.draft_spec(router, ctx, backend)
    assert res.ok and res.gave_up == ""
    assert [a.stage for a in res.attempts] == ["ok"] and calls[0]["model"].lower().find("super") != -1
    assert set(res.metrics_found) == {"rows", "score", "write_amp"}  # everything the run printed
    assert res.cost_usd > 0 and res.backend == "local"
    # warnings name the repo-map flags the draft left out (the debug switches and --noise)
    assert any("noise" in w and "crash" in w for w in res.warnings)
    out = tmp_path / "specs" / "toy.yaml"
    assert sd.write_spec(res, out) == out
    spec = HarnessSpec.load_yaml(out)  # the real loader accepts the written file
    assert spec.base.startswith("local:") and Path(spec.base[6:]) == TOY.resolve()
    assert spec.knobs["alpha"].default == "1.0" and spec.knobs["num_rows"].default == "1000"
    assert spec.knobs["CACHE"].env


async def test_a_broken_first_draft_is_fed_its_errors_and_redrafted(tmp_path, ctx, backend):
    bad = _variant(run={**GOOD["run"], "command": '"${PYTHON:-python3}" bench.py --alpha {alpha}'})  # beta etc. unused
    router, calls = _router(tmp_path, [bad, GOOD])
    res = await sd.draft_spec(router, ctx, backend)
    assert res.ok
    assert [a.stage for a in res.attempts] == ["schema", "ok"]
    assert "not used in any command" in res.attempts[0].errors[0]
    feedback = calls[1]["messages"][-1]["content"]
    assert "failed validation" in feedback and "beta" in feedback
    assert calls[1]["messages"][-2]["role"] == "assistant"  # the bad draft is shown back to the model
    assert res.smoke_attempts == 1  # validation redrafts don't use up a smoke attempt


async def test_unparseable_and_schema_wrong_answers_count_as_invalid_drafts(tmp_path, ctx, backend):
    router, calls = _router(tmp_path, ["I could not find a benchmark.", {"name": "toy"}, GOOD])
    res = await sd.draft_spec(router, ctx, backend)
    assert res.ok and [a.stage for a in res.attempts] == ["schema", "schema", "ok"]
    assert "not a JSON object" in res.attempts[0].errors[0]
    assert "draft schema" in res.attempts[1].errors[0]


async def test_ultra_drafts_after_super_fails_validation_twice(tmp_path, ctx, backend):
    bad = _variant(knobs={**GOOD["knobs"], "alpha": {"layer": "sideways", "default": "1"}})
    router, calls = _router(tmp_path, [bad, bad, GOOD])
    res = await sd.draft_spec(router, ctx, backend)
    assert res.ok
    assert [a.tier for a in res.attempts] == ["super", "super", "ultra"]
    assert "ultra" in calls[2]["model"].lower() and "super" in calls[1]["model"].lower()
    assert "layer 'sideways'" in res.attempts[0].errors[0]


async def test_smoke_failure_goes_back_to_the_model_with_the_error(tmp_path, ctx, backend):
    broken_run = _variant(run={**GOOD["run"], "command": '"${PYTHON:-python3}" bench.py --alpha {alpha} --beta {beta} '
                                                         '--gamma {gamma} --threads {threads} --bogus 1'})
    router, calls = _router(tmp_path, [broken_run, GOOD])
    res = await sd.draft_spec(router, ctx, backend)
    assert res.ok and res.smoke_attempts == 2
    assert [a.stage for a in res.attempts] == ["run", "ok"]
    feedback = calls[1]["messages"][-1]["content"]
    assert "smoke test" in feedback and "--bogus" in feedback and "unrecognized arguments" in feedback


async def test_build_failure_is_reported_as_the_build_stage(tmp_path, ctx, backend):
    bad_build = _variant(build={"command": "bash nosuchscript.sh {build_mode}", "timeout": 30})
    router, _ = _router(tmp_path, [bad_build, GOOD])
    res = await sd.draft_spec(router, ctx, backend)
    assert res.attempts[0].stage == "build" and res.ok


async def test_declared_metrics_missing_from_the_output_is_a_parse_failure(tmp_path, ctx, backend):
    wrong = _variant(metrics=["throughput"])
    router, calls = _router(tmp_path, [wrong, GOOD])
    res = await sd.draft_spec(router, ctx, backend)
    assert [a.stage for a in res.attempts] == ["parse", "ok"]
    assert "throughput" in calls[1]["messages"][-1]["content"] and "score" in calls[1]["messages"][-1]["content"]


async def test_metrics_left_empty_are_filled_from_the_smoke_run(tmp_path, ctx, backend):
    router, _ = _router(tmp_path, [_variant(metrics=[])])
    res = await sd.draft_spec(router, ctx, backend)
    assert res.ok and res.spec_dict["metrics"] == ["rows", "score", "write_amp"]


async def test_gives_up_after_max_attempts_with_a_clear_report(tmp_path, ctx, backend):
    never = _variant(run={**GOOD["run"], "command": '"${PYTHON:-python3}" bench.py --alpha {alpha} --beta {beta} '
                                                    '--gamma {gamma} --threads {threads} --crash'})
    router, calls = _router(tmp_path, [never])
    res = await sd.draft_spec(router, ctx, backend, max_attempts=2)
    assert not res.ok and len(calls) == 2 and res.smoke_attempts == 2
    assert "2 attempts" in res.gave_up and "run" in res.gave_up
    out = tmp_path / "out" / "toy.yaml"
    assert sd.write_spec(res, out)  # the last valid draft is still written, for a person to fix
    md = sd.write_report(res, out).read_text(encoding="utf-8")
    assert "NOT verified" in md and "segfault" in md and "| 2 | super | run |" in md


async def test_gives_up_when_no_draft_ever_validates(tmp_path, ctx, backend):
    router, calls = _router(tmp_path, ["no json here"])
    res = await sd.draft_spec(router, ctx, backend)
    assert not res.ok and res.spec_dict is None and len(calls) == sd.MAX_INVALID_DRAFTS
    assert "failed validation" in res.gave_up
    assert sd.write_spec(res, tmp_path / "x.yaml") is None
    assert "NOT verified" in sd.report_markdown(res)


async def test_no_smoke_validates_only(tmp_path, ctx):
    router, _ = _router(tmp_path, [GOOD])
    res = await sd.draft_spec(router, ctx, None, smoke=False)
    assert res.ok and res.backend == "none" and res.metrics_found == []


# ---------------------------------------------------- router rules still apply


async def test_spend_cap_stops_drafting(tmp_path, ctx, backend, monkeypatch):
    monkeypatch.setenv("GF_SPEND_CAP_USD", "0.0001")
    router, calls = _router(tmp_path, [GOOD])
    with pytest.raises(budget.BudgetExceeded):
        await sd.draft_spec(router, ctx, backend)
    assert calls == []  # refused before any call was made


async def test_a_repeated_draft_is_served_from_the_cache(tmp_path, ctx, backend):
    router, calls = _router(tmp_path, [GOOD])
    await sd.draft_spec(router, ctx, backend)
    again = await sd.draft_spec(router, ctx, backend)
    assert len(calls) == 1 and again.ok
    assert again.cost_usd == 0 and again.fresh_cost_usd > 0  # free now, and the fair cost is still reported


# ---------------------------------------------------------- compare and diff


def test_knob_recall_against_the_hand_written_spec():
    draft = {"alpha": {"layer": "config", "default": "1.0"}, "beta": {"layer": "workload", "default": "0.7"},
             "num_rows": {"layer": "dataset", "default": "1000"}, "CACHE": {"layer": "environment", "default": "off"},
             "extra_flag": {"layer": "config", "default": "1"}}
    c = sd.compare_knobs(draft, TOY_HAND)
    assert set(c.found) == {"alpha", "beta", "num_rows", "CACHE"}
    assert "gamma" in c.missing and "threads" in c.missing and len(c.missing) == 6
    assert c.extra == ["extra_flag"]
    assert c.recall == pytest.approx(0.4)
    assert c.default_diffs == {"beta": ("0.5", "0.7")} and c.layer_diffs == {"beta": ("config", "workload")}
    assert c.default_match == 3 and c.layer_match == 3


def test_recall_ignores_dashes_and_case_and_numeric_defaults(tmp_path):
    hand = tmp_path / "hand.yaml"
    hand.write_text("name: h\nknobs:\n  batch_size: {layer: config, default: '32'}\n  lr: {layer: config, default: 0.05}\n")
    c = sd.compare_knobs({"--Batch-Size": {"layer": "config", "default": "32"}, "lr": {"layer": "config", "default": "0.05"}}, hand)
    assert c.recall == 1.0 and not c.default_diffs and not c.missing and not c.extra


async def test_report_lists_attempts_knobs_cost_and_recall(tmp_path, ctx, backend):
    router, _ = _router(tmp_path, [GOOD])
    res = await sd.draft_spec(router, ctx, backend)
    comp = sd.compare_knobs(res.spec_dict["knobs"], TOY_HAND)
    md = sd.report_markdown(res, "toy.yaml", comp)
    assert "verified: the spec built, ran" in md and "| 1 | super | ok |" in md
    assert "| alpha | config | `1.0` |" in md and "recall: 7/10" in md and "missing: noise, fault" in md
    assert "Nemotron cost" in md and "score, write_amp" in md


def test_diff_shows_what_a_person_changed(tmp_path):
    a, b = tmp_path / "a.yaml", tmp_path / "b.yaml"
    a.write_text("# draft\nname: t\nknobs:\n  alpha: {layer: config, default: '1.0'}\n")
    b.write_text("name: t\nknobs:\n  alpha: {layer: config, default: '2.0'}\n")
    d = sd.diff_specs(a, b)
    assert "-    default: '1.0'" in d and "+    default: '2.0'" in d
    assert sd.diff_specs(a, a) == "no differences\n"


def test_cli_diff_needs_no_key(tmp_path, capsys):
    from gapfinder.cli import main

    a, b = tmp_path / "a.yaml", tmp_path / "b.yaml"
    a.write_text("name: t\n")
    b.write_text("name: u\n")
    assert main(["spec-draft", "--diff", str(a), str(b)]) == 0
    assert "+name: u" in capsys.readouterr().out
