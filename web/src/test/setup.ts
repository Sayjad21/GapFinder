import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

// jsdom has no layout: reduced motion makes every animation land at once, and scrolling is a no-op
Object.defineProperty(window, "matchMedia", {
  writable: true,
  value: (query: string) => ({
    matches: query.includes("prefers-reduced-motion"), media: query, onchange: null,
    addEventListener: () => {}, removeEventListener: () => {}, addListener: () => {}, removeListener: () => {}, dispatchEvent: () => false,
  }),
});
Element.prototype.scrollIntoView = function scrollIntoView() {};
window.scrollTo = (() => {}) as typeof window.scrollTo;

afterEach(() => cleanup());
