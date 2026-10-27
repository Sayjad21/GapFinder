import { useEffect, useState } from "react";
import { api } from "./api.js";

// ------------------------------------------------------------------ the showcase manifest, fetched once
let manifest = null;
export function useShowcase() {
  const [data, setData] = useState(manifest);
  const [error, setError] = useState(null);
  useEffect(() => {
    if (manifest) return;
    api.showcase().then((d) => { manifest = d; setData(d); }).catch((e) => setError(e));
  }, []);
  return { data, error };
}

export function Loading({ what = "Loading…", error }) {
  if (error) return <p className="notice" role="alert">Couldn’t load the showcase data ({String(error.message || error)}). Start the server with <code>uvicorn gapfinder.api.server:app</code> and reload.</p>;
  return <p className="status-line" aria-live="polite">{what}</p>;
}

// ------------------------------------------------------------------ numbers
const LOCALE = typeof navigator !== "undefined" ? navigator.languages?.[0] : undefined;
export function digits(values) {
  // enough decimals to tell the readings apart, at most 4
  const span = Math.max(...values) - Math.min(...values) || Math.abs(values[0]) || 1;
  return Math.min(4, Math.max(0, Math.ceil(-Math.log10(span / 20))));
}
export function num(x, d = 2) {
  if (x === null || x === undefined || Number.isNaN(x)) return "n/a";
  return new Intl.NumberFormat(LOCALE, { minimumFractionDigits: d, maximumFractionDigits: d }).format(x);
}
export function signedPct(x, d = 1) {
  if (x === null || x === undefined) return "n/a";
  return new Intl.NumberFormat(LOCALE, { style: "percent", minimumFractionDigits: d, maximumFractionDigits: d,
    signDisplay: "exceptZero" }).format(x).replace("-", "−"); // a true minus, not a hyphen
}
// A patch knob "@ast:gae/preprocessing.py:32:test_percent" reads "test_percent (gae/preprocessing.py:32)". A code edit,
// "@ast:src/utils.py:79:@mut.32.num.mul2" set to 1, reads "edit: double the number (src/utils.py:79)"; a call whose result
// is replaced carries the new expression base64-encoded, too long to show, so it is named, not printed.
const EDIT_WORDS = { "num.mul2": "double the number", "num.div2": "halve the number", "num.neg": "negate the number",
  "num.zero": "set the number to zero", "num.one": "set the number to one" };
const EDIT = /^@ast:(.+?):(\d+):@mut\.\d+\.(.+)$/;
export function prettyKnob(k) {
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
export const changeText = (k, v) => (EDIT.test(k) && String(v) === "1" ? `edit: ${prettyKnob(k)}` : `${prettyKnob(k)} = ${v}`);
export const changesText = (c) => Object.entries(c || {}).map(([k, v]) => changeText(k, v)).join(", ");

// ------------------------------------------------------------------ verdicts
export const VERDICT = {
  found: "Found the documented cause",
  partial: "Found part of it",
  no_gap: "Correctly found no gap",
  missed: "Missed it",
};
export const VERDICT_SHORT = { found: "Found", partial: "Partly", no_gap: "No gap", missed: "Missed" };

export function Glyph({ v }) {
  const p = { fill: "none", stroke: "currentColor", strokeWidth: 2.4, strokeLinecap: "round", strokeLinejoin: "round" };
  if (v === "found") return <svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2.2 6.4 4.8 9 9.8 3.2" {...p} /></svg>;
  if (v === "partial") return <svg viewBox="0 0 12 12" aria-hidden="true"><path d="M6 1.8a4.2 4.2 0 0 1 0 8.4z" fill="currentColor" /><circle cx="6" cy="6" r="4.2" {...p} strokeWidth="1.6" /></svg>;
  if (v === "no_gap") return <svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2.4 4.4h7.2M2.4 7.6h7.2" {...p} /></svg>;
  if (v === "missed") return <svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 3l6 6M9 3 3 9" {...p} /></svg>;
  return <svg viewBox="0 0 12 12" aria-hidden="true"><circle cx="6" cy="6" r="1.6" fill="currentColor" /></svg>;
}

export function Verdict({ v, big = false, short = false }) {
  const cls = v || "none";
  return (
    <span className={`verdict ${cls}${big ? " big" : ""}`}>
      <span className="glyph"><Glyph v={v} /></span>
      {v ? (short ? VERDICT_SHORT[v] : VERDICT[v]) : "Not run"}
    </span>
  );
}

// ------------------------------------------------------------------ theme: system, light or dark, remembered per viewer
const THEMES = ["system", "light", "dark"];
function readTheme() {
  try { return localStorage.getItem("gf-theme") || "system"; } catch { return "system"; }
}
export function applyTheme(t) {
  const root = document.documentElement;
  if (t === "system") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", t);
}
export function ThemeToggle() {
  const [theme, setTheme] = useState(readTheme);
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
export function useTooltip() {
  const [tip, setTip] = useState(null);
  const show = (e, content) => {
    const r = e.currentTarget.getBoundingClientRect();
    const x = Math.min(window.innerWidth - 316, Math.max(8, r.left + r.width / 2 - 150));
    setTip({ x, y: r.top - 8, content });
  };
  const hide = () => setTip(null);
  const node = tip && (
    <div className="tooltip" role="status" style={{ left: tip.x, top: tip.y, transform: "translateY(-100%)" }}>{tip.content}</div>
  );
  return { show, hide, node };
}

export function prefersReducedMotion() {
  return typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
}
