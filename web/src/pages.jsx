import { useEffect, useMemo, useState } from "react";
import { api } from "./api.js";
import Gauge from "./Gauge.jsx";
import { PlantedChart, VersionStrips } from "./Record.jsx";
import Replay from "./Replay.jsx";
import Report from "./Report.jsx";
import Scoreboard from "./Scoreboard.jsx";
import { VERDICT, Verdict, changesText, num, prettyKnob, signedPct, useShowcase } from "./ui.jsx";

export const href = (path, q = {}) => {
  const qs = new URLSearchParams(Object.entries(q).filter(([, v]) => v)).toString();
  return `#${path}${qs ? `?${qs}` : ""}`;
};
const HERO_CASES = ["fastgcn-v15", "sdcn", "gcn-attack", "fair-clustering"];
const SHORT = { "gcn-attack": "Topology attack", sdcn: "SDCN", "fastgcn-v15": "FastGCN", "fair-clustering": "Fair Clustering" };

function Loading({ what = "Loading…", error }) {
  if (error) return <p className="notice" role="alert">Couldn’t load the showcase data ({String(error.message || error)}). Start the server with <code>uvicorn gapfinder.api.server:app</code> and reload.</p>;
  return <p className="status-line" aria-live="polite">{what}</p>;
}

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
export function Home() {
  const { data, error } = useShowcase();
  const [pick, setPick] = useState(HERO_CASES[0]);
  const [play, setPlay] = useState(1);
  if (!data) return <div className="shell"><Loading error={error} /></div>;
  const cases = HERO_CASES.map((s) => data.real.find((r) => r.slug === s)).filter(Boolean);
  const c = cases.find((x) => x.slug === pick) || cases[0];
  const cur = c?.versions[c.current];
  const tally = data.real_tally || {};
  const p7 = data.planted_totals.find((t) => t.version === "c5" && t.seed === 7);
  const dev = data.dev_suite[data.dev_suite.length - 1];
  return (
    <div className="shell">
      <section className="hero" aria-labelledby="hero-title">
        <h1 id="hero-title">When a paper’s number and its code’s number disagree, GapFinder finds out why.</h1>
        <p className="lede">It runs the released code in cloud sandboxes, changes one condition at a time, and ends each claim with a
          verdict: the cause, part of it, or a plain statement that nothing it could change explains the gap.</p>
        {c && (
          <div className="hero-instrument">
            <div className="case-switch" role="group" aria-label="Choose a case">
              {cases.map((x) => (
                <button key={x.slug} type="button" className="seg" aria-pressed={x.slug === c.slug}
                        onClick={() => { setPick(x.slug); setPlay((k) => k + 1); }}>{SHORT[x.slug] || x.title}</button>
              ))}
            </div>
            <Gauge key={c.slug} g={cur.gauge} autoplay playKey={play} label={c.title} />
            <div className="closed-by">
              <div>
                <p className="what">{cur.reading}</p>
                <p className="small">{c.title}, {c.venue}. Documented cause: {c.documented_cause} Found in {cur.gauge?.runs} sandbox runs.</p>
              </div>
              <a className="btn quiet" href={href(`/case/${c.slug}`)}>Open this case</a>
            </div>
          </div>
        )}
      </section>

      <section className="section" aria-labelledby="record-title">
        <header>
          <h2 id="record-title">Sixteen earlier papers, misses included</h2>
          <p>Each square is one paper whose cause is documented, re-run on each version of the engine. The fixes in c7 and c8 were
            found on these same papers, so the rows show what the engine does now, not what it would do on a paper it has never seen.</p>
        </header>
        <VersionStrips real={data.real} />
        <p className="small" style={{ marginTop: 16 }}>
          On the current version: {tally.found || 0} found, {tally.partial || 0} partly found, {tally.no_gap || 0} correctly reported no gap,
          and {tally.missed || 0} missed. <a href={href("/cases")}>Read every case</a>.
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
            <p>sealed blind papers explained, all run before this work. {data.blind.partial} partly, {data.blind.missed} missed, {data.blind.confidently_wrong} confidently wrong.</p>
          </div>
          {p7 && (
            <div className="fact">
              <div className="figure">{p7.found} <small>of {p7.gaps}</small></div>
              <p>fresh planted gaps found by c5, the adopted version, on seed 7, with {p7.confidently_wrong} confidently wrong and {p7.controls_correct} of {p7.controls} controls left alone.</p>
            </div>
          )}
          {dev && (
            <div className="fact">
              <div className="figure">{dev.correct} <small>of 138</small></div>
              <p>dev-suite runs with a cause found by {dev.version}, pooled over two replicates, and every one of the 114 abstentions correct.</p>
            </div>
          )}
        </div>
        <div style={{ marginTop: 48 }}>
          <h3>Planted gaps found by each version</h3>
          <p className="muted" style={{ marginTop: 8 }}>Gaps planted into papers whose code reproduces, searched without the paper. Each dot is a fresh batch made after the version was frozen.</p>
          <PlantedChart totals={data.planted_totals} />
        </div>
        <p style={{ marginTop: 24 }}><a href={href("/evidence")}>See all the measurements</a>, including the comparison with a general coding agent.</p>
      </section>
    </div>
  );
}

// ------------------------------------------------------------------ cases index
export function Cases() {
  const { data, error } = useShowcase();
  if (!data) return <div className="shell"><Loading error={error} /></div>;
  const versions = ["c5", "c7", "c8"].filter((v) => data.real.some((p) => p.versions[v]));
  const order = { found: 0, partial: 1, no_gap: 2, missed: 3 };
  const rows = [...data.real].sort((a, b) => order[a.versions[a.current].verdict] - order[b.versions[b.current].verdict]);
  return (
    <div className="shell">
      <section className="hero" style={{ paddingBottom: 0 }}>
        <h1>Cases</h1>
        <p className="lede">Sixteen papers whose reproduction gap has a documented cause, each re-run on the engine’s later versions.</p>
        <p className="notice">Post-hoc: these causes were known, and the engine’s fixes since c5 were found on these runs. Read them as a
          demonstration of what the current engine does, not as evidence of how it does on new papers.</p>
      </section>
      <div className="ledger-wrap" style={{ marginTop: 32 }}>
        <table>
          <thead><tr>
            <th scope="col">Paper</th><th scope="col">Documented cause</th><th scope="col">GapFinder now</th>
            {versions.map((v) => <th scope="col" key={v}>{v}</th>)}
          </tr></thead>
          <tbody>
            {rows.map((p) => {
              const cur = p.versions[p.current];
              return (
                <tr key={p.slug} className="link">
                  <td className="paper-cell"><a href={href(`/case/${p.slug}`)}>{p.title}</a><small>{p.venue}</small></td>
                  <td className="cause">{p.documented_cause}</td>
                  <td style={{ maxWidth: "34ch" }}>{cur.reading}</td>
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
      <dt>Label</dt><dd>{g.label}</dd>
      <dt>Change</dt><dd>{Object.keys(g.changes || {}).length ? <code>{changesText(g.changes)}</code> : "none"}</dd>
      <dt>Gap</dt><dd className="num">{signedPct((g.code - g.paper) / Math.abs(g.paper))}{g.after != null ? ` to ${signedPct((g.after - g.paper) / Math.abs(g.paper))}` : ""}</dd>
      <dt>Runs</dt><dd className="num">{g.runs} in sandboxes, on {v}</dd>
      {g.figure && <><dt>Claim</dt><dd>{g.figure}</dd></>}
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
            {["c5", "c7", "c8"].filter((x) => c.versions[x]).map((x) => (
              <a key={x} href={href(`/case/${slug}`, { v: x })} aria-current={x === v ? "page" : undefined}>{x}</a>
            ))}
          </nav>
        </div>
      </header>

      <section className="document" aria-labelledby="gap-title">
        <h2 id="gap-title">The gap</h2>
        <div className="two">
          <div>
            {hasAfter && (
              <div className="toggle" role="group" aria-label="Show the code’s reading" style={{ marginBottom: 12 }}>
                {[["before", "As released"], ["after", "After GapFinder’s change"]].map(([k, t]) => (
                  <button key={k} type="button" aria-pressed={show === k} onClick={() => { setShow(k); setPlay((n) => n + 1); }}>{t}</button>
                ))}
              </div>
            )}
            <Gauge g={g} show={show} playKey={play} label={c.title} />
          </div>
          <div>
            <h3 style={{ fontSize: "var(--t1)", marginBottom: 8 }}>The documented cause</h3>
            <p className="claimtext quote">{c.documented_cause}</p>
            <h3 style={{ fontSize: "var(--t1)", margin: "24px 0 8px" }}>What GapFinder found</h3>
            <p>{sel.reading}</p>
            <Answer v={v} g={g} />
          </div>
        </div>
      </section>

      <section className="document" aria-labelledby="versions-title">
        <h2 id="versions-title">Across versions</h2>
        <ol className="timeline">
          {["c5", "c7", "c8"].filter((x) => c.versions[x]).map((x) => (
            <li key={x}>
              <div className="v">{x}</div>
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
      <p className="notice" style={{ marginTop: 24 }}>Post-hoc rerun. The cause is documented, and the engine’s fixes since c5 were found on these
        very runs, so this is a demonstration, not evidence.</p>
    </div>
  );
}

// a planted change as the scorer words it ("scale: lr: the paper's v is the code's 0.5 x v", "setting: wd = 0.001"):
// the identifier as code, the description as prose
function Planted({ text }) {
  const t = text.replace(/^\w+: /, "");
  const i = t.indexOf(": ");
  if (i > 0 && !t.slice(0, i).includes(" ")) {
    return <span style={{ display: "block" }}><code>{prettyKnob(t.slice(0, i))}</code> {t.slice(i + 2).replace(/ x /g, " × ")}</span>;
  }
  const [k, v] = t.split(" = ");
  return <span style={{ display: "block" }}><code>{v !== undefined ? `${prettyKnob(k)} = ${v}` : t}</code></span>;
}

// ------------------------------------------------------------------ synthetic cases
const FAMILIES = [["", "All"], ["setting", "Settings"], ["scale", "Scale conventions"], ["data", "Data cuts"], ["code", "Code defects"],
  ["reporting", "Reporting rules"], ["control", "Controls"]];

export function Synthetic({ query, navigate }) {
  const { data, error } = useShowcase();
  const tab = query.get("tab") === "gapbench" ? "gapbench" : "planted";
  const fam = query.get("family") || "";
  const set = (q) => navigate("/synthetic", { tab, family: fam, ...q });
  const planted = useMemo(() => (data?.planted || []).filter((p) => !fam || p.family === fam), [data, fam]);
  if (!data) return <div className="shell"><Loading error={error} /></div>;
  return (
    <div className="shell">
      <section className="hero" style={{ paddingBottom: 0 }}>
        <h1>Synthetic cases</h1>
        <p className="lede">Gaps with known answers: changes planted into papers whose code reproduces, and the GapBench tasks. These are the
          ones it got right. The evidence page has the full rates, misses included.</p>
      </section>
      <div className="toggle" role="group" aria-label="Which set" style={{ margin: "32px 0 16px" }}>
        <button type="button" aria-pressed={tab === "planted"} onClick={() => set({ tab: "planted" })}>Planted gaps ({data.planted.length})</button>
        <button type="button" aria-pressed={tab === "gapbench"} onClick={() => set({ tab: "gapbench", family: "" })}>GapBench tasks ({data.gapbench.length})</button>
      </div>
      {tab === "planted" ? (
        <>
          <div className="filters" role="group" aria-label="Filter by kind of gap">
            {FAMILIES.map(([k, t]) => (
              <button key={k || "all"} type="button" className="seg" aria-pressed={fam === k} onClick={() => set({ family: k })}>{t}</button>
            ))}
          </div>
          <div className="ledger-wrap">
            <table>
              <thead><tr><th scope="col">Case</th><th scope="col">What was planted</th><th scope="col">What GapFinder found</th><th scope="col">Label</th><th scope="col">Version</th></tr></thead>
              <tbody>
                {planted.map((p) => (
                  <tr key={p.id} className="link">
                    <td className="paper-cell"><a href={href(`/run/${p.id}`)}>{p.title.replace(/^Planted /, "").replace(/^./, (m) => m.toUpperCase())}</a></td>
                    <td>{p.planted.length ? p.planted.map((x) => <Planted key={x} text={x} />) : <span className="muted">nothing (a control)</span>}</td>
                    <td>{Object.keys(p.found || {}).length ? <code>{changesText(p.found)}</code> : <span className="muted">no change: reported as reproduced</span>}</td>
                    <td>{p.label || "Reproduced"}</td>
                    <td className="num" style={{ whiteSpace: "nowrap" }}>{p.version}, seed {p.seed}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : (
        <div className="ledger-wrap">
          <table>
            <thead><tr><th scope="col">Task</th><th scope="col">Kind</th><th scope="col">Outcome</th><th scope="col">What GapFinder found</th></tr></thead>
            <tbody>
              {data.gapbench.map((p) => (
                <tr key={p.id} className="link">
                  <td className="paper-cell"><a href={href(`/run/${p.id}`)}>{p.title.split(":")[0].replace("GapBench ", "")}</a></td>
                  <td>{p.title.split(": ").slice(1).join(": ")}</td>
                  <td>{p.outcome === "correct" ? "Found the cause" : "Correctly abstained"}</td>
                  <td>{Object.values(p.found || {}).map((f, i) => <code key={i}>{changesText(f.changes) || "no change"}</code>)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

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
        <div className="meta">{m.version && <span>{m.version}{m.seed ? `, seed ${m.seed}` : ""}</span>}{g?.label && <span>{g.label}</span>}</div>
      </header>
      <section className="document" aria-labelledby="gap-title">
        <h2 id="gap-title">The gap</h2>
        <div className="two">
          <div>{g ? <Gauge g={g} label={m.title} /> : <p className="muted">This run records no gap on its target.</p>}</div>
          <div>
            {m.planted && <><h3 style={{ fontSize: "var(--t1)", marginBottom: 8 }}>What was planted</h3>
              <p>{m.planted.length ? m.planted.map((x) => <code key={x}>{x}</code>) : "Nothing: a control, where the right answer is no gap."}</p></>}
            {m.hidden && <><h3 style={{ fontSize: "var(--t1)", marginBottom: 8 }}>The hidden setting</h3><p><code>{changesText(m.hidden)}</code></p></>}
            <h3 style={{ fontSize: "var(--t1)", margin: "16px 0 8px" }}>What GapFinder found</h3>
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
  ["Describe how to run the code", "A harness says how to build the released code, run it, read its output, and which settings may change. A person approves it."],
  ["Measure the noise", "Five runs of the code as released give its number and its run-to-run spread. A gap inside that spread is not a gap."],
  ["Search the settings", "Each candidate setting runs once from the same saved checkpoint in its own sandbox. What moves the number is repeated, and what survives is combined."],
  ["Check the answer", "Revert each change: the gap must come back. Held-out claims must not get worse. The value needs evidence beyond the fact that it fits."],
  ["Look beyond the settings", "When no setting fits every claim, it tests what settings can’t express: a unit or counting convention, how the paper picks its epoch, a library release, a hard-coded value or a small code edit, made in memory, never on disk."],
  ["Label it honestly", "Explained needs evidence. A code change is never called Explained. And Unexplained is an answer, said plainly, when nothing it could change explains the gap."],
];

export function How() {
  return (
    <div className="shell">
      <section className="hero" style={{ paddingBottom: 0 }}>
        <h1>How it works</h1>
        <p className="lede">An investigation is a sequence of experiments, each forked from one built and loaded copy of the code, so a
          hypothesis costs one run, not one setup.</p>
      </section>
      <section className="section" style={{ paddingTop: 32 }}>
        <ol className="steps">
          {STEPS.map(([t, d]) => <li key={t}><div><h3>{t}</h3><p>{d}</p></div></li>)}
        </ol>
      </section>
      <section className="section" aria-labelledby="limits-title">
        <header><h2 id="limits-title">What it can’t do yet</h2></header>
        <ul style={{ maxWidth: "68ch", paddingLeft: 20 }}>
          <li>Tell apart causes that fit the paper’s numbers equally well. With one reported number, several changes often fit, and it says so.</li>
          <li>Find a cause the paper never states and the code doesn’t express, such as a different model variant behind the number.</li>
          <li>Prove itself on new papers. Its blind record on sealed papers is 1 of 8, from before this work; a fresh blind batch is the next test.</li>
        </ul>
      </section>
    </div>
  );
}

// ------------------------------------------------------------------ the evidence
export function Evidence() {
  const { data, error } = useShowcase();
  if (!data) return <div className="shell"><Loading error={error} /></div>;
  return (
    <div className="shell">
      <section className="hero" style={{ paddingBottom: 0 }}>
        <h1>The evidence</h1>
        <p className="lede">Every measurement, with what it can and can’t show. Only the sealed blind papers are clean evidence; the rest were
          made while the engine was being built.</p>
      </section>
      <section className="section" aria-labelledby="ev-real">
        <header><h2 id="ev-real">Real papers, re-run post-hoc</h2>
          <p>Sixteen papers with documented causes. A demonstration: the fixes were found on them.</p></header>
        <VersionStrips real={data.real} />
      </section>
      <section className="section" aria-labelledby="ev-planted">
        <header><h2 id="ev-planted">Planted gaps on fresh batches</h2>
          <p>Each batch is made after the version is frozen, from operators the engine doesn’t share. Versions are adopted only when they
            are no worse on a fresh batch.</p></header>
        <PlantedChart totals={data.planted_totals} />
        <div className="ledger-wrap" style={{ marginTop: 24 }}>
          <table>
            <thead><tr><th scope="col">Version</th><th scope="col">Seed</th><th scope="col" className="num">Gaps found</th><th scope="col" className="num">Confidently wrong</th><th scope="col" className="num">Controls right</th><th scope="col">By kind</th></tr></thead>
            <tbody>
              {[...data.planted_totals].sort((a, b) => a.seed - b.seed || +a.version.slice(1) - +b.version.slice(1)).map((t) => (
                <tr key={`${t.version}-${t.seed}`}>
                  <td>{t.version}{t.adopted ? "" : <span className="muted"> (not adopted)</span>}</td><td className="num">{t.seed}</td>
                  <td className="num">{t.found} of {t.gaps}</td><td className="num">{t.confidently_wrong}</td>
                  <td className="num">{t.controls ? `${t.controls_correct} of ${t.controls}` : "none"}</td>
                  <td className="small">{Object.entries(t.by_kind).map(([k, [f, n]]) => `${k} ${f}/${n}`).join(", ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
      <section className="section" aria-labelledby="ev-dev">
        <header><h2 id="ev-dev">The development suite</h2>
          <p>GapBench tasks run locally at no cost, two replicates per version. Identical code swings by about five between runs.</p></header>
        <div className="ledger-wrap"><table>
          <thead><tr><th scope="col">Version</th><th scope="col" className="num">Runs with a cause found (of 138)</th><th scope="col">Replicates</th></tr></thead>
          <tbody>{data.dev_suite.map((d) => <tr key={d.version}><td>{d.version}</td><td className="num">{d.correct}</td><td className="num">{d.runs.join(", ")}</td></tr>)}</tbody>
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

export { VERDICT, num };
