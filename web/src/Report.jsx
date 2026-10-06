import { useState } from "react";
import { api, pct, LABEL_CLASS } from "./api.js";

function Copy({ text }) {
  const [done, setDone] = useState(false);
  return (
    <button className="copy" onClick={() => { navigator.clipboard?.writeText(text); setDone(true); setTimeout(() => setDone(false), 1200); }}>
      {done ? "copied" : "copy"}
    </button>
  );
}

function Card({ c }) {
  const a = c.attribution;
  const label = a?.confidence_label || "Reproduced";
  const replay = c.replay?.[0];
  const cmd = replay ? `${Object.entries(replay.env || {}).map(([k, v]) => `${k}=${v}`).join(" ")} ${replay.command}` : null;
  return (
    <article className="card">
      <header>
        <span className={`label ${LABEL_CLASS[label] || "muted"}`}>{label}</span>
        <h4>{c.target.claim_id} · {c.target.metric}</h4>
        <span className="paperval">paper {c.target.paper_value}</span>
      </header>
      {c.status === "reproduced" ? (
        <p>Reproduces: the naive gap {pct(c.gap_before)} is inside the noise band ±{(c.band * 100).toFixed(1)}%.</p>
      ) : (
        <>
          <p className="gap">gap <b>{pct(c.gap_before)}</b> → <b>{pct(c.gap_after)}</b> · noise ±{(c.band * 100).toFixed(1)}% · {c.hypotheses_tested} hypotheses tested</p>
          {Object.keys(c.changes || {}).length > 0 && (
            <p>Explained by {Object.entries(c.changes).map(([k, v]) => <code key={k}>{k}={v}</code>)}</p>
          )}
          {Object.keys(c.plausibility || {}).length > 0 && (
            <div className="sub"><h5>Evidence</h5><ul>
              {Object.entries(c.plausibility).map(([k, p]) => (
                <li key={k}><code>{k}={c.changes[k]}</code> {p.supported ? "supported" : <b className="warn">unsupported</b>}: {p.reason}</li>
              ))}
            </ul></div>
          )}
          {Object.keys(c.counterfactual || {}).length > 0 && (
            <div className="sub"><h5>Counterfactual (revert one knob; the gap must come back)</h5><ul>
              {Object.entries(c.counterfactual).map(([k, v]) => (
                <li key={k}>without <code>{k}</code>: gap {pct(v.gap_without)} {v.ok ? "✓" : "✗ did not return"}</li>
              ))}
            </ul></div>
          )}
          {Object.keys(c.held_out || {}).length > 0 && (
            <div className="sub"><h5>Held-out claims (must not get worse beyond noise)</h5><ul>
              {Object.entries(c.held_out).map(([cid, v]) => (
                <li key={cid}>{cid}: {pct(v.gap_before)} → {pct(v.gap_after)} {v.ok ? "✓" : "✗ worse"}</li>
              ))}
            </ul></div>
          )}
          {cmd && (
            <div className="sub"><h5>Replay this branch</h5>
              <p className="small">Fork checkpoint <code>{replay.parent_checkpoint}</code> and run:</p>
              <pre>{cmd}<Copy text={cmd} /></pre>
            </div>
          )}
          {c.notes?.length > 0 && <div className="sub"><h5>Notes</h5><ul>{c.notes.map((n, i) => <li key={i}>{n}</li>)}</ul></div>}
        </>
      )}
    </article>
  );
}

export default function Report({ run }) {
  const r = run?.report;
  if (!r) return <p>Loading…</p>;
  return (
    <section>
      <div className="report-head">
        <h2>Gap Report: {r.paper}</h2>
        <p className="small">
          Artifact <code>{r.artifact}</code> · {r.runs} branch runs ({r.setup_runs} build/load setups) · generated {r.generated}
          {" · "}<a href={api.reportMdUrl(run.id)}>Markdown</a> · <a href={`/api/runs/${encodeURIComponent(run.id)}`}>JSON</a>
        </p>
        {r.partial && <p className="warn">Partial report: the run or dollar budget ran out before every claim was verified.</p>}
      </div>
      {r.claims.map((c) => <Card key={c.target.claim_id} c={c} />)}
      {r.unmapped_assumptions?.length > 0 && (
        <p className="small">Not testable with this harness: {r.unmapped_assumptions.map((k) => <code key={k}>{k}</code>)}</p>
      )}
    </section>
  );
}
