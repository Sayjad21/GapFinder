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

const MATRIX_COLS = [
  ["correct_cause", "Correct cause"], ["partial", "Part of it"],
  ["wrong_confident", "Wrong, stated confidently"], ["abstained", "Abstained"], ["missed", "Missed"],
];
const MATRIX_ROWS = [["cause", "A cause exists"], ["no_cause", "No cause"]];

// Cells that are the right answer for their row are green, confident errors are red.
function cellClass(row, col, n) {
  if (!n) return "zero";
  if (col === "wrong_confident") return "bad";
  return (row === "cause" && col === "correct_cause") || (row === "no_cause" && col === "abstained") ? "good" : "";
}

function TrustMatrix({ arm, stats }) {
  const m = stats.trust_matrix;
  if (!m) return null;
  return (
    <div className="matrix">
      <h5>{ARM_NAMES[arm] || arm}</h5>
      <table>
        <thead><tr><th>Truth / arm said</th>{MATRIX_COLS.map(([c, label]) => <th key={c}>{label}</th>)}</tr></thead>
        <tbody>
          {MATRIX_ROWS.map(([row, label]) => (
            <tr key={row}>
              <th>{label} <small>({m[row].runs} runs)</small></th>
              {MATRIX_COLS.map(([col]) => {
                const impossible = row === "no_cause" && (col === "correct_cause" || col === "partial");
                return (
                  <td key={col} className={impossible ? "zero" : cellClass(row, col, m[row][col])}>
                    {impossible ? "–" : m[row][col]}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function pct(r) {
  if (!r || r.rate == null) return "n/a";
  return r.k + "/" + r.n + " (" + (r.lo * 100).toFixed(0) + "–" + (r.hi * 100).toFixed(0) + "%)";
}

function stable(s) {
  const m = s.answer_stability && s.answer_stability.mean;
  return m == null ? "n/a" : (m * 100).toFixed(0) + "%";
}

function Split({ name, data }) {
  const arms = Object.entries(data.summary || {});
  return (
    <div className="panel wide">
      <h3>{name === "dev" ? "Dev set" : "Test set" + (data.run ? ", run " + data.run : "") + (data.run === 2 ? " (frozen v1.0)" : "")} <small>({data.file})</small></h3>
      {name === "dev" && (
        <p className="note">Dev tasks are the ones GapFinder was tuned on, so these numbers show the method works,
          not how well it generalises. The test set is 8 tasks drawn by a sealed generator and run twice (run 2 on the
          frozen v1.0 tag); both runs are shown below.</p>
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
      {arms.some(([, s]) => s.trust_matrix) && (
        <>
          <h4>Trust matrix</h4>
          <p className="note">Rows are what was true; columns are what the arm said. A trustworthy arm is right when a
            cause exists and abstains when none does. Cells count runs. Intervals in the table below are 95% Wilson,
            and with this few tasks they are wide.</p>
          <div className="matrices">
            {arms.map(([arm, s]) => <TrustMatrix key={arm} arm={arm} stats={s} />)}
          </div>
          <table className="rates">
            <thead>
              <tr><th>Arm</th><th>Correct</th><th>Confidently wrong</th><th>Correct abstention</th><th>Missed</th><th>Same answer across runs</th></tr>
            </thead>
            <tbody>
              {arms.filter(([, s]) => s.rates).map(([arm, s]) => (
                <tr key={arm} className={arm === "gapfinder" ? "us" : ""}>
                  <td>{ARM_NAMES[arm] || arm}</td><td>{pct(s.rates.correct)}</td>
                  <td>{pct(s.rates.confidently_wrong)}</td><td>{pct(s.rates.correct_abstention)}</td>
                  <td>{pct(s.rates.missed)}</td><td>{stable(s)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
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
