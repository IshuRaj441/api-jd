import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Load env file based on `mode` in the current directory.
  // Set the third parameter to '' to load all env regardless of the `VITE_` prefix.
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [react()],
    // Resolve absolute imports
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src')
      }
    },
    // Ensure environment variables are properly exposed to the client
    define: {
      'process.env': {}
    },
    // Configure development server
    server: {
      port: 3000,
      strictPort: true
    },
    // Build configuration
    build: {
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: false,
      // Ensure environment variables are properly embedded in the build
      rollupOptions: {
        output: {
          manualChunks: {
            react: ['react', 'react-dom', 'react-router-dom'],
            vendor: ['axios', 'date-fns']
          }
        }
      }
    },
    // Environment variables that should be exposed to the client
    envPrefix: 'VITE_'
  }
})
