import { useEffect, useState } from "react";
import { api } from "./api.js";

const ARM_NAMES = {
  gapfinder: "GapFinder",
  "gapfinder-noverify": "GapFinder, no verification",
  "gapfinder-noevidence": "GapFinder, evidence step off",
  "gapfinder-random": "GapFinder, random search order",
  "baseline-super": "mini-swe-agent + Nemotron 3 Super",
  "baseline-ultra": "mini-swe-agent + Nemotron 3 Ultra",
};

function Split({ name, data }) {
  const arms = Object.entries(data.summary || {});
  return (
    <div className="panel wide">
      <h3>{name === "dev" ? "Dev set" : "Test set"} <small>({data.file})</small></h3>
      {name === "dev" && (
        <p className="note">Dev tasks are the ones GapFinder was tuned on, so these numbers show the method works,
          not how well it generalises. The test set is written by a second author and run twice.</p>
      )}
      <table>
        <thead><tr><th>Arm</th><th>Tasks</th><th>Solved (median run)</th><th>Solved (best run)</th><th>False attribution</th><th>Median $/task</th><th>Median wall</th></tr></thead>
        <tbody>
          {arms.map(([arm, s]) => (
            <tr key={arm} className={arm === "gapfinder" ? "us" : ""}>
              <td>{ARM_NAMES[arm] || arm}</td><td>{s.tasks}</td>
              <td><b>{s.solved_median_run}</b> / {s.tasks}</td><td>{s.solved_best_run} / {s.tasks}</td>
              <td>{(s.false_attribution_rate * 100).toFixed(0)}%</td>
              <td>${s.median_cost_usd.toFixed(3)}</td><td>{Math.round(s.median_wall_s)} s</td>
            </tr>
          ))}
        </tbody>
      </table>
      <h4>Per task</h4>
      <table className="rows">
        <thead><tr><th>Task</th><th>Type</th><th>Arm</th><th>Correct</th><th>Answer</th></tr></thead>
        <tbody>
          {(data.rows || []).map((r, i) => {
            const c = Object.values(r.claims)[0] || {};
            return (
              <tr key={i} className={r.false_attr ? "bad" : r.correct ? "good" : ""}>
                <td>{r.task}</td><td>{r.type}</td><td>{ARM_NAMES[r.arm] || r.arm}</td>
                <td>{r.correct ? "✓" : "✗"}{r.false_attr ? " (confidently wrong)" : ""}</td>
                <td><small>{c.label}</small> {Object.entries(c.knobs || {}).map(([k, v]) => <code key={k}>{k}={v}</code>)}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default function Scoreboard() {
  const [data, setData] = useState(null);
  useEffect(() => { api.scoreboard().then(setData).catch(() => setData({})); }, []);
  if (!data) return <p>Loading…</p>;
  const splits = Object.entries(data);
  if (!splits.length) return <p>No GapBench results yet.</p>;
  return <section>{splits.map(([name, d]) => <Split key={name} name={name} data={d} />)}</section>;
}
