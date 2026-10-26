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
export const changesText = (c) => Object.entries(c || {}).map(([k, v]) => `${prettyKnob(k)} = ${v}`).join(", ");
// a patch knob "@ast:gae/preprocessing.py:32:test_percent" reads as "test_percent (gae/preprocessing.py:32)"
export function prettyKnob(k) {
  const m = /^@ast:(.+?):(\d+):(.+)$/.exec(k);
  if (!m) return k;
  const name = m[3].replace(/^@mut\.\d+\./, "");
  return `${name} (${m[1]}:${m[2]})`;
}

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
