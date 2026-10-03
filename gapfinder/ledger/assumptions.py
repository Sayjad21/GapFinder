"""Assumption space (Ultra): setup section + repo map + relevant files -> ranked Assumption[]."""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import BaseModel

from gapfinder.ingest.pdf import PaperText
from gapfinder.ingest.repo_map import RepoMap
from gapfinder.ledger.grounding import Grounder, GroundingReport
from gapfinder.ledger.schemas import Assumption, AssumptionStatus, Claim
from gapfinder.models.router import Router

ASSUMPTION_PROMPT = """You are enumerating the experimental assumptions behind a paper's results,
so that a reproduction gap can be searched knob by knob.

An assumption is any experimental condition that could change the measured
numbers WITHOUT editing the algorithm: build options, configuration flags,
dataset size/distribution, workload mix, warm-up, run length, environment
(threads, disk, page cache, CPU frequency).

For each knob:
- `knob`: the exact flag / option / env var name as it appears in the code.
- `layer`: build | dataset | config | workload | environment.
- `paper_value`: the value the paper states, or "unstated".
- `code_default`: the default in the repo, from the repo map.
- `status`: "unstated"; "stated_matches" (paper value == code default);
  or "stated_code_differs" (the paper states a value the default does not
  match -- a paper-artifact inconsistency, flag these).
- `candidate_values`: 1-3 plausible values to try, prioritising the paper's
  stated value and values used in other scripts in the repo.
- `evidence`: for paper evidence use kind "paper", ref "p.N", and a verbatim
  quote; for code evidence use kind "code", ref "path:line" exactly as listed
  in the repo map. Evidence that is not verbatim will be discarded.
- `prior_score`: 0-1, how likely this knob explains a gap in the claims below.
- `affects_claims`: claim ids.

Return the 30 most promising, highest prior first. Ids A1, A2, ...

CLAIMS:
{claims}

PAPER EXPERIMENTAL SETUP:
{setup}

REPO MAP:
{repo_map}

RELEVANT FILES:
{files}
"""

SETUP_HEADINGS = r"^\s*\d+(\.\d+)?\s+(experimental (setup|evaluation)|evaluation|experiments)\s*$"


class _Assumptions(BaseModel):
    assumptions: list[Assumption]


def relevant_files(rm: RepoMap, claims: list[Claim], limit: int = 20, max_bytes: int = 12_000) -> str:
    """Pick the files most likely to matter: run scripts, build files, flag-heavy sources."""
    flag_counts: dict[str, int] = {}
    for f in rm.flags:
        flag_counts[f.file] = flag_counts.get(f.file, 0) + 1
    words = {w.lower() for c in claims for w in re.findall(r"[a-zA-Z_]{4,}", c.metric + " " + " ".join(c.conditions.values()))}
    def score(path: str) -> float:
        s = flag_counts.get(path, 0) * 2 + (10 if path in rm.scripts else 0) + (8 if path in rm.build_files else 0)
        s += sum(3 for w in words if w in path.lower())
        return s
    ranked = sorted({*flag_counts, *rm.scripts, *rm.build_files}, key=score, reverse=True)[:limit]
    chunks = []
    for rel in ranked:
        try:
            text = (rm.root / rel).read_text(encoding="utf-8", errors="replace")[:max_bytes]
        except OSError:
            continue
        numbered = "\n".join(f"{i:5d}| {line}" for i, line in enumerate(text.splitlines(), 1))
        chunks.append(f"=== {rel} ===\n{numbered}")
    return "\n\n".join(chunks)


async def build_assumption_space(router: Router, paper: PaperText, rm: RepoMap, claims: list[Claim]) -> list[Assumption]:
    setup = paper.section(SETUP_HEADINGS, max_chars=25_000) or paper.full_text[:25_000]
    prompt = ASSUMPTION_PROMPT.format(
        claims="\n".join(f"{c.id}: {c.metric} = {c.reported_value} {c.unit or ''} ({c.figure_or_table}) {c.conditions}" for c in claims),
        setup=setup,
        repo_map=rm.summary(max_files=300, max_flags=500),
        files=relevant_files(rm, claims),
    )
    out = await router.structured("ultra", [{"role": "user", "content": prompt}], _Assumptions)
    return _fill_defaults(out.assumptions, rm)


def _fill_defaults(assumptions: list[Assumption], rm: RepoMap) -> list[Assumption]:
    """Code defaults come from the repo map, not the model, whenever we can find the flag."""
    fixed = []
    for a in assumptions:
        flags = rm.find_flag(a.knob)
        if flags and flags[0].default is not None:
            a = a.model_copy(update={"code_default": flags[0].default})
        fixed.append(a)
    return sorted(fixed, key=lambda a: a.prior_score, reverse=True)


def ground_assumptions(paper: PaperText, repo_root: Path, assumptions: list[Assumption]) -> GroundingReport:
    g = Grounder(paper.full_text, repo_root, pages={p.number: p.text for p in paper.pages})
    return g.check_assumptions(assumptions)


def inconsistencies(assumptions: list[Assumption]) -> list[Assumption]:
    return [a for a in assumptions if a.status == AssumptionStatus.stated_code_differs.value]
