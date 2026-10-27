import { useMemo, type ReactNode } from "react";
import { useShowcase } from "../data.ts";
import { href } from "../nav.ts";
import type { GapBenchCase, PlantedCase } from "../types.ts";
import { Loading, changesText } from "../ui.tsx";
import { GAPBENCH_WORDS, KIND_WORDS, PlainLabel, PlantedChange, Term, vName } from "../words.tsx";

const FAMILIES: [string, string][] = [["", "All"], ["setting", "Settings"], ["scale", "Scale conventions"], ["data", "Data cuts"],
  ["code", "Code defects"], ["reporting", "Reporting rules"], ["control", "Controls"]];
const KIND_COUNT: Record<string, [string, string]> = { setting: ["setting", "settings"], scale: ["scale convention", "scale conventions"],
  data: ["data cut", "data cuts"], code: ["code defect", "code defects"], reporting: ["reporting rule", "reporting rules"], control: ["control", "controls"] };

// cases grouped by a key, the largest group first
function groupBy<T>(rows: T[], key: (r: T) => string): [string, T[]][] {
  const m = new Map<string, T[]>();
  for (const r of rows) m.set(key(r), [...(m.get(key(r)) || []), r]);
  return [...m.entries()].sort((a, b) => b[1].length - a[1].length);
}

const breakdown = (rows: PlantedCase[]) => groupBy(rows, (p) => p.family)
  .map(([k, rs]) => `${rs.length} ${(KIND_COUNT[k] || [k, k])[rs.length === 1 ? 0 : 1]}`).join(", ");

// One group: a line that says what is inside (how many, of which kinds) and opens to the cases.
function Group({ title, count, detail, open, children }: { title: string; count: string; detail: string; open: boolean; children: ReactNode }) {
  return (
    <details className="group" open={open}>
      <summary>
        <span className="group-title">{title}</span>
        <span className="group-count num">{count}</span>
        <span className="group-detail">{detail}</span>
      </summary>
      <div className="ledger-wrap">{children}</div>
    </details>
  );
}

function PlantedGroups({ rows }: { rows: PlantedCase[] }) {
  const groups = groupBy(rows, (p) => p.paper);
  if (!groups.length) return <p className="muted">No planted cases of this kind were solved.</p>;
  return <>{groups.map(([paper, ps], i) => (
    <Group key={paper} title={paper} count={`${ps.length} solved`} open={i === 0 && groups.length < 4} detail={breakdown(ps)}>
      <table>
        <thead><tr><th scope="col">Kind</th><th scope="col">What was planted</th><th scope="col">What GapFinder found</th>
          <th scope="col">Verdict</th><th scope="col">Searched by</th></tr></thead>
        <tbody>
          {ps.map((p) => (
            <tr key={p.id} className="link">
              <td className="paper-cell"><a href={href(`/run/${p.id}`)}>{KIND_WORDS[p.family] || p.family}</a></td>
              <td>{p.planted.length ? p.planted.map((x) => <PlantedChange key={x} text={x} />) : <span className="muted">nothing (a control)</span>}</td>
              <td>{Object.keys(p.found || {}).length ? <code>{changesText(p.found)}</code> : <span className="muted">no change: reported as reproduced</span>}</td>
              <td><PlainLabel label={p.label} /></td>
              <td className="num nowrap">{vName(p.version)} · batch {p.seed}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </Group>
  ))}</>;
}

function GapBenchGroups({ rows }: { rows: GapBenchCase[] }) {
  const detail = (ps: GapBenchCase[]) => {
    const found = ps.filter((p) => p.outcome === "correct").length;
    return [found && `${found} found the cause`, ps.length - found && `${ps.length - found} correctly abstained`].filter(Boolean).join(", ");
  };
  return <>{groupBy(rows, (p) => p.category).map(([cat, ps], i) => (
    <Group key={cat} title={GAPBENCH_WORDS[cat] || cat} count={`${ps.length} solved`} open={i === 0} detail={detail(ps)}>
      <table>
        <thead><tr><th scope="col">Task</th><th scope="col">Outcome</th><th scope="col">What GapFinder found</th></tr></thead>
        <tbody>
          {ps.map((p) => (
            <tr key={p.id} className="link">
              <td className="paper-cell"><a href={href(`/run/${p.id}`)}>{p.title.split(":")[0].replace("GapBench ", "")}</a></td>
              <td>{p.outcome === "correct" ? "Found the cause" : "Correctly abstained"}</td>
              <td>{Object.values(p.found || {}).map((f, k) => <span className="planted" key={k}><code>{changesText(f.changes) || "no change"}</code> <PlainLabel label={f.label} /></span>)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </Group>
  ))}</>;
}

export default function Synthetic({ query, navigate }: { query: URLSearchParams; navigate: (path: string, q: Record<string, string>) => void }) {
  const { data, error } = useShowcase();
  const tab = query.get("tab") === "gapbench" ? "gapbench" : "planted";
  const fam = query.get("family") || "";
  const set = (q: Record<string, string>) => navigate("/synthetic", { tab, family: fam, ...q });
  const planted = useMemo(() => (data?.planted || []).filter((p) => !fam || p.family === fam), [data, fam]);
  const head = (
    <section className="hero page-head">
      <h1>Synthetic cases</h1>
      <p className="lede">Gaps with known answers: changes <Term k="planted">planted</Term> into papers whose code reproduces, and
        the <Term k="gapbench">GapBench</Term> tasks. These are the ones it got right; the evidence page has the full rates, misses included.</p>
    </section>
  );
  if (!data) return <div className="shell">{head}<Loading error={error} /></div>;
  const counts = Object.fromEntries(groupBy(data.planted, (p) => p.family).map(([k, rs]) => [k, rs.length]));
  return (
    <div className="shell">
      {head}
      <div className="toggle tabs" role="group" aria-label="Which set">
        <button type="button" aria-pressed={tab === "planted"} onClick={() => set({ tab: "planted" })}>Planted gaps ({data.planted.length})</button>
        <button type="button" aria-pressed={tab === "gapbench"} onClick={() => set({ tab: "gapbench", family: "" })}>GapBench tasks ({data.gapbench.length})</button>
      </div>
      {tab === "planted" ? (
        <>
          <p className="muted group-lede">{data.planted.length} solved across {groupBy(data.planted, (p) => p.paper).length} papers:
            {" "}{breakdown(data.planted)}. Open a paper to see each case; open a case for its replay and report.</p>
          <div className="filters" role="group" aria-label="Filter by kind of gap">
            {FAMILIES.filter(([k]) => !k || counts[k]).map(([k, t]) => (
              <button key={k || "all"} type="button" className="seg" aria-pressed={fam === k} onClick={() => set({ family: k })}>
                {t} <span className="num">{k ? counts[k] : data.planted.length}</span>
              </button>
            ))}
          </div>
          <div className="groups"><PlantedGroups key={fam} rows={planted} /></div>
        </>
      ) : (
        <>
          <p className="muted group-lede">{data.gapbench.length} tasks solved by {vName(data.gapbench_totals?.version || "c5")} on
            the <Term k="dev_suite">dev suite</Term>, one per task. A correct abstention is the right answer on a task with no cause.</p>
          <div className="groups"><GapBenchGroups rows={data.gapbench} /></div>
        </>
      )}
    </div>
  );
}
