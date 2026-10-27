import { GLOSSARY } from "../words.tsx";

const STEPS: [string, string][] = [
  ["Read the paper", "Nemotron reads the paper and lists every number it reports, each with its exact quote, and every setting it states or leaves out."],
  ["Describe how to run the code", "A harness, a short file, says how to build the released code, run it, read its output, and which settings may change. A person approves it."],
  ["Measure the noise", "Five runs of the code as released give its number and its run-to-run spread. A gap inside that spread is not a gap."],
  ["Search the settings", "Each candidate setting runs once from the same saved checkpoint in its own sandbox. What moves the number is repeated, and what survives is combined."],
  ["Check the answer", "Revert each change: the gap must come back. Held-out claims must not get worse. The value needs evidence beyond the fact that it fits."],
  ["Look beyond the settings", "When no setting fits every claim, it tests what settings can’t express: a unit or counting convention, how the paper picks its epoch, a library release, a hard-coded value or a small code edit, made in memory, never on disk."],
  ["Label it honestly", "Explained needs evidence. A code change is never called Explained. And Unexplained is an answer, said plainly, when nothing it could change explains the gap."],
];

export default function How() {
  return (
    <div className="shell">
      <section className="hero page-head">
        <h1>How it works</h1>
        <p className="lede">An investigation is a sequence of experiments, each forked from one built and loaded copy of the code, so a
          hypothesis costs one run, not one setup.</p>
      </section>
      <section className="section tight" aria-label="The steps">
        <ol className="steps">
          {STEPS.map(([t, d]) => <li key={t}><div><h2 className="step-title">{t}</h2><p>{d}</p></div></li>)}
        </ol>
      </section>
      <section className="section" aria-labelledby="limits-title">
        <header><h2 id="limits-title">What it can’t do yet</h2></header>
        <ul className="prose-list">
          <li>Tell apart causes that fit the paper’s numbers equally well. With one reported number, several changes often fit, and it says so.</li>
          <li>Find a cause the paper never states and the code doesn’t express, such as a different model variant behind the number.</li>
          <li>Prove itself on new papers. Its blind record on sealed papers is 1 of 8, from before this work; a fresh blind batch is the next test.</li>
        </ul>
        <p className="spaced-s">To try it on a paper of your own, <a href="#/check">check a paper</a>.</p>
      </section>
      <section className="section" aria-labelledby="words-title">
        <header><h2 id="words-title">Words used on this site</h2>
          <p>Underlined words elsewhere on the site show these definitions on hover, focus or tap.</p></header>
        <dl className="glossary">
          {Object.entries(GLOSSARY).map(([k, [w, d]]) => <div key={k}><dt>{w}</dt><dd>{d}</dd></div>)}
        </dl>
      </section>
    </div>
  );
}
