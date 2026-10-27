import { useEffect, useRef, useState, type RefObject } from "react";
import HeroInstrument from "../components/Hero.tsx";
import GapField from "../components/GapField.tsx";
import { PlantedChart } from "../components/Record.tsx";
import Replay from "../components/Replay.tsx";
import { useRun, useShowcase } from "../data.ts";
import { href } from "../nav.ts";
import type { RealCase } from "../types.ts";
import { Loading, digits, num, prefersReducedMotion } from "../ui.tsx";
import { Term, currentVersion, vName, versionStatus } from "../words.tsx";

const HERO_CASES = ["fastgcn-v15", "sdcn", "gcn-attack", "fair-clustering"];
const SHORT: Record<string, string> = { "gcn-attack": "Topology attack", sdcn: "SDCN", "fastgcn-v15": "FastGCN", "fair-clustering": "Fair Clustering" };
// the investigation the home page plays: the longest of the hero cases, so the replay has a search to show
const WATCH_CASE = "fastgcn-v15";

// true once `ref` comes within a screen of the viewport (at once where there is no IntersectionObserver), so a section
// below the fold fetches its data only when it is about to be seen
function useNear(ref: RefObject<HTMLElement | null>): boolean {
  const [near, setNear] = useState(typeof IntersectionObserver === "undefined");
  useEffect(() => {
    if (near || !ref.current) return undefined;
    const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) setNear(true); }, { rootMargin: "100% 0px" });
    io.observe(ref.current);
    return () => io.disconnect();
  });
  return near;
}

function Watch({ c, load }: { c: RealCase; load: boolean }) {
  const sel = c.versions[c.current];
  const { run, error } = useRun(load ? sel.id : undefined);
  const g = sel.gauge;
  const d = g ? digits([g.paper, g.code]) : 2;
  return (
    <>
      <header>
        <h2 id="watch-title">Watch one investigation</h2>
        {g && <p>{c.title}’s released code gives {num(g.code, d)} where the paper reports {num(g.paper, d)}. This is the recorded search,
          all {g.runs} runs: it measures the noise first, screens each setting from one saved checkpoint, then repeats and combines
          what moved the number. The gauge follows the closest run, and ends on the answer.</p>}
      </header>
      <div className="document">
        {run ? <Replay run={run} key={run.id} /> : <Loading error={error} what="Loading the recorded run…" />}
      </div>
    </>
  );
}

// The headline and lede need no data, so they paint before the manifest arrives; the instrument's space is held meanwhile.
function HeroText() {
  return (
    <>
      <h1 id="hero-title">When a paper’s number and its code’s number disagree, GapFinder finds out why.</h1>
      <p className="lede">It runs the released code in cloud sandboxes, changes one condition at a time, and ends each claim with a
        verdict: the cause, part of it, or a plain statement that nothing it could change explains the gap.</p>
    </>
  );
}

export default function Home() {
  const { data, error } = useShowcase();
  const watch = useRef<HTMLElement>(null);
  const near = useNear(watch);
  if (!data) {
    return (
      <div className="shell">
        <section className="hero" aria-labelledby="hero-title"><HeroText /><div className="instrument-placeholder"><Loading error={error} /></div></section>
      </div>
    );
  }
  const cases = HERO_CASES.map((s) => data.real.find((r) => r.slug === s)).filter((c): c is RealCase => Boolean(c));
  const watchCase = data.real.find((r) => r.slug === WATCH_CASE);
  const tally = data.real_tally || {};
  const cur = currentVersion(data);
  const latest = data.planted_totals.filter((t) => t.adopted).sort((a, b) => b.seed - a.seed || +b.version.slice(1) - +a.version.slice(1))[0];
  const dev = [...data.dev_suite].reverse().find((d) => d.adopted !== false) || data.dev_suite[data.dev_suite.length - 1];
  const toWatch = () => {
    watch.current?.scrollIntoView({ behavior: prefersReducedMotion() ? "auto" : "smooth", block: "start" });
    watch.current?.querySelector<HTMLButtonElement>(".btn.play")?.focus({ preventScroll: true });
  };
  return (
    <div className="shell">
      <section className="hero" aria-labelledby="hero-title">
        <HeroText />
        {cases.length > 0 && <HeroInstrument cases={cases} short={SHORT} />}
        <nav className="start-here" aria-label="Start here">
          {watchCase && <button type="button" className="start" onClick={toWatch}><b>Watch an investigation</b>
            <span>{watchCase.versions[watchCase.current].gauge?.runs} runs, replayed in under a minute</span></button>}
          <a className="start" href={href("/cases")}><b>Browse the 16 real papers</b><span>finds and misses, case by case</span></a>
          <a className="start" href={href("/evidence")}><b>Check the evidence</b><span>what each measurement can and can’t show</span></a>
        </nav>
      </section>

      {watchCase && (
        <section className="section" aria-labelledby="watch-title" ref={watch}>
          <Watch c={watchCase} load={near} />
        </section>
      )}

      <section className="section" aria-labelledby="record-title">
        <header>
          <h2 id="record-title">Sixteen earlier papers, misses included</h2>
          <p>Every paper with a documented cause, its gap drawn from the paper’s number, then closed by what each <Term k="version">version</Term> of
            the engine found. The fixes since {vName(data.real_versions?.[0] || "c5")} were found on these same papers, so this is <Term k="posthoc">post-hoc</Term>:
            it shows what the engine does now, not what it would do on a paper it has never seen.</p>
        </header>
        <GapField data={data} />
        <p className="small after-chart">
          On {vName(cur)}, the current version and the one every paper was re-run on: {tally.found || 0} found, {tally.partial || 0} partly
          found, {tally.no_gap || 0} correctly reported no gap, and {tally.missed || 0} missed. <a href={href("/cases")}>Read every case</a>, or
          see <a href={href("/evidence")}>each version paper by paper</a>.
        </p>
      </section>

      <section className="section" aria-labelledby="evidence-title">
        <header>
          <h2 id="evidence-title">What the evidence says</h2>
          <p>Reruns of known papers are a demonstration. These are the measurements that were sealed or fresh when they were taken.</p>
        </header>
        <div className="facts">
          <div className="fact">
            <div className="figure">{data.blind.correct} <small>of {data.blind.papers}</small></div>
            <p><Term k="sealed">sealed blind papers</Term> explained, all run before this work: {data.blind.partial} partly,
              {" "}{data.blind.missed} missed, {data.blind.confidently_wrong} <Term k="confidently_wrong">confidently wrong</Term>.</p>
          </div>
          {latest && (
            <div className="fact">
              <div className="figure">{latest.found} <small>of {latest.gaps}</small></div>
              <p><Term k="planted">planted gaps</Term> found by {vName(latest.version)}, the {versionStatus(data, latest.version) || "adopted"} version,
                on <Term k="batch">fresh batch</Term> {latest.seed}: {latest.confidently_wrong} confidently wrong, and {latest.controls_correct} of
                {" "}{latest.controls} <Term k="control">controls</Term> left alone.</p>
            </div>
          )}
          {dev && (
            <div className="fact">
              <div className="figure">{dev.correct} <small>of 138</small></div>
              <p>runs of the <Term k="dev_suite">dev suite</Term> with a cause found by {vName(dev.version)}, pooled over two replicates;
                all 114 <Term k="abstain">abstentions</Term> correct.</p>
            </div>
          )}
        </div>
        <div className="subsection">
          <h3>Planted gaps found by each version</h3>
          <p className="muted">Gaps planted into papers whose code reproduces, searched without the paper. Each dot is a fresh batch
            made after the version was frozen.</p>
          <PlantedChart totals={data.planted_totals} />
        </div>
        <p className="after-chart"><a href={href("/evidence")}>See all the measurements</a>, including the comparison with a general coding agent.</p>
      </section>
    </div>
  );
}
