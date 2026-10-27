// Hash routes, so the static site (GitHub Pages) needs no server rewrites. State lives in the query: #/case/sdcn?v=c7
export const href = (path: string, q: Record<string, string | undefined> = {}): string => {
  const qs = new URLSearchParams(Object.entries(q).filter((e): e is [string, string] => Boolean(e[1]))).toString();
  return `#${path}${qs ? `?${qs}` : ""}`;
};

export interface Route { parts: string[]; query: URLSearchParams }

export function parseHash(hash: string): Route {
  const raw = hash.replace(/^#/, "") || "/";
  const [path, qs = ""] = raw.split("?");
  return { parts: path.split("/").filter(Boolean).map(decodeURIComponent), query: new URLSearchParams(qs) };
}
