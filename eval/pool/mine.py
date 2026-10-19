"""Mine a pool of blind cases from GitHub fix commits (plan item 1, docs/CONTEXT_v11.md section 7).

    python eval/pool/mine.py mine          # search, filter, seal; prints counts only
    python eval/pool/mine.py list          # the public candidates (repo, parent commit, arXiv id), no answers

A case is a research repository with a commit whose message says it fixes a setting or code to match the paper
("match the paper", "fix default", "wrong hyperparameter", ...). The commit before the fix is the blind input; the
fix commit (its message and diff) is the answer.
- The answer is written to the sealed folder by this script. The runner never reads it before a run is committed,
  and never browses the repository's history past the parent commit.
- The public list has the repository, the parent commit and the paper's arXiv id: nothing about the fix.
- The cause type (setting value, true/false switch, other code) is derived from the diff and sealed with it, so
  rates can be reported per type after scoring.
- A candidate is a case only after its gap is measured: the numbers at the parent and at the fix must differ
  beyond noise (a later step, with the automatic harness). Many "match the paper" commits change nothing measurable.

Commit mining is an established way to build bug datasets (BugHunter, Ray et al.). GitHub's search API is used
without a token (10 searches a minute); diffs and READMEs come from github.com and raw.githubusercontent.com, which
don't count against the API limit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "eval" / "pool" / "candidates.json"
SEALED = ROOT / "eval" / "pool" / "sealed"  # answers: never opened by the runner before scoring

# phrases authors and contributors use when they bring code in line with the paper
QUERIES = [
    '"match the paper"', '"to match paper"', '"as in the paper"', '"same as the paper"', '"consistent with the paper"',
    '"reproduce the paper"', '"reproduce the results"', '"reproduce paper results"', '"paper setting"',
    '"hyperparameters in the paper"', '"hyperparameters from the paper"', '"according to the paper"',
    '"fix default" hyperparameter', '"wrong hyperparameter"', '"fix hyperparameter"', '"correct hyperparameter"',
    '"update default" paper', '"fix learning rate"', '"fix config" paper', '"default settings" paper',
]
UA = {"User-Agent": "gapfinder-pool-miner", "Accept": "application/vnd.github+json"}
CODE_EXT = (".py", ".yaml", ".yml", ".json", ".sh", ".cfg", ".ini", ".toml", ".txt")
MAX_CHANGED_LINES = 40


def _get(url: str, timeout: float = 60, api: bool = False) -> bytes | None:
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=UA if api else {"User-Agent": UA["User-Agent"]})
            return urllib.request.urlopen(req, timeout=timeout).read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):  # rate limit: wait it out
                time.sleep(65)
                continue
            if e.code == 404:
                return None
            time.sleep(5)
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            time.sleep(10)
    return None


def search(q: str, pages: int = 3) -> list[dict]:
    out = []
    for page in range(1, pages + 1):
        url = "https://api.github.com/search/commits?per_page=100&page=%d&q=%s" % (page, urllib.parse.quote(q))
        raw = _get(url, api=True)
        time.sleep(7)  # 10 searches a minute without a token
        if raw is None:
            break
        items = json.loads(raw).get("items", [])
        out += items
        if len(items) < 100:
            break
    return out


def diff_stats(diff: str) -> dict:
    files = re.findall(r"^diff --git a/(\S+) b/", diff, re.M)
    added = [l for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]
    removed = [l for l in diff.splitlines() if l.startswith("-") and not l.startswith("---")]
    return {"files": files, "changed": len(added) + len(removed), "added": added, "removed": removed}


def cause_type(st: dict) -> str:
    """setting: only numbers or strings change in config files or flag defaults; switch: a True/False flips; code."""
    pairs = list(zip(st["removed"], st["added"]))
    if not pairs:
        return "code"
    def skeleton(line: str) -> str:
        return re.sub(r"(?i)\b(true|false)\b", "B", re.sub(r"[-+]?\d+(\.\d+)?(e[-+]?\d+)?", "N", line[1:])).strip()
    if all(skeleton(a) == skeleton(b) for a, b in pairs) and len(st["removed"]) == len(st["added"]):
        if any(re.search(r"(?i)\b(true|false)\b", a) for a, _ in pairs) and not any(
                re.search(r"\d", a) != re.search(r"\d", b) for a, b in pairs):
            return "switch"
        return "setting"
    return "code"


_ARXIV = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", re.I)


def mine() -> None:
    SEALED.mkdir(parents=True, exist_ok=True)
    seen, public = set(), []
    per_repo: dict[str, int] = {}
    counts = {"hits": 0, "merge_or_dup": 0, "diff_missing": 0, "not_code_or_too_big": 0, "no_arxiv": 0, "kept": 0}
    for q in QUERIES:
        for it in search(q):
            counts["hits"] += 1
            repo, sha = it["repository"]["full_name"], it["sha"]
            if len(it.get("parents") or []) != 1 or sha in seen or per_repo.get(repo, 0) >= 2:
                counts["merge_or_dup"] += 1
                continue
            seen.add(sha)
            parent = it["parents"][0]["sha"]
            raw = _get(f"https://github.com/{repo}/commit/{sha}.diff")
            time.sleep(1)
            if raw is None:
                counts["diff_missing"] += 1
                continue
            diff = raw.decode("utf-8", "replace")
            st = diff_stats(diff)
            code_files = [f for f in st["files"] if f.endswith(CODE_EXT) and "readme" not in f.lower()]
            if not code_files or st["changed"] > MAX_CHANGED_LINES or st["changed"] == 0:
                counts["not_code_or_too_big"] += 1
                continue
            readme = None
            for name in ("README.md", "readme.md", "README.rst", "README"):
                readme = _get(f"https://raw.githubusercontent.com/{repo}/{parent}/{name}")
                if readme:
                    break
            m = _ARXIV.search(readme.decode("utf-8", "replace")) if readme else None
            if not m:
                counts["no_arxiv"] += 1
                continue
            cid = "p" + hashlib.sha1(sha.encode()).hexdigest()[:8]
            d = SEALED / cid
            d.mkdir(exist_ok=True)
            (d / "fix.diff").write_text(diff, encoding="utf-8")
            (d / "meta.json").write_text(json.dumps({
                "repo": repo, "fix_commit": sha, "parent": parent, "message": it["commit"]["message"],
                "query": q, "cause_type": cause_type(st), "changed_lines": st["changed"], "files": st["files"]},
                indent=1), encoding="utf-8")
            public.append({"id": cid, "repo": f"https://github.com/{repo}", "commit": parent, "arxiv": m.group(1)})
            per_repo[repo] = per_repo.get(repo, 0) + 1
            counts["kept"] += 1
        PUBLIC.write_text(json.dumps(public, indent=1), encoding="utf-8")  # after every query: resumable output
        print(f"after {q!r}: " + ", ".join(f"{k} {v}" for k, v in counts.items()), flush=True)
    types: dict[str, int] = {}
    for p in SEALED.glob("*/meta.json"):
        t = json.loads(p.read_text(encoding="utf-8"))["cause_type"]
        types[t] = types.get(t, 0) + 1
    print(f"\n{counts['kept']} candidates (public list: {PUBLIC}); sealed cause types: {types}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("mine")
    sub.add_parser("list")
    a = ap.parse_args()
    if a.cmd == "mine":
        mine()
    else:
        for c in json.loads(PUBLIC.read_text(encoding="utf-8")):
            print(c["id"], c["repo"], c["commit"][:10], "arXiv", c["arxiv"])


if __name__ == "__main__":
    sys.exit(main())
