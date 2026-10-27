import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";
import { primeShowcase } from "../data.ts";
import { SHOWCASE } from "../test/fixtures.ts";
import Search, { index, search } from "./Search.tsx";

describe("search", () => {
  const all = index(SHOWCASE);
  it("indexes papers, planted cases, GapBench tasks, pages and words", () => {
    expect(new Set(all.map((h) => h.kind))).toEqual(new Set(["Page", "Paper", "Planted", "GapBench", "Word"]));
  });
  it("needs every word, and ranks a title match over a mention in the detail", () => {
    expect(search(all, "fast")[0]).toMatchObject({ kind: "Paper", title: "FastGCN" });
    expect(search(all, "fastgcn scale").map((h) => h.title)).toEqual(["A scale or unit convention in FastGCN"]);
    expect(search(all, "no such thing")).toEqual([]);
  });
});

describe("the palette", () => {
  beforeEach(() => { primeShowcase(SHOWCASE); window.location.hash = "#/"; });
  it("opens on /, moves with the arrows, and opens the match on Enter", () => {
    render(<Search />);
    fireEvent.keyDown(window, { key: "/" });
    const box = screen.getByRole("combobox", { name: "Search" });
    fireEvent.change(box, { target: { value: "sdcn" } });
    expect(screen.getAllByRole("option")[0].getAttribute("aria-selected")).toBe("true");
    fireEvent.keyDown(box, { key: "Enter" });
    expect(window.location.hash).toBe("#/case/sdcn");
    expect(screen.queryByRole("dialog")).toBeNull();
  });
  it("closes on Escape", () => {
    render(<Search />);
    fireEvent.click(screen.getByRole("button", { name: /Search/ }));
    fireEvent.keyDown(screen.getByRole("combobox"), { key: "Escape" });
    expect(screen.queryByRole("dialog")).toBeNull();
  });
});
