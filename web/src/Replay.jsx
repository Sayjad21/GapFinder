import { useEffect, useMemo, useReducer, useRef, useState } from "react";
import { api, pct, LABEL_CLASS } from "./api.js";
import { ROUNDS, chipClass, initialState, reduce } from "./replay.js";

const SPEEDS = [1, 4, 16];

function useReplay(runId, speed, epoch) {
  const [state, dispatch] = useReducer((s, a) => (a === "reset" ? initialState() : a.type === "done"
    ? { ...s, done: true } : reduce(s, a)), undefined, initialState);
  useEffect(() => {
    if (!runId) return;
    dispatch("reset");
    const es = new EventSource(api.replayUrl(runId, speed));
    es.addEventListener("gf", (m) => dispatch(JSON.parse(m.data)));
    es.addEventListener("done", () => { dispatch({ type: "done" }); es.close(); });
    es.onerror = () => es.close();
    return () => es.close();
  }, [runId, speed, epoch]);
  return state;
}

function ClaimBars({ claims, state }) {
  return (
    <div className="bars">
      {claims.map(({ target }) => {
        const nb = state.noise[target.metric];
        const finished = Object.values(state.branches).filter(
          (b) => b.status === "succeeded" && b.parsed_metrics?.[target.metric] !== undefined && Object.keys(b.knob_changes || {}).length);
        let best = null;
        for (const b of finished) {
          const v = b.parsed_metrics[target.metric];
          if (best === null || Math.abs(v - target.paper_value) < Math.abs(best.v - target.paper_value)) best = { v, b };
        }
        const naive = nb?.median;
        const vals = [target.paper_value, naive, best?.v].filter((x) => x !== undefined && x !== null);
        const hi = Math.max(...vals) * 1.18 || 1;
        const x = (v) => `${Math.max(0, Math.min(100, (v / hi) * 100))}%`;
        const band = nb ? nb.band : 0;
        const inside = best && Math.abs(best.v - target.paper_value) <= band;
        return (
          <div className="claim" key={target.claim_id}>
            <div className="claim-head">
              <b>{target.claim_id}</b> {target.metric}
              {target.held_out && <span className="tag">held-out</span>}
            </div>
            <div className="track">
              <div className="window" style={{ left: x(target.paper_value - band), width: `calc(${x(target.paper_value + band)} - ${x(target.paper_value - band)})` }} title="paper ± noise band" />
              {naive !== undefined && <div className="bar naive" style={{ width: x(naive) }} title={`naive ${naive}`} />}
              {best && <div className={`bar best ${inside ? "inside" : ""}`} style={{ width: x(best.v) }} title={`best so far ${best.v}`} />}
              <div className="paper" style={{ left: x(target.paper_value) }} title={`paper ${target.paper_value}`} />
            </div>
            <div className="claim-legend">
              <span>paper <b>{target.paper_value}</b></span>
              <span className="lg naive">naive {naive?.toFixed?.(3) ?? "…"}</span>
              <span className="lg best">best {best ? `${best.v} (${Object.entries(best.b.knob_changes).map(([k, v]) => `${k}=${v}`).join(", ")})` : "…"}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default function Replay({ run }) {
  const [speed, setSpeed] = useState(4);
  const [epoch, setEpoch] = useState(0);
  const state = useReplay(run?.id, speed, epoch);
  const report = run?.report;
  const claims = report?.claims || [];
  const grouped = useMemo(() => {
    const g = Object.fromEntries(ROUNDS.map((r) => [r, []]));
    for (const id of state.order) g[state.branches[id].round].push(state.branches[id]);
    return g;
  }, [state.order, state.branches]);
  const stages = ["source", "built", "loaded"].map((st) => state.checkpoints.filter((c) => c.stage === st).length);
  const feedRef = useRef(null);
  const recorded = run?.recorded_at ? new Date(run.recorded_at * 1000).toLocaleString() : "unknown date";
  const llm = run?.prediction?.llm_usd;

  return (
    <section>
      <div className="replay-bar">
        <span className="badge replay">REPLAY · recorded {recorded}</span>
        <span className="speeds">
          {SPEEDS.map((s) => (
            <button key={s} className={s === speed ? "on" : ""} onClick={() => setSpeed(s)}>{s}×</button>
          ))}
          <button onClick={() => setEpoch((e) => e + 1)}>restart</button>
        </span>
        <span className="status">{state.done ? "finished" : "playing…"}</span>
      </div>

      <div className="grid">
        <div className="panel">
          <h3>Checkpoint tree</h3>
          <div className="chain">
            <span className="node">source <small>{stages[0]}</small></span>→
            {stages[1] + stages[2] > 0 ? (<>
              <span className="node">built <small>{stages[1]}</small></span>→
              <span className="node">loaded <small>{stages[2]}</small></span>→
            </>) : <span className="node" title="this artifact has no build or load step">no build/load</span>}
            <span className="node branches">{state.order.length} branches</span>
          </div>
          {ROUNDS.filter((r) => grouped[r].length).map((r) => (
            <div className="round" key={r}>
              <div className="round-name">{r} <small>{grouped[r].length}</small></div>
              <div className="chips">
                {grouped[r].map((b) => (
                  <span key={b.id} className={`chip ${chipClass(b, state.verdicts)}`}
                        title={`${b.id} ${Object.entries(b.knob_changes || {}).map(([k, v]) => `${k}=${v}`).join(", ") || "defaults"}\n${JSON.stringify(b.parsed_metrics || {})}`} />
                ))}
              </div>
            </div>
          ))}
          <div className="legend">
            <span className="chip running" /> running <span className="chip survivor" /> survives screen
            <span className="chip pruned" /> pruned <span className="chip done" /> measured <span className="chip failed" /> failed
          </div>
        </div>

        <div className="panel">
          <h3>Claims: paper vs naive vs best branch</h3>
          <ClaimBars claims={claims} state={state} />
          {Object.values(state.attributions).map((a) => (
            <div key={a.claim} className={`verdict ${LABEL_CLASS[a.label] || "muted"}`}>
              {a.claim}: <b>{a.label || a.status}</b>
              {a.changes && Object.keys(a.changes).length > 0 && <> · {Object.entries(a.changes).map(([k, v]) => `${k}=${v}`).join(", ")}</>}
              {a.gap_before !== undefined && <> · gap {pct(a.gap_before)} → {pct(a.gap_after)}</>}
            </div>
          ))}
        </div>

        <div className="panel">
          <h3>Budget</h3>
          <div className="meters">
            <div><small>branch runs</small><b>{state.order.length}</b></div>
            <div><small>build/load setups</small><b>{state.cost?.setup_runs ?? 0}</b></div>
            <div><small>sandbox</small><b>${(state.cost?.sandbox_usd ?? 0).toFixed(4)}</b></div>
            <div><small>Nemotron (ledger)</small><b>{llm !== undefined ? `$${llm.toFixed(4)}` : "—"}</b></div>
          </div>
          <h3>Events</h3>
          <ol className="feed" ref={feedRef}>
            {state.feed.map((f) => <li key={f.seq} className={f.type}>{f.line}</li>)}
          </ol>
        </div>
      </div>
    </section>
  );
}
