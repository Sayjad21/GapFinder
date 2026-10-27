import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { SHOWCASE } from "../test/fixtures.ts";
import Gauge from "./Gauge.tsx";

const g = SHOWCASE.real[0].versions.c7.gauge;

describe("the gap gauge", () => {
  it("labels both readings on the rule as released", () => {
    const { container } = render(<Gauge g={g} show="before" />);
    const text = container.querySelector("svg")?.textContent || "";
    expect(text).toContain("the paper");
    expect(text).toContain("0.818");
    expect(text).toContain("the code, as released");
    expect(text).toContain("0.795");
    expect(text).toContain("−2.8%");
    expect(screen.getByRole("img").getAttribute("aria-label")).toMatch(/The paper reports 0\.818\. The code, as released, gives 0\.795/);
  });
  it("after GapFinder's change, moves the code's jaw and keeps where it started, labelled", () => {
    const { container } = render(<Gauge g={g} show="after" />);
    const text = container.querySelector("svg")?.textContent || "";
    expect(text).toContain("after GapFinder’s change");
    expect(text).toContain("as released");
    expect(text).toContain("−0.1%");
  });
  it("follows a live reading with its own label", () => {
    const { container } = render(<Gauge g={{ ...g!, after: null }} live={0.819} liveLabel="closest run so far" />);
    expect(container.querySelector("svg")?.textContent).toContain("closest run so far");
  });
  it("captions the paper's source and the noise band in a sentence, not a legend", () => {
    render(<Gauge g={g} />);
    expect(screen.getByText(/The paper’s number: Table 5\./)).toBeTruthy();
    expect(screen.getByText(/run-to-run noise around the paper’s number, ±1\.0%/)).toBeTruthy();
  });
});
