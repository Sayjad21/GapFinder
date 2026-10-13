from gapfinder.ingest.config_flow import flag_scales
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.hypotheses import mark_multipliers_from_flow


def test_a_flag_that_scales_epochs_is_a_multiplier(tmp_path):
    (tmp_path / "experiment.py").write_text(
        "import argparse\n"
        "parser = argparse.ArgumentParser()\n"
        "parser.add_argument('--epochx', default=500, type=int)\n"
        "parser.add_argument('--lr', default=0.01, type=float)\n"
        "args = parser.parse_args()\n"
        "epochs_multiplier = args.epochx\n"
        "n_epochs = 40\n"
        "step = args.lr * grad\n"
        "train(n_epochs=int(n_epochs * epochs_multiplier))\n", encoding="utf-8")
    sc = flag_scales(tmp_path)
    assert sc["epochx"] == ["n_epochs"] and sc["lr"] == ["grad"]
    spec = HarnessSpec(name="t", base=f"local:{tmp_path}", run={"command": "python experiment.py"},
                       knobs={"epochx": {"layer": "config", "default": "500"}, "lr": {"layer": "config", "default": "0.01"}})
    assert mark_multipliers_from_flow(spec, sc) == 1
    assert spec.knobs["epochx"].multiplier and spec.knobs["epochx"].scales == ["n_epochs"]
    assert not spec.knobs["lr"].multiplier  # lr x gradient is arithmetic, not a count multiplier
