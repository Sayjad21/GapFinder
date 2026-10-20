"""The paper-year environment knob (gapfinder/env_year.py): which versions, from PyPI's upload dates."""

import json
from datetime import date

from gapfinder.env_year import install_command, paper_date, paper_year_pins, parse_freeze, version_at


def _rel(when, py=None):
    return [{"upload_time": f"{when}T10:00:00", "requires_python": py}]


RELEASES = {"0.20.0": _rel("2018-09-26"), "0.21.0": _rel("2019-05-10"), "0.22rc1": _rel("2019-11-20"),
            "0.22": _rel("2019-12-03"), "1.0": _rel("2021-09-24", ">=3.7")}


def test_version_at_takes_the_newest_final_release_before_the_date():
    assert version_at(RELEASES, date(2019, 12, 1), "3.6.9") == "0.21.0"  # 0.22rc1 is a pre-release
    assert version_at(RELEASES, date(2022, 1, 1), "3.6.9") == "0.22"  # 1.0 needs Python 3.7
    assert version_at(RELEASES, date(2022, 1, 1), "3.8.10") == "1.0"
    assert version_at(RELEASES, date(2018, 1, 1), "3.8.10") is None


def test_paper_date_from_the_arxiv_month():
    assert paper_date("1912.01703") == date(2020, 1, 1) and paper_date("1803.03467v4") == date(2018, 4, 1)
    assert paper_date(None, "2017-06-30") == date(2017, 6, 30) and paper_date(None) is None


def test_pins_only_where_the_installed_version_is_newer(tmp_path):
    (tmp_path / "scikit-learn.json").write_text(json.dumps({"releases": RELEASES}), encoding="utf-8")
    (tmp_path / "numpy.json").write_text(json.dumps({"releases": {"1.16.0": _rel("2019-01-14")}}), encoding="utf-8")
    pins, why = paper_year_pins(["sklearn", "numpy", "torch_scatter", "absent"], {"scikit-learn": "1.3.2",
                                "numpy": "1.16.0"}, date(2019, 12, 1), "3.7.3", cache=tmp_path)
    assert pins == {"scikit-learn": "0.21.0"}
    assert "already" in why["numpy"] and "compiled" in why["torch-scatter"] and "not installed" in why["absent"]
    cmd = install_command(pins)
    assert '"scikit-learn==0.21.0"' in cmd and '--no-deps --target "${GF_PY_ROOT:-/opt/gf_py}/scikit_learn"' in cmd


def test_parse_freeze():
    py, pk = parse_freeze("GF_PY 3.7.17\nGF_FREEZE numpy==1.21.6\nGF_FREEZE tensorflow==1.15.5\nGF_FREEZE -e git+x\n")
    assert py == "3.7.17" and pk == {"numpy": "1.21.6", "tensorflow": "1.15.5"}
