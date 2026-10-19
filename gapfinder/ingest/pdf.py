"""PDF ingest: page text with page numbers, plus figure crops around captions."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

_CAPTION_RE = re.compile(r"^\s*(Figure|Fig\.|Table)\s+(\d+)[\s:.]", re.IGNORECASE)


@dataclass
class Page:
    number: int  # 1-based
    text: str


@dataclass
class FigureCrop:
    label: str  # "Figure 6"
    page: int
    caption: str
    png_path: Path | None = None


@dataclass
class PaperText:
    path: Path
    pages: list[Page]
    figures: list[FigureCrop] = field(default_factory=list)
    # tables and figure data from the arXiv LaTeX source (gapfinder/ingest/arxiv_source.py), appended to the text
    supplement: str = ""

    @property
    def full_text(self) -> str:
        text = "\n".join(f"[[page {p.number}]]\n{p.text}" for p in self.pages)
        return text + (f"\n[[source]]\n{self.supplement}" if self.supplement else "")

    def section(self, heading_regex: str, max_chars: int = 30000) -> str:
        """Text from the first heading matching `heading_regex` onward, capped."""
        text = self.full_text
        m = re.search(heading_regex, text, re.IGNORECASE | re.MULTILINE)
        return text[m.start() : m.start() + max_chars] if m else ""


def load_pdf(path: str | Path, figure_dir: str | Path | None = None, dpi: int = 150) -> PaperText:
    path = Path(path)
    doc = pymupdf.open(path)
    pages = [Page(i + 1, page.get_text("text")) for i, page in enumerate(doc)]
    paper = PaperText(path=path, pages=pages)
    if figure_dir is not None:
        paper.figures = _crop_figures(doc, Path(figure_dir), dpi)
    doc.close()
    return paper


def _crop_figures(doc, out: Path, dpi: int) -> list[FigureCrop]:
    """Render the region above each 'Figure N' caption.

    Figures in two-column systems papers sit above their caption; we take the
    union of image/drawing blocks between the previous text block and the
    caption, falling back to a fixed band when the page has vector art only.
    """
    out.mkdir(parents=True, exist_ok=True)
    crops: list[FigureCrop] = []
    seen: set[str] = set()
    for pno, page in enumerate(doc):
        blocks = page.get_text("blocks")  # (x0, y0, x1, y1, text, block_no, type)
        for b in blocks:
            text = b[4].strip()
            m = _CAPTION_RE.match(text)
            if not m or m.group(1).lower().startswith("tab"):
                continue
            label = f"Figure {m.group(2)}"
            if label in seen:
                continue
            seen.add(label)
            cap_rect = pymupdf.Rect(b[:4])
            col = _column_rect(page.rect, cap_rect)
            art = [pymupdf.Rect(r["bbox"]) for r in page.get_image_info()] + [
                d["rect"] for d in page.get_drawings()
            ]
            art = [r for r in art if r.y1 <= cap_rect.y0 + 2 and r.intersects(col)]
            if art:
                region = art[0]
                for r in art[1:]:
                    region |= r
                region = region & col
                region.y1 = cap_rect.y0
            else:
                region = pymupdf.Rect(col.x0, max(col.y0, cap_rect.y0 - 250), col.x1, cap_rect.y0)
            png = out / f"{label.replace(' ', '_').lower()}_p{pno + 1}.png"
            if region.height > 20 and region.width > 20:
                page.get_pixmap(clip=region, dpi=dpi).save(png)
            else:
                png = None
            crops.append(FigureCrop(label=label, page=pno + 1, caption=text[:500], png_path=png))
    return crops


def _column_rect(page_rect, cap_rect):
    """The column (or full width) that a caption spans."""
    mid = page_rect.width / 2
    if cap_rect.x0 < mid - 20 and cap_rect.x1 > mid + 20:
        return pymupdf.Rect(page_rect.x0, page_rect.y0, page_rect.x1, page_rect.y1)
    if cap_rect.x1 <= mid + 20:
        return pymupdf.Rect(page_rect.x0, page_rect.y0, mid, page_rect.y1)
    return pymupdf.Rect(mid, page_rect.y0, page_rect.x1, page_rect.y1)


def load_text_paper(path: str | Path) -> PaperText:
    """A Markdown/plain-text paper (GapBench mini-papers). Form feeds split pages; else one page."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    chunks = text.split("\f") if "\f" in text else [text]
    return PaperText(path=path, pages=[Page(i + 1, c) for i, c in enumerate(chunks)])


def load_paper(path: str | Path, figure_dir: str | Path | None = None) -> PaperText:
    path = Path(path)
    if path.suffix.lower() in {".md", ".txt"}:
        return load_text_paper(path)
    return load_pdf(path, figure_dir=figure_dir)
