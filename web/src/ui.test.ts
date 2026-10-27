import { describe, expect, it } from "vitest";
import { changesText, digits, prettyKnob, signedPct } from "./ui.tsx";

describe("numbers", () => {
  it("signs percentages with a true minus", () => {
    expect(signedPct(-0.028)).toBe("−2.8%");
    expect(signedPct(0.031)).toBe("+3.1%");
    expect(signedPct(null)).toBe("n/a");
  });
  it("gives enough decimals to tell readings apart", () => {
    expect(digits([0.818, 0.795])).toBe(3);
    expect(digits([90.45, 88.75])).toBe(2);
  });
});

describe("changes in words", () => {
  it("names a patched constant by its file and line", () => {
    expect(prettyKnob("@ast:gae/preprocessing.py:32:test_percent")).toBe("test_percent (gae/preprocessing.py:32)");
  });
  it("reads a code edit as an edit, not a setting set to 1", () => {
    expect(changesText({ "@ast:src/utils.py:79:@mut.32.num.mul2": "1" })).toBe("edit: double the number (src/utils.py:79)");
    expect(changesText({ "@ast:src/train.py:58:@mut.17.Call.red.sum": "1" })).toBe("edit: reduce with sum instead (src/train.py:58)");
  });
  it("names a replaced call without printing its encoded expression", () => {
    const k = "@ast:src/data_loader.py:40:@mut.20.Call.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMSAvLyAyKV0p";
    expect(changesText({ [k]: "1" })).toBe("edit: replace the call’s result (src/data_loader.py:40)");
  });
  it("keeps an ordinary setting as name = value", () => {
    expect(changesText({ learning_rate: "0.001", hidden: "16" })).toBe("learning_rate = 0.001, hidden = 16");
  });
});
