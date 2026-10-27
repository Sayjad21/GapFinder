import { useEffect, useRef, useState } from "react";
import { href } from "./nav.js";
import { Case, Cases, Home, How, RunPage } from "./pages.jsx";
import Evidence from "./pages/Evidence.jsx";
import Synthetic from "./pages/Synthetic.jsx";
import { ThemeToggle } from "./ui.jsx";

// Hash routes (see nav.js): the path picks the page, the query holds its state
function parse() {
  const raw = window.location.hash.replace(/^#/, "") || "/";
  const [path, qs = ""] = raw.split("?");
  return { parts: path.split("/").filter(Boolean).map(decodeURIComponent), query: new URLSearchParams(qs) };
}

const NAV = [["/cases", "Cases"], ["/synthetic", "Synthetic"], ["/evidence", "Evidence"], ["/how", "How it works"]];

function Wordmark() {
  return (
    <a className="wordmark" href="#/" aria-label="GapFinder, home">
      <svg width="28" height="28" viewBox="0 0 32 32" aria-hidden="true">
        <rect width="32" height="32" rx="7" fill="var(--ink)" />
        <rect x="9" y="13" width="14" height="6" rx="1" fill="var(--marker)" />
        <path d="M8 8v16M24 8v16" stroke="var(--sheet)" strokeWidth="2.5" strokeLinecap="round" />
      </svg>
      GapFinder
    </a>
  );
}

export default function App() {
  const [route, setRoute] = useState(parse);
  const mainRef = useRef(null);
  useEffect(() => {
    const on = () => setRoute(parse());
    window.addEventListener("hashchange", on);
    return () => window.removeEventListener("hashchange", on);
  }, []);
  const key = route.parts.join("/");
  const first = useRef(true);
  useEffect(() => {
    if (first.current) { first.current = false; return; }
    window.scrollTo({ top: 0 });
    // move focus to the new page’s heading, so a screen reader announces it
    const h = mainRef.current?.querySelector("h1");
    if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
  }, [key]);
  const navigate = (path, q) => { window.location.hash = href(path, q).slice(1); };
  const [top, a, b] = route.parts;
  const section = `/${top || ""}`;

  let page;
  if (!top) page = <Home />;
  else if (top === "cases") page = <Cases />;
  else if (top === "case") page = <Case slug={a} query={route.query} />;
  else if (top === "synthetic") page = <Synthetic query={route.query} navigate={navigate} />;
  else if (top === "run") page = <RunPage id={[a, b].filter(Boolean).join("/")} />;
  else if (top === "how") page = <How />;
  else if (top === "evidence") page = <Evidence />;
  else page = <div className="shell"><h1 style={{ marginTop: 64 }}>Nothing here</h1><p>That page doesn’t exist. <a href="#/">Go to the start</a>.</p></div>;

  const current = (p) => section === p || (p === "/cases" && top === "case") || (p === "/synthetic" && top === "run");
  return (
    <>
      <a className="skip" href="#main" onClick={(e) => { e.preventDefault(); mainRef.current?.focus(); }}>Skip to the content</a>
      <header className="masthead">
        <div className="shell">
          <Wordmark />
          <nav className="mainnav" aria-label="Main">
            {NAV.map(([p, t]) => <a key={p} href={`#${p}`} aria-current={current(p) ? "page" : undefined}>{t}</a>)}
          </nav>
          <ThemeToggle />
        </div>
      </header>
      <main id="main" ref={mainRef} tabIndex={-1} style={{ outline: "none" }}>{page}</main>
      <footer className="colophon">
        <div className="shell">
          <p>GapFinder runs released code in Nebius Token Factory Sandboxes and reads papers with NVIDIA Nemotron. Every number on this
            site comes from a recorded run in the repository, and every case links to its full Gap Report.</p>
          <p>Real-paper cases are post-hoc reruns; planted and GapBench cases are development measurements. Open source, MIT licence.</p>
        </div>
      </footer>
    </>
  );
}
