import { useEffect, useMemo, useReducer, useState } from "react";
import { STATIC, api } from "./api.js";
import { ROUNDS, chipClass, initialState, play, reduce } from "./replay.js";
import Gauge from "./Gauge.jsx";
import { changesText, signedPct } from "./ui.jsx";

const SPEEDS = [4, 16, 64];
const STAGE_NAME = { noise: "Measuring the noise", screen: "Screening settings", confirm: "Confirming with repeats",
  combine: "Combining what survived", bisect: "Cutting to the smallest answer", counterfactual: "Reverting each change",
  other: "Code rounds, probes and checks" };

// Plays a recorded investigation when the viewer asks for it; nothing moves until then.
function useReplay(runId, speed, epoch) {
  const [state, dispatch] = useReducer((s, a) => (a === "reset" ? initialState() : a.type === "done"
    ? { ...s, done: true } : reduce(s, a)), undefined, initialState);
  useEffect(() => {
    if (!runId || !epoch) return undefined;
    dispatch("reset");
    if (STATIC) {
      let stop = () => {}, dead = false;
      api.events(runId).then((evs) => {
        if (!dead) stop = play(evs, speed, (e) => dispatch(e), () => dispatch({ type: "done" }));
      }).catch(() => dispatch({ type: "done" }));
      return () => { dead = true; stop(); };
    }
    const es = new EventSource(api.replayUrl(runId, speed));
    es.addEventListener("gf", (m) => dispatch(JSON.parse(m.data)));
    es.addEventListener("done", () => { dispatch({ type: "done" }); es.close(); });
    es.onerror = () => es.close();
    return () => es.close();
  }, [runId, speed, epoch]);
  return state;
}

function ClaimTracks({ claims, state }) {
  return (
    <div className="claims-live">
      {claims.map(({ target }) => {
        const nb = state.noise[target.metric];
        const done = Object.values(state.branches).filter(
          (b) => b.status === "succeeded" && b.parsed_metrics?.[target.metric] !== undefined && Object.keys(b.knob_changes || {}).length);
        let best = null;
        for (const b of done) {
          const v = b.parsed_metrics[target.metric];
          if (best === null || Math.abs(v - target.paper_value) < Math.abs(best.v - target.paper_value)) best = { v, b };
        }
        return (
          <div className="claim" key={target.claim_id}>
            <div className="claim-head"><b>{target.claim_id}</b> {target.metric}{target.held_out && <span className="tag">held out</span>}</div>
            {nb ? (
              <Gauge compact g={{ paper: target.paper_value, code: nb.median, after: null, band: nb.band / Math.abs(target.paper_value || 1) }}
                     live={best ? best.v : null} label={`${target.claim_id}, run by run`} />
            ) : <p className="small">Waiting for the runs that measure the noise…</p>}
            {best && <p className="small" style={{ margin: "2px 0 0" }}>The closest single run so far: {changesText(best.b.knob_changes)}. A label needs confirmed repeats.</p>}
          </div>
        );
      })}
    </div>
  );
}

export default function Replay({ run }) {
  const [speed, setSpeed] = useState(16);
  const [epoch, setEpoch] = useState(0);
  const state = useReplay(run?.id, speed, epoch);
  const claims = (run?.report?.claims || []).slice(0, 4);
  const grouped = useMemo(() => {
    const g = Object.fromEntries(ROUNDS.map((r) => [r, []]));
    for (const id of state.order) g[state.branches[id].round].push(state.branches[id]);
    return g;
  }, [state.order, state.branches]);
  const stages = ["source", "built", "loaded"].map((st) => state.checkpoints.filter((c) => c.stage === st).length);
  const total = run?.report?.runs;
  const recorded = run?.recorded_at ? new Intl.DateTimeFormat(undefined, { dateStyle: "medium" }).format(new Date(run.recorded_at * 1000)) : null;
  const started = epoch > 0;
  const status = !started ? `Recorded${recorded ? ` ${recorded}` : ""}: ${total ?? "?"} runs in sandboxes, ${Math.round((run?.duration_s || 0) / 60)} minutes of wall time.`
    : state.done ? `Replayed: ${state.order.length} runs.` : `Replaying at ${speed}x: ${state.order.length} of ${total ?? "?"} runs…`;

  return (
    <section aria-label="The investigation, replayed">
      <div className="replay-controls">
        <button type="button" className="btn" onClick={() => setEpoch((e) => e + 1)}>{started ? "Replay from the start" : "Replay the investigation"}</button>
        <span className="toggle" role="group" aria-label="Replay speed">
          {SPEEDS.map((s) => <button key={s} type="button" aria-pressed={s === speed} onClick={() => setSpeed(s)}>{s}x</button>)}
        </span>
        <span className="status-line" aria-live="polite">{status}</span>
      </div>
      {started && (
        <div className="inv-grid">
          <div>
            <div className="chain">
              <span className="node">source</span>
              {stages[1] + stages[2] > 0 && <><span aria-hidden="true">/</span><span className="node">built</span><span aria-hidden="true">/</span><span className="node">loaded</span></>}
              <span aria-hidden="true">/</span>
              <span className="node branches">{state.order.length} forked runs</span>
            </div>
            {ROUNDS.filter((r) => grouped[r].length).map((r) => (
              <div className="stage" key={r}>
                <div className="stage-name"><b>{STAGE_NAME[r]}</b><span className="num">{grouped[r].length}</span></div>
                <div className="chips">
                  {grouped[r].map((b) => (
                    <span key={b.id} className={`chip ${chipClass(b, state.verdicts)}`}
                          title={`${b.id}: ${changesText(b.knob_changes) || "as run"}`} />
                  ))}
                </div>
              </div>
            ))}
            <div className="chip-legend">
              <span><span className="chip running" />running</span><span><span className="chip survivor" />survived the screen</span>
              <span><span className="chip pruned" />pruned</span><span><span className="chip" />measured</span>
              <span><span className="chip failed" />failed</span>
            </div>
            <h3 style={{ fontSize: "var(--t1)", margin: "32px 0 12px" }}>The claims, run by run</h3>
            <ClaimTracks claims={claims} state={state} />
            {Object.values(state.attributions).map((a) => (
              <p key={a.claim} className="live-verdict"><b>{a.claim}: {a.label || a.status}</b>
                {a.changes && Object.keys(a.changes).length > 0 && <> with {changesText(a.changes)}</>}
                {a.gap_before !== undefined && <>, gap {signedPct(a.gap_before)} to {signedPct(a.gap_after)}</>}</p>
            ))}
          </div>
          <div>
            <div className="meters">
              <div><small>runs forked</small><b className="num">{state.order.length}</b></div>
              <div><small>builds and loads</small><b className="num">{state.cost?.setup_runs ?? 0}</b></div>
            </div>
            <h3 style={{ fontSize: "var(--t1)", marginBottom: 8 }}>What it did, newest first</h3>
            <ol className="feed">{state.feed.map((f) => <li key={f.seq} className={f.type}>{f.line}</li>)}</ol>
          </div>
        </div>
      )}
    </section>
  );
}
