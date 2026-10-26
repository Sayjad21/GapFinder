import { useEffect, useRef, useState } from "react";
import { digits, num, prefersReducedMotion, signedPct } from "./ui.jsx";

// The gap gauge: a measuring rule with two jaws, the paper’s reading and the code’s, and the gap highlighted between
// them. With an answer, the code’s jaw moves to its reading after GapFinder’s change and the highlight shrinks to what
// is left. `g`: {paper, code, after, band (relative), metric, figure}. `show`: "before" or "after".

const H = 204;
const Y = { pLabel: 20, pVal: 46, jawTop: 58, gapTop: 94, gapBot: 112, axis: 120, tickLab: 142, jawBot: 152, cLabel: 176, cVal: 198 };

function niceTicks(lo, hi, n = 6) {
  const raw = (hi - lo) / n;
  const mag = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => s >= raw) || raw;
  const out = [];
  for (let v = Math.ceil(lo / step) * step; v <= hi + 1e-12; v += step) out.push(+v.toFixed(12));
  return { ticks: out, step };
}

const easeOut = (t) => 1 - (1 - t) ** 3;

export default function Gauge({ g, show = "after", playKey = 0, autoplay = false, label }) {
  const ref = useRef(null);
  const [w, setW] = useState(760);
  useEffect(() => {
    if (!ref.current) return undefined;
    const ro = new ResizeObserver(([e]) => setW(Math.max(280, Math.round(e.contentRect.width))));
    ro.observe(ref.current);
    return () => ro.disconnect();
  }, []);

  const hasAfter = g && g.after !== null && g.after !== undefined;
  const target = hasAfter && show === "after" ? 1 : 0;
  const reduced = prefersReducedMotion();
  const [p, setP] = useState(autoplay && hasAfter && !reduced ? 0 : target);
  const from = useRef(p);
  useEffect(() => {
    if (reduced) { setP(target); return undefined; }
    let raf = 0;
    const start = performance.now();
    const p0 = autoplay && playKey && target === 1 ? 0 : from.current;
    const dur = 1500;
    const tick = (now) => {
      const t = Math.min(1, (now - start) / dur);
      const v = p0 + (target - p0) * easeOut(t);
      from.current = v;
      setP(v);
      if (t < 1) raf = requestAnimationFrame(tick);
    };
    const delay = setTimeout(() => { raf = requestAnimationFrame(tick); }, autoplay && p0 === 0 ? 450 : 0);
    return () => { clearTimeout(delay); cancelAnimationFrame(raf); };
  }, [target, playKey]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!g) return null;
  const band = (g.band || 0) * Math.abs(g.paper);
  const vals = [g.paper, g.code, ...(hasAfter ? [g.after] : []), g.paper - band, g.paper + band];
  const lo0 = Math.min(...vals), hi0 = Math.max(...vals);
  const pad = (hi0 - lo0) * 0.28 || Math.abs(g.paper) * 0.04 || 1;
  const lo = lo0 - pad, hi = hi0 + pad;
  const L = 18, R = 18;
  const x = (v) => L + ((v - lo) / (hi - lo)) * (w - L - R);
  const { ticks, step } = niceTicks(lo, hi, w < 480 ? 4 : 7);
  const minor = [];
  for (let v = Math.ceil(lo / (step / 5)) * (step / 5); v <= hi; v += step / 5) minor.push(v);
  const d = digits([g.paper, g.code, ...(hasAfter ? [g.after] : [])]);
  const td = Math.max(0, Math.min(4, Math.ceil(-Math.log10(step)) + (step / 10 ** Math.floor(Math.log10(step)) === 2.5 ? 1 : 0)));

  const codeNow = hasAfter ? g.code + (g.after - g.code) * p : g.code;
  const xp = x(g.paper), xc = x(codeNow), xc0 = x(g.code);
  const gapNow = (codeNow - g.paper) / Math.abs(g.paper);
  const gapW = Math.abs(xp - xc);
  const left = Math.min(xp, xc);
  const slant = Math.min(5, gapW / 4);
  const anchor = (xx) => (xx < 90 ? "start" : xx > w - 90 ? "end" : "middle");
  const after = hasAfter && p > 0.5;
  const codeLabel = after ? "the code, after GapFinder’s change" : "the code, as run";
  const desc = `${label ? `${label}. ` : ""}The paper reports ${num(g.paper, d)}. The code, as run, gives ${num(g.code, d)}, a gap of `
    + `${signedPct((g.code - g.paper) / Math.abs(g.paper))}.` + (hasAfter ? ` After GapFinder’s change it gives ${num(g.after, d)}, `
    + `${signedPct((g.after - g.paper) / Math.abs(g.paper))} from the paper.` : " GapFinder changed nothing that moved it.");

  return (
    <figure className="gauge" ref={ref} style={{ margin: 0 }}>
      <svg width={w} height={H} viewBox={`0 0 ${w} ${H}`} role="img" aria-label={desc}>
        {/* the rule */}
        {minor.map((v) => <line key={`m${v}`} className="tick minor" x1={x(v)} x2={x(v)} y1={Y.axis - 4} y2={Y.axis + 4} />)}
        {ticks.map((v) => <line key={`t${v}`} className="tick" x1={x(v)} x2={x(v)} y1={Y.axis - 8} y2={Y.axis + 8} />)}
        <line className="axis" x1={L} x2={w - R} y1={Y.axis} y2={Y.axis} />
        {ticks.map((v) => (
          <text key={`l${v}`} className="ticklabel" x={x(v)} y={Y.tickLab} textAnchor="middle">{num(v, td)}</text>
        ))}
        {/* the paper’s noise band, on the rule */}
        {band > 0 && <rect className="band" x={x(g.paper - band)} y={Y.axis - 3} width={Math.max(2, x(g.paper + band) - x(g.paper - band))} height={6} rx="3" />}
        {/* the gap: a highlighter stroke with chisel ends */}
        {gapW > 0.5 && (
          <path className="gap" d={`M${left + slant},${Y.gapTop} L${left + gapW},${Y.gapTop} L${left + gapW - slant},${Y.gapBot} L${left},${Y.gapBot} Z`} />
        )}
        {gapW > 78
          ? <text className="gaptext" x={left + gapW / 2} y={(Y.gapTop + Y.gapBot) / 2 + 4.5} textAnchor="middle">{signedPct(gapNow)}</text>
          : <text className="gaptext out" x={left + gapW / 2} y={Y.gapTop - 10} textAnchor="middle">{signedPct(gapNow)}</text>}
        {/* where the code started, once it has moved */}
        {hasAfter && p > 0.02 && <line className="ghost" x1={xc0} x2={xc0} y1={Y.gapTop - 2} y2={Y.axis + 10} />}
        {/* the paper’s jaw */}
        <line className="jaw-paper" x1={xp} x2={xp} y1={Y.jawTop} y2={Y.axis + 6} />
        <text className="lbl serif" x={xp} y={Y.pLabel} textAnchor={anchor(xp)}>the paper</text>
        <text className="val" x={xp} y={Y.pVal} textAnchor={anchor(xp)}>{num(g.paper, d)}</text>
        {/* the code’s jaw */}
        <line className="jaw-code" x1={xc} x2={xc} y1={Y.gapTop - 4} y2={Y.jawBot} />
        <text className="lbl" x={xc} y={Y.cLabel} textAnchor={anchor(xc)}>{codeLabel}</text>
        <text className="val" x={xc} y={Y.cVal} textAnchor={anchor(xc)}>{num(codeNow, d)}</text>
      </svg>
      <figcaption className="gauge-caption">
        <span className="key"><span className="sw paper" />the paper{g.figure ? `, ${g.figure}` : ""}</span>
        <span className="key"><span className="sw code" />the code{hasAfter ? `: as run ${num(g.code, d)}, after ${num(g.after, d)}` : `, as run`}</span>
        <span className="key"><span className="sw gap" />the gap</span>
        {band > 0 && <span className="key"><span className="sw band" />the run-to-run noise around the paper’s number</span>}
      </figcaption>
    </figure>
  );
}
