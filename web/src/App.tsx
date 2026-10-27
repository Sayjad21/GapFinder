import { Suspense, lazy, useEffect, useRef, useState, type ReactNode } from "react";
import Search from "./components/Search.tsx";
import { href, parseHash } from "./nav.ts";
import { Loading, ThemeToggle } from "./ui.tsx";
import Home from "./pages/Home.tsx";

// The home page ships in the first bundle; every other page loads when it is first opened.
const Cases = lazy(() => import("./pages/Cases.tsx"));
const Case = lazy(() => import("./pages/Case.tsx"));
const Synthetic = lazy(() => import("./pages/Synthetic.tsx"));
const RunPage = lazy(() => import("./pages/RunPage.tsx"));
const How = lazy(() => import("./pages/How.tsx"));
const Evidence = lazy(() => import("./pages/Evidence.tsx"));

const NAV: [string, string][] = [["/cases", "Cases"], ["/synthetic", "Known answers"], ["/evidence", "Evidence"], ["/how", "How it works"]];

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

const navigate = (path: string, q: Record<string, string>) => { window.location.hash = href(path, q).slice(1); };

function NotFound() {
  return <div className="shell"><h1 className="not-found">Nothing here</h1><p>That page doesn’t exist. <a href="#/">Go to the start</a>.</p></div>;
}

export default function App() {
  const [route, setRoute] = useState(() => parseHash(window.location.hash));
  const mainRef = useRef<HTMLElement>(null);
  useEffect(() => {
    const on = () => setRoute(parseHash(window.location.hash));
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
  }, [key]); // oxlint-disable-line react/exhaustive-effect-dependencies -- once per route change
  const [top, a, b] = route.parts;
  const section = `/${top || ""}`;

  let page: ReactNode;
  if (!top) page = <Home />;
  else if (top === "cases") page = <Cases />;
  else if (top === "case" && a) page = <Case slug={a} query={route.query} />;
  else if (top === "synthetic") page = <Synthetic query={route.query} navigate={navigate} />;
  else if (top === "run" && a) page = <RunPage id={[a, b].filter(Boolean).join("/")} />;
  else if (top === "how") page = <How />;
  else if (top === "evidence") page = <Evidence />;
  else page = <NotFound />;

  const current = (p: string) => section === p || (p === "/cases" && top === "case") || (p === "/synthetic" && top === "run");
  return (
    <>
      <a className="skip" href="#main" onClick={(e) => { e.preventDefault(); mainRef.current?.focus(); }}>Skip to the content</a>
      <header className="masthead">
        <div className="shell">
          <Wordmark />
          <nav className="mainnav" aria-label="Main">
            {NAV.map(([p, t]) => <a key={p} href={`#${p}`} aria-current={current(p) ? "page" : undefined}>{t}</a>)}
          </nav>
          <Search />
          <ThemeToggle />
        </div>
      </header>
      <main id="main" ref={mainRef} tabIndex={-1}>
        <Suspense fallback={<div className="shell"><Loading what="Loading the page…" /></div>}>{page}</Suspense>
      </main>
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
