"""The paper-year environment knob (gapfinder/env_year.py): which versions, from PyPI's upload dates."""

import json
from datetime import date

from gapfinder.env_year import first_after, install_command, paper_date, paper_year_pins, parse_freeze, version_at


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


def test_a_release_without_a_wheel_for_this_python_is_not_pinned():
    """Old wheels declare no requires_python: tensorflow 1.7 has cp36 wheels and none for 3.7. A compiled release's
    source archive doesn't count (it would build against 3.7), a pure package's does, and when nothing before the
    date installs, the first release after it within NEAREST_DAYS is the era's package."""
    def rel(day, *names):
        return [{"upload_time": f"{day}T00:00:00", "requires_python": None, "filename": n} for n in names]

    releases = {"1.7.0": rel("2018-03-29", "tensorflow-1.7.0-cp36-cp36m-manylinux1_x86_64.whl"),
                "1.13.1": rel("2019-02-26", "tensorflow-1.13.1-cp37-cp37m-manylinux1_x86_64.whl"),
                "1.5.0": rel("2018-01-26", "tensorflow-1.5.0-cp36-cp36m-manylinux1_x86_64.whl",
                             "tensorflow-1.5.0.tar.gz")}
    assert version_at(releases, date(2018, 4, 1), "3.7.17") is None  # 1.5.0's source archive would be compiled
    assert version_at(releases, date(2018, 4, 1), "3.6.9") == "1.7.0"
    assert first_after(releases, date(2018, 4, 1), "3.7.17") is None  # 1.13.1 is ten months later
    releases["1.9.0"] = rel("2018-07-10", "tensorflow-1.9.0-cp37-cp37m-manylinux1_x86_64.whl")
    releases["1.10.0"] = rel("2018-08-08", "tensorflow-1.10.0-cp37-cp37m-manylinux1_x86_64.whl")
    assert first_after(releases, date(2018, 4, 1), "3.7.17") == ("1.9.0", date(2018, 7, 10))
    pure = {"0.4": rel("2018-01-02", "pkg-0.4.tar.gz"), "0.5": rel("2018-05-01", "pkg-0.5-py3-none-any.whl")}
    assert version_at(pure, date(2018, 4, 1), "3.7.17") == "0.4"
    old = {"1.5.0": rel("2010-08-31", "numpy-1.5.0.tar.gz", "numpy-1.5.0-win32-superpack-python2.6.exe"),
           "1.14.5": rel("2018-06-12", "numpy-1.14.5-cp37-cp37m-manylinux1_x86_64.whl", "numpy-1.14.5.zip")}
    assert version_at(old, date(2018, 4, 1), "3.7.17") is None  # later platform wheels mark it compiled
    old["0.9"] = rel("2010-01-02", "pure-0.9.tar.gz", "pure-0.9.win32.exe")
    assert version_at({"0.9": old["0.9"]}, date(2018, 4, 1), "3.7.17") == "0.9"  # an installer alone doesn't
    assert first_after(old, date(2018, 4, 1), "3.7.17") == ("1.14.5", date(2018, 6, 12))
