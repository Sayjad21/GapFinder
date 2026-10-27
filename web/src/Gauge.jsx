import { useEffect, useRef, useState } from "react";
import { digits, num, prefersReducedMotion, signedPct } from "./ui.jsx";

// The gap gauge: a measuring rule with two jaws, the paper’s reading and the code’s, and the gap highlighted between
// them. With an answer, the code’s jaw moves to its reading after GapFinder’s change and the highlight shrinks to what
// is left; a faint line, labelled, stays where the code started. Every reading is labelled on the rule itself, so the
// gauge needs no legend. `g`: {paper, code, after, band (relative), metric, figure}. `show`: "before" or "after".
// `compact`: one-line labels and no caption (the replay's claims); `live`: a reading the code's jaw follows (the closest
// run so far), labelled `liveLabel`.

const H0 = 204, HC = 108;
const Y0 = { pLabel: 20, pVal: 46, jawTop: 58, gLabel: 74, gVal: 90, gapTop: 94, gapBot: 112, axis: 120, tickLab: 142, jawBot: 152,
             cLabel: 176, cVal: 198 };
const YC = { pLabel: 14, jawTop: 22, gapTop: 38, gapBot: 50, axis: 56, tickLab: 74, jawBot: 80, cLabel: 100 };

function niceTicks(lo, hi, n = 6) {
  const raw = (hi - lo) / n;
  const mag = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => s >= raw) || raw;
  const out = [];
  for (let v = Math.ceil(lo / step) * step; v <= hi + 1e-12; v += step) out.push(+v.toFixed(12));
  return { ticks: out, step };
}

const easeOut = (t) => 1 - (1 - t) ** 3;

export default function Gauge({ g, show = "after", playKey = 0, label, compact = false, live = null,
                                liveLabel = "closest run so far", caption = true }) {
  const H = compact ? HC : H0, Y = compact ? YC : Y0;
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
  const [p, setP] = useState(target);
  const from = useRef(p);
  // `playKey` replays the move from the start: a toggle pressed again shows it again
  const lastKey = useRef(playKey);
  useEffect(() => {
    if (reduced) { setP(target); from.current = target; return undefined; }
    let raf = 0;
    const start = performance.now();
    const replay = lastKey.current !== playKey && target === 1;
    lastKey.current = playKey;
    const p0 = replay ? 0 : from.current;
    const dur = 1400;
    const tick = (now) => {
      const t = Math.min(1, (now - start) / dur);
      const v = p0 + (target - p0) * easeOut(t);
      from.current = v;
      setP(v);
      if (t < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target, playKey]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!g) return null;
  const band = (g.band || 0) * Math.abs(g.paper);
  const vals = [g.paper, g.code, ...(hasAfter ? [g.after] : []), ...(live !== null ? [live] : []), g.paper - band, g.paper + band];
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

  const codeNow = live !== null ? live : hasAfter ? g.code + (g.after - g.code) * p : g.code;
  const xp = x(g.paper), xc = x(codeNow), xc0 = x(g.code);
  const gapNow = (codeNow - g.paper) / Math.abs(g.paper);
  const gapW = Math.abs(xp - xc);
  const left = Math.min(xp, xc);
  const slant = Math.min(5, gapW / 4);
  const anchor = (xx) => (xx < 90 ? "start" : xx > w - 90 ? "end" : "middle");
  const moved = (hasAfter && p > 0.02) || (live !== null && live !== g.code);
  const codeLabel = live !== null ? liveLabel : hasAfter && p > 0.5 ? "after GapFinder’s change" : "the code, as released";
  // the start line's label sits on the far side from the paper, so it never crosses the paper's jaw
  const ghostLeft = xc0 < xp;
  const ghostX = ghostLeft ? Math.max(xc0 - 6, 74) : Math.min(xc0 + 6, w - 74);
  // the gap's figure: inside the highlight when it fits, else beside it on the side away from the start line
  const inside = gapW > (compact ? 58 : 78);
  const besideRight = moved ? ghostLeft : Math.max(xp, xc) + 60 < w;
  const gapX = inside ? left + gapW / 2 : besideRight ? Math.max(xp, xc) + 8 : left - 8;
  const desc = `${label ? `${label}. ` : ""}The paper reports ${num(g.paper, d)}. The code, as released, gives ${num(g.code, d)}, a gap of `
    + `${signedPct((g.code - g.paper) / Math.abs(g.paper))}.` + (hasAfter ? ` After GapFinder’s change it gives ${num(g.after, d)}, `
    + `${signedPct((g.after - g.paper) / Math.abs(g.paper))} from the paper.` : " GapFinder changed nothing that moved it.");

  return (
    <figure className="gauge" ref={ref}>
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
        <text className={`gaptext${inside ? "" : " out"}`} x={gapX} y={(Y.gapTop + Y.gapBot) / 2 + 4.5}
              textAnchor={inside ? "middle" : besideRight ? "start" : "end"}>{signedPct(gapNow)}</text>
        {/* where the code started, once it has moved, labelled with its reading */}
        {moved && <line className="ghost" x1={xc0} x2={xc0} y1={compact ? Y.gapTop - 2 : Y.gLabel - 12} y2={Y.axis + 10} />}
        {moved && !compact && (<>
          <text className="lbl" x={ghostX} y={Y.gLabel} textAnchor={ghostLeft ? "end" : "start"}>as released</text>
          <text className="val small" x={ghostX} y={Y.gVal} textAnchor={ghostLeft ? "end" : "start"}>{num(g.code, d)}</text>
        </>)}
        {/* the paper’s jaw */}
        <line className="jaw-paper" x1={xp} x2={xp} y1={Y.jawTop} y2={Y.axis + 6} />
        {compact ? (
          <text className="lbl" x={xp} y={Y.pLabel} textAnchor={anchor(xp)}><tspan className="serif-i">the paper</tspan> <tspan className="v">{num(g.paper, d)}</tspan></text>
        ) : (<>
          <text className="lbl serif" x={xp} y={Y.pLabel} textAnchor={anchor(xp)}>the paper</text>
          <text className="val" x={xp} y={Y.pVal} textAnchor={anchor(xp)}>{num(g.paper, d)}</text>
        </>)}
        {/* the code’s jaw */}
        <line className="jaw-code" x1={xc} x2={xc} y1={Y.gapTop - 4} y2={Y.jawBot} />
        {compact ? (
          <text className="lbl" x={xc} y={Y.cLabel} textAnchor={anchor(xc)}>{live !== null ? liveLabel : "as released"} <tspan className="v">{num(codeNow, d)}</tspan></text>
        ) : (<>
          <text className="lbl" x={xc} y={Y.cLabel} textAnchor={anchor(xc)}>{codeLabel}</text>
          <text className="val" x={xc} y={Y.cVal} textAnchor={anchor(xc)}>{num(codeNow, d)}</text>
        </>)}
      </svg>
      {!compact && caption && (g.figure || band > 0) && (
        <figcaption className="gauge-caption">
          {g.figure && <span>The paper’s number: {g.figure}.</span>}
          {band > 0 && <span><span className="sw band" aria-hidden="true" /> Shaded on the rule: the run-to-run noise around the paper’s number, ±{(g.band * 100).toFixed(1)}%.</span>}
        </figcaption>
      )}
    </figure>
  );
}
