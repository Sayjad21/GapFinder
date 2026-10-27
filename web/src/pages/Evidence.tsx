import { useState } from "react";
import { PlantedChart, VersionStrips } from "../components/Record.tsx";
import Scoreboard from "../components/Scoreboard.tsx";
import { useShowcase } from "../data.ts";
import type { Showcase } from "../types.ts";
import { Loading } from "../ui.tsx";
import { Term, vName, versionStatus } from "../words.tsx";

const KIND_SHORT: Record<string, string> = { setting: "settings", scale: "scale", data: "data cuts", code: "code", reporting: "reporting" };

function PlantedTable({ data }: { data: Showcase }) {
  const [open, setOpen] = useState(false);
  const rows = [...data.planted_totals].sort((a, b) => a.seed - b.seed || +a.version.slice(1) - +b.version.slice(1));
  return (
    <div className="spaced-s">
      <button type="button" className="btn quiet" aria-expanded={open} onClick={() => setOpen((x) => !x)}>
        {open ? "Hide the table" : `Show every batch as a table (${rows.length})`}
      </button>
      {open && (
        <div className="ledger-wrap spaced-s">
          <table>
            <thead><tr><th scope="col">Version</th><th scope="col" className="num">Fresh batch</th><th scope="col" className="num">Gaps found</th>
              <th scope="col" className="num">Confidently wrong</th><th scope="col" className="num">Controls left alone</th><th scope="col">Found, by kind</th></tr></thead>
            <tbody>
              {rows.map((t) => (
                <tr key={`${t.version}-${t.seed}`}>
                  <td>{vName(t.version)}{t.adopted ? "" : <span className="muted"> (not adopted)</span>}</td><td className="num">{t.seed}</td>
                  <td className="num">{t.found} of {t.gaps}</td><td className="num">{t.confidently_wrong}</td>
                  <td className="num">{t.controls ? `${t.controls_correct} of ${t.controls}` : "none"}</td>
                  <td className="small">{Object.entries(t.by_kind).map(([k, [f, n]]) => `${KIND_SHORT[k] || k} ${f} of ${n}`).join(", ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

const HEAD = (
  <section className="hero page-head">
    <h1>The evidence</h1>
    <p className="lede">Every measurement, with what it can and can’t show. Only the <Term k="sealed">sealed blind papers</Term> are
      clean evidence; the rest were made while the engine was being built.</p>
  </section>
);

export default function Evidence() {
  const { data, error } = useShowcase();
  if (!data) return <div className="shell">{HEAD}<Loading error={error} /></div>;
  return (
    <div className="shell">
      {HEAD}
      <section className="section" aria-labelledby="ev-real">
        <header><h2 id="ev-real">Real papers, re-run post-hoc</h2>
          <p>Sixteen papers with documented causes. A demonstration: the fixes were found on them.</p></header>
        <VersionStrips data={data} />
      </section>
      <section className="section" aria-labelledby="ev-planted">
        <header><h2 id="ev-planted">Planted gaps on fresh batches</h2>
          <p>Each <Term k="batch">fresh batch</Term> is made after the version is frozen, from operators the engine doesn’t share.
            A version is adopted only when it is no worse on a fresh batch.</p></header>
        <PlantedChart totals={data.planted_totals} />
        <PlantedTable data={data} />
      </section>
      <section className="section" aria-labelledby="ev-dev">
        <header><h2 id="ev-dev">The development suite</h2>
          <p><Term k="gapbench">GapBench</Term> tasks run locally at no cost, two replicates per version. With identical code the count
            moves by about five between replicates, so the suite checks that nothing broke; it can’t rank close versions.</p></header>
        <div className="ledger-wrap"><table>
          <thead><tr><th scope="col">Version</th><th scope="col">Standing</th><th scope="col" className="num">Runs with a cause found (of 138)</th></tr></thead>
          <tbody>{data.dev_suite.map((d) => (
            <tr key={d.version}><td>{vName(d.version)}</td><td>{versionStatus(data, d.version) || (d.adopted === false ? "not adopted" : "adopted")}</td>
              <td className="num">{d.correct}</td></tr>
          ))}</tbody>
        </table></div>
      </section>
      <section className="section" aria-labelledby="ev-agent">
        <header><h2 id="ev-agent">Against a general coding agent</h2>
          <p>The same inputs and dollar cap on GapBench’s sealed tasks.</p></header>
        <Scoreboard />
      </section>
    </div>
  );
}
