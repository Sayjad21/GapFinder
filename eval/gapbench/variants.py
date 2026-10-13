"""Out-of-space variants: older, buggy versions of a GapBench artifact, built as patched copies.

The artifacts under eval/gapbench/artifacts never change. A variant is a text patch applied to a fresh
copy in a temporary directory, used only by the generator and the task builder to make the paper's
numbers. So GapFinder's repo map can't see a switch for the bug (an environment variable in the artifact
would show up in its env-var list), and cached model answers for the artifacts stay valid.

Each variant passed the generator's checks in a dry run: the gap is well over 3 noise bands, and no
single setting GapFinder can test reproduces both claims (eval/gapbench/gen_tasks.py, `Screen.rivals`).
Rejected candidates, for the record:
- rlbench (any): the held-out claim min_reward is noisier than its own median (band ~90 on ~62), so it
  rules nothing out, and some single setting mimics every evaluation or reporting bug tried (missing
  reset, exploration left on, an evaluation step cap, a reward-unit bug); a best-seed reporting bug
  moves the mean by under 2 bands (capped at 200).
- mlbench test-set epoch selection: under 3 noise bands from the near-chance default.
- mlbench dropping only the x400 column: some single setting reproduces both claims.
"""

from __future__ import annotations

import copy
import shutil
from pathlib import Path

GB = Path(__file__).resolve().parent

#: family -> variant -> (what went wrong, file, [(old, new)] exact replacements, each found once)
VARIANTS: dict[str, dict[str, tuple[str, str, list[tuple[str, str]]]]] = {
    "mlbench": {
        "drop_scaled": (
            "data bug: an older loader read only the unit-scale feature columns",
            "train.py",
            [("    k = int(a.split * a.n)\n",
              "    X = [[v for v, s in zip(r, SCALES) if s <= 10] for r in X]\n    k = int(a.split * a.n)\n")],
        ),
        "clip5": (
            "preprocessing bug: a leftover outlier filter clipped every feature to [-5, 5]",
            "train.py",
            [("    k = int(a.split * a.n)\n",
              "    X = [[max(-5.0, min(5.0, v)) for v in r] for r in X]\n    k = int(a.split * a.n)\n")],
        ),
    },
}


def describe(family: str, variant: str) -> str:
    return VARIANTS[family][variant][0]


def build(family: str, variant: str, dest: Path) -> Path:
    """A patched copy of the artifact under `dest`; returns its directory."""
    _, rel, patches = VARIANTS[family][variant]
    out = Path(dest) / f"{family}-{variant}"
    if out.exists():
        return out
    shutil.copytree(GB / "artifacts" / family, out, ignore=shutil.ignore_patterns("out", "__pycache__"))
    f = out / rel
    s = f.read_text(encoding="utf-8")
    for old, new in patches:
        if s.count(old) != 1:
            raise ValueError(f"variant {family}/{variant}: patch target found {s.count(old)} times in {rel}")
        s = s.replace(old, new)
    f.write_text(s, encoding="utf-8", newline="\n")
    return out


def spec_for(spec, family: str, variant: str, dest: Path):
    """A copy of the harness spec whose base is the buggy copy (same knobs, same command)."""
    s = copy.deepcopy(spec)
    s.base = "local:" + str(build(family, variant, dest))
    return s
