import { useRef, useState, useEffect } from "react";
import { Glyph, VERDICT, Verdict, useTooltip } from "./ui.jsx";

const ORDER = ["found", "partial", "no_gap", "missed"];
const GOOD = new Set(["found", "no_gap"]);
const VERSION_NOTE = { c5: "adopted 2026-10-23", c7: "frozen 2026-10-26", c8: "frozen 2026-10-26" };

// Every real paper, one square each, per engine version: a part-to-whole that keeps each paper clickable.
export function VersionStrips({ real, versions = ["c5", "c7", "c8"] }) {
  const tip = useTooltip();
  const [table, setTable] = useState(false);
  const rows = versions.map((v) => {
    const cells = real.map((p) => ({ p, r: p.versions[v] })).filter((c) => c.r && c.r.verdict);
    cells.sort((a, b) => ORDER.indexOf(a.r.verdict) - ORDER.indexOf(b.r.verdict));
    return { v, cells };
  }).filter((r) => r.cells.length);
  const n = real.length;
  return (
    <div className="record">
      <div className="legend-row" aria-label="Legend">
        {ORDER.map((v) => <Verdict key={v} v={v} />)}
      </div>
      {rows.map(({ v, cells }) => {
        const good = cells.filter((c) => GOOD.has(c.r.verdict)).length;
        return (
          <div className="strip-row" key={v}>
            <div className="ver">{v}<small>{cells.length < n ? `${cells.length} of ${n} papers run` : VERSION_NOTE[v] || ""}</small></div>
            <div className="strip" style={{ "--n": n }} role="list" aria-label={`${v}: one square per paper`}>
              {cells.map(({ p, r }) => (
                <a key={p.slug} role="listitem" className={`cell ${r.verdict}`} href={`#/case/${p.slug}`}
                   aria-label={`${p.title}: ${VERDICT[r.verdict]}`}
                   onPointerEnter={(e) => tip.show(e, <><b>{p.title}</b>{VERDICT[r.verdict]} on {v}. {r.reading}</>)}
                   onPointerLeave={tip.hide} onFocus={(e) => tip.show(e, <><b>{p.title}</b>{VERDICT[r.verdict]} on {v}.</>)} onBlur={tip.hide}>
                  <Glyph v={r.verdict} />
                </a>
              ))}
            </div>
            <div className="count"><b>{good}</b> of {cells.length} right</div>
          </div>
        );
      })}
      {tip.node}
      <div>
        <button type="button" className="btn quiet" aria-expanded={table} onClick={() => setTable((t) => !t)}>
          {table ? "Hide the table" : "Show as a table"}
        </button>
        {table && (
          <div className="ledger-wrap" style={{ marginTop: 16 }}>
            <table>
              <thead><tr><th scope="col">Paper</th>{rows.map(({ v }) => <th scope="col" key={v}>{v}</th>)}</tr></thead>
              <tbody>
                {real.map((p) => (
                  <tr key={p.slug}>
                    <td><a href={`#/case/${p.slug}`}>{p.title}</a></td>
                    {rows.map(({ v }) => <td key={v}>{p.versions[v]?.verdict ? <Verdict v={p.versions[v].verdict} short /> : <span className="muted">not run</span>}</td>)}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

// The planted curriculum: the share of fresh planted gaps each frozen version found, one dot per fresh batch.
export function PlantedChart({ totals }) {
  const ref = useRef(null);
  const [w, setW] = useState(640);
  useEffect(() => {
    if (!ref.current) return undefined;
    const ro = new ResizeObserver(([e]) => setW(Math.max(300, Math.round(e.contentRect.width))));
    ro.observe(ref.current);
    return () => ro.disconnect();
  }, []);
  const tip = useTooltip();
  const versions = [...new Set(totals.map((t) => t.version))].sort((a, b) => +a.slice(1) - +b.slice(1));
  const H = 240, top = 16, bottom = 40, left = 40, right = 12;
  const x = (v) => left + ((versions.indexOf(v) + 0.5) / versions.length) * (w - left - right);
  const yMax = 0.6;
  const y = (s) => top + (1 - s / yMax) * (H - top - bottom);
  const grid = [0, 0.2, 0.4, 0.6];
  const pts = totals.filter((t) => t.gaps > 0).map((t) => ({ ...t, s: t.found / t.gaps }));
  const byVer = versions.map((v) => {
    const ps = pts.filter((p) => p.version === v);
    const f = ps.reduce((a, p) => a + p.found, 0), g = ps.reduce((a, p) => a + p.gaps, 0);
    return { v, s: g ? f / g : null, f, g, adopted: ps.every((p) => p.adopted) };
  });
  const jitter = (p) => {
    const same = pts.filter((q) => q.version === p.version);
    const i = same.indexOf(p);
    return (i - (same.length - 1) / 2) * 14;
  };
  return (
    <div className="chart" ref={ref}>
      <svg width={w} height={H} viewBox={`0 0 ${w} ${H}`} role="img"
           aria-label={`Share of planted gaps found per version: ${byVer.map((b) => `${b.v} ${b.f} of ${b.g}`).join("; ")}`}>
        <g className="grid">
          {grid.map((s) => <line key={s} x1={left} x2={w - right} y1={y(s)} y2={y(s)} />)}
        </g>
        {grid.map((s) => <text key={s} className="axis-label" x={left - 8} y={y(s) + 4} textAnchor="end">{Math.round(s * 100)}%</text>)}
        {versions.map((v) => <text key={v} className="axis-label" x={x(v)} y={H - 14} textAnchor="middle">{v}</text>)}
        {byVer.map((b) => b.s !== null && (
          <line key={`m${b.v}`} className="mean" x1={x(b.v) - 22} x2={x(b.v) + 22} y1={y(b.s)} y2={y(b.s)} />
        ))}
        {pts.map((p) => (
          <g key={`${p.version}-${p.seed}`}>
            <circle className={`dot${p.adopted ? "" : " rejected"}`} cx={x(p.version) + jitter(p)} cy={y(p.s)} r={5} />
            <circle className="hit" cx={x(p.version) + jitter(p)} cy={y(p.s)} r={14} tabIndex={0}
                    aria-label={`${p.version}, seed ${p.seed}: ${p.found} of ${p.gaps} planted gaps found`}
                    onPointerEnter={(e) => tip.show(e, <><b>{p.found} of {p.gaps}</b>planted gaps found by {p.version} on seed {p.seed}{p.confidently_wrong ? `; ${p.confidently_wrong} confidently wrong` : "; none confidently wrong"}{p.adopted ? "" : ". Not adopted."}</>)}
                    onPointerLeave={tip.hide} onFocus={(e) => tip.show(e, <><b>{p.found} of {p.gaps}</b>{p.version}, seed {p.seed}</>)} onBlur={tip.hide} />
          </g>
        ))}
      </svg>
      {tip.node}
      <div className="gauge-caption">
        <span className="key"><svg width="12" height="12" aria-hidden="true"><circle cx="6" cy="6" r="4.5" fill="var(--proof)" /></svg>one fresh batch, version adopted</span>
        <span className="key"><svg width="12" height="12" aria-hidden="true"><circle cx="6" cy="6" r="4" fill="none" stroke="var(--proof)" strokeWidth="2" /></svg>one fresh batch, version not adopted</span>
        <span className="key"><span className="sw paper" />pooled over the version’s batches</span>
      </div>
    </div>
  );
}
