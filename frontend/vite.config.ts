import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
  plugins: [svelte()],
  // for dev
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:7935',
      },
      '/data': {
        target: 'http://127.0.0.1:7935',
      },
    },
  },
})
