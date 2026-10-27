import { act, fireEvent, render, screen, within } from "@testing-library/react";
import axe from "axe-core";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App.tsx";
import { primeShowcase } from "../data.ts";
import { EVENTS, RUN, SCOREBOARD, SHOWCASE } from "../test/fixtures.ts";

vi.mock("../api.ts", async (orig) => {
  const m = await orig<typeof import("../api.ts")>();
  const fx = await import("../test/fixtures.ts");
  return {
    ...m,
    api: {
      ...m.api,
      run: async (id: string) => ({ ...fx.RUN, id }),
      events: async () => fx.EVENTS,
      scoreboard: async () => fx.SCOREBOARD,
      showcase: async () => fx.SHOWCASE,
      submit: async () => ({ ok: false, reason: "This public site replays recorded investigations; it can’t start new ones." }),
    },
  };
});

// WCAG A and AA rules; jsdom has no layout, so colour contrast is checked in the browser (Lighthouse in CI), not here
async function violations(container: HTMLElement) {
  const r = await axe.run(container, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"] },
    rules: { "color-contrast": { enabled: false } } });
  return r.violations.map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(" ")).join(", ")}`);
}

async function open(hash: string, heading: string | RegExp) {
  window.location.hash = hash;
  const view = render(<App />);
  await screen.findByRole("heading", { level: 1, name: heading });
  return view;
}

beforeEach(() => { primeShowcase(SHOWCASE); });

describe("every page renders and passes axe", () => {
  const PAGES: [string, string | RegExp][] = [
    ["#/", /GapFinder finds out why/],
    ["#/cases", "Cases"],
    ["#/case/sdcn", "Structural Deep Clustering Network (SDCN)"],
    ["#/synthetic", "Cases with known answers"],
    ["#/synthetic?tab=gapbench", "Cases with known answers"],
    ["#/run/synthetic~planted~a", "FastGCN (on c7)"],
    ["#/evidence", "The evidence"],
    ["#/how", "How it works"],
    ["#/check", "Check a paper"],
  ];
  for (const [hash, h1] of PAGES) {
    it(hash, async () => {
      const { container } = await open(hash, h1);
      await act(async () => { await new Promise((r) => setTimeout(r, 0)); });
      expect(await violations(container)).toEqual([]);
    });
  }
});

describe("the home page", () => {
  it("opens on the gap as released, and the toggle applies GapFinder's change", async () => {
    await open("#/", /GapFinder finds out why/);
    expect(screen.getByText(/As released, the code gives/)).toBeTruthy();
    fireEvent.click(screen.getAllByRole("button", { name: "After GapFinder’s change" })[0]);
    expect(screen.getByText(/The gap shrinks from −2\.8% to/)).toBeTruthy();
  });
  it("draws the record as the Gap Field, one linked stroke per paper, on the current version", async () => {
    await open("#/", /GapFinder finds out why/);
    expect(screen.getByRole("button", { name: "v7 (current)" }).getAttribute("aria-pressed")).toBe("true");
    expect(screen.getAllByRole("link", { name: /as released/ }).map((a) => a.getAttribute("href"))).toEqual(
      expect.arrayContaining(["#/case/fastgcn-v15", "#/case/gat", "#/case/sdcn"]));
  });
});

describe("the replay", () => {
  it("plays to the verdict, and the timeline seeks back to the start", async () => {
    await open("#/", /GapFinder finds out why/);
    const scrub = await screen.findByRole("slider", { name: "Position in the recorded investigation" });
    fireEvent.change(scrub, { target: { value: String(EVENTS.length) } });
    expect(await screen.findByText(/Replayed: all 11 runs/)).toBeTruthy();
    expect(screen.getAllByText(/Explained, with evidence/).length).toBeGreaterThan(0);
    fireEvent.change(scrub, { target: { value: "0" } });
    expect(await screen.findByText(/Press play, or press on the chart/)).toBeTruthy();
  });
});

describe("the report", () => {
  it("leads with the verdict and keeps each question one click away, with its answer on the heading", async () => {
    await open("#/case/sdcn", "Structural Deep Clustering Network (SDCN)");
    expect(await screen.findByText("The full Gap Report")).toBeTruthy();
    const q = screen.getByText("What did we measure?").closest("details") as HTMLDetailsElement;
    expect(q.open).toBe(false);
    expect(within(q).getByText(/0\.795 over 5 runs as released/)).toBeTruthy();
    expect(screen.getByText(/Settings the paper names that this run couldn’t change/)).toBeTruthy();
    expect(screen.getByText("The code trains for 200 epochs; the paper says 50.")).toBeTruthy();
    expect(RUN.report?.claims[0].unknown?.unmapped).toHaveLength(2);
  });
});

describe("the evidence page", () => {
  it("keeps every run behind a filterable list shown 25 at a time", async () => {
    await open("#/evidence", "The evidence");
    expect(await screen.findByText("Every run, task by task")).toBeTruthy();
    expect(screen.getByRole("button", { name: "Show 5 more of 5" })).toBeTruthy();
    fireEvent.change(screen.getByRole("combobox", { name: /Arm/ }), { target: { value: "gapfinder" } });
    expect(screen.getByText("15 runs")).toBeTruthy();
    expect(SCOREBOARD.test.rows).toHaveLength(30);
  });
});

const names = () => screen.getAllByRole("row").slice(1).map((r) => r.querySelector(".paper-cell a")?.textContent);

describe("the cases page", () => {
  it("sorts by a column and filters by what you type", async () => {
    await open("#/cases", "Cases");
    fireEvent.click(screen.getByRole("button", { name: "Paper" }));
    expect(names()).toEqual(["FastGCN", "Graph Attention Networks (GAT)", "Structural Deep Clustering Network (SDCN)"]);
    expect(screen.getByRole("columnheader", { name: /Paper/ }).getAttribute("aria-sort")).toBe("ascending");
    fireEvent.change(screen.getByRole("searchbox"), { target: { value: "pubmed" } });
    expect(names()).toEqual(["Graph Attention Networks (GAT)"]);
  });
});

describe("a case page", () => {
  it("has a contents bar naming its sections", async () => {
    await open("#/case/sdcn", "Structural Deep Clustering Network (SDCN)");
    const nav = screen.getByRole("navigation", { name: "On this page" });
    expect(within(nav).getAllByRole("button").map((b) => b.textContent)).toEqual(["The gap", "Across versions", "The investigation", "The report"]);
  });
});

describe("the synthetic page", () => {
  it("groups planted cases by paper with their counts, and reads code edits in words", async () => {
    await open("#/synthetic", "Cases with known answers");
    expect(screen.getByText(/4 solved across 3 papers/)).toBeTruthy();
    expect(screen.getByText("FastGCN").closest("summary")?.textContent).toMatch(/2 solved.*1 setting, 1 scale convention/);
    expect(screen.getByText("edit: reduce with sum instead (src/train.py:58)")).toBeTruthy();
  });
});

const pdf = (name: string, text: string) => new File([Uint8Array.from(text, (c) => c.charCodeAt(0))], name, { type: "application/pdf" });

describe("checking a paper", () => {
  afterEach(() => { vi.unstubAllGlobals(); });

  it("says what is missing, takes a PDF and a repository, and makes the request without starting it", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ description: "The sample codes for FastGCN", language: "Python",
      stargazers_count: 400, pushed_at: "2019-01-01T00:00:00Z", size: 5196, license: null, archived: false, default_branch: "master" }))));
    await open("#/check", "Check a paper");
    const start = screen.getByRole("button", { name: "Start the investigation" });
    fireEvent.click(start);
    expect(await screen.findByText("Add the paper’s PDF or its arXiv link.")).toBeTruthy();
    expect(screen.getByText("Add the repository the paper released.")).toBeTruthy();
    const drop = screen.getByLabelText(/Drop the paper’s PDF here/);
    expect(document.activeElement).toBe(drop);

    fireEvent.change(drop, { target: { files: [new File(["just text"], "notes.txt", { type: "text/plain" })] } });
    expect(await screen.findByText(/That file isn’t a PDF/)).toBeTruthy();
    fireEvent.change(drop, { target: { files: [pdf("1801.10247v2.pdf", "%PDF-1.4\n<< /Type /Page >>\n<< /Type /Page >>\n<< /Title (FastGCN: Fast Learning with GCNs) >>")] } });
    expect(await screen.findByText("1801.10247v2.pdf")).toBeTruthy();
    expect(screen.getByText(/2 pages/)).toBeTruthy();
    expect((screen.getByLabelText(/^Title/) as HTMLInputElement).value).toBe("FastGCN: Fast Learning with GCNs");
    expect((screen.getByLabelText(/^arXiv ID/) as HTMLInputElement).value).toBe("1801.10247v2");

    fireEvent.change(screen.getByLabelText("Repository"), { target: { value: "https://github.com/matenure/FastGCN" } });
    expect(await screen.findByText("The sample codes for FastGCN", undefined, { timeout: 2000 })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "200 runs" }));
    fireEvent.click(start);

    expect(await screen.findByRole("heading", { name: "Your request is ready" })).toBeTruthy();
    expect(screen.getByText("Not started")).toBeTruthy();
    expect(screen.getByText(/can’t start new ones/)).toBeTruthy();
    const script = document.querySelector("pre.script")?.textContent ?? "";
    expect(script).toContain("git clone https://github.com/matenure/FastGCN work/fastgcn");
    expect(script).toContain("--max-runs 200");
    expect(await violations(document.body)).toEqual([]);

    fireEvent.click(screen.getByRole("button", { name: "Change the request" }));
    expect((screen.getByLabelText("Repository") as HTMLInputElement).value).toBe("https://github.com/matenure/FastGCN");
  });

  it("fills in a real example, and keeps going when GitHub can't be reached", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => { throw new TypeError("offline"); }));
    await open("#/check", "Check a paper");
    fireEvent.change(screen.getByLabelText("Repository"), { target: { value: "someone/elsewhere" } });
    expect(await screen.findByText(/couldn’t be reached/, undefined, { timeout: 2000 })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Fill in an example" }));
    expect((screen.getByLabelText("Repository") as HTMLInputElement).value).toBe("https://github.com/matenure/FastGCN");
    fireEvent.click(screen.getByRole("button", { name: "Start the investigation" }));
    expect(await screen.findByRole("heading", { name: "Your request is ready" })).toBeTruthy();
    expect(screen.getByText("Number").nextElementSibling?.textContent).toBe("Table 5, transductive Cora accuracy · the paper reports 0.818");
  });
});
