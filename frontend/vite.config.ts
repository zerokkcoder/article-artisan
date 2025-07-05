import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  build: {
    // 代码分割优化
    rollupOptions: {
      output: {
        manualChunks: {
          // 将Vue相关库分离到单独的chunk
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          // 将Element Plus分离到单独的chunk
          'element-plus': ['element-plus', '@element-plus/icons-vue'],
          // 将工具库分离
          'utils': ['lodash-es', 'dayjs']
        },
        // 为chunk文件命名
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]'
      }
    },
    // 调整chunk大小警告限制
    chunkSizeWarningLimit: 1000,
    // 启用源码映射（开发时）
    sourcemap: process.env.NODE_ENV === 'development'
  },
  // 开发服务器配置
  server: {
    port: 5173,
    open: false,
    cors: true,
    // 代理配置（如果需要）
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  // 预览服务器配置
  preview: {
    port: 4173,
    open: false
  }
})
