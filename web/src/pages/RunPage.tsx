import Gauge from "../components/Gauge.tsx";
import SectionNav from "../components/SectionNav.tsx";
import Replay from "../components/Replay.tsx";
import Report from "../components/Report.tsx";
import { gaugeOf, useRun } from "../data.ts";
import { href } from "../nav.ts";
import { Loading, changesText } from "../ui.tsx";
import { PlainLabel, PlantedChange, Term, vName } from "../words.tsx";

// any recorded run: a planted case or a GapBench task
export default function RunPage({ id }: { id: string }) {
  const { run, error } = useRun(id);
  if (error) return <div className="shell"><p className="notice spaced" role="alert">No recorded run “{id}”. <a href={href("/synthetic")}>Back to the cases with known answers</a>.</p></div>;
  if (!run) return <div className="shell"><Loading what="Loading the recorded run…" /></div>;
  const m = run.meta || {};
  const g = gaugeOf(run.report);
  return (
    <div className="shell">
      <a className="crumb" href={href("/synthetic", m.group === "gapbench" ? { tab: "gapbench" } : {})}>Cases with known answers</a>
      <header className="case-head">
        <h1>{m.title || run.report?.paper || id}</h1>
        <div className="meta">
          {m.version && <span>Engine <Term k="version">version</Term> {vName(m.version)}{m.seed ? <>, <Term k="batch">fresh batch</Term> {m.seed}</> : ""}</span>}
          {g?.label && <PlainLabel label={g.label} formal />}
        </div>
      </header>
      <SectionNav items={[["sec-gap", "The gap"], ["sec-investigation", "The investigation"], ["sec-report", "The report"]]} />
      <section className="document" id="sec-gap" aria-labelledby="gap-title">
        <h2 id="gap-title">The gap</h2>
        <div className="two">
          <div>{g ? <Gauge g={g} label={m.title} /> : <p className="muted">This run records no gap on its target.</p>}</div>
          <div>
            {m.planted && <><h3 className="minor-head">What was <Term k="planted">planted</Term></h3>
              <p>{m.planted.length ? m.planted.map((x) => <PlantedChange key={x} text={x} />) : <>Nothing: a <Term k="control">control</Term>, where the right answer is no gap.</>}</p></>}
            {m.hidden && <><h3 className="minor-head">The hidden setting</h3><p><code>{changesText(m.hidden)}</code></p></>}
            <h3 className="minor-head">What GapFinder found</h3>
            <p>{g && Object.keys(g.changes || {}).length ? <code>{changesText(g.changes)}</code> : "No change: it reported the number as reproduced."}</p>
            {m.note && <p className="small">{m.note}</p>}
          </div>
        </div>
      </section>
      <section className="document" id="sec-investigation" aria-labelledby="inv-title"><h2 id="inv-title">The investigation</h2><Replay run={run} key={run.id} /></section>
      <section className="document" id="sec-report" aria-label="The full report"><Report run={run} /></section>
    </div>
  );
}
