import { useEffect, useMemo, useRef, useState } from "react";
import { href } from "../nav.ts";
import type { RealCase, Showcase, VerdictWord } from "../types.ts";
import { Glyph, VERDICT, VERDICT_SHORT, prefersReducedMotion, signedPct } from "../ui.tsx";
import { vName, versionStatus } from "../words.tsx";

// The Gap Field: every real paper's gap on one shared rule, the paper's number at zero. Each gap is a highlighter stroke
// from the paper to the code as released; with a version's answer applied, each stroke shrinks to what that version
// left, one after another, and a faint tick stays where it started. A miss keeps its full stroke. The rule is
// logarithmic away from zero, so a 1% gap and a 75% one both read. Every row links to its case.

const K = 0.01; // the scale is linear inside ±1% and logarithmic beyond
const f = (g: number) => Math.sign(g) * Math.log1p(Math.abs(g) / K);
const TICKS = [-0.5, -0.2, -0.1, -0.05, -0.02, -0.01, 0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5];
const STAGGER = 55, DUR = 750;
const RANK: Record<VerdictWord, number> = { found: 0, partial: 1, no_gap: 2, missed: 3 };

interface Row { c: RealCase; verdict: VerdictWord | null; before: number | null; after: number | null; band: number; reading: string }

function rows(data: Showcase, v: string): Row[] {
  return data.real.map((c) => {
    const r = c.versions[v];
    const g = r?.gauge;
    const rel = (x: number) => (g ? (x - g.paper) / Math.abs(g.paper) : 0);
    return { c, verdict: r?.verdict ?? null, before: g ? rel(g.code) : null, after: g && g.after != null ? rel(g.after) : null,
             band: g?.band ?? 0, reading: r?.reading ?? "" };
  });
}

export default function GapField({ data }: { data: Showcase }) {
  const versions = (data.real_versions || ["c5", "c7"]).filter((v) => data.real.filter((p) => p.versions[v]).length >= data.real.length / 2);
  const [v, setV] = useState(data.tally_version || versions[versions.length - 1]);
  const [show, setShow] = useState<"before" | "after">("before");
  const [sort, setSort] = useState<"gap" | "verdict">("gap");
  const [touched, setTouched] = useState(false);
  const [clock, setClock] = useState(0); // ms into the closing animation
  const box = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const [w, setW] = useState(640);
  useEffect(() => {
    if (!track.current || typeof ResizeObserver === "undefined") return undefined;
    const ro = new ResizeObserver(([e]) => setW(Math.max(260, Math.round(e.contentRect.width))));
    ro.observe(track.current);
    return () => ro.disconnect();
  }, []);

  const all = useMemo(() => rows(data, v), [data, v]);
  const shown = useMemo(() => [...all].sort((a, b) => (sort === "verdict" ? (a.verdict ? RANK[a.verdict] : 9) - (b.verdict ? RANK[b.verdict] : 9) : 0)
    || Math.abs(b.before ?? 0) - Math.abs(a.before ?? 0)), [all, sort]);
  const total = STAGGER * shown.length + DUR;

  // play the closing: on first sight (unless reduced motion or the viewer already chose), and on every version switch.
  // As released, nothing has closed; under reduced motion, everything has.
  const reduced = prefersReducedMotion();
  const t = show !== "after" ? 0 : reduced ? total : clock;
  useEffect(() => {
    if (show !== "after" || reduced) return undefined;
    let raf = 0;
    const start = performance.now();
    const tick = (now: number) => { const e = now - start; setClock(e); if (e < total) raf = requestAnimationFrame(tick); };
    raf = requestAnimationFrame((now) => { setClock(0); tick(now); });
    return () => cancelAnimationFrame(raf);
  }, [show, v, total, reduced]); // oxlint-disable-line react/exhaustive-effect-dependencies -- replayed on each version switch
  useEffect(() => {
    if (touched || show !== "before" || prefersReducedMotion() || !box.current || typeof IntersectionObserver === "undefined") return undefined;
    let timer: ReturnType<typeof setTimeout> | undefined;
    const io = new IntersectionObserver(([e]) => {
      clearTimeout(timer);
      if (e.isIntersecting) timer = setTimeout(() => setShow("after"), 700);
    }, { threshold: 0.35 });
    io.observe(box.current);
    return () => { io.disconnect(); clearTimeout(timer); };
  }, [touched, show]);

  // the rule: from the largest gap on the left to the largest on the right, through zero
  const vals = all.flatMap((r) => [r.before ?? 0, r.after ?? 0, -r.band, r.band]);
  const lo = f(Math.min(-0.02, ...vals) * 1.15), hi = f(Math.max(0.02, ...vals) * 1.15);
  const PL = 10, PR = 52; // room on the right for the last stroke's figure
  const x = (g: number) => PL + ((f(g) - lo) / (hi - lo)) * (w - PL - PR);
  const x0 = x(0);

  const right = all.filter((r) => r.verdict === "found" || r.verdict === "no_gap").length;
  const ran = all.filter((r) => r.verdict).length;
  const closed = all.filter((r) => (r.after !== null ? Math.abs(r.after) <= r.band : r.verdict === "no_gap")).length;
  const missed = all.filter((r) => r.verdict === "missed").length;

  return (
    <div className="gapfield" ref={box}>
      <div className="field-bar">
        <span className="toggle" role="group" aria-label="Engine version">
          {versions.map((ver) => (
            <button key={ver} type="button" aria-pressed={ver === v} title={versionStatus(data, ver) || ""}
                    onClick={() => { setTouched(true); setV(ver); }}>{vName(ver)}{ver === data.tally_version ? " (current)" : ""}</button>
          ))}
        </span>
        <span className="toggle" role="group" aria-label="Show the gaps">
          <button type="button" aria-pressed={show === "before"} onClick={() => { setTouched(true); setShow("before"); }}>As released</button>
          <button type="button" aria-pressed={show === "after"} onClick={() => { setTouched(true); setShow("after"); }}>After {vName(v)}’s answers</button>
        </span>
        <span className="toggle" role="group" aria-label="Order">
          <button type="button" aria-pressed={sort === "gap"} onClick={() => setSort("gap")}>Largest gap first</button>
          <button type="button" aria-pressed={sort === "verdict"} onClick={() => setSort("verdict")}>By verdict</button>
        </span>
      </div>
      <div className="field">
        <div className="field-row field-axis" aria-hidden="true">
          <span />
          <div className="field-track" ref={track}>
            <svg width={w} height={26}>
              {TICKS.filter((g) => f(g) > lo && f(g) < hi).map((g) => (
                <text key={g} x={x(g)} y={16} textAnchor="middle" className={g === 0 ? "zero" : ""}>{g === 0 ? "the paper" : signedPct(g, 0)}</text>
              ))}
            </svg>
          </div>
          <span />
        </div>
        <ol className="field-rows">
          {shown.map((r, k) => {
            const p = r.after === null ? 0 : Math.max(0, Math.min(1, (t - k * STAGGER) / DUR));
            const ease = 1 - (1 - p) ** 3;
            const cur = r.before === null ? null : r.after === null ? r.before : r.before + (r.after - r.before) * ease;
            const label = r.before === null ? `${r.c.title}: not run on ${vName(v)}.`
              : `${r.c.title}: ${signedPct(r.before)} as released${r.after !== null ? `, ${signedPct(r.after)} after ${vName(v)}’s change` : ", unchanged"}. ${r.verdict ? VERDICT[r.verdict] : ""}.`;
            const xe = cur === null ? x0 : x(cur);
            const left = Math.min(x0, xe), wd = Math.abs(xe - x0);
            return (
              <li key={r.c.slug} className={r.verdict ? "" : "not-run"}>
                <a className="field-row" href={href(`/case/${r.c.slug}`, { v: v !== r.c.current ? v : undefined })} aria-label={label} title={r.reading}>
                  <span className="field-name">{r.c.title}</span>
                  <span className="field-track">
                    <svg width={w} height={28} aria-hidden="true">
                      {r.band > 0 && <rect className="field-band" x={x(-r.band)} y={4} width={x(r.band) - x(-r.band)} height={20} />}
                      {cur !== null && wd > 0.5 && (
                        <path className="field-gap" d={`M${left + Math.min(4, wd / 3)},7 L${left + wd},7 L${left + wd - Math.min(4, wd / 3)},21 L${left},21 Z`} />
                      )}
                      {r.before !== null && p > 0 && <line className="field-ghost" x1={x(r.before)} x2={x(r.before)} y1={5} y2={23} />}
                      <line className="field-zero" x1={x0} x2={x0} y1={0} y2={28} />
                      {cur !== null && (
                        <text className="field-val" x={xe + (cur < 0 ? -6 : 6)} y={18} textAnchor={cur < 0 ? "end" : "start"}>{signedPct(cur)}</text>
                      )}
                    </svg>
                  </span>
                  <span className={`field-verdict verdict ${r.verdict || "none"}`}>
                    <span className="glyph"><Glyph v={r.verdict} /></span>{r.verdict ? VERDICT_SHORT[r.verdict] : "not run"}
                  </span>
                </a>
              </li>
            );
          })}
        </ol>
      </div>
      <p className="small field-sum">
        On {vName(v)}: {right} of {ran} right (the documented cause found, or correctly no gap), {closed} gaps within the noise
        {show === "after" ? " after its answers" : " once its answers are applied"}, {missed} missed. Each stroke is the gap from the paper’s number;
        the shaded band is that paper’s run-to-run noise. Select a paper to open its case.
      </p>
    </div>
  );
}
