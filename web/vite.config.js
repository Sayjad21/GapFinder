import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In dev, /api goes to the FastAPI server (uvicorn gapfinder.api.server:app --port 8000).
export default defineConfig({
  plugins: [react()],
  base: "./", // relative asset paths: the static site is served under /GapFinder/ on GitHub Pages
  server: { proxy: { "/api": "http://localhost:8000" } },
});
