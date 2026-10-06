import { useEffect, useState } from "react";
import { api, LABEL_CLASS } from "./api.js";
import Replay from "./Replay.jsx";
import Report from "./Report.jsx";
import Scoreboard from "./Scoreboard.jsx";

const TABS = [["replay", "Replay"], ["report", "Gap Report"], ["scoreboard", "Scoreboard"], ["about", "Judge's guide"]];

function parseHash() {
  const [, tab = "replay", id = ""] = window.location.hash.split("/");
  return { tab: tab || "replay", id: decodeURIComponent(id) };
}

function About() {
  return (
    <section className="panel wide about">
      <h3>Judge's guide</h3>
      <ol>
        <li><b>Replay</b> plays a recorded GapFinder run at 1×, 4× or 16×. Watch one checkpoint fan out into
          branches, weak hypotheses get pruned, and the claim bars move toward the paper's number.</li>
        <li><b>Gap Report</b> gives one card per claim: its label, the knob(s) that explain the gap, the evidence
          for the value, the counterfactual check, held-out claims, and a copy-paste command to replay the branch.</li>
        <li><b>Scoreboard</b> compares GapFinder with a standard coding agent (mini-swe-agent on Nemotron) on
          planted-gap tasks with known answers. Every transcript is in the repo under <code>eval/gapbench/runs/</code>.</li>
      </ol>
      <p>GapFinder never edits the paper's algorithm code: it changes only experimental conditions (configs, flags,
        workload, build options, environment), and it says "Unexplained" when nothing it tested explains a gap.</p>
      <p className="small">Models: Nemotron 3 Ultra builds the claim ledger and assumption space; the search runs
        in Token Factory Sandboxes, forking every hypothesis from one built-and-loaded checkpoint.</p>
    </section>
  );
}

export default function App() {
  const [route, setRoute] = useState(parseHash());
  const [runs, setRuns] = useState([]);
  const [run, setRun] = useState(null);

  useEffect(() => {
    const on = () => setRoute(parseHash());
    window.addEventListener("hashchange", on);
    return () => window.removeEventListener("hashchange", on);
  }, []);
  useEffect(() => { api.runs().then(setRuns).catch(() => setRuns([])); }, []);
  const runId = route.id || runs[0]?.id;
  useEffect(() => {
    if (!runId) return;
    setRun(null);
    api.run(runId).then(setRun).catch(() => setRun(null));
  }, [runId]);

  const go = (tab, id = runId) => { window.location.hash = `#/${tab}/${id ? encodeURIComponent(id) : ""}`; };

  return (
    <div className="app">
      <header className="top">
        <div className="brand"><b>GapFinder</b> <span>why paper reproductions diverge</span></div>
        <nav>{TABS.map(([t, name]) => (
          <a key={t} className={route.tab === t ? "on" : ""} onClick={() => go(t)}>{name}</a>
        ))}</nav>
      </header>
      {(route.tab === "replay" || route.tab === "report") && (
        <div className="picker">
          <label>Run</label>
          <select value={runId || ""} onChange={(e) => go(route.tab, e.target.value)}>
            {runs.map((r) => (
              <option key={r.id} value={r.id}>
                {r.title} — {Object.values(r.labels).join(", ")}
              </option>
            ))}
          </select>
          {run && Object.entries(runs.find((r) => r.id === runId)?.labels || {}).map(([c, l]) => (
            <span key={c} className={`label ${LABEL_CLASS[l] || "muted"}`}>{c}: {l}</span>
          ))}
        </div>
      )}
      <main>
        {route.tab === "replay" && (run ? <Replay run={run} key={run.id} /> : <p>Loading run…</p>)}
        {route.tab === "report" && <Report run={run} />}
        {route.tab === "scoreboard" && <Scoreboard />}
        {route.tab === "about" && <About />}
      </main>
      <footer>Open source (MIT) · every number links to a log in the repository</footer>
    </div>
  );
}
