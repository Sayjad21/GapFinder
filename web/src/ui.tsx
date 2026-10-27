import { Component, useEffect, useState, type PointerEvent, type FocusEvent, type ReactNode } from "react";
import type { Changes, VerdictWord } from "./types.ts";

export function Loading({ what = "Loading…", error }: { what?: string; error?: Error | null }) {
  if (error) return <p className="notice" role="alert">Couldn’t load the showcase data ({String(error.message || error)}). Start the server with <code>uvicorn gapfinder.api.server:app</code> and reload.</p>;
  return <p className="status-line" aria-live="polite">{what}</p>;
}

// A page that fails to render says so in a sentence, and the rest of the site keeps working
export class PageBoundary extends Component<{ children: ReactNode }, { failed: boolean }> {
  state = { failed: false };
  static getDerivedStateFromError() { return { failed: true }; }
  render() {
    if (!this.state.failed) return this.props.children;
    return (
      <div className="shell">
        <h1 className="not-found">This page couldn’t be shown</h1>
        <p>Something on it failed to load. <a href="#/">Go to the start</a>, or reload the page.</p>
      </div>
    );
  }
}

// ------------------------------------------------------------------ numbers
const LOCALE = typeof navigator !== "undefined" ? navigator.languages?.[0] : undefined;
export function digits(values: number[]): number {
  // enough decimals to tell the readings apart, at most 4
  const span = Math.max(...values) - Math.min(...values) || Math.abs(values[0]) || 1;
  return Math.min(4, Math.max(0, Math.ceil(-Math.log10(span / 20))));
}
export function num(x: number | null | undefined, d = 2): string {
  if (x === null || x === undefined || Number.isNaN(x)) return "n/a";
  return new Intl.NumberFormat(LOCALE, { minimumFractionDigits: d, maximumFractionDigits: d }).format(x);
}
export function signedPct(x: number | null | undefined, d = 1): string {
  if (x === null || x === undefined) return "n/a";
  return new Intl.NumberFormat(LOCALE, { style: "percent", minimumFractionDigits: d, maximumFractionDigits: d,
    signDisplay: "exceptZero" }).format(x).replace("-", "−"); // a true minus, not a hyphen
}

// A patch knob "@ast:gae/preprocessing.py:32:test_percent" reads "test_percent (gae/preprocessing.py:32)". A code edit,
// "@ast:src/utils.py:79:@mut.32.num.mul2" set to 1, reads "edit: double the number (src/utils.py:79)"; a call whose result
// is replaced carries the new expression base64-encoded, too long to show, so it is named, not printed.
const EDIT_WORDS: Record<string, string> = { "num.mul2": "double the number", "num.div2": "halve the number", "num.neg": "negate the number",
  "num.zero": "set the number to zero", "num.one": "set the number to one" };
const EDIT = /^@ast:(.+?):(\d+):@mut\.\d+\.(.+)$/;
export function prettyKnob(k: string): string {
  const e = EDIT.exec(k);
  if (e) {
    const op = e[3];
    const words = op.startsWith("Call.set.") ? "replace the call’s result" : op.startsWith("Call.red.") ? `reduce with ${op.slice(9)} instead`
      : EDIT_WORDS[op] || op;
    return `${words} (${e[1]}:${e[2]})`;
  }
  const m = /^@ast:(.+?):(\d+):(.+)$/.exec(k);
  return m ? `${m[3]} (${m[1]}:${m[2]})` : k;
}
export const changeText = (k: string, v: string | number): string => (EDIT.test(k) && String(v) === "1" ? `edit: ${prettyKnob(k)}` : `${prettyKnob(k)} = ${v}`);
export const changesText = (c: Changes | null | undefined): string => Object.entries(c || {}).map(([k, v]) => changeText(k, v)).join(", ");

// ------------------------------------------------------------------ verdicts
export const VERDICT: Record<VerdictWord, string> = {
  found: "Found the documented cause",
  partial: "Found part of it",
  no_gap: "Correctly found no gap",
  missed: "Missed it",
};
export const VERDICT_SHORT: Record<VerdictWord, string> = { found: "Found", partial: "Partly", no_gap: "No gap", missed: "Missed" };

export function Glyph({ v }: { v?: VerdictWord | null }) {
  const p = { fill: "none", stroke: "currentColor", strokeWidth: 2.4, strokeLinecap: "round", strokeLinejoin: "round" } as const;
  if (v === "found") return <svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2.2 6.4 4.8 9 9.8 3.2" {...p} /></svg>;
  if (v === "partial") return <svg viewBox="0 0 12 12" aria-hidden="true"><path d="M6 1.8a4.2 4.2 0 0 1 0 8.4z" fill="currentColor" /><circle cx="6" cy="6" r="4.2" {...p} strokeWidth="1.6" /></svg>;
  if (v === "no_gap") return <svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2.4 4.4h7.2M2.4 7.6h7.2" {...p} /></svg>;
  if (v === "missed") return <svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 3l6 6M9 3 3 9" {...p} /></svg>;
  return <svg viewBox="0 0 12 12" aria-hidden="true"><circle cx="6" cy="6" r="1.6" fill="currentColor" /></svg>;
}

export function Verdict({ v, big = false, short = false }: { v?: VerdictWord | null; big?: boolean; short?: boolean }) {
  return (
    <span className={`verdict ${v || "none"}${big ? " big" : ""}`}>
      <span className="glyph"><Glyph v={v} /></span>
      {v ? (short ? VERDICT_SHORT[v] : VERDICT[v]) : "Not run"}
    </span>
  );
}

// ------------------------------------------------------------------ theme: system, light or dark, remembered per viewer
type Theme = "system" | "light" | "dark";
const THEMES: Theme[] = ["system", "light", "dark"];
function readTheme(): Theme {
  try { return (localStorage.getItem("gf-theme") as Theme | null) || "system"; } catch { return "system"; }
}
export function applyTheme(t: Theme): void {
  const root = document.documentElement;
  if (t === "system") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", t);
}
export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>(readTheme);
  useEffect(() => { applyTheme(theme); try { localStorage.setItem("gf-theme", theme); } catch { /* private mode */ } }, [theme]);
  const next = THEMES[(THEMES.indexOf(theme) + 1) % THEMES.length];
  const label = { system: "Theme: follows the system", light: "Theme: light", dark: "Theme: dark" }[theme];
  return (
    <button type="button" className="iconbtn theme" onClick={() => setTheme(next)} aria-label={`${label}. Switch to ${next}`} title={label}>
      <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.8">
        {theme === "dark" && <path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z" />}
        {theme === "light" && <><circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" /></>}
        {theme === "system" && <><circle cx="12" cy="12" r="8" /><path d="M12 4a8 8 0 0 1 0 16Z" fill="currentColor" /></>}
      </svg>
    </button>
  );
}

// ------------------------------------------------------------------ one tooltip for every chart
// placed above the element it describes, clamped to the window; its position is the only style set inline
export function tipPlace(el: Element): { left: number; top: number } {
  const r = el.getBoundingClientRect();
  return { left: Math.min(window.innerWidth - 316, Math.max(8, r.left + r.width / 2 - 150)), top: r.top - 8 };
}

export function useTooltip() {
  const [tip, setTip] = useState<{ left: number; top: number; content: ReactNode } | null>(null);
  const show = (e: PointerEvent<Element> | FocusEvent<Element>, content: ReactNode) => setTip({ ...tipPlace(e.currentTarget), content });
  const hide = () => setTip(null);
  const node = tip && <div className="tooltip" role="status" style={{ left: tip.left, top: tip.top }}>{tip.content}</div>;
  return { show, hide, node };
}

export function prefersReducedMotion(): boolean {
  return typeof window !== "undefined" && Boolean(window.matchMedia?.("(prefers-reduced-motion: reduce)").matches);
}
