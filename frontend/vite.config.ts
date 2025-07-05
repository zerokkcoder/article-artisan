import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    port: 5173,
    host: 'localhost',
    cors: true,
    open: false // 不自动打开浏览器，因为我们使用pywebview
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    rollupOptions: {
      input: {
        main: resolve(__dirname,'index.html')
      }
    },
    // 优化构建
    minify: 'terser',
    terserOptions: {
        compress: {
          drop_console: true,
          drop_debugger: true
        }
      } as any
  },
  base: './' // 使用相对路径，适配pywebview
})
