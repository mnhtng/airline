import path from "path"
import tailwindcss from "@tailwindcss/vite"
import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd(), '') // Load all env variables including those without VITE_ prefix
  console.log(">>> Command:", command)
  console.log('>>> Current mode:', mode)
  console.log('>>> Loaded env variables:', env)

  return {
    plugins: [react(), tailwindcss()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    server: {
      allowedHosts: ['localhost', '.ngrok-free.app', 'airline-gamma.vercel.app'],
      host: true, // Listen on all addresses, including LAN and public IPs
      port: 5173,
      ...(env.VITE_DEBUG === 'true' && {
        // Enable debugging options
        cors: true, // Enable CORS for development
        open: false, // Open the browser on server start
        strictPort: true, // Exit if the port is already in use
        hmr: {
          overlay: false, // Disable the error overlay
        },
        // Proxy API requests to the backend server (instead of using env variables for API URLs)
        // proxy: {
        //   '/api/v1': {
        //     target: 'http://localhost:8000',
        //     changeOrigin: true, // Enable CORS for the proxied requests
        //     secure: false, // Disable SSL verification
        //     ws: true, // Enable WebSocket support
        //   },
        // },
      }),
    }
  }
})
