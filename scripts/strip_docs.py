"""Copy a repository without its documentation: the "no README" arm of the MC Dropout case.

    .venv/Scripts/python scripts/strip_docs.py <repo> <out>

Removes every `README*` / `readme*` file (any depth, any case) and every `docs` directory, and the
`.git` history, then lists what it removed and which other prose files remain (CHANGELOG, *.md, *.rst,
*.txt outside data folders), so the person running the arm can judge whether the documentation really
is gone. Then run `gapfinder ledger <paper> --repo <out> ...` on the stripped copy.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

PROSE_EXT = {".md", ".rst", ".txt", ".markdown"}


def is_doc(path: Path) -> bool:
    return path.is_file() and path.name.lower().startswith("readme")


def strip_docs(src: Path, dest: Path) -> dict:
    """Copy `src` to `dest` (which must not exist) minus README*, docs/ and .git. Returns what happened."""
    src, dest = Path(src).resolve(), Path(dest).resolve()
    if not src.is_dir():
        raise SystemExit(f"{src} is not a directory")
    if dest.exists():
        raise SystemExit(f"{dest} already exists; pick a new output folder")
    if dest == src or src in dest.parents:
        raise SystemExit("the output folder must be outside the repository")
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns(".git"))
    removed_files, removed_dirs = [], []
    for p in sorted(dest.rglob("*"), key=lambda q: len(q.parts)):  # parents first
        if not p.exists():
            continue  # inside a docs/ directory already removed
        rel = p.relative_to(dest).as_posix()
        if p.is_dir() and p.name.lower() == "docs":
            removed_dirs.append(rel + "/")
            shutil.rmtree(p)
        elif is_doc(p):
            removed_files.append(rel)
            p.unlink()
    remaining = sorted(p.relative_to(dest).as_posix() for p in dest.rglob("*")
                       if p.is_file() and p.suffix.lower() in PROSE_EXT)
    return {"removed_files": removed_files, "removed_dirs": removed_dirs, "remaining_prose": remaining}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", help="local path of the repository clone")
    ap.add_argument("out", help="new folder for the stripped copy")
    args = ap.parse_args(argv)
    r = strip_docs(Path(args.repo), Path(args.out))
    for rel in r["removed_dirs"] + r["removed_files"]:
        print(f"removed {rel}")
    if not (r["removed_dirs"] or r["removed_files"]):
        print("removed nothing: the repository has no README* or docs/")
    if r["remaining_prose"]:
        print("prose files still present (check them): " + ", ".join(r["remaining_prose"]))
    print(f"wrote {Path(args.out).resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
