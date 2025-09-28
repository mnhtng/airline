import path from "path"
import tailwindcss from "@tailwindcss/vite"
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  // server: {
  //   proxy: {
  //     // Proxy API requests to the backend server (instead of using env variables for API URLs)
  //     '/api/v1': {
  //       target: 'http://localhost:8000',
  //       changeOrigin: true, // Enable CORS for the proxied requests
  //       secure: false, // Disable SSL verification
  //       ws: true, // Enable WebSocket support
  //     },
  //   },
  // }
})
