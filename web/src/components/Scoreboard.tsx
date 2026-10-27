import { useEffect, useState } from "react";
import { api } from "../api.ts";
import type { ArmStats, ScoreRow, Scoreboard as ScoreboardT, Split as SplitT, WilsonRate } from "../types.ts";
import { GAPBENCH_WORDS, PlainLabel, Term } from "../words.tsx";

const ARM_NAMES: Record<string, string> = {
  gapfinder: "GapFinder",
  "gapfinder-noverify": "GapFinder, no verification",
  "gapfinder-noevidence": "GapFinder, evidence step off",
  "gapfinder-random": "GapFinder, random search order",
  "baseline-super": "mini-swe-agent + Nemotron 3 Super",
  "baseline-ultra": "mini-swe-agent + Nemotron 3 Ultra",
};
const armName = (a: string) => ARM_NAMES[a] || a;
// the two arms the comparison is about; the ablations and the trivial arm open on request
const HEADLINE_ARMS = new Set(["gapfinder", "baseline-super", "baseline-ultra"]);
const PAGE = 25;

const MATRIX_COLS: [string, string][] = [
  ["correct_cause", "Correct cause"], ["partial", "Part of it"],
  ["wrong_confident", "Wrong, stated confidently"], ["abstained", "Abstained"], ["missed", "Missed"],
];
const MATRIX_ROWS: ["cause" | "no_cause", string][] = [["cause", "A cause exists"], ["no_cause", "No cause"]];

// Cells that are the right answer for their row are green, confident errors are red.
function cellClass(row: string, col: string, n: number | undefined): string {
  if (!n) return "zero";
  if (col === "wrong_confident") return "bad";
  return (row === "cause" && col === "correct_cause") || (row === "no_cause" && col === "abstained") ? "good" : "";
}

function TrustMatrix({ arm, stats }: { arm: string; stats: ArmStats }) {
  const m = stats.trust_matrix;
  if (!m) return null;
  return (
    <div className="matrix">
      <h4>{armName(arm)}</h4>
      <table>
        <thead><tr><th scope="col">Truth / arm said</th>{MATRIX_COLS.map(([c, label]) => <th scope="col" key={c}>{label}</th>)}</tr></thead>
        <tbody>
          {MATRIX_ROWS.map(([row, label]) => (
            <tr key={row}>
              <th scope="row">{label} <small>({m[row].runs} runs)</small></th>
              {MATRIX_COLS.map(([col]) => {
                const impossible = row === "no_cause" && (col === "correct_cause" || col === "partial");
                return <td key={col} className={impossible ? "zero" : cellClass(row, col, m[row][col])}>{impossible ? "–" : m[row][col]}</td>;
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function rate(r: WilsonRate | undefined): string {
  if (!r || r.rate == null) return "n/a";
  return `${r.k} of ${r.n} (${(r.lo * 100).toFixed(0)}–${(r.hi * 100).toFixed(0)}%)`;
}
function stable(s: ArmStats): string {
  const m = s.answer_stability?.mean;
  return m == null ? "n/a" : `${(m * 100).toFixed(0)}%`;
}

// gapbench_test_v13.json -> "Sealed test v1.3"; the two v1.0 runs were files v1 and v2
const splitName = (name: string, run: number) => (name === "dev" ? "Dev set" : run >= 10 ? `Sealed test v${Math.floor(run / 10)}.${run % 10}`
  : run === 2 ? "Test set, run 2 (frozen v1.0)" : run ? `Test set, run ${run}` : "Test set");

// Every run on every task: closed by default, filtered by arm or by wrong answers, shown 25 rows at a time.
function PerTask({ rows }: { rows: ScoreRow[] }) {
  const [arm, setArm] = useState("");
  const [wrong, setWrong] = useState(false);
  const [shown, setShown] = useState(PAGE);
  const arms = [...new Set(rows.map((r) => r.arm))];
  const sel = rows.filter((r) => (!arm || r.arm === arm) && (!wrong || !r.correct));
  return (
    <details className="group">
      <summary>
        <span className="group-title">Every run, task by task</span>
        <span className="group-count num">{rows.length} runs</span>
        <span className="group-detail">each arm ran each task several times; filter by arm or by wrong answers</span>
      </summary>
      <div className="pertask-controls">
        <label>Arm <select value={arm} onChange={(e) => { setArm(e.target.value); setShown(PAGE); }}>
          <option value="">All arms</option>
          {arms.map((a) => <option key={a} value={a}>{armName(a)}</option>)}
        </select></label>
        <label className="check"><input type="checkbox" checked={wrong} onChange={(e) => { setWrong(e.target.checked); setShown(PAGE); }} /> Only wrong answers</label>
        <span className="status-line" aria-live="polite">{sel.length} runs</span>
      </div>
      <div className="ledger-wrap">
        <table className="rows">
          <thead><tr><th scope="col">Task</th><th scope="col">Kind</th><th scope="col">Arm</th><th scope="col">Right?</th><th scope="col">Answer</th></tr></thead>
          <tbody>
            {sel.slice(0, shown).map((r, i) => {
              const c = Object.values(r.claims)[0] || {};
              return (
                <tr key={i} className={r.false_attr ? "bad" : ""}>
                  <td className="nowrap">{r.task}</td><td>{GAPBENCH_WORDS[r.type] || r.type}</td><td>{armName(r.arm)}</td>
                  <td className="nowrap">{r.correct ? "Right" : r.false_attr ? "Confidently wrong" : "Wrong"}</td>
                  <td>{c.label && <PlainLabel label={c.label} />} {Object.entries(c.knobs || {}).map(([k, v]) => <code key={k}>{k}={v}</code>)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      {sel.length > shown && (
        <button type="button" className="btn quiet spaced-s" onClick={() => setShown((n) => n + PAGE)}>
          Show {Math.min(PAGE, sel.length - shown)} more of {sel.length - shown}
        </button>
      )}
    </details>
  );
}

const of = (x: number | null | undefined, tasks: number) => (x == null ? "n/a" : `${x} of ${tasks}`);

function Split({ name, data }: { name: string; data: SplitT }) {
  const [all, setAll] = useState(false);
  const arms = Object.entries(data.summary || {});
  const matrices = arms.filter(([a, s]) => s.trust_matrix && (all || HEADLINE_ARMS.has(a)));
  const more = arms.filter(([a, s]) => s.trust_matrix && !HEADLINE_ARMS.has(a)).length;
  return (
    <div className="panel">
      <p className="small">{name === "dev"
        ? "Dev tasks are the ones GapFinder was tuned on, so these numbers show the method works, not how well it generalises."
        : "Tasks drawn by a sealed generator from a seed made after that version’s git tag."}
        {" "}Source: <code>eval/results/{data.file}</code>.</p>
      <div className="ledger-wrap">
        <table>
          <thead><tr><th scope="col">Arm</th><th scope="col" className="num">Tasks</th><th scope="col" className="num">Solved (median run)</th>
            <th scope="col" className="num">Solved (best run)</th><th scope="col" className="num"><Term k="confidently_wrong">Confidently wrong</Term></th>
            <th scope="col" className="num">Median $ per task</th><th scope="col" className="num">Median time</th></tr></thead>
          <tbody>
            {arms.map(([arm, s]) => (
              <tr key={arm} className={arm === "gapfinder" ? "us" : ""}>
                <td>{armName(arm)}</td><td className="num">{s.tasks}</td>
                <td className="num">{s.solved_median_run == null ? "n/a" : <><b>{s.solved_median_run}</b> of {s.tasks}</>}</td>
                <td className="num">{of(s.solved_best_run, s.tasks)}</td>
                <td className="num">{s.false_attribution_rate == null ? "n/a" : `${(s.false_attribution_rate * 100).toFixed(0)}%`}</td>
                <td className="num">{s.median_cost_usd == null ? "n/a" : `$${s.median_cost_usd.toFixed(3)}`}</td>
                <td className="num">{s.median_wall_s == null ? "n/a" : `${Math.round(s.median_wall_s)} s`}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {matrices.length > 0 && (
        <>
          <h3 className="sub-title">Trust matrix</h3>
          <p className="small">Rows are what was true; columns are what the arm said. A trustworthy arm finds the cause when one exists
            and <Term k="abstain">abstains</Term> when none does. Cells count runs.</p>
          <div className="matrices">{matrices.map(([arm, s]) => <TrustMatrix key={arm} arm={arm} stats={s} />)}</div>
          {more > 0 && <button type="button" className="btn quiet" aria-expanded={all} onClick={() => setAll((x) => !x)}>
            {all ? "Show only GapFinder and the agent" : `Show the ${more} other arms (ablations and a trivial one)`}</button>}
          <h3 className="sub-title">Rates</h3>
          <p className="small">95% Wilson intervals; with this few tasks they are wide.</p>
          <div className="ledger-wrap">
            <table className="rates">
              <thead><tr><th scope="col">Arm</th><th scope="col">Correct</th><th scope="col">Confidently wrong</th><th scope="col">Correct abstention</th>
                <th scope="col">Missed</th><th scope="col">Same answer across runs</th></tr></thead>
              <tbody>
                {arms.filter(([, s]) => s.rates).map(([arm, s]) => (
                  <tr key={arm} className={arm === "gapfinder" ? "us" : ""}>
                    <td>{armName(arm)}</td><td>{rate(s.rates?.correct)}</td><td>{rate(s.rates?.confidently_wrong)}</td>
                    <td>{rate(s.rates?.correct_abstention)}</td><td>{rate(s.rates?.missed)}</td><td>{stable(s)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
      {(data.rows || []).length > 0 && <PerTask key={name} rows={data.rows || []} />}
    </div>
  );
}

const ORDER = ["test", "test_prev", "dev"];

export default function Scoreboard() {
  const [data, setData] = useState<ScoreboardT | null>(null);
  const [pick, setPick] = useState<string | null>(null);
  useEffect(() => { api.scoreboard().then(setData).catch(() => setData({})); }, []);
  if (!data) return <p className="status-line">Loading…</p>;
  const splits = ORDER.filter((k) => data[k]).concat(Object.keys(data).filter((k) => !ORDER.includes(k)));
  if (!splits.length) return <p>No GapBench results yet.</p>;
  const cur = pick && data[pick] ? pick : splits[0];
  return (
    <section>
      <div className="toggle tabs" role="group" aria-label="Which task set">
        {splits.map((k) => <button key={k} type="button" aria-pressed={k === cur} onClick={() => setPick(k)}>{splitName(k, data[k].run)}</button>)}
      </div>
      <Split key={cur} name={cur} data={data[cur]} />
    </section>
  );
}
