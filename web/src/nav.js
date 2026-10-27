// Hash routes, so the static site (GitHub Pages) needs no server rewrites. State lives in the query: #/case/sdcn?v=c7
export const href = (path, q = {}) => {
  const qs = new URLSearchParams(Object.entries(q).filter(([, v]) => v)).toString();
  return `#${path}${qs ? `?${qs}` : ""}`;
};
