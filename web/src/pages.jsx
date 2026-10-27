import { useEffect, useRef, useState } from "react";
import { api } from "./api.js";
import Gauge from "./Gauge.jsx";
import HeroInstrument from "./Hero.jsx";
import { href } from "./nav.js";
import { PlantedChart, VersionStrips } from "./Record.jsx";
import Replay from "./Replay.jsx";
import Report from "./Report.jsx";
import { Loading, Verdict, changesText, digits, num, prefersReducedMotion, signedPct, useShowcase } from "./ui.jsx";
import { GLOSSARY, PlainLabel, PlantedChange, Term, currentVersion, vName, versionStatus } from "./words.jsx";

const HERO_CASES = ["fastgcn-v15", "sdcn", "gcn-attack", "fair-clustering"];
const SHORT = { "gcn-attack": "Topology attack", sdcn: "SDCN", "fastgcn-v15": "FastGCN", "fair-clustering": "Fair Clustering" };

function useRun(id) {
  const [run, setRun] = useState(null);
  const [error, setError] = useState(null);
  useEffect(() => {
    if (!id) return;
    setRun(null); setError(null);
    api.run(id).then(setRun).catch(setError);
  }, [id]);
  return { run, error };
}

// a run’s gauge, computed from its report when the manifest has none
function gaugeOf(report) {
  const c = (report?.claims || []).find((x) => !x.target?.held_out);
  if (!c || c.gap_before === null || c.gap_before === undefined) return null;
  const pv = c.target.paper_value;
  const moved = c.gap_after !== null && c.gap_after !== undefined && Math.abs(c.gap_after - c.gap_before) > 1e-9;
  return { paper: pv, code: pv * (1 + c.gap_before), after: moved ? pv * (1 + c.gap_after) : null, band: c.band,
           metric: c.target.metric, figure: c.target.figure, changes: c.changes, label: c.attribution?.confidence_label, runs: report.runs };
}

// ------------------------------------------------------------------ home
// the investigation the home page plays: the longest of the hero cases, so the replay has a search to show
const WATCH_CASE = "fastgcn-v15";

function Watch({ c }) {
  const sel = c.versions[c.current];
  const { run, error } = useRun(sel.id);
  const g = sel.gauge;
  return (
    <>
      <header>
        <h2 id="watch-title">Watch one investigation</h2>
        <p>{c.title}’s released code gives {num(g.code, digits([g.paper, g.code]))} where the paper reports {num(g.paper, digits([g.paper, g.code]))}. This is the recorded search, all {g.runs} runs:
          it measures the noise first, screens each setting from one saved checkpoint, then repeats and combines what moved the
          number. The gauge follows the closest run, and ends on the answer.</p>
      </header>
      <div className="document">
        {run ? <Replay run={run} key={run.id} /> : <Loading error={error} what="Loading the recorded run…" />}
      </div>
    </>
  );
}

export function Home() {
  const { data, error } = useShowcase();
  const watch = useRef(null);
  if (!data) return <div className="shell"><Loading error={error} /></div>;
  const cases = HERO_CASES.map((s) => data.real.find((r) => r.slug === s)).filter(Boolean);
  const watchCase = data.real.find((r) => r.slug === WATCH_CASE);
  const tally = data.real_tally || {};
  const cur = currentVersion(data);
  const p7 = data.planted_totals.filter((t) => t.adopted).sort((a, b) => b.seed - a.seed || +b.version.slice(1) - +a.version.slice(1))[0];
  const dev = [...data.dev_suite].reverse().find((d) => d.adopted !== false) || data.dev_suite[data.dev_suite.length - 1];
  const toWatch = () => {
    watch.current?.scrollIntoView({ behavior: prefersReducedMotion() ? "auto" : "smooth", block: "start" });
    watch.current?.querySelector(".btn.play")?.focus({ preventScroll: true });
  };
  return (
    <div className="shell">
      <section className="hero" aria-labelledby="hero-title">
        <h1 id="hero-title">When a paper’s number and its code’s number disagree, GapFinder finds out why.</h1>
        <p className="lede">It runs the released code in cloud sandboxes, changes one condition at a time, and ends each claim with a
          verdict: the cause, part of it, or a plain statement that nothing it could change explains the gap.</p>
        {cases.length > 0 && <HeroInstrument cases={cases} short={SHORT} />}
        <nav className="start-here" aria-label="Start here">
          {watchCase && <button type="button" className="start" onClick={toWatch}><b>Watch an investigation</b>
            <span>{watchCase.versions[watchCase.current].gauge?.runs} runs, replayed in under a minute</span></button>}
          <a className="start" href={href("/cases")}><b>Browse the 16 real papers</b><span>finds and misses, case by case</span></a>
          <a className="start" href={href("/evidence")}><b>Check the evidence</b><span>what each measurement can and can’t show</span></a>
        </nav>
      </section>

      {watchCase && (
        <section className="section" aria-labelledby="watch-title" ref={watch}>
          <Watch c={watchCase} />
        </section>
      )}

      <section className="section" aria-labelledby="record-title">
        <header>
          <h2 id="record-title">Sixteen earlier papers, misses included</h2>
          <p>Each square is one paper with a documented cause, re-run on each <Term k="version">version</Term> of the engine. The fixes
            since {vName(data.real_versions?.[0] || "c5")} were found on these same papers, so the rows are <Term k="posthoc">post-hoc</Term>:
            they show what the engine does now, not what it would do on a paper it has never seen.</p>
        </header>
        <VersionStrips data={data} />
        <p className="small after-chart">
          On {vName(cur)}, the current version and the one every paper was re-run on: {tally.found || 0} found, {tally.partial || 0} partly
          found, {tally.no_gap || 0} correctly reported no gap, and {tally.missed || 0} missed. <a href={href("/cases")}>Read every case</a>.
        </p>
      </section>

      <section className="section" aria-labelledby="evidence-title">
        <header>
          <h2 id="evidence-title">What the evidence says</h2>
          <p>Reruns of known papers are a demonstration. These are the measurements that were sealed or fresh when they were taken.</p>
        </header>
        <div className="facts">
          <div className="fact">
            <div className="figure">{data.blind.correct} <small>of {data.blind.papers}</small></div>
            <p><Term k="sealed">sealed blind papers</Term> explained, all run before this work: {data.blind.partial} partly,
              {" "}{data.blind.missed} missed, {data.blind.confidently_wrong} <Term k="confidently_wrong">confidently wrong</Term>.</p>
          </div>
          {p7 && (
            <div className="fact">
              <div className="figure">{p7.found} <small>of {p7.gaps}</small></div>
              <p><Term k="planted">planted gaps</Term> found by {vName(p7.version)}, the {versionStatus(data, p7.version) || "adopted"} version,
                on <Term k="batch">fresh batch</Term> {p7.seed}: {p7.confidently_wrong} confidently wrong, and {p7.controls_correct} of
                {" "}{p7.controls} <Term k="control">controls</Term> left alone.</p>
            </div>
          )}
          {dev && (
            <div className="fact">
              <div className="figure">{dev.correct} <small>of 138</small></div>
              <p>runs of the <Term k="dev_suite">dev suite</Term> with a cause found by {vName(dev.version)}, pooled over two replicates;
                all 114 <Term k="abstain">abstentions</Term> correct.</p>
            </div>
          )}
        </div>
        <div className="subsection">
          <h3>Planted gaps found by each version</h3>
          <p className="muted">Gaps planted into papers whose code reproduces, searched without the paper. Each dot is a fresh batch
            made after the version was frozen.</p>
          <PlantedChart totals={data.planted_totals} />
        </div>
        <p className="after-chart"><a href={href("/evidence")}>See all the measurements</a>, including the comparison with a general coding agent.</p>
      </section>
    </div>
  );
}

// ------------------------------------------------------------------ cases index
export function Cases() {
  const { data, error } = useShowcase();
  if (!data) return <div className="shell"><Loading error={error} /></div>;
  const versions = (data.real_versions || ["c5", "c7"]).filter((v) => data.real.some((p) => p.versions[v]));
  const order = { found: 0, partial: 1, no_gap: 2, missed: 3 };
  const rows = [...data.real].sort((a, b) => order[a.versions[a.current].verdict] - order[b.versions[b.current].verdict]);
  return (
    <div className="shell">
      <section className="hero page-head">
        <h1>Cases</h1>
        <p className="lede">Sixteen papers whose reproduction gap has a documented cause, each re-run on the engine’s later versions.</p>
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
            {rows.map((p) => {
              const cur = p.versions[p.current];
              return (
                <tr key={p.slug} className="link">
                  <td className="paper-cell"><a href={href(`/case/${p.slug}`)}>{p.title}</a><small>{p.venue}</small></td>
                  <td className="cause">{p.documented_cause}</td>
                  <td className="reading">{cur.reading}</td>
                  {versions.map((v) => <td key={v}>{p.versions[v] ? <Verdict v={p.versions[v].verdict} short /> : <span className="muted">not run</span>}</td>)}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ------------------------------------------------------------------ one case
function Answer({ v, g }) {
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

export function Case({ slug, query }) {
  const { data, error } = useShowcase();
  const c = data?.real.find((x) => x.slug === slug);
  const v = c && (query.get("v") && c.versions[query.get("v")] ? query.get("v") : c.current);
  const sel = c?.versions[v];
  const { run } = useRun(sel?.id);
  const [show, setShow] = useState("after");
  const [play, setPlay] = useState(0);
  if (!data) return <div className="shell"><Loading error={error} /></div>;
  if (!c) return <div className="shell"><p className="notice">No case called “{slug}”. <a href={href("/cases")}>See every case</a>.</p></div>;
  const g = sel.gauge;
  const hasAfter = g && g.after !== null && g.after !== undefined;
  return (
    <div className="shell">
      <a className="crumb" href={href("/cases")}>All cases</a>
      <header className="case-head">
        <h1>{c.title}</h1>
        <div className="meta">
          <Verdict v={sel.verdict} big />
          <span>{c.venue}</span>
          <nav className="toggle" aria-label="Engine version">
            {(data.real_versions || ["c5", "c7"]).filter((x) => c.versions[x]).map((x) => (
              <a key={x} href={href(`/case/${slug}`, { v: x })} aria-current={x === v ? "page" : undefined}
                 title={versionStatus(data, x) || ""}>{vName(x)}</a>
            ))}
          </nav>
          <span>Showing engine <Term k="version">version</Term> {vName(v)}{versionStatus(data, v) ? ` (${versionStatus(data, v)})` : ""}</span>
        </div>
      </header>

      <section className="document" aria-labelledby="gap-title">
        <h2 id="gap-title">The gap</h2>
        <div className="two">
          <div>
            {hasAfter && (
              <div className="toggle gauge-toggle" role="group" aria-label="Show the code’s number">
                {[["before", "As released"], ["after", "After GapFinder’s change"]].map(([k, t]) => (
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

      <section className="document" aria-labelledby="versions-title">
        <h2 id="versions-title">Across versions</h2>
        <ol className="timeline">
          {(data.real_versions || ["c5", "c7"]).filter((x) => c.versions[x]).map((x) => (
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

      <section className="document" aria-labelledby="inv-title">
        <h2 id="inv-title">The investigation</h2>
        {run ? <Replay run={run} key={run.id} /> : <Loading what="Loading the recorded run…" />}
      </section>
      <section className="document" aria-labelledby="report-title">
        <h2 id="report-title" className="visually-hidden">The full report</h2>
        {run ? <Report run={run} /> : <Loading what="Loading the report…" />}
      </section>
      <p className="notice spaced"><Term k="posthoc">Post-hoc</Term> rerun. The cause is documented, and the engine’s fixes since
        {" "}{vName((data.real_versions || ["c5"])[0])} were found on these very runs, so this is a demonstration, not evidence.</p>
    </div>
  );
}

// a planted change as the scorer words it ("scale: lr: the paper's v is the code's 0.5 x v", "setting: wd = 0.001"):
// the identifier as code, the description as prose
// ------------------------------------------------------------------ any recorded run
export function RunPage({ id }) {
  const { run, error } = useRun(id);
  if (error) return <div className="shell"><p className="notice" role="alert">No recorded run “{id}”. <a href={href("/synthetic")}>Back to the synthetic cases</a>.</p></div>;
  if (!run) return <div className="shell"><Loading what="Loading the recorded run…" /></div>;
  const m = run.meta || {};
  const g = gaugeOf(run.report);
  return (
    <div className="shell">
      <a className="crumb" href={href("/synthetic", m.group === "gapbench" ? { tab: "gapbench" } : {})}>Synthetic cases</a>
      <header className="case-head">
        <h1>{m.title || run.report?.paper || id}</h1>
        <div className="meta">
          {m.version && <span>Engine <Term k="version">version</Term> {vName(m.version)}{m.seed ? <>, <Term k="batch">fresh batch</Term> {m.seed}</> : ""}</span>}
          {g?.label && <PlainLabel label={g.label} formal />}
        </div>
      </header>
      <section className="document" aria-labelledby="gap-title">
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
      <section className="document" aria-labelledby="inv-title"><h2 id="inv-title">The investigation</h2><Replay run={run} key={run.id} /></section>
      <section className="document" aria-labelledby="report-title"><h2 id="report-title" className="visually-hidden">The full report</h2><Report run={run} /></section>
    </div>
  );
}

// ------------------------------------------------------------------ how it works
const STEPS = [
  ["Read the paper", "Nemotron reads the paper and lists every number it reports, each with its exact quote, and every setting it states or leaves out."],
  ["Describe how to run the code", "A harness, a short file, says how to build the released code, run it, read its output, and which settings may change. A person approves it."],
  ["Measure the noise", "Five runs of the code as released give its number and its run-to-run spread. A gap inside that spread is not a gap."],
  ["Search the settings", "Each candidate setting runs once from the same saved checkpoint in its own sandbox. What moves the number is repeated, and what survives is combined."],
  ["Check the answer", "Revert each change: the gap must come back. Held-out claims must not get worse. The value needs evidence beyond the fact that it fits."],
  ["Look beyond the settings", "When no setting fits every claim, it tests what settings can’t express: a unit or counting convention, how the paper picks its epoch, a library release, a hard-coded value or a small code edit, made in memory, never on disk."],
  ["Label it honestly", "Explained needs evidence. A code change is never called Explained. And Unexplained is an answer, said plainly, when nothing it could change explains the gap."],
];

export function How() {
  return (
    <div className="shell">
      <section className="hero page-head">
        <h1>How it works</h1>
        <p className="lede">An investigation is a sequence of experiments, each forked from one built and loaded copy of the code, so a
          hypothesis costs one run, not one setup.</p>
      </section>
      <section className="section tight">
        <ol className="steps">
          {STEPS.map(([t, d]) => <li key={t}><div><h3>{t}</h3><p>{d}</p></div></li>)}
        </ol>
      </section>
      <section className="section" aria-labelledby="limits-title">
        <header><h2 id="limits-title">What it can’t do yet</h2></header>
        <ul className="prose-list">
          <li>Tell apart causes that fit the paper’s numbers equally well. With one reported number, several changes often fit, and it says so.</li>
          <li>Find a cause the paper never states and the code doesn’t express, such as a different model variant behind the number.</li>
          <li>Prove itself on new papers. Its blind record on sealed papers is 1 of 8, from before this work; a fresh blind batch is the next test.</li>
        </ul>
      </section>
      <section className="section" aria-labelledby="words-title">
        <header><h2 id="words-title">Words used on this site</h2>
          <p>Underlined words elsewhere on the site show these definitions on hover, focus or tap.</p></header>
        <dl className="glossary">
          {Object.entries(GLOSSARY).map(([k, [w, d]]) => <div key={k}><dt>{w}</dt><dd>{d}</dd></div>)}
        </dl>
      </section>
    </div>
  );
}
