"""Claim extraction (Ultra): paper text in, grounded Claim[] out."""

from __future__ import annotations

from pydantic import BaseModel

from gapfinder.ingest.pdf import PaperText
from gapfinder.ledger.grounding import Grounder, GroundingReport
from gapfinder.ledger.schemas import Claim
from gapfinder.models.router import Router

CLAIM_PROMPT = """You are building a claim ledger for a reproduction study.

List every QUANTITATIVE claim the paper makes about its own experimental results:
numbers in prose, values in tables, and values or trends shown in figures.

For each claim:
- `quote`: copy the exact sentence or table cell it came from, verbatim, as it
  appears in the text below (no paraphrase; this is string-matched against the PDF).
- `page`: the number from the nearest preceding [[page N]] marker.
- `figure_or_table`: e.g. "Figure 6" or "Table 2"; null for prose-only claims.
- `type`: "absolute" (a value), "ratio" (X times / % better than a baseline) or
  "trend" (direction of change, no number).
- `conditions`: workload, dataset size, baseline, hardware -- whatever the claim depends on.
- `headline`: true for the 5-10 claims in the abstract/introduction/conclusion
  that the paper's contribution rests on.

Skip claims about other people's systems and purely analytical (model) numbers
unless the paper checks them experimentally. Number ids C1, C2, ...

PAPER:
{paper}
"""


class _Claims(BaseModel):
    claims: list[Claim]


async def extract_claims(router: Router, paper: PaperText, *, max_chars: int = 180_000) -> list[Claim]:
    text = paper.full_text[:max_chars]
    out = await router.structured("ultra", [{"role": "user", "content": CLAIM_PROMPT.format(paper=text)}], _Claims)
    return out.claims


def ground_claims(paper: PaperText, claims: list[Claim]) -> GroundingReport:
    g = Grounder(paper.full_text, pages={p.number: p.text for p in paper.pages})
    return g.check_claims(claims)
