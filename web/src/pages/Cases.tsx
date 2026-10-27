import { useMemo, useState } from "react";
import { useShowcase } from "../data.ts";
import { href } from "../nav.ts";
import type { RealCase, VerdictWord } from "../types.ts";
import { Loading, Verdict, signedPct } from "../ui.tsx";
import { Term, currentVersion, vName, versionStatus } from "../words.tsx";

const RANK: Record<VerdictWord, number> = { found: 0, partial: 1, no_gap: 2, missed: 3 };
type Key = "verdict" | "paper" | "gap";

const HEAD = (
  <>
    <h1>Cases</h1>
    <p className="lede">Sixteen papers whose reproduction gap has a documented cause, each re-run on the engine’s later versions.</p>
  </>
);

// a column header that sorts the table, saying which way it is sorted
function SortHead({ k, cur, asc, onSort, children }: { k: Key; cur: Key; asc: boolean; onSort: (k: Key) => void; children: string }) {
  return (
    <th scope="col" aria-sort={k === cur ? (asc ? "ascending" : "descending") : "none"}>
      <button type="button" className="sort" onClick={() => onSort(k)}>{children}<span aria-hidden="true">{k === cur ? (asc ? " ↓" : " ↑") : ""}</span></button>
    </th>
  );
}

const gapOf = (p: RealCase): number | null => {
  const g = p.versions[p.current]?.gauge;
  return g ? (g.code - g.paper) / Math.abs(g.paper) : null;
};

export default function Cases() {
  const { data, error } = useShowcase();
  const [key, setKey] = useState<Key>("verdict");
  const [asc, setAsc] = useState(true);
  const [q, setQ] = useState("");
  const rows = useMemo(() => {
    const words = q.toLowerCase().split(/\s+/).filter(Boolean);
    const match = (p: RealCase) => words.every((w) => `${p.title} ${p.venue} ${p.documented_cause} ${p.versions[p.current]?.reading}`.toLowerCase().includes(w));
    const cmp = (a: RealCase, b: RealCase) => (key === "paper" ? a.title.localeCompare(b.title)
      : key === "gap" ? Math.abs(gapOf(b) ?? 0) - Math.abs(gapOf(a) ?? 0)
      : RANK[a.versions[a.current].verdict] - RANK[b.versions[b.current].verdict]);
    const out = (data?.real || []).filter(match).sort(cmp);
    return asc ? out : out.reverse();
  }, [data, key, asc, q]);
  if (!data) return <div className="shell"><section className="hero page-head">{HEAD}<Loading error={error} /></section></div>;
  const versions = (data.real_versions || ["c5", "c7"]).filter((v) => data.real.some((p) => p.versions[v]));
  const sortBy = (k: Key) => { if (k === key) setAsc((x) => !x); else { setKey(k); setAsc(true); } };
  const head = { cur: key, asc, onSort: sortBy };
  return (
    <div className="shell">
      <section className="hero page-head">
        {HEAD}
        <p className="notice"><Term k="posthoc">Post-hoc</Term>: these causes were known, and the engine’s fixes since {vName(versions[0])} were
          found on these runs. Read them as a demonstration of what the current engine does, not as evidence of how it does on new papers.</p>
      </section>
      <div className="table-tools spaced">
        <label className="find">
          <span className="visually-hidden">Find a paper</span>
          <input type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Find a paper, a venue or a cause…" />
        </label>
        <span className="status-line" aria-live="polite">{rows.length === data.real.length ? `${rows.length} papers` : `${rows.length} of ${data.real.length} papers`}</span>
      </div>
      <div className="ledger-wrap">
        <table>
          <thead><tr>
            <SortHead k="paper" {...head}>Paper</SortHead><th scope="col">Documented cause</th>
            <th scope="col">What the current version ({vName(currentVersion(data))}) found</th>
            <SortHead k="gap" {...head}>Gap as released</SortHead>
            <SortHead k="verdict" {...head}>{`Verdict, ${vName(currentVersion(data))}`}</SortHead>
            {versions.filter((v) => v !== currentVersion(data)).map((v) => <th scope="col" key={v}><span title={versionStatus(data, v) || ""}>{vName(v)}</span></th>)}
          </tr></thead>
          <tbody>
            {rows.map((p) => {
              const g = gapOf(p);
              return (
                <tr key={p.slug} className="link">
                  <td className="paper-cell"><a href={href(`/case/${p.slug}`)}>{p.title}</a><small>{p.venue}</small></td>
                  <td className="cause">{p.documented_cause}</td>
                  <td className="reading">{p.versions[p.current].reading}</td>
                  <td className="num nowrap">{g === null ? "n/a" : signedPct(g)}</td>
                  <td><Verdict v={p.versions[p.current].verdict} short /></td>
                  {versions.filter((v) => v !== currentVersion(data)).map((v) => (
                    <td key={v}>{p.versions[v] ? <Verdict v={p.versions[v].verdict} short /> : <span className="muted">not run</span>}</td>
                  ))}
                </tr>
              );
            })}
            {!rows.length && <tr><td colSpan={5 + versions.length} className="muted">No paper matches “{q}”.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}
