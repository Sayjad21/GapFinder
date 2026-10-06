"""Claim extraction (Ultra): paper text in, grounded Claim[] out."""

from __future__ import annotations

from pydantic import BaseModel

from gapfinder.ingest.pdf import PaperText
from gapfinder.ledger.grounding import Grounder, GroundingReport
from gapfinder.ledger.schemas import Claim
from gapfinder.models.router import Router

CLAIM_PROMPT = """You are building a claim ledger for a reproduction study.

List every claim the paper makes about its own experimental results that a
reproduction could check:
- numbers in prose and values in tables;
- values shown in figures;
- QUALITATIVE results the text states about a figure: which method or
  configuration is best on which workload, which setting the method chooses or
  converges to, orderings ("A outperforms B on X"), and trends ("latency falls
  as K rises"). These are often the claims a reproduction disagrees with, so
  never skip them because they have no number. Use type "trend" for them, and
  put a value in `reported_value` when the text gives one (e.g. a chosen K).
Give each distinct statement its own claim. Split a sentence that makes
several checkable statements into several claims.

For each claim:
- `quote`: copy the exact sentence or table cell it came from, verbatim, as it
  appears in the text below (no paraphrase; this is string-matched against the PDF).
- `page`: the number from the nearest preceding [[page N]] marker.
- `figure_or_table`: e.g. "Figure 6" or "Table 2"; null for prose-only claims.
- `type`: "absolute" (a value), "ratio" (X times / % better than a baseline) or
  "trend" (direction of change, no number).
- `conditions`: workload, dataset size, baseline, hardware -- whatever the claim depends on.
- `headline`: true for the 5-10 claims the paper's contribution rests on: those
  in the abstract, and the main results about the paper's primary figures.

Include what the paper says about its BASELINES as measured in its own
experiments (which baseline is best or worst on which workload, how they rank):
a reproduction re-measures those too. Skip only results quoted from other
papers, and purely analytical (model) numbers the paper never checks
experimentally. For table rows, quote the row exactly as the text prints it,
do not reformat numbers. Number ids C1, C2, ...

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
