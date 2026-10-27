import { useEffect, useMemo, useRef, useState, type PointerEvent as RPointerEvent } from "react";
import { STAGE_NAME, STAGE_SHORT, chipClass, type ReplayState } from "../replay.ts";
import { closestPath, runStages, seekTo, type RunSlot } from "../story.ts";
import type { Target } from "../types.ts";
import { changesText, digits, num, signedPct, useTooltip } from "../ui.tsx";

// The Hunt: the whole investigation on one chart. Every run is a dot at the number it gave, in the order it started; the
// paper's number is a line, and the highlighter fills what is left between it and the closest run so far, so the gap
// visibly shrinks as the search goes. Runs far off the paper sit on the chart's edge, marked as off the scale. Pressing
// or dragging on the chart moves the replay to that run.

const H = 300, T = 30, B = 30, L = 58, R = 150;

// round values for the value axis, with as many decimals as their step needs
function ticks(lo: number, hi: number, n = 4): { vals: number[]; dec: number } {
  const raw = (hi - lo) / n, mag = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => s >= raw) || raw;
  const vals: number[] = [];
  for (let v = Math.ceil(lo / step) * step; v <= hi + 1e-12; v += step) vals.push(+v.toFixed(12));
  return { vals, dec: Math.max(0, Math.ceil(-Math.log10(step) - 1e-9) + (String(step / mag).includes(".") ? 1 : 0)) };
}

export interface HuntProps {
  slots: RunSlot[];
  state: ReplayState;
  final: ReplayState; // the state at the end: fixes the scales so nothing moves as the replay plays
  target: Target;
  setPos: (p: number) => void;
}

export default function Hunt({ slots, state, final, target, setPos }: HuntProps) {
  const ref = useRef<HTMLDivElement>(null);
  const [w, setW] = useState(900);
  useEffect(() => {
    if (!ref.current || typeof ResizeObserver === "undefined") return undefined;
    const ro = new ResizeObserver(([e]) => setW(Math.max(420, Math.round(e.contentRect.width))));
    ro.observe(ref.current);
    return () => ro.disconnect();
  }, []);
  const tip = useTooltip();
  const drag = useRef(false);

  const paper = target.paper_value;
  const released = final.noise[target.metric]?.median;
  const band = final.noise[target.metric]?.band ?? 0;
  const verdict = final.attributions[target.claim_id];
  const answer = verdict?.gap_after != null ? paper * (1 + verdict.gap_after) : null;
  // the vertical scale: the paper, the code as released and the answer, with room around them; runs beyond it are clamped
  const [lo, hi] = useMemo(() => {
    const anchors = [paper, released ?? paper, answer ?? paper, paper - band, paper + band];
    const a = Math.min(...anchors), b = Math.max(...anchors);
    const pad = (b - a) * 0.55 || Math.abs(paper) * 0.02 || 1;
    return [a - pad, b + pad];
  }, [paper, released, answer, band]);
  const n = Math.max(slots.length, 1);
  const x = (i: number) => L + ((i + 0.5) / n) * (w - L - R);
  const y = (v: number) => T + (1 - (Math.min(hi, Math.max(lo, v)) - lo) / (hi - lo)) * (H - T - B);
  const off = (v: number) => v < lo || v > hi;
  const d = digits([paper, released ?? paper]) + 1;
  const axis = ticks(lo, hi);

  const stages = useMemo(() => runStages(slots), [slots]);
  const path = closestPath(state, slots, target);
  const now = state.order.length - 1; // the last run started
  const nowX = now >= 0 ? x(now) : L;
  const dots = slots.map((s) => ({ s, b: state.branches[s.id] })).filter(({ b }) => b && (b.status === "succeeded" || b.status === "failed"));
  const done = state.attributions[target.claim_id];

  // the highlighter between the paper's line and the closest run so far, out to the playhead
  let area = "";
  if (path.length && now >= path[0].i) {
    const pts: string[] = [];
    path.forEach((p, k) => {
      const x0 = x(p.i) - (k === 0 ? (w - L - R) / n / 2 : 0);
      if (k > 0) pts.push(`${x0},${y(path[k - 1].v)}`);
      pts.push(`${x0},${y(p.v)}`);
    });
    pts.push(`${nowX},${y(path[path.length - 1].v)}`);
    area = `M${x(path[0].i) - (w - L - R) / n / 2},${y(paper)} L${pts.join(" L")} L${nowX},${y(paper)} Z`;
  }

  const seek = (e: RPointerEvent<SVGSVGElement>) => {
    const r = e.currentTarget.getBoundingClientRect();
    const i = Math.round(((e.clientX - r.left - L) / (w - L - R)) * n - 0.5);
    const s = slots[Math.max(0, Math.min(slots.length - 1, i))];
    if (s) setPos(seekTo(s));
  };

  const last = path[path.length - 1];
  return (
    <div className="hunt" ref={ref}>
      <svg width={w} height={H} viewBox={`0 0 ${w} ${H}`} role="img"
           aria-label={`${slots.length} runs. The paper reports ${num(paper, d)}; the code as released gives ${num(released, d)}.`
             + (last ? ` The closest run so far gives ${num(last.v, d)}.` : "") + (done && answer !== null ? ` GapFinder’s answer gives ${num(answer, d)}.` : "")}
           onPointerDown={(e) => { drag.current = true; e.currentTarget.setPointerCapture?.(e.pointerId); seek(e); }}
           onPointerMove={(e) => { if (drag.current) seek(e); }}
           onPointerUp={() => { drag.current = false; }}>
        {/* the stages, as columns */}
        {stages.map((s, k) => (
          <g key={k} className={`stage-col ${s.round}${now >= s.from && now < s.to ? " now" : ""}`}>
            <rect x={x(s.from) - (w - L - R) / n / 2} y={T - 22} width={((s.to - s.from) / n) * (w - L - R)} height={H - B - T + 22} />
            {((s.to - s.from) / n) * (w - L - R) > 46 && <text x={x(s.from) - (w - L - R) / n / 2 + 6} y={T - 8}>{STAGE_SHORT[s.round]}</text>}
          </g>
        ))}
        {/* the value axis */}
        {axis.vals.map((v) => (
          <g key={v} className="hunt-tick">
            <line x1={L} x2={w - R} y1={y(v)} y2={y(v)} />
            <text x={L - 8} y={y(v) + 4} textAnchor="end">{num(v, axis.dec)}</text>
          </g>
        ))}
        {/* the paper's noise band and the remaining gap */}
        {band > 0 && <rect className="hunt-band" x={L} width={w - L - R} y={y(paper + band)} height={Math.max(1, y(paper - band) - y(paper + band))} />}
        {area && <path className="hunt-gap" d={area} />}
        {released !== undefined && state.noise[target.metric] && (
          <g className="hunt-released">
            <line x1={L} x2={w - R} y1={y(released)} y2={y(released)} />
            <text x={w - R + 8} y={y(released) + 4}>as released {num(released, d)}</text>
          </g>
        )}
        <g className="hunt-paper">
          <line x1={L} x2={w - R} y1={y(paper)} y2={y(paper)} />
          <text x={w - R + 8} y={y(paper) + 4}><tspan className="serif-i">the paper</tspan> {num(paper, d)}</text>
        </g>
        {/* the closest run so far, as a step line */}
        {path.length > 1 && (
          <polyline className="hunt-path" points={path.flatMap((p, k) => (k ? [`${x(p.i)},${y(path[k - 1].v)}`, `${x(p.i)},${y(p.v)}`] : [`${x(p.i)},${y(p.v)}`])).concat(`${nowX},${y(last.v)}`).join(" ")} />
        )}
        {/* the runs */}
        {dots.map(({ s, b }) => {
          const v = b.parsed_metrics?.[target.metric];
          const cls = chipClass(b, state.verdicts);
          const cx = x(s.i);
          if (b.status === "failed" || v === undefined) {
            return <path key={s.id} className="hunt-dot failed" d={`M${cx - 3},${H - B - 9} l6,6 M${cx + 3},${H - B - 9} l-6,6`} />;
          }
          const cy = y(v);
          return (
            <circle key={s.id} className={`hunt-dot ${cls}${off(v) ? " off" : ""}`} cx={cx} cy={cy} r={off(v) ? 2.5 : 3.6}
                    onPointerEnter={(e) => tip.show(e, <><b>{s.id}: {num(v, d)}{off(v) ? " (off the scale)" : ""}</b>
                      {changesText(b.knob_changes) || "the code as released"} · {STAGE_NAME[s.round].toLowerCase()} · gap {signedPct((v - paper) / Math.abs(paper))}</>)}
                    onPointerLeave={tip.hide} />
          );
        })}
        {/* the answer */}
        {done && answer !== null && (
          <g className="hunt-answer">
            <circle cx={nowX} cy={y(answer)} r={6} />
            <text x={w - R + 8} y={y(answer) + (Math.abs(y(answer) - y(paper)) < 14 ? 18 : 4)}>answer {num(answer, d)} ({signedPct(done.gap_after)})</text>
          </g>
        )}
        {/* the playhead */}
        {now >= 0 && <line className="hunt-now" x1={nowX} x2={nowX} y1={T - 22} y2={H - B} />}
        <text className="hunt-axis" x={L} y={H - 8}>run 1</text>
        <text className="hunt-axis" x={w - R} y={H - 8} textAnchor="end">run {slots.length}</text>
        {now >= 0 && nowX > L + 44 && nowX < w - R - 44 && <text className="hunt-axis now" x={nowX} y={H - 8} textAnchor="middle">run {now + 1}</text>}
      </svg>
      {tip.node}
      <p className="hunt-key">
        <span><span className="k paper" />the paper’s number</span>
        <span><span className="k released" />the code as released</span>
        <span><span className="k gap" />the gap left: paper to the closest run so far</span>
        <span><span className="k dot survivor" />kept after the screen</span>
        <span><span className="k dot pruned" />dropped</span>
        <span><span className="k dot done" />measured</span>
        <span>Press or drag on the chart to move through the runs.</span>
      </p>
    </div>
  );
}
