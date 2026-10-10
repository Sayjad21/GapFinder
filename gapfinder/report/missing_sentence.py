"""The sentence the paper was missing: a model-drafted methods sentence for confirmed causes.

Only cards labelled Explained or Paper-artifact inconsistency qualify. For each, one Nemotron
Super call (through the router, so the cache and the spend cap apply) drafts the sentence the
paper should have contained and says where it fits in the paper's own setup paragraph. The
paragraph itself is chosen by code from the paper text, never by the model, so what the report
shows as "the paper's paragraph" is always verbatim paper text. Everything the model wrote is
marked as drafted. Off by default; nothing here posts anywhere.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from pydantic import BaseModel, Field

from gapfinder.models import budget

ELIGIBLE_LABELS = ("Explained", "Paper-artifact inconsistency")

MISSING_SENTENCE_PROMPT = """You help authors close a reproducibility gap in their paper.
A reproduction of the paper's artifact matched the paper's reported number only after one
setting was changed, and the checks (reverting the setting, held-out claims, evidence) passed.
Draft the single methods sentence the paper should have contained so a reader could have
reproduced the result, and say where it belongs in the paper's own setup paragraph.

Rules:
- State the setting and its value exactly as given in the evidence. Do not invent numbers,
  units, tools or reasons that are not in the evidence.
- One sentence, in the paper's own voice and tense, no mention of GapFinder or of any gap.
- Choose `insert_after`: 0 to put it before the paragraph's first sentence, or k to put it
  after sentence k of the numbered paragraph (1 <= k <= number of sentences).
- If the evidence does not pin down a value, write the sentence without the value rather than
  guessing."""

PROMPT_SHA256 = hashlib.sha256(MISSING_SENTENCE_PROMPT.encode("utf-8")).hexdigest()

_SETUP_WORDS = ("experimental setup", "experiment setup", "evaluation setup", "we use", "we used", "we set",
                "we configure", "default", "configured", "setup", "testbed", "hardware", "workload")
_SENT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\[\"'])")


class _Draft(BaseModel):
    sentence: str = Field(description="The drafted methods sentence")
    insert_after: int = Field(description="0 = before the first sentence, k = after sentence k")


def is_eligible(card: dict) -> bool:
    label = (card.get("attribution") or {}).get("confidence_label")
    return label in ELIGIBLE_LABELS and bool(card.get("changes"))


def split_sentences(paragraph: str) -> list[str]:
    return [s.strip() for s in _SENT_RE.split(" ".join(paragraph.split())) if s.strip()]


def _tokens(card: dict) -> set[str]:
    words: set[str] = set()
    for k, v in (card.get("changes") or {}).items():
        words |= {w for w in re.split(r"[^a-z0-9]+", f"{k} {v}".lower()) if len(w) > 2}
    return words


def find_setup_paragraph(paper, card: dict) -> tuple[str, int] | None:
    """The paper's setup paragraph for this card: (verbatim text, 1-based page), or None."""
    want = _tokens(card)
    best: tuple[float, str, int] | None = None
    for page in paper.pages:
        for raw in re.split(r"\n\s*\n", page.text):
            para = " ".join(raw.split())
            if len(para) < 200 or len(split_sentences(para)) < 2:
                continue
            low = para.lower()
            score = sum(2 for w in want if w in low) + sum(1 for w in _SETUP_WORDS if w in low)
            if score and (best is None or score > best[0]):
                best = (score, para, page.number)
    return (best[1], best[2]) if best else None


def _norm(k: str) -> str:
    return k.lower().lstrip("-").replace("-", "_")


def _evidence_text(card: dict, assumptions: list[dict]) -> str:
    t = card.get("target") or {}
    lines = [f"Claim {t.get('claim_id')}: {t.get('metric')}, paper value {t.get('paper_value')}",
             f"Naive gap {card.get('gap_before')} became {card.get('gap_after')} (noise band {card.get('band')})"]
    for k, v in card["changes"].items():
        lines.append(f"Setting changed: {k} = {v}")
        p = (card.get("plausibility") or {}).get(k)
        if p:
            lines.append(f"  evidence ({'supported' if p.get('supported') else 'unsupported'}): {p.get('reason')}")
        for a in assumptions:
            if _norm(str(a.get("knob", ""))) == _norm(k):
                lines.append(f"  paper says: {a.get('paper_value')}; code default: {a.get('code_default')}")
    for k, v in (card.get("counterfactual") or {}).items():
        lines.append(f"Reverting {k}: gap {v.get('gap_without')} ({'returned' if v.get('ok') else 'did not return'})")
    return "\n".join(lines)


async def draft_missing_sentences(report: dict, paper, router, assumptions: list[dict] | None = None) -> dict:
    """Add `missing_sentence` to each eligible card of `report` (a gap_report.json dict).

    Returns the meta block, also stored as report["missing_sentence_meta"]. Stops at the first
    spend-cap refusal and records the skipped cards; a card whose paper has no setup paragraph
    is skipped without a call.
    """
    assumptions = assumptions or []
    meta = {"model_drafted": True, "prompt_sha256": PROMPT_SHA256, "drafted": 0, "skipped": [], "cost_usd": 0.0}
    capped = False
    for card in report.get("claims", []):
        if not is_eligible(card):
            continue
        cid = (card.get("target") or {}).get("claim_id")
        if capped:
            meta["skipped"].append({"claim_id": cid, "reason": "spend cap"})
            continue
        found = find_setup_paragraph(paper, card)
        if not found:
            meta["skipped"].append({"claim_id": cid, "reason": "no setup paragraph found in the paper text"})
            continue
        paragraph, page = found
        sents = split_sentences(paragraph)
        numbered = "\n".join(f"{i}. {s}" for i, s in enumerate(sents, 1))
        user = (f"Evidence:\n{_evidence_text(card, assumptions)}\n\n"
                f"The paper's setup paragraph (page {page}), numbered by sentence:\n{numbered}")
        try:
            draft = await router.structured(
                "super", [{"role": "system", "content": MISSING_SENTENCE_PROMPT}, {"role": "user", "content": user}],
                _Draft)
        except budget.BudgetExceeded:
            capped = True
            meta["skipped"].append({"claim_id": cid, "reason": "spend cap"})
            continue
        sentence = " ".join(draft.sentence.split())
        if not sentence:
            meta["skipped"].append({"claim_id": cid, "reason": "empty draft"})
            continue
        card["missing_sentence"] = {
            "sentence": sentence, "paragraph": paragraph, "insert_after": max(0, min(draft.insert_after, len(sents))),
            "page": page, "model_drafted": True, "model": router.tiers["super"].model_id,
            "prompt_sha256": PROMPT_SHA256}
        meta["drafted"] += 1
    meta["cost_usd"] = round(router.meter.total_cost(), 6)
    report["missing_sentence_meta"] = meta
    return meta


_MD_MARK = "## The sentence the paper was missing"


async def add_to_run_dir(run_dir, paper, router, assumptions: list[dict] | None = None, repo: str | None = None) -> dict:
    """Add drafted sentences to a finished report in `run_dir`: gap_report.json, gap_report.md, issue_draft.md.

    Re-reads gap_report.json, so it works on any finished run. Returns the meta block. When no card
    got a sentence, the report is left as it was and no issue draft is written.
    """
    run_dir = Path(run_dir)
    js = run_dir / "gap_report.json"
    report = json.loads(js.read_text(encoding="utf-8"))
    for c in report.get("claims", []):  # re-running replaces earlier drafts
        c.pop("missing_sentence", None)
    meta = await draft_missing_sentences(report, paper, router, assumptions)
    js.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    md = run_dir / "gap_report.md"
    if md.exists():
        text = md.read_text(encoding="utf-8")
        if _MD_MARK in text:
            text = text[: text.index(_MD_MARK)].rstrip() + "\n"
        md.write_text(text + markdown_section(report), encoding="utf-8")
    if meta["drafted"]:
        (run_dir / "issue_draft.md").write_text(issue_draft(report, repo), encoding="utf-8")
    return meta


def paragraph_with_insertion(ms: dict) -> list[tuple[str, str]]:
    """The paragraph as [("paper"|"drafted", text)] parts."""
    sents = split_sentences(ms["paragraph"])
    k = ms["insert_after"]
    return ([("paper", " ".join(sents[:k]))] if k else []) + [("drafted", ms["sentence"])] + \
        ([("paper", " ".join(sents[k:]))] if k < len(sents) else [])


def markdown_section(report: dict) -> str:
    """Short Markdown section for the cards that have a drafted sentence; empty when none."""
    cards = [c for c in report.get("claims", []) if c.get("missing_sentence")]
    if not cards:
        return ""
    out = ["", "## The sentence the paper was missing",
           "Drafted by GapFinder (Nemotron 3 Super), not written by the authors. Check it before use. "
           "The drafted sentence is in bold, inserted into the paper's own setup paragraph."]
    for c in cards:
        ms = c["missing_sentence"]
        text = " ".join(f"**[drafted by GapFinder: {t}]**" if kind == "drafted" else t
                        for kind, t in paragraph_with_insertion(ms) if t)
        out += ["", f"### {c['target']['claim_id']} (paper p.{ms['page']})", "", f"> {text}"]
    out += ["", "An issue draft for the artifact's repository is in `issue_draft.md` (never posted)."]
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------ issue draft

_SECRET_RE = re.compile(r"(?i)\b(?:[A-Z0-9_]*(?:API_?KEY|TOKEN|SECRET|PASSWORD)[A-Z0-9_]*\s*[=:]\s*\S+|"
                        r"sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|v1\.[A-Za-z0-9_-]{30,})")


def scrub(text: str) -> str:
    return _SECRET_RE.sub("[redacted]", text)


def issue_draft(report: dict, repo: str | None = None, report_path: str = "gap_report.md") -> str:
    """A polite, factual GitHub issue as Markdown text. Written to a file by the caller, never posted."""
    cards = [c for c in report.get("claims", []) if c.get("missing_sentence")]
    paper, repo_line = report.get("paper", "the paper"), repo or "<the artifact's repository>"
    out = [f"<!-- Draft for {repo_line}. Written by GapFinder, never posted automatically: review before use. -->", "",
           "# Documentation request: a setting the paper does not state", "",
           f"Thank you to the authors of *{paper}* for releasing the artifact; it built and ran for us, "
           "which made this comparison possible.", "",
           "While reproducing the reported numbers we found that one setting matters for matching them, "
           "and we could not find it stated in the paper. We may well have missed it, so please correct us "
           "if it is documented somewhere."]
    for c in cards:
        t, ms = c["target"], c["missing_sentence"]
        changes = ", ".join(f"`{k}={v}`" for k, v in c["changes"].items())
        out += ["", f"## {t['claim_id']}: {t['metric']} (paper value {t['paper_value']})",
                f"- With the artifact's defaults our naive run differed from the paper by "
                f"{(c.get('gap_before') or 0) * 100:+.1f}% (noise band ±{(c.get('band') or 0) * 100:.1f}%).",
                f"- With {changes} the difference was {(c.get('gap_after') or 0) * 100:+.1f}%.",
                "- Reverting the setting brought the difference back, and the claims we held out did not get worse."]
        rep = (c.get("replay") or [None])[0]
        if rep:
            env = " ".join(f"{k}={v}" for k, v in (rep.get("env") or {}).items())
            out += ["", "To replay the run:", "```", f"{env} {rep.get('command', '')}".strip(), "```"]
        out += ["", f"Suggested wording for the setup paragraph (page {ms['page']}), drafted by a language model "
                    "and not yet checked by us against your intent:", "", f"> {ms['sentence']}"]
    out += ["", f"The full evidence (measurements, reversal test, held-out claims) is in the Gap Report: "
                f"`{report_path}`, generated by GapFinder. This is a documentation suggestion only; we are not "
                "claiming anything is wrong with the results. Thanks again for the work."]
    return scrub("\n".join(out)) + "\n"
