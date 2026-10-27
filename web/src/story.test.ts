import { describe, expect, it } from "vitest";
import { foldTo } from "./replay.ts";
import { chapters, closestPath, runSlots, runStages, seekTo } from "./story.ts";
import { EVENTS, RUN } from "./test/fixtures.ts";

const target = RUN.report!.claims[0].target;

describe("the runs, laid out", () => {
  it("gives every run a slot in the order it started, with where it finished", () => {
    const slots = runSlots(EVENTS);
    expect(slots.map((s) => s.id)).toEqual(["B0001", "B0002", "B0003", "B0004", "B0005", "B0006", "B0007", "B0008", "B0009", "B0010", "B0011"]);
    expect(slots.every((s) => s.finishedAt !== null && s.finishedAt > s.createdAt)).toBe(true);
    expect(seekTo(slots[0])).toBe(slots[0].finishedAt! + 1);
  });
  it("groups the runs into stages", () => {
    expect(runStages(runSlots(EVENTS))).toEqual([{ round: "noise", from: 0, to: 5 }, { round: "screen", from: 5, to: 9 }, { round: "confirm", from: 9, to: 11 }]);
  });
  it("tracks the closest run so far, starting from the code as released and only ever closer", () => {
    const path = closestPath(foldTo(EVENTS, EVENTS.length), runSlots(EVENTS), target);
    expect(path[0]).toEqual({ i: 5, v: 0.795 });
    expect(path[path.length - 1].v).toBe(0.818);
    const gaps = path.map((p) => Math.abs(p.v - target.paper_value));
    gaps.slice(1).forEach((g, k) => expect(g).toBeLessThan(gaps[k]));
  });
});

describe("the narrator", () => {
  it("says it is setting up before any run", () => {
    expect(chapters(foldTo(EVENTS, 1), target, false).map((c) => c.title)).toEqual(["Setting up"]);
  });
  it("tells a stage in progress, then its summary once the round reports", () => {
    const during = chapters(foldTo(EVENTS, 16), target, false);
    expect(during[during.length - 1]).toMatchObject({ title: "Screening settings", now: true });
    expect(during[during.length - 1].text).toMatch(/Trying one setting at a time/);
    const after = chapters(foldTo(EVENTS, EVENTS.length), target, true);
    expect(after.map((c) => c.title)).toEqual(["Measuring the noise", "Screening settings", "Confirming with repeats", "The verdict"]);
    expect(after[0].text).toMatch(/gives 0\.7950 ± 0\.0080/);
    expect(after[1].text).toBe("Tried 4 settings one at a time from the saved checkpoint; 1 moved the number beyond the noise.");
    expect(after[2].text).toBe("Repeated what moved the number 2 times, to rule out luck.");
    expect(after[3].text).toBe("Explained, with evidence. learning_rate = 0.001 takes the gap from −2.8% to −0.1%.");
  });
});
