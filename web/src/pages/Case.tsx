import { useState } from "react";
import Gauge from "../components/Gauge.tsx";
import SectionNav from "../components/SectionNav.tsx";
import Replay from "../components/Replay.tsx";
import Report from "../components/Report.tsx";
import { useRun, useShowcase } from "../data.ts";
import { href } from "../nav.ts";
import type { GaugeData } from "../types.ts";
import { Loading, Verdict, changesText, signedPct } from "../ui.tsx";
import { PlainLabel, Term, vName, versionStatus } from "../words.tsx";

function Answer({ v, g }: { v: string; g: GaugeData | null }) {
  if (!g) return null;
  return (
    <dl className="facts-list">
      <dt>Verdict</dt><dd><PlainLabel label={g.label} formal /></dd>
      <dt>Change</dt><dd>{Object.keys(g.changes || {}).length ? <code>{changesText(g.changes)}</code> : "no setting changed"}</dd>
      <dt>Gap</dt><dd className="num">{signedPct((g.code - g.paper) / Math.abs(g.paper))}{g.after != null ? ` to ${signedPct((g.after - g.paper) / Math.abs(g.paper))}` : ""}</dd>
      <dt>Runs</dt><dd className="num">{g.runs} in sandboxes, on {vName(v)}</dd>
      {g.figure && <><dt>Number</dt><dd>{g.figure}</dd></>}
    </dl>
  );
}

const SECTIONS: [string, string][] = [["sec-gap", "The gap"], ["sec-versions", "Across versions"], ["sec-investigation", "The investigation"],
  ["sec-report", "The report"]];

const GAUGE_STATES: ["before" | "after", string][] = [["before", "As released"], ["after", "After GapFinder’s change"]];

export default function Case({ slug, query }: { slug: string; query: URLSearchParams }) {
  const { data, error } = useShowcase();
  const c = data?.real.find((x) => x.slug === slug);
  const asked = query.get("v");
  const v = c ? (asked && c.versions[asked] ? asked : c.current) : "";
  const sel = c?.versions[v];
  const { run } = useRun(sel?.id);
  const [show, setShow] = useState<"before" | "after">("after");
  const [play, setPlay] = useState(0);
  if (!data) return <div className="shell"><Loading error={error} /></div>;
  if (!c || !sel) return <div className="shell"><p className="notice spaced">No case called “{slug}”. <a href={href("/cases")}>See every case</a>.</p></div>;
  const g = sel.gauge;
  const hasAfter = Boolean(g && g.after !== null && g.after !== undefined);
  const versions = (data.real_versions || ["c5", "c7"]).filter((x) => c.versions[x]);
  const status = versionStatus(data, v);
  return (
    <div className="shell">
      <a className="crumb" href={href("/cases")}>All cases</a>
      <header className="case-head">
        <h1>{c.title}</h1>
        <div className="meta">
          <Verdict v={sel.verdict} big />
          <span>{c.venue}</span>
          <nav className="toggle" aria-label="Engine version">
            {versions.map((x) => (
              <a key={x} href={href(`/case/${slug}`, { v: x })} aria-current={x === v ? "page" : undefined}
                 title={versionStatus(data, x) || ""}>{vName(x)}</a>
            ))}
          </nav>
          <span>Showing engine <Term k="version">version</Term> {vName(v)}{status ? ` (${status})` : ""}</span>
        </div>
      </header>
      <SectionNav items={SECTIONS} />

      <section className="document" id="sec-gap" aria-labelledby="gap-title">
        <h2 id="gap-title">The gap</h2>
        <div className="two">
          <div>
            {hasAfter && (
              <div className="toggle gauge-toggle" role="group" aria-label="Show the code’s number">
                {GAUGE_STATES.map(([k, t]) => (
                  <button key={k} type="button" aria-pressed={show === k} onClick={() => { setShow(k); setPlay((n) => n + 1); }}>{t}</button>
                ))}
              </div>
            )}
            <Gauge g={g} show={show} playKey={play} label={c.title} />
          </div>
          <div>
            <h3 className="minor-head">The documented cause</h3>
            <p className="claimtext quote">{c.documented_cause}</p>
            <h3 className="minor-head">What GapFinder found</h3>
            <p>{sel.reading}</p>
            <Answer v={v} g={g} />
          </div>
        </div>
      </section>

      <section className="document" id="sec-versions" aria-labelledby="versions-title">
        <h2 id="versions-title">Across versions</h2>
        <ol className="timeline">
          {versions.map((x) => (
            <li key={x}>
              <div className="v">{vName(x)}<small>{versionStatus(data, x)}</small></div>
              <div>
                <Verdict v={c.versions[x].verdict} />
                <p>{c.versions[x].reading} {x !== v && <a href={href(`/case/${slug}`, { v: x })}>Show this run</a>}</p>
              </div>
            </li>
          ))}
        </ol>
      </section>

      <section className="document" id="sec-investigation" aria-labelledby="inv-title">
        <h2 id="inv-title">The investigation</h2>
        {run ? <Replay run={run} key={run.id} /> : <Loading what="Loading the recorded run…" />}
      </section>
      <section className="document" id="sec-report" aria-label="The full report">
        {run ? <Report run={run} /> : <Loading what="Loading the report…" />}
      </section>
      <p className="notice spaced"><Term k="posthoc">Post-hoc</Term> rerun. The cause is documented, and the engine’s fixes since
        {" "}{vName(versions[0])} were found on these very runs, so this is a demonstration, not evidence.</p>
    </div>
  );
}
