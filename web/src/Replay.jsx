import { useEffect, useMemo, useRef, useState } from "react";
import { api } from "./api.js";
import Gauge from "./Gauge.jsx";
import { ROUNDS, STAGE_NAME, STAGE_SHORT, chipClass, gap, initialState, reduce, stages } from "./replay.js";
import { changesText, signedPct } from "./ui.jsx";
import { claimName, plain } from "./words.jsx";

const SPEEDS = [4, 16, 64];
const SNAP = 64; // a folded state is kept every SNAP events, so dragging back never refolds more than SNAP

function useEvents(runId) {
  const [events, setEvents] = useState(null);
  const [error, setError] = useState(null);
  useEffect(() => {
    let dead = false;
    setEvents(null); setError(null);
    api.events(runId).then((e) => !dead && setEvents(e)).catch((e) => !dead && setError(e));
    return () => { dead = true; };
  }, [runId]);
  return { events, error };
}

// The state after the first `pos` events: folded forward from where it was, or from the nearest kept state behind.
function useFold(events, pos) {
  const cache = useRef(null);
  return useMemo(() => {
    if (!events) return initialState();
    let c = cache.current;
    if (!c || c.events !== events) c = cache.current = { events, snaps: new Map([[0, initialState()]]), pos: 0, state: initialState() };
    let from = c.pos, s = c.state;
    if (pos < from) {
      from = Math.floor(pos / SNAP) * SNAP;
      while (!c.snaps.has(from)) from -= SNAP;
      s = c.snaps.get(from);
    }
    for (let i = from; i < pos; i++) {
      s = reduce(s, events[i]);
      if ((i + 1) % SNAP === 0) c.snaps.set(i + 1, s);
    }
    c.pos = pos; c.state = s;
    return s;
  }, [events, pos]);
}

// Plays the recorded spacing divided by `speed`: each frame shows the next event, and any that follow within 30 ms.
function usePlayer(events, speed) {
  const [pos, setPos] = useState(0);
  const [playing, setPlaying] = useState(false);
  useEffect(() => { setPos(0); setPlaying(false); }, [events]);
  useEffect(() => {
    if (!playing || !events) return undefined;
    if (pos >= events.length) { setPlaying(false); return undefined; }
    const delay = gap(events, pos - 1, pos, speed);
    let i = pos + 1;
    while (i < events.length && gap(events, i - 1, i, speed) < 0.03) i += 1;
    const id = setTimeout(() => setPos(i), delay * 1000);
    return () => clearTimeout(id);
  }, [playing, pos, events, speed]);
  const toggle = () => {
    if (!events) return;
    if (!playing && pos >= events.length) setPos(0);
    setPlaying((p) => !p);
  };
  return { pos, setPos, playing, toggle };
}

// the closest finished run to the paper's number on this claim's metric, among runs that changed something
function closest(state, target) {
  let best = null;
  for (const b of Object.values(state.branches)) {
    const v = b.parsed_metrics?.[target.metric];
    if (b.status !== "succeeded" || v === undefined || !Object.keys(b.knob_changes || {}).length) continue;
    if (best === null || Math.abs(v - target.paper_value) < Math.abs(best.v - target.paper_value)) best = { v, b };
  }
  return best;
}

// One claim's gauge, run by run: the paper's number, the code as released once the noise is measured, and the closest
// run so far; when the verdict arrives, the answer's reading.
function ClaimGauge({ target, state, compact }) {
  const nb = state.noise[target.metric];
  const best = closest(state, target);
  const verdict = state.attributions[target.claim_id];
  const answer = verdict?.gap_after != null ? target.paper_value * (1 + verdict.gap_after) : null;
  if (!nb) return <p className="small waiting">Waiting for the five runs that measure the noise…</p>;
  const g = { paper: target.paper_value, code: nb.median, after: null, band: nb.band / Math.abs(target.paper_value || 1), figure: target.figure };
  return (
    <>
      <Gauge compact={compact} caption={false} g={g} live={answer ?? best?.v ?? null}
             liveLabel={answer !== null ? "GapFinder’s answer" : "closest run so far"} label={`${claimName(target)}, run by run`} />
      {verdict ? (
        <p className="live-verdict"><b>{plain(verdict.label || verdict.status)}</b>
          {verdict.changes && Object.keys(verdict.changes).length > 0 && <> with <code>{changesText(verdict.changes)}</code></>}
          {verdict.gap_before !== undefined && <>: the gap went from {signedPct(verdict.gap_before)} to {signedPct(verdict.gap_after)}</>}.</p>
      ) : best ? (
        <p className="small">Closest single run so far: <code>{changesText(best.b.knob_changes)}</code>. One run is not an answer; a
          verdict needs confirmed repeats and the reverse test.</p>
      ) : null}
    </>
  );
}

function Timeline({ events, pos, setPos, segs, label }) {
  const n = events.length || 1;
  return (
    <div className="timeline-bar">
      <input type="range" className="scrub" min={0} max={events.length} step={1} value={pos} aria-label="Position in the recorded investigation"
             aria-valuetext={label} onChange={(e) => setPos(Number(e.target.value))}
             style={{ "--done": `${(pos / n) * 100}%` }} />
      <div className="stage-band" aria-hidden="true">
        {segs.map((s, i) => (
          <button key={i} type="button" tabIndex={-1} className={`seg-stage ${s.round}${pos >= s.from && pos < s.to ? " now" : ""}`}
                  style={{ flexGrow: Math.max(1, s.to - s.from) }} onClick={() => setPos(s.from)} title={STAGE_NAME[s.round]}>
            <span>{STAGE_SHORT[s.round]}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

export default function Replay({ run, intro = null }) {
  const { events, error } = useEvents(run?.id);
  const [speed, setSpeed] = useState(16);
  const { pos, setPos, playing, toggle } = usePlayer(events, speed);
  const state = useFold(events, pos);
  const segs = useMemo(() => (events ? stages(events) : []), [events]);
  const claims = (run?.report?.claims || []).slice(0, 4);
  // the feed names claims as the page does, not by internal id
  const named = useMemo(() => {
    const ids = (run?.report?.claims || []).map((c) => [c.target.claim_id, claimName(c.target)]).filter(([id]) => id);
    return (line) => ids.reduce((s, [id, name]) => s.split(id).join(name), line);
  }, [run]);
  const head = claims.find((c) => !c.target.held_out) || claims[0];
  const rest = claims.filter((c) => c !== head);
  const grouped = useMemo(() => {
    const g = Object.fromEntries(ROUNDS.map((r) => [r, []]));
    for (const id of state.order) g[state.branches[id].round].push(state.branches[id]);
    return g;
  }, [state.order, state.branches]);
  const total = run?.report?.runs;
  const n = events?.length || 0;
  const now = state.order.length ? STAGE_NAME[state.branches[state.order[state.order.length - 1]].round] : null;
  const mins = (s) => Math.max(1, Math.round(s / 60));
  const elapsed = state.t0 != null && state.t != null ? state.t - state.t0 : 0;
  const status = !events ? (error ? "Couldn’t load this run’s events." : "Loading the recorded events…")
    : pos === 0 ? `Recorded: ${total ?? "?"} runs in sandboxes over ${mins(run?.duration_s || 0)} minutes. Press play, or drag the timeline.`
    : pos >= n ? `Replayed: all ${state.order.length} runs.`
    : `Run ${state.order.length} of ${total ?? "?"}, ${mins(elapsed)} of ${mins(run?.duration_s || 0)} minutes in${now ? `: ${now.toLowerCase()}` : ""}.`;

  return (
    <section className="player" aria-label="The investigation, replayed">
      {intro}
      <div className="replay-controls">
        <button type="button" className="btn play" onClick={toggle} disabled={!events} aria-pressed={playing}>
          {playing ? "Pause" : pos > 0 && pos < n ? "Resume" : pos >= n && n ? "Replay from the start" : "Play the investigation"}
        </button>
        <span className="toggle" role="group" aria-label="Replay speed">
          {SPEEDS.map((s) => <button key={s} type="button" aria-pressed={s === speed} onClick={() => setSpeed(s)}>{s}×</button>)}
        </span>
        <span className="status-line" aria-live="polite">{status}</span>
      </div>
      {events && events.length > 0 && <Timeline events={events} pos={pos} setPos={setPos} segs={segs} label={status} />}
      {head && (
        <div className="headline-claim">
          <div className="claim-head"><b>{claimName(head.target)}</b> <span className="muted">{head.target.metric}</span></div>
          <ClaimGauge target={head.target} state={state} />
        </div>
      )}
      {pos > 0 && (
        <div className="inv-grid">
          <div>
            <div className="meters">
              <div><small>runs so far</small><b className="num">{state.order.length}</b></div>
              <div><small>builds and loads</small><b className="num">{state.cost?.setup_runs ?? 0}</b></div>
              <div><small>stage</small><b className="stage-now">{now || "setting up"}</b></div>
            </div>
            {ROUNDS.filter((r) => grouped[r].length).map((r) => (
              <div className="stage" key={r}>
                <div className="stage-name"><b>{STAGE_NAME[r]}</b><span className="num">{grouped[r].length}</span></div>
                <div className="chips">
                  {grouped[r].map((b) => (
                    <span key={b.id} className={`chip ${chipClass(b, state.verdicts)}`} title={`${b.id}: ${changesText(b.knob_changes) || "as released"}`} />
                  ))}
                </div>
              </div>
            ))}
            <div className="chip-legend">
              <span><span className="chip running" />running</span><span><span className="chip survivor" />kept after the screen</span>
              <span><span className="chip pruned" />dropped</span><span><span className="chip" />measured</span>
              <span><span className="chip failed" />failed</span>
            </div>
            {rest.length > 0 && (
              <>
                <h3 className="minor-head">The other numbers, run by run</h3>
                <div className="claims-live">
                  {rest.map((c) => (
                    <div className="claim" key={c.target.claim_id}>
                      <div className="claim-head"><b>{claimName(c.target)}</b>{c.target.held_out && <span className="tag">held out</span>}</div>
                      <ClaimGauge compact target={c.target} state={state} />
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
          <div>
            <h3 className="minor-head">What it did, newest first</h3>
            <ol className="feed">{state.feed.map((f) => <li key={f.seq} className={f.type}>{named(f.line)}</li>)}</ol>
          </div>
        </div>
      )}
    </section>
  );
}
