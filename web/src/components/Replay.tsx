import { useEffect, useMemo, useState, type CSSProperties } from "react";
import { api } from "../api.ts";
import { ROUNDS, STAGE_NAME, STAGE_SHORT, chipClass, gap, stages, useFold, type ReplayState, type RunState, type Segment,
  type Round } from "../replay.ts";
import type { GfEvent, Run, Target } from "../types.ts";
import { changesText, signedPct } from "../ui.tsx";
import { claimName, plain } from "../words.tsx";
import Gauge from "./Gauge.tsx";

const SPEEDS = [4, 16, 64];

function useEvents(runId: string | undefined) {
  const [events, setEvents] = useState<GfEvent[] | null>(null);
  const [error, setError] = useState<Error | null>(null);
  useEffect(() => {
    if (!runId) return undefined;
    let dead = false;
    setEvents(null); setError(null);
    api.events(runId).then((e) => !dead && setEvents(e)).catch((e: Error) => !dead && setError(e));
    return () => { dead = true; };
  }, [runId]);
  return { events, error };
}

// Plays the recorded spacing divided by `speed`: each frame shows the next event, and any that follow within 30 ms.
function usePlayer(events: GfEvent[] | null, speed: number) {
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
function closest(state: ReplayState, target: Target): { v: number; b: RunState } | null {
  let best: { v: number; b: RunState } | null = null;
  for (const b of Object.values(state.branches)) {
    const v = b.parsed_metrics?.[target.metric];
    if (b.status !== "succeeded" || v === undefined || !Object.keys(b.knob_changes || {}).length) continue;
    if (best === null || Math.abs(v - target.paper_value) < Math.abs(best.v - target.paper_value)) best = { v, b };
  }
  return best;
}

// One claim's gauge, run by run: the paper's number, the code as released once the noise is measured, and the closest
// run so far; when the verdict arrives, the answer's reading.
function ClaimGauge({ target, state, compact = false }: { target: Target; state: ReplayState; compact?: boolean }) {
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
        <p className="live-verdict"><b>{plain(verdict.label || verdict.status || "")}</b>
          {verdict.changes && Object.keys(verdict.changes).length > 0 && <> with <code>{changesText(verdict.changes)}</code></>}
          {verdict.gap_before !== undefined && <>: the gap went from {signedPct(verdict.gap_before)} to {signedPct(verdict.gap_after)}</>}.</p>
      ) : best ? (
        <p className="small">Closest single run so far: <code>{changesText(best.b.knob_changes)}</code>. One run is not an answer; a
          verdict needs confirmed repeats and the reverse test.</p>
      ) : null}
    </>
  );
}

function Timeline({ events, pos, setPos, segs, label }: { events: GfEvent[]; pos: number; setPos: (p: number) => void; segs: Segment[]; label: string }) {
  const n = events.length || 1;
  return (
    <div className="timeline-bar">
      <input type="range" className="scrub" min={0} max={events.length} step={1} value={pos} aria-label="Position in the recorded investigation"
             aria-valuetext={label} onChange={(e) => setPos(Number(e.target.value))}
             style={{ "--done": `${(pos / n) * 100}%` } as CSSProperties} />
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

export default function Replay({ run }: { run: Run }) {
  const { events, error } = useEvents(run.id);
  const [speed, setSpeed] = useState(16);
  const { pos, setPos, playing, toggle } = usePlayer(events, speed);
  const state = useFold(events, pos);
  const segs = useMemo(() => (events ? stages(events) : []), [events]);
  const all = run.report?.claims || [];
  const claims = all.slice(0, 4);
  // the feed names claims as the page does, not by internal id
  const named = useMemo(() => {
    const ids = all.map((c): [string, string] => [c.target.claim_id, claimName(c.target)]).filter(([id]) => id);
    return (line: string) => ids.reduce((s, [id, name]) => s.split(id).join(name), line);
  }, [all]);
  const head = claims.find((c) => !c.target.held_out) || claims[0];
  const rest = claims.filter((c) => c !== head);
  const grouped = useMemo(() => {
    const g = Object.fromEntries(ROUNDS.map((r) => [r, [] as RunState[]])) as Record<Round, RunState[]>;
    for (const id of state.order) g[state.branches[id].round].push(state.branches[id]);
    return g;
  }, [state.order, state.branches]);
  const total = run.report?.runs;
  const n = events?.length || 0;
  const last = state.order[state.order.length - 1];
  const now = last ? STAGE_NAME[state.branches[last].round] : null;
  const mins = (s: number) => Math.max(1, Math.round(s / 60));
  const elapsed = state.t0 != null && state.t != null ? state.t - state.t0 : 0;
  const status = !events ? (error ? "Couldn’t load this run’s events." : "Loading the recorded events…")
    : pos === 0 ? `Recorded: ${total ?? "?"} runs in sandboxes over ${mins(run.duration_s || 0)} minutes. Press play, or drag the timeline.`
    : pos >= n ? `Replayed: all ${state.order.length} runs.`
    : `Run ${state.order.length} of ${total ?? "?"}, ${mins(elapsed)} of ${mins(run.duration_s || 0)} minutes in${now ? `: ${now.toLowerCase()}` : ""}.`;

  return (
    <section className="player" aria-label="The investigation, replayed">
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
