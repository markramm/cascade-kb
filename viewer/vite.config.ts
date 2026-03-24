/// <reference types="vitest" />
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/viewer/',
  server: {
    proxy: {
      '/viewer/api': {
        target: 'http://localhost:8088',
        changeOrigin: true,
        rewrite: (p) => p.replace(/^\/viewer\/api/, '/api'),
      }
    }
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    testTimeout: 15000,
  },
})
