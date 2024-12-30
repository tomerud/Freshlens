import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
    plugins: [
        react(),
        VitePWA({
            registerType: 'autoUpdate',
            manifest: {
                name: 'FreshLens',
                short_name: 'FreshLens',
                description: 'My smart refrigerator',
                theme_color: '#ffffff',
                icons: [
                    {
                        src: '/public/FreshLens.png',
                        sizes: '192x192',
                        type: 'image/png',
                    }
                ],
            },
        }),
    ],
    server: {
        proxy: {
          "/api": {
            target: 'http://localhost:5000',
            changeOrigin: true,
            rewrite: (path) => path.replace(/^\/api/, ''),
          },
        },
    },
});
