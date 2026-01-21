import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath } from 'url'
import path from 'path'

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [react()],
    resolve: {
      alias: [
        {
          find: '@',
          replacement: path.resolve(__dirname, 'src')
        }
      ]
    },
    define: {
      'process.env': {}
    },
    server: {
      port: 3000,
      strictPort: true,
      open: true
    },
    build: {
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: false,
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (id.includes('node_modules')) {
              if (id.includes('react') || id.includes('react-dom') || id.includes('react-router-dom')) {
                return 'vendor-react';
              }
              return 'vendor';
            }
          },
          chunkFileNames: 'js/[name]-[hash].js',
          entryFileNames: 'js/[name]-[hash].js',
          assetFileNames: 'assets/[name]-[hash][ext]'
        },
        // Improve build performance
        external: [],
        treeshake: true
      },
      // Improve build performance
      minify: 'esbuild',
      target: 'esnext',
      cssCodeSplit: true,
      reportCompressedSize: true,
      chunkSizeWarningLimit: 1000
    },
    envPrefix: 'VITE_',
    // Improve dev server performance
    optimizeDeps: {
      include: ['react', 'react-dom'],
      force: false
    }
  }
})
