"""v1.1 value coverage: the true value has to be among the values tested (14 of v1.0's 18 blind misses
never tested it)."""

from gapfinder.ingest.repo_map import build_repo_map
from gapfinder.sandbox.spec import HarnessSpec, Knob
from gapfinder.search.hypotheses import coverage_values, fill_choices, generate_values, LADDER


def test_argparse_choices_are_read_from_the_code(tmp_path):
    (tmp_path / "train.py").write_text(
        'p.add_argument("--normalize", choices=["none", "zscore", "minmax"], default="none")\n'
        'p.add_argument("--k", type=int, choices=(1, 5, 10),\n'
        '               default=5)\n'
        'p.add_argument("--lr", type=float, default=0.05)\n', encoding="utf-8")
    flags = {f.name: f for f in build_repo_map(tmp_path).flags}
    assert flags["--normalize"].choices == ["none", "zscore", "minmax"]
    assert flags["--k"].choices == ["1", "5", "10"] and flags["--k"].default == "5"
    assert flags["--lr"].choices is None


def test_every_choice_of_a_categorical_knob_is_a_candidate():
    k = Knob(layer="config", default="none", choices=["none", "zscore", "minmax"])
    assert coverage_values(k) == ["zscore", "minmax"]  # minmax was never tested in 3 v1.0 decoy runs


def test_the_ladder_reaches_far_values_early():
    vals = generate_values("500", LADDER)
    assert vals[:2] == ["50", "5000"] and "10" in vals[:6]  # MC Dropout: epochx 500 -> 10
    assert "600" in generate_values("1200", LADDER)[:4]  # gen-06: n 1200 -> 600


def test_choices_are_filled_into_a_spec_from_the_repo_map(tmp_path):
    (tmp_path / "train.py").write_text('p.add_argument("--normalize", choices=["none", "zscore"], default="none")\n',
                                       encoding="utf-8")
    spec = HarnessSpec(name="t", base=f"local:{tmp_path}", run={"command": "python train.py --normalize {normalize}"},
                       knobs={"normalize": {"layer": "config", "default": "none"}})
    assert fill_choices(spec, build_repo_map(tmp_path).flags) == 1
    assert spec.knobs["normalize"].choices == ["none", "zscore"]


def test_fractions_stay_below_one():
    k = Knob(layer="config", default="0.5")
    vals = coverage_values(k)
    assert all(0 <= float(v) < 1 for v in vals) and "0.95" in vals and "0.05" in vals and "0.0" in vals  # never 5


def test_a_multiplier_knob_gets_the_literal_factors_first(tmp_path):
    (tmp_path / "experiment.py").write_text(
        "parser.add_argument('--epochx','-e', default=500, type=int, help='Multiplier for the number of epochs for training.')\n"
        "parser.add_argument('--hidden', '-nh', default=2, type=int, help='Number of hidden layers for the neural net')\n",
        encoding="utf-8")
    spec = HarnessSpec(name="t", base=f"local:{tmp_path}", run={"command": "python experiment.py"},
                       knobs={"epochx": {"layer": "config", "default": "500"}, "hidden": {"layer": "config", "default": "2"}})
    fill_choices(spec, build_repo_map(tmp_path).flags)
    assert spec.knobs["epochx"].multiplier and not spec.knobs["hidden"].multiplier
    assert coverage_values(spec.knobs["epochx"])[:4] == ["1", "2", "5", "10"]  # MC Dropout's epochx=10, by construction
    assert "1" in coverage_values(spec.knobs["hidden"])[:3]  # one hidden layer, the paper's setting
