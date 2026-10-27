import { useCallback, useEffect, useId, useMemo, useRef, useState, type KeyboardEvent } from "react";
import { useShowcase } from "../data.ts";
import { href } from "../nav.ts";
import type { Showcase } from "../types.ts";
import { VERDICT } from "../ui.tsx";
import { GAPBENCH_WORDS, GLOSSARY, KIND_WORDS, vName } from "../words.tsx";

// Search everything from anywhere: press / or Ctrl+K (⌘K), type, and Enter opens the match. Papers, planted cases,
// GapBench tasks, the pages and the glossary's words are all in one list, best match first.

export interface Hit { kind: string; title: string; detail: string; to: string }

const PAGES: Hit[] = [
  { kind: "Page", title: "Cases", detail: "the sixteen real papers, finds and misses", to: href("/cases") },
  { kind: "Page", title: "Known answers", detail: "planted gaps and GapBench tasks it solved", to: href("/synthetic") },
  { kind: "Page", title: "The evidence", detail: "every measurement, with what it can and can’t show", to: href("/evidence") },
  { kind: "Page", title: "How it works", detail: "the seven steps, the limits, the glossary", to: href("/how") },
];

export function index(data: Showcase | null): Hit[] {
  const out: Hit[] = [...PAGES];
  for (const c of data?.real || []) {
    const v = c.versions[c.current];
    out.push({ kind: "Paper", title: c.title, detail: `${c.venue} · ${v ? VERDICT[v.verdict] : ""} · ${c.documented_cause}`, to: href(`/case/${c.slug}`) });
  }
  for (const p of data?.planted || []) {
    out.push({ kind: "Planted", title: `${KIND_WORDS[p.family] || p.family} in ${p.paper}`, detail: `${vName(p.version)}, batch ${p.seed} · ${p.planted.join("; ") || "nothing planted"}`,
               to: href(`/run/${p.id}`) });
  }
  for (const g of data?.gapbench || []) {
    out.push({ kind: "GapBench", title: g.title.split(":")[0].replace("GapBench ", ""), detail: GAPBENCH_WORDS[g.category] || g.category, to: href(`/run/${g.id}`) });
  }
  for (const [, [word, text]] of Object.entries(GLOSSARY)) out.push({ kind: "Word", title: word, detail: text, to: href("/how") });
  return out;
}

// every word of the query must appear; a match in the title counts most, at its start most of all
export function search(hits: Hit[], q: string, limit = 10): Hit[] {
  const words = q.toLowerCase().split(/\s+/).filter(Boolean);
  if (!words.length) return hits.filter((h) => h.kind === "Page" || h.kind === "Paper").slice(0, limit);
  const scored = hits.map((h) => {
    const t = h.title.toLowerCase(), d = h.detail.toLowerCase();
    let s = 0;
    for (const w of words) {
      if (t.startsWith(w)) s += 6; else if (t.includes(w)) s += 4; else if (d.includes(w)) s += 1; else return null;
    }
    return { h, s: s + (h.kind === "Paper" ? 1 : h.kind === "Page" ? 0.5 : 0) };
  }).filter((x): x is { h: Hit; s: number } => x !== null);
  return scored.sort((a, b) => b.s - a.s).slice(0, limit).map((x) => x.h);
}

export default function Search() {
  const { data } = useShowcase();
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState("");
  const [sel, setSel] = useState(0);
  const input = useRef<HTMLInputElement>(null);
  const opener = useRef<HTMLElement | null>(null);
  const listId = useId();
  const all = useMemo(() => index(data), [data]);
  const hits = useMemo(() => search(all, q), [all, q]);

  // opening starts from an empty query; the input takes focus as it mounts
  const show = useCallback((from: HTMLElement | null) => { opener.current = from; setQ(""); setSel(0); setOpen(true); }, []);
  useEffect(() => {
    const onKey = (e: globalThis.KeyboardEvent) => {
      const typing = e.target instanceof HTMLElement && (e.target.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName));
      if ((e.key === "k" && (e.ctrlKey || e.metaKey)) || (e.key === "/" && !typing && !open)) {
        e.preventDefault();
        show(document.activeElement as HTMLElement | null);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, show]);

  const close = () => { setOpen(false); opener.current?.focus?.(); };
  const go = (h: Hit | undefined) => { if (!h) return; setOpen(false); window.location.hash = h.to.slice(1); };
  const onKey = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "ArrowDown") { e.preventDefault(); setSel((s) => Math.min(hits.length - 1, s + 1)); }
    else if (e.key === "ArrowUp") { e.preventDefault(); setSel((s) => Math.max(0, s - 1)); }
    else if (e.key === "Enter") { e.preventDefault(); go(hits[sel]); }
    else if (e.key === "Escape") { e.preventDefault(); close(); }
  };

  return (
    <>
      <button type="button" className="search-btn" onClick={(e) => show(e.currentTarget)} aria-haspopup="dialog">
        <svg width="15" height="15" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round">
          <circle cx="10.5" cy="10.5" r="6.5" /><path d="m20 20-4.6-4.6" />
        </svg>
        <span>Search</span><kbd>/</kbd>
      </button>
      {open && (
        // the backdrop closes on a click outside; the keyboard closes with Escape, from the input
        <div className="palette-backdrop" role="presentation" onMouseDown={(e) => { if (e.target === e.currentTarget) close(); }}>
          <div className="palette" role="dialog" aria-modal="true" aria-label="Search the site">
            {/* the ARIA combobox pattern: a text input driving a listbox of options (ul and li carry those roles by design) */}
            <input ref={input} autoFocus type="text" role="combobox" aria-expanded="true" aria-controls={listId} aria-autocomplete="list"
                   aria-activedescendant={hits[sel] ? `${listId}-${sel}` : undefined} placeholder="Search papers, planted cases, pages and words…"
                   value={q} onChange={(e) => { setQ(e.target.value); setSel(0); }} onKeyDown={onKey} aria-label="Search" />
            {/* oxlint-disable-next-line jsx-a11y/no-noninteractive-element-to-interactive-role */}
            <ul id={listId} role="listbox" aria-label="Matches">
              {hits.map((h, i) => (
                // oxlint-disable-next-line jsx-a11y/no-noninteractive-element-to-interactive-role
                <li key={`${h.kind}-${h.to}-${h.title}`} id={`${listId}-${i}`} role="option" aria-selected={i === sel}
                    onMouseEnter={() => setSel(i)} onMouseDown={(e) => { e.preventDefault(); go(h); }}>
                  <span className="hit-kind">{h.kind}</span><span className="hit-title">{h.title}</span><span className="hit-detail">{h.detail}</span>
                </li>
              ))}
              {/* oxlint-disable-next-line jsx-a11y/no-noninteractive-element-to-interactive-role */}
              {!hits.length && <li className="hit-none" role="option" aria-selected="false" aria-disabled="true">Nothing matches “{q}”.</li>}
            </ul>
            <p className="palette-keys"><kbd>↑</kbd><kbd>↓</kbd> to move · <kbd>Enter</kbd> to open · <kbd>Esc</kbd> to close</p>
          </div>
        </div>
      )}
    </>
  );
}
