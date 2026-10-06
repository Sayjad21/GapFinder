"""Download the RusKey paper from arXiv into papers/ruskey/ (PDFs aren't committed).

    python scripts/fetch_paper.py

Fetches arXiv:2308.07013v2, the exact version the gold ledger's quotes and
page numbers were checked against, and writes a text extract next to it.
"""

from __future__ import annotations

import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PAPERS = {
    "ruskey": ("https://arxiv.org/pdf/2308.07013v2", ROOT / "papers" / "ruskey" / "ruskey_paper.pdf"),
}


def fetch(name: str) -> Path:
    url, dest = PAPERS[name]
    if dest.exists():
        print(f"{name}: already present at {dest}")
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        r = httpx.get(url, follow_redirects=True, timeout=60, headers={"User-Agent": "gapfinder-setup"})
        r.raise_for_status()
        if not r.content.startswith(b"%PDF"):
            raise SystemExit(f"{url} did not return a PDF")
        dest.write_bytes(r.content)
        print(f"{name}: downloaded {len(r.content) // 1024} KB -> {dest}")
    from gapfinder.ingest.pdf import load_pdf

    txt = dest.with_suffix(".txt")
    if not txt.exists():
        txt.write_text(load_pdf(dest).full_text, encoding="utf-8")
        print(f"{name}: text extract -> {txt}")
    return dest


if __name__ == "__main__":
    for n in sys.argv[1:] or PAPERS:
        fetch(n)
