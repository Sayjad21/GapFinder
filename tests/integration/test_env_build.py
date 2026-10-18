"""Environment builder (gapfinder/env_build.py): one command at a time, a failed command is rolled back."""

from gapfinder.env_build import NextStep, build_env, third_party_imports
from gapfinder.sandbox.backend import LocalBackend


def _repo(tmp_path):
    root = tmp_path / "repo"
    (root / "src").mkdir(parents=True)
    (root / "src" / "main.py").write_text("import argparse\nimport helper\nif __name__ == '__main__':\n    pass\n",
                                          encoding="utf-8")
    (root / "src" / "helper.py").write_text("import os\nimport toylib.core\n", encoding="utf-8")
    (root / "requirements.txt").write_text("toylib\n", encoding="utf-8")
    return root


def test_third_party_imports_follow_local_modules(tmp_path):
    assert third_party_imports(_repo(tmp_path)) == ["toylib"]


async def test_a_failed_command_is_rolled_back_and_the_recipe_keeps_the_good_ones(tmp_path):
    root = _repo(tmp_path)
    prompts = []
    answers = iter([NextStep(command="echo broken > toylib.py && exit 3", why="try"),
                    NextStep(command="mkdir -p src/toylib && touch src/toylib/__init__.py src/toylib/core.py",
                             why="provide the package")])

    class FakeRouter:
        meter = type("Meter", (), {"total_cost": lambda self: 0.0})()

        async def structured(self, tier, messages, schema):
            prompts.append(messages[0]["content"])
            return next(answers)

    res = await build_env(FakeRouter(), LocalBackend(tmp_path / "sbx"), root, image="python:3.12-slim", max_steps=4)
    assert res.ok, res.reason
    assert [s.ok for s in res.steps] == [False, True]
    assert res.recipe == ["mkdir -p src/toylib && touch src/toylib/__init__.py src/toylib/core.py"]
    assert "toylib" in prompts[0] and "FAIL $ echo broken" in prompts[1]
    assert not (tmp_path / "sbx" / "images" / res.checkpoint / "toylib.py").exists()  # the failed step's file


async def test_it_stops_when_the_model_gives_up(tmp_path):
    class FakeRouter:
        meter = type("Meter", (), {"total_cost": lambda self: 0.0})()

        async def structured(self, tier, messages, schema):
            return NextStep(give_up="needs a CUDA-only package")

    res = await build_env(FakeRouter(), LocalBackend(tmp_path / "sbx"), _repo(tmp_path), image="python:3.12-slim")
    assert not res.ok and "CUDA" in res.reason and res.steps == []


async def test_the_model_can_switch_the_base_image_and_the_recipe_keeps_only_the_final_images_commands(tmp_path):
    root = _repo(tmp_path)
    answers = iter([NextStep(command="true", why="a step on the first image"),
                    NextStep(switch_image="python:3.7-slim", why="this Python can't install toylib"),
                    NextStep(command="mkdir -p src/toylib && touch src/toylib/__init__.py src/toylib/core.py")])
    prompts = []

    class FakeRouter:
        meter = type("Meter", (), {"total_cost": lambda self: 0.0})()

        async def structured(self, tier, messages, schema):
            prompts.append(messages[0]["content"])
            return next(answers)

    res = await build_env(FakeRouter(), LocalBackend(tmp_path / "sbx"), root, image="python:3.12-slim", max_steps=4)
    assert res.ok and res.image == "python:3.7-slim"
    assert res.recipe == ["mkdir -p src/toylib && touch src/toylib/__init__.py src/toylib/core.py"]
    assert any(s.command.startswith("# switch base image python:3.12-slim -> python:3.7-slim") for s in res.steps)
    assert "python:3.12-slim" not in prompts[-1].split("this list instead:")[1].split("\n")[0]  # not offered again
