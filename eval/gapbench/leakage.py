"""Leakage check: no task may hand agents its answer.

    python eval/gapbench/leakage.py            # all tasks; exit 1 on any leak
    python eval/gapbench/leakage.py --answers eval/gapbench/sealed   # answers kept outside the task folders

For every hidden knob=value of a task, flag:
  * `--knob value`, `knob=value`, `knob: value` or `knob value` anywhere in
    paper.md or the artifact's files;
  * the knob name and the value within 60 characters of each other in paper.md.
stated_code_differs tasks are exempt from the paper.md checks: stating the
value in the paper is the point of that task type. They are still checked
against the artifact.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

GB = Path(__file__).resolve().parent


def leaks(text: str, knob: str, value: str, near: bool) -> list[str]:
    k, v = re.escape(knob), re.escape(str(value))
    found = []
    for pat in (rf"--{k}[\s=]+{v}\b", rf"\b{k}\s*[=:]\s*['\"]?{v}\b", rf"\b{k}\s+{v}\b"):
        found += [m.group(0) for m in re.finditer(pat, text, re.IGNORECASE)]
    if near:
        for m in re.finditer(rf"\b{k}\b", text, re.IGNORECASE):
            window = text[max(0, m.start() - 60): m.end() + 60]
            if re.search(rf"(?<![\w.]){v}(?![\w.])", window):
                found.append(window.replace("\n", " "))
    return found


def check_task(task_dir: Path, answers_dir: Path | None = None) -> list[str]:
    """`answers_dir` holds <task>/answer.json for tasks whose answers live outside the task folder."""
    answer_file = (answers_dir / task_dir.name if answers_dir else task_dir) / "answer.json"
    answer = json.loads(answer_file.read_text(encoding="utf-8"))
    import yaml

    task = yaml.safe_load((task_dir / "task.yaml").read_text(encoding="utf-8"))
    paper = (task_dir / "paper.md").read_text(encoding="utf-8")
    artifact = GB / "artifacts" / task["family"]
    problems = []
    for knob, value in answer["hidden"].items():
        if answer["type"] != "stated_code_differs":
            problems += [f"{task_dir.name}: paper.md: {hit!r}" for hit in leaks(paper, knob, value, near=True)]
        for f in artifact.rglob("*"):
            if f.is_file() and f.suffix in {".py", ".md", ".txt", ".yaml", ".yml", ".sh", ".json", ".cfg", ".ini"}:
                problems += [f"{task_dir.name}: {f.relative_to(GB)}: {hit!r}"
                             for hit in leaks(f.read_text(encoding="utf-8", errors="replace"), knob, value, near=False)]
    return problems


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("task_dirs", nargs="*", type=Path)
    ap.add_argument("--answers", type=Path, help="directory with <task>/answer.json (e.g. eval/gapbench/sealed)")
    args = ap.parse_args()
    dirs = args.task_dirs or sorted(
        p for p in (GB / "tasks").iterdir()
        if ((args.answers / p.name) if args.answers else p).joinpath("answer.json").exists())
    all_problems = [p for d in dirs for p in check_task(d, args.answers)]
    for p in all_problems:
        print("LEAK", p)
    print(f"{len(dirs)} tasks checked, {len(all_problems)} leaks")
    sys.exit(1 if all_problems else 0)
