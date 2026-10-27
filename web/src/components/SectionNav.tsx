import { useEffect, useState } from "react";
import { prefersReducedMotion } from "../ui.tsx";

// A long page's contents, kept in view under the masthead: one button per section, the one being read marked. They
// scroll rather than link, because the hash holds the route.
export default function SectionNav({ items }: { items: [string, string][] }) {
  const [active, setActive] = useState(items[0]?.[0]);
  useEffect(() => {
    if (typeof IntersectionObserver === "undefined") return undefined;
    const els = items.map(([id]) => document.getElementById(id)).filter((e): e is HTMLElement => Boolean(e));
    const io = new IntersectionObserver((entries) => {
      const seen = entries.filter((e) => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (seen[0]) setActive(seen[0].target.id);
    }, { rootMargin: "-120px 0px -55% 0px" });
    els.forEach((e) => io.observe(e));
    return () => io.disconnect();
  }, [items]);
  return (
    <nav className="section-nav" aria-label="On this page">
      {items.map(([id, label]) => (
        <button key={id} type="button" aria-current={active === id ? "location" : undefined}
                onClick={() => {
                  document.getElementById(id)?.scrollIntoView({ behavior: prefersReducedMotion() ? "auto" : "smooth", block: "start" });
                  setActive(id);
                }}>{label}</button>
      ))}
    </nav>
  );
}
