import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Defaults to the docker-compose service hostname (Plan A). Plan B (no Docker, backend and frontend
// running as plain processes on the same host) overrides this via API_PROXY_TARGET, e.g.
// `API_PROXY_TARGET=http://localhost:8000 npm run dev`.
const apiProxyTarget = process.env.API_PROXY_TARGET || "http://backend:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      "/api": {
        target: apiProxyTarget,
        changeOrigin: true,
      },
    },
  },
});
