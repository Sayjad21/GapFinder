import { useEffect, useRef, useState } from "react";
import { href } from "../nav.ts";
import type { RealCase } from "../types.ts";
import { digits, num, prefersReducedMotion, signedPct } from "../ui.tsx";
import Gauge from "./Gauge.tsx";

const AUTO_MS = 1800;

// The home page's instrument: one solved case at a time, shown first as released (the gap the paper and the code
// leave), then, once it has been on screen a moment or when the viewer asks, with GapFinder's change applied. The
// sentence under the gauge says what the current state shows. Moves on its own only once per case, never under
// reduced motion, and never after the viewer has used the toggle.
export default function HeroInstrument({ cases, short }: { cases: RealCase[]; short: Record<string, string> }) {
  const [pick, setPick] = useState(cases[0]?.slug);
  const [show, setShow] = useState<"before" | "after">("before");
  const [touched, setTouched] = useState(false);
  const box = useRef<HTMLDivElement>(null);
  const c = cases.find((x) => x.slug === pick) || cases[0];
  const cur = c?.versions[c.current];
  const g = cur?.gauge;

  useEffect(() => {
    if (touched || show !== "before" || prefersReducedMotion() || !box.current || typeof IntersectionObserver === "undefined") return undefined;
    let timer: ReturnType<typeof setTimeout> | undefined;
    const io = new IntersectionObserver(([e]) => {
      clearTimeout(timer);
      if (e.isIntersecting) timer = setTimeout(() => setShow("after"), AUTO_MS);
    }, { threshold: 0.6 });
    io.observe(box.current);
    return () => { io.disconnect(); clearTimeout(timer); };
  }, [pick, show, touched]); // oxlint-disable-line react/exhaustive-effect-dependencies -- re-armed for each case

  if (!c || !cur || !g) return null;
  const d = digits([g.paper, g.code, g.after ?? g.code]);
  const before = (g.code - g.paper) / Math.abs(g.paper);
  const after = g.after != null ? (g.after - g.paper) / Math.abs(g.paper) : null;
  const choose = (slug: string) => { setPick(slug); setShow("before"); };
  const toggle = (k: "before" | "after") => { setTouched(true); setShow(k); };
  return (
    <div className="hero-instrument" ref={box}>
      <div className="instrument-bar">
        <div className="case-switch" role="group" aria-label="Choose a case">
          {cases.map((x) => (
            <button key={x.slug} type="button" className="seg" aria-pressed={x.slug === c.slug} onClick={() => choose(x.slug)}>
              {short[x.slug] || x.title}
            </button>
          ))}
        </div>
        {after !== null && (
          <div className="toggle" role="group" aria-label="Show the code’s number">
            <button type="button" aria-pressed={show === "before"} onClick={() => toggle("before")}>As released</button>
            <button type="button" aria-pressed={show === "after"} onClick={() => toggle("after")}>After GapFinder’s change</button>
          </div>
        )}
      </div>
      <Gauge key={c.slug} g={g} show={show} label={c.title} />
      <div className="closed-by" aria-live="polite">
        <div>
          {show === "before" || after === null ? (
            <p className="what">As released, the code gives <b>{num(g.code, d)}</b> where the paper reports <b>{num(g.paper, d)}</b>: a gap
              of {signedPct(before)}, beyond the run-to-run noise of ±{((g.band || 0) * 100).toFixed(1)}%.</p>
          ) : (
            <p className="what">{cur.reading} The gap shrinks from {signedPct(before)} to <b>{signedPct(after)}</b>.</p>
          )}
          <p className="small">{c.title}, {c.venue}. Documented cause: {c.documented_cause} {g.runs} runs in sandboxes.</p>
        </div>
        <a className="btn quiet" href={href(`/case/${c.slug}`)}>Open this case</a>
      </div>
    </div>
  );
}
