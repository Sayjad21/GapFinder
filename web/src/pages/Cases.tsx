import { useShowcase } from "../data.ts";
import { href } from "../nav.ts";
import type { VerdictWord } from "../types.ts";
import { Loading, Verdict } from "../ui.tsx";
import { Term, currentVersion, vName, versionStatus } from "../words.tsx";

const ORDER: Record<VerdictWord, number> = { found: 0, partial: 1, no_gap: 2, missed: 3 };

const HEAD = (
  <>
    <h1>Cases</h1>
    <p className="lede">Sixteen papers whose reproduction gap has a documented cause, each re-run on the engine’s later versions.</p>
  </>
);

export default function Cases() {
  const { data, error } = useShowcase();
  if (!data) return <div className="shell"><section className="hero page-head">{HEAD}<Loading error={error} /></section></div>;
  const versions = (data.real_versions || ["c5", "c7"]).filter((v) => data.real.some((p) => p.versions[v]));
  const rows = [...data.real].sort((a, b) => ORDER[a.versions[a.current].verdict] - ORDER[b.versions[b.current].verdict]);
  return (
    <div className="shell">
      <section className="hero page-head">
        {HEAD}
        <p className="notice"><Term k="posthoc">Post-hoc</Term>: these causes were known, and the engine’s fixes since {vName(versions[0])} were
          found on these runs. Read them as a demonstration of what the current engine does, not as evidence of how it does on new papers.</p>
      </section>
      <div className="ledger-wrap spaced">
        <table>
          <thead><tr>
            <th scope="col">Paper</th><th scope="col">Documented cause</th><th scope="col">What the current version ({vName(currentVersion(data))}) found</th>
            {versions.map((v) => <th scope="col" key={v}><span title={versionStatus(data, v) || ""}>{vName(v)}</span></th>)}
          </tr></thead>
          <tbody>
            {rows.map((p) => (
              <tr key={p.slug} className="link">
                <td className="paper-cell"><a href={href(`/case/${p.slug}`)}>{p.title}</a><small>{p.venue}</small></td>
                <td className="cause">{p.documented_cause}</td>
                <td className="reading">{p.versions[p.current].reading}</td>
                {versions.map((v) => <td key={v}>{p.versions[v] ? <Verdict v={p.versions[v].verdict} short /> : <span className="muted">not run</span>}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
