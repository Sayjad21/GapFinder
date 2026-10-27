import { fireEvent, render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { SHOWCASE } from "../test/fixtures.ts";
import GapField from "./GapField.tsx";

const rowNames = () => within(screen.getByRole("list")).getAllByRole("link").map((a) => a.getAttribute("aria-label")?.split(":")[0]);

describe("the Gap Field", () => {
  it("draws every paper as a link, largest gap first, as released", () => {
    render(<GapField data={SHOWCASE} />);
    expect(rowNames()).toEqual(["FastGCN", "Graph Attention Networks (GAT)", "Structural Deep Clustering Network (SDCN)"]);
    expect(screen.getByRole("link", { name: /^FastGCN: −2\.8% as released, −0\.1% after v7’s change\. Found the documented cause/ })).toBeTruthy();
  });
  it("applies a version's answers, and switches version", () => {
    render(<GapField data={SHOWCASE} />);
    fireEvent.click(screen.getByRole("button", { name: "After v7’s answers" }));
    expect(screen.getByText(/On v7: 3 of 3 right/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "v5" }));
    expect(screen.getByRole("link", { name: /^Structural Deep Clustering Network \(SDCN\): .*Missed it/ })).toBeTruthy();
    expect(screen.getByRole("link", { name: /^Graph Attention Networks \(GAT\): not run on v5/ })).toBeTruthy();
  });
  it("orders by verdict on request", () => {
    render(<GapField data={SHOWCASE} />);
    fireEvent.click(screen.getByRole("button", { name: "By verdict" }));
    expect(rowNames()).toEqual(["FastGCN", "Structural Deep Clustering Network (SDCN)", "Graph Attention Networks (GAT)"]);
  });
});
