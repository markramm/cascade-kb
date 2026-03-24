import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			'/viewer/api': {
				target: 'http://localhost:8088',
				changeOrigin: true,
				rewrite: (p) => p.replace(/^\/viewer\/api/, '/api')
			}
		}
	}
});
