import { renderHook } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { foldTo, gap, MAX_IDLE_S, stages, useFold } from "./replay.ts";
import { EVENTS } from "./test/fixtures.ts";

describe("the timeline", () => {
  it("lays the stream out as the search's stages, in order, covering every event", () => {
    const segs = stages(EVENTS);
    expect(segs.map((s) => s.round)).toEqual(["noise", "screen", "confirm"]);
    expect(segs[0].from).toBe(0);
    expect(segs[segs.length - 1].to).toBe(EVENTS.length);
    segs.slice(1).forEach((s, i) => expect(s.from).toBe(segs[i].to));
  });
  it("divides the recorded spacing by the speed and caps idle time", () => {
    expect(gap(EVENTS, 0, 1, 4)).toBeCloseTo(0.5);
    expect(gap(EVENTS, -1, 0, 4)).toBe(0);
    expect(gap([{ seq: 1, t: 0, type: "done" }, { seq: 2, t: 1000, type: "done" }], 0, 1, 1)).toBe(MAX_IDLE_S);
  });
});

describe("folding the events", () => {
  it("ends with every run, the noise, the screen's verdicts and the attribution", () => {
    const s = foldTo(EVENTS, EVENTS.length);
    expect(s.order).toHaveLength(11);
    expect(s.noise.acc.median).toBe(0.795);
    expect(s.verdicts["learning_rate=0.001"]).toBe("survivor");
    expect(s.attributions.C_cora.label).toBe("Explained");
    expect(s.feed[0].line).toBe("verdict on C_cora: Explained");
  });
  it("gives the same state seeking back and forth as folding from the start", () => {
    const { result, rerender } = renderHook(({ pos }) => useFold(EVENTS, pos), { initialProps: { pos: 0 } });
    for (const pos of [20, 5, 28, 1, 13, 13, 0, 26]) {
      rerender({ pos });
      expect(result.current).toEqual(foldTo(EVENTS, pos));
    }
  });
});
