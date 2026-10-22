"""Plan F5: the paper-era code for a repository that starts after its paper, and the reason when there is none.

pygcn's repository was created 13 months after its paper and VGAE's 7 months after: no commit predates the paper,
so the era knob was silently dropped. The code as first published (the first commit) is the nearest era code."""

from datetime import date

import gapfinder.env_year as ey


def _fake(history: list[tuple[str, str]]):
    """GitHub's commits API over a history [(sha, ISO date)], newest first."""
    def github(url, timeout=30):
        rows = [{"sha": s, "commit": {"committer": {"date": d + "T00:00:00Z"}, "message": f"commit {s}"}} for s, d in history]
        if "until=" in url:
            until = url.split("until=")[1][:10]
            rows = [r for r in rows if r["commit"]["committer"]["date"][:10] < until]
            return rows[:1]
        import re

        m = re.search(r"[?&]page=(\d+)", url)
        page = int(m.group(1)) if m else 1
        return rows[(page - 1) * 100: page * 100]
    return github


def test_the_last_commit_before_the_paper(monkeypatch):
    monkeypatch.setattr(ey, "_github", _fake([("c3", "2019-06-01"), ("c2", "2018-03-01"), ("c1", "2018-01-01")]))
    era, why = ey.paper_era_commit("https://github.com/o/r", "c3", date(2018, 4, 1))
    assert era["sha"] == "c2" and era["kind"] == "before" and why == ""


def test_a_repository_younger_than_its_paper_gets_its_first_commit(monkeypatch):
    monkeypatch.setattr(ey, "_github", _fake([("c3", "2018-02-01"), ("c2", "2017-12-01"), ("c1", "2017-10-26")]))
    era, why = ey.paper_era_commit("https://github.com/o/r", "c3", date(2016, 9, 9))
    assert era["sha"] == "c1" and era["kind"] == "first"


def test_no_era_knob_says_why(monkeypatch):
    monkeypatch.setattr(ey, "_github", _fake([("c1", "2017-10-26")]))
    era, why = ey.paper_era_commit("https://github.com/o/r", "c1", date(2016, 9, 9))
    assert era is None and "first" in why
    monkeypatch.setattr(ey, "_github", _fake([("c2", "2019-01-01"), ("c1", "2016-01-01")]))
    era, why = ey.paper_era_commit("https://github.com/o/r", "c1", date(2018, 1, 1))
    assert era is None and "already the last one before" in why

    def broken(url, timeout=30):
        raise OSError("offline")
    monkeypatch.setattr(ey, "_github", broken)
    era, why = ey.paper_era_commit("https://github.com/o/r", "c1", date(2018, 1, 1))
    assert era is None and "could not be read" in why
