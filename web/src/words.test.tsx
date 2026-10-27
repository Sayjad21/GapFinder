import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { SHOWCASE } from "./test/fixtures.ts";
import { PlantedChange, Term, WithCode, claimName, plain, vName, versionStatus } from "./words.tsx";

describe("versions", () => {
  it("calls c7 v7 and says where it stands", () => {
    expect(vName("c7")).toBe("v7");
    expect(versionStatus(SHOWCASE, "c7")).toBe("current");
    expect(versionStatus(SHOWCASE, "c5")).toBe("earlier, adopted");
    expect(versionStatus(SHOWCASE, "c10")).toBe("on trial");
  });
});

describe("labels and names", () => {
  it("turns the engine's labels into sentences and leaves unknown ones alone", () => {
    expect(plain("Fits but unsupported")).toBe("A change fits, but nothing else confirms it");
    expect(plain("Something new")).toBe("Something new");
  });
  it("names a claim by where the paper prints it, else by its id", () => {
    expect(claimName({ claim_id: "C_z_acc", figure: "Table 2 (SDCN ACC)" })).toBe("Table 2 (SDCN ACC)");
    expect(claimName({ claim_id: "C_trans_cora_f1", figure: null })).toBe("trans cora f1");
  });
});

describe("planted changes", () => {
  it("says a scale convention in words", () => {
    render(<PlantedChange text="scale: lr: the paper's v is the code's 0.5 x v" />);
    expect(screen.getByText("lr").tagName).toBe("CODE");
    expect(screen.getByText(/a value the paper states as v is 0.5 × v in the code/)).toBeTruthy();
  });
  it("sets backticked identifiers as code", () => {
    const { container } = render(<p><WithCode text="the code calls `np.mean(x)` here" /></p>);
    expect(container.querySelector("code")?.textContent).toBe("np.mean(x)");
  });
});

describe("Term", () => {
  it("is described by its definition, which opens on click and closes on Escape", () => {
    render(<p>a <Term k="batch">fresh batch</Term> of gaps</p>);
    const button = screen.getByRole("button", { name: "fresh batch" });
    const tip = document.getElementById(button.getAttribute("aria-describedby") || "");
    expect(tip?.textContent).toMatch(/new random seed/);
    expect(tip?.className).toBe("visually-hidden");
    fireEvent.click(button);
    expect(tip?.className).toBe("tooltip");
    fireEvent.keyDown(button, { key: "Escape" });
    expect(tip?.className).toBe("visually-hidden");
  });
});
