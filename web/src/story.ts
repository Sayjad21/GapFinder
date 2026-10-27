// The investigation told two ways from the same events: as chapters in plain words (what the narrator says), and as
// runs laid out in order for the Hunt chart (each run a dot at its reading, the paper's number a line).
import { STAGE_NAME, roundOf, type ReplayState, type Round } from "./replay.ts";
import type { Changes, GfEvent, Target } from "./types.ts";
import { changesText, digits, num, signedPct } from "./ui.tsx";
import { plain } from "./words.tsx";

// ------------------------------------------------------------------ the runs, in the order they started
export interface RunSlot { id: string; i: number; round: Round; createdAt: number; finishedAt: number | null }

export function runSlots(events: GfEvent[]): RunSlot[] {
  const slots: RunSlot[] = [];
  const at = new Map<string, RunSlot>();
  events.forEach((ev, k) => {
    if (ev.type === "branch_created" && ev.branch.id !== undefined && !at.has(ev.branch.id)) {
      const s: RunSlot = { id: ev.branch.id, i: slots.length, round: roundOf(ev.branch.note), createdAt: k, finishedAt: null };
      slots.push(s); at.set(s.id, s);
    } else if (ev.type === "branch_finished" && ev.branch.id !== undefined) {
      const s = at.get(ev.branch.id);
      if (s && s.finishedAt === null) s.finishedAt = k;
    }
  });
  return slots;
}

// the event position that shows run i finished (or started, if it never finished): where a click on the chart seeks
export const seekTo = (s: RunSlot): number => (s.finishedAt ?? s.createdAt) + 1;

// the stretches of consecutive runs in one stage: [round, first run, last run + 1]
export function runStages(slots: RunSlot[]): { round: Round; from: number; to: number }[] {
  const out: { round: Round; from: number; to: number }[] = [];
  for (const s of slots) {
    const last = out[out.length - 1];
    if (last && last.round === s.round) last.to = s.i + 1;
    else out.push({ round: s.round, from: s.i, to: s.i + 1 });
  }
  return out;
}

// The closest reading to the paper's number so far, run by run: [run index, reading] at each run that improved on it,
// starting from the code as released. Only runs that changed something and finished count.
export function closestPath(state: ReplayState, slots: RunSlot[], target: Target): { i: number; v: number }[] {
  const nb = state.noise[target.metric];
  if (!nb) return [];
  const first = slots.find((s) => s.round !== "noise")?.i ?? slots.length;
  const out = [{ i: first, v: nb.median }];
  let best = nb.median;
  for (const s of slots) {
    const b = state.branches[s.id];
    const v = b?.parsed_metrics?.[target.metric];
    if (!b || b.status !== "succeeded" || v === undefined || !Object.keys(b.knob_changes || {}).length) continue;
    if (Math.abs(v - target.paper_value) < Math.abs(best - target.paper_value)) { best = v; out.push({ i: s.i, v }); }
  }
  return out;
}

// ------------------------------------------------------------------ the chapters
export interface Chapter { key: string; title: string; text: string; now: boolean }

const plural = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;

export function chapters(state: ReplayState, target: Target | undefined, finished: boolean): Chapter[] {
  const runs = state.order.map((id) => state.branches[id]);
  const segs: { round: Round; ids: string[] }[] = [];
  for (const b of runs) {
    const last = segs[segs.length - 1];
    if (last && last.round === b.round) last.ids.push(b.id); else segs.push({ round: b.round, ids: [b.id] });
  }
  const seen: Record<string, number> = {};
  const nb = target ? state.noise[target.metric] : undefined;
  const d = target && nb ? digits([target.paper_value, nb.median]) + 1 : 3;
  const out: Chapter[] = [];
  if (!segs.length) {
    out.push({ key: "setup", title: "Setting up", now: !finished,
      text: "Building the released code once and saving a checkpoint: every experiment starts from that same copy." });
  }
  segs.forEach((seg, k) => {
    const n = seg.ids.length;
    const nth = (seen[seg.round] = (seen[seg.round] ?? 0) + 1);
    const summary = state.rounds.filter((r) => r.name === seg.round && (!r.claim || !target || r.claim === target.claim_id))[nth - 1];
    const open = k === segs.length - 1 && !summary && !finished;
    const kept = seg.ids.filter((id) => {
      const ch = Object.entries(state.branches[id]?.knob_changes || {});
      return ch.length === 1 && state.verdicts[`${ch[0][0]}=${ch[0][1]}`] === "survivor";
    }).length;
    let text: string;
    switch (seg.round) {
      case "noise":
        text = nb ? `The released code, run ${plural(n, "time", "times")} unchanged, gives ${num(nb.median, d)} ± ${num(nb.band, d)}. A number inside that spread is not a gap.`
          : `Running the released code unchanged, ${n} of 5 times, to see how much its number moves on its own.`;
        break;
      // a stage reads in the present while it runs, and in the past once a later stage began or the search ended; its
      // round summary, when the engine wrote one, gives the counts
      case "screen":
        text = summary?.tested != null
          ? `Tried ${plural(summary.tested, "setting", "settings")} one at a time from the saved checkpoint; ${summary.survivors ?? kept} moved the number beyond the noise.`
          : open ? `Trying one setting at a time from the saved checkpoint: ${n} tried so far${kept ? `; ${kept} moved the number beyond the noise` : ""}.`
          : `Tried ${plural(n, "setting", "settings")} one at a time from the saved checkpoint${kept ? `; ${kept} moved the number beyond the noise` : ""}.`;
        break;
      case "confirm":
        text = summary ? `Repeated the strongest leads ${plural(n, "time", "times")}, to rule out luck; ${summary.confirmed ?? 0} held up.`
          : open ? `Repeating what moved the number, to rule out luck: ${plural(n, "repeat", "repeats")} so far.`
          : `Repeated what moved the number ${plural(n, "time", "times")}, to rule out luck.`;
        break;
      case "combine":
        text = summary?.tried != null ? `Tried ${plural(summary.tried, "combination", "combinations")} of what held up; kept ${summary.kept ?? 0}.`
          : open ? `Combining the settings that held up: ${plural(n, "run", "runs")} so far.`
          : `Tried ${plural(n, "combination", "combinations")} of what held up.`;
        break;
      case "bisect": text = `Cutting the answer down to the smallest change that still closes the gap: ${plural(n, "run", "runs")}.`; break;
      case "counterfactual": text = `Undoing each change to check the gap comes back without it: ${plural(n, "run", "runs")}.`; break;
      default: text = `Looking beyond the settings: unit conventions, how the paper reports its number, library versions and small code edits. ${plural(n, "run", "runs")}.`;
    }
    out.push({ key: `${seg.round}-${k}`, title: STAGE_NAME[seg.round], text, now: open });
  });
  const v = target ? state.attributions[target.claim_id] : undefined;
  if (v) {
    const ch: Changes = v.changes || {};
    const moved = v.gap_before !== undefined && v.gap_after !== undefined;
    const change = Object.keys(ch).length ? `${changesText(ch)} takes the gap` : "The gap goes";
    out.push({ key: "verdict", title: "The verdict", now: true,
      text: `${plain(v.label || v.status || "")}.${moved ? ` ${change} from ${signedPct(v.gap_before)} to ${signedPct(v.gap_after)}.` : ""}` });
  }
  return out;
}
