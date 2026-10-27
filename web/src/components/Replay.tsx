import { useEffect, useMemo, useState, type CSSProperties } from "react";
import { api } from "../api.ts";
import { STAGE_NAME, foldTo, gap, useFold, type ReplayState, type RunState } from "../replay.ts";
import { chapters, runSlots } from "../story.ts";
import type { GfEvent, Run, Target } from "../types.ts";
import { changesText, signedPct } from "../ui.tsx";
import { claimName, plain } from "../words.tsx";
import Gauge from "./Gauge.tsx";
import Hunt from "./Hunt.tsx";

const SPEEDS = [4, 16, 64];
const mins = (s: number) => Math.max(1, Math.round(s / 60));

// a run's events, kept with the id they belong to, so a new id reads as loading without resetting anything
function useEvents(runId: string | undefined) {
  const [got, setGot] = useState<{ id: string; events?: GfEvent[]; error?: Error } | null>(null);
  useEffect(() => {
    if (!runId) return undefined;
    let dead = false;
    api.events(runId).then((events) => !dead && setGot({ id: runId, events })).catch((error: Error) => !dead && setGot({ id: runId, error }));
    return () => { dead = true; };
  }, [runId]);
  const mine = got && got.id === runId ? got : null;
  return { events: mine?.events ?? null, error: mine?.error ?? null };
}

// Plays the recorded spacing divided by `speed`: each frame shows the next event, and any that follow within 30 ms.
// The player is keyed by run, so a new run starts from a fresh one; at the last event it simply stops.
function usePlayer(events: GfEvent[] | null, speed: number) {
  const [pos, setPos] = useState(0);
  const [wants, setPlaying] = useState(false);
  const playing = wants && Boolean(events) && pos < (events?.length ?? 0);
  useEffect(() => {
    if (!playing || !events) return undefined;
    const delay = gap(events, pos - 1, pos, speed);
    let i = pos + 1;
    while (i < events.length && gap(events, i - 1, i, speed) < 0.03) i += 1;
    const id = setTimeout(() => setPos(i), delay * 1000);
    return () => clearTimeout(id);
  }, [playing, pos, events, speed]);
  const toggle = () => {
    if (!events) return;
    if (playing) { setPlaying(false); return; }
    if (pos >= events.length) setPos(0);
    setPlaying(true);
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

// Another claim, run by run, as a small gauge: the code as released once the noise is measured, then the closest run
// so far, then the answer.
function ClaimGauge({ target, state }: { target: Target; state: ReplayState }) {
  const nb = state.noise[target.metric];
  const best = closest(state, target);
  const verdict = state.attributions[target.claim_id];
  const answer = verdict?.gap_after != null ? target.paper_value * (1 + verdict.gap_after) : null;
  if (!nb) return <p className="small">Waiting for the runs that measure the noise…</p>;
  const g = { paper: target.paper_value, code: nb.median, after: null, band: nb.band / Math.abs(target.paper_value || 1), figure: target.figure };
  return (
    <>
      <Gauge compact caption={false} g={g} live={answer ?? best?.v ?? null}
             liveLabel={answer !== null ? "GapFinder’s answer" : "closest run so far"} label={`${claimName(target)}, run by run`} />
      {verdict && <p className="live-verdict"><b>{plain(verdict.label || verdict.status || "")}</b>
        {verdict.gap_before !== undefined && <>: {signedPct(verdict.gap_before)} to {signedPct(verdict.gap_after)}</>}.</p>}
    </>
  );
}

const RECENT = 4;

// The narrator: the stages so far, each in a sentence; the one in progress is marked. A long search shows its latest
// stages, with the earlier ones a click away.
function Narration({ items }: { items: ReturnType<typeof chapters> }) {
  const [all, setAll] = useState(false);
  const hidden = all ? 0 : Math.max(0, items.length - RECENT);
  return (
    <div>
      {hidden > 0 && <button type="button" className="btn quiet earlier" onClick={() => setAll(true)}>Show the {hidden} earlier stages</button>}
      <ol className="chapters" aria-label="What it did, stage by stage" start={hidden + 1}>
        {items.slice(hidden).map((c) => (
          <li key={c.key} className={`${c.now ? "now" : ""}${c.key === "verdict" ? " verdict" : ""}`} aria-current={c.now ? "step" : undefined}>
            <b>{c.title}</b><span>{c.text}</span>
          </li>
        ))}
      </ol>
    </div>
  );
}

export default function Replay({ run }: { run: Run }) {
  const { events, error } = useEvents(run.id);
  const [speed, setSpeed] = useState(16);
  const { pos, setPos, playing, toggle } = usePlayer(events, speed);
  const state = useFold(events, pos);
  const final = useMemo(() => (events ? foldTo(events, events.length) : null), [events]);
  const slots = useMemo(() => (events ? runSlots(events) : []), [events]);
  const all = useMemo(() => run.report?.claims || [], [run]);
  const head = all.find((c) => !c.target.held_out) || all[0];
  const rest = all.filter((c) => c !== head).slice(0, 3);
  const n = events?.length || 0;
  const story = chapters(state, head?.target, n > 0 && pos >= n);
  // the raw log names claims as the page does, not by internal id
  const named = useMemo(() => {
    const ids = all.map((c): [string, string] => [c.target.claim_id, claimName(c.target)]).filter(([id]) => id);
    return (line: string) => ids.reduce((s, [id, name]) => s.split(id).join(name), line);
  }, [all]);
  const total = run.report?.runs;
  const last = state.order[state.order.length - 1];
  const now = last ? STAGE_NAME[state.branches[last].round] : null;
  const elapsed = state.t0 != null && state.t != null ? state.t - state.t0 : 0;
  const status = !events ? (error ? "Couldn’t load this run’s events." : "Loading the recorded events…")
    : pos === 0 ? `Recorded: ${total ?? "?"} runs in sandboxes over ${mins(run.duration_s || 0)} minutes. Press play, or press on the chart.`
    : pos >= n ? `Replayed: all ${state.order.length} runs.`
    : `Run ${state.order.length} of ${total ?? "?"}, ${mins(elapsed)} of ${mins(run.duration_s || 0)} minutes in${now ? `: ${now.toLowerCase()}` : ""}.`;
  const hasReadings = Boolean(head && final?.noise[head.target.metric]);

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
      {events && head && hasReadings && final && (
        <>
          <div className="claim-head hunt-head"><b>{claimName(head.target)}</b> <span className="muted">{head.target.metric}</span></div>
          <Hunt slots={slots} state={state} final={final} target={head.target} setPos={setPos} />
        </>
      )}
      {events && events.length > 0 && (
        <input type="range" className="scrub" min={0} max={events.length} step={1} value={pos} aria-label="Position in the recorded investigation"
               aria-valuetext={status} onChange={(e) => setPos(Number(e.target.value))} style={{ "--done": `${(pos / (n || 1)) * 100}%` } as CSSProperties} />
      )}
      {events && (
        <div className="story-grid">
          <Narration items={story} />
          <div>
            {rest.length > 0 && (
              <>
                <h3 className="minor-head">The other numbers, run by run</h3>
                <div className="claims-live">
                  {rest.map((c) => (
                    <div className="claim" key={c.target.claim_id}>
                      <div className="claim-head"><b>{claimName(c.target)}</b>{c.target.held_out && <span className="tag">held out</span>}</div>
                      <ClaimGauge target={c.target} state={state} />
                    </div>
                  ))}
                </div>
              </>
            )}
            {state.feed.length > 0 && (
              <details className="more raw-log">
                <summary>The raw event log, newest first</summary>
                <ol className="feed">{state.feed.map((f) => <li key={f.seq} className={f.type}>{named(f.line)}</li>)}</ol>
              </details>
            )}
            {(() => {
              const best = head ? closest(state, head.target) : null;
              return best && !state.attributions[head!.target.claim_id] ? (
                <p className="small closest-note">Closest single run so far: <code>{changesText(best.b.knob_changes)}</code>. One run is not an
                  answer; a verdict needs confirmed repeats and the reverse test.</p>
              ) : null;
            })()}
          </div>
        </div>
      )}
    </section>
  );
}
