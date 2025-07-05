<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { DataModel, SystemInfo } from '@/types/env'
import { apiService } from '@/services/api'
import ApiStatus from '@/components/ApiStatus.vue'

// 使用环境变量
const appTitle = import.meta.env.VITE_APP_TITLE || 'Article Artisan'
const appVersion = import.meta.env.VITE_APP_VERSION || '1.0.0'

const message = ref<string>('')
const backendData = ref<DataModel | null>(null)
const systemInfo = ref<SystemInfo | null>(null)
const newMessage = ref<string>('')
const loading = ref<boolean>(false)
const error = ref<string>('')

// 清除错误信息
const clearError = (): void => {
  error.value = ''
}

// 获取后端数据
const fetchData = async (): Promise<void> => {
  try {
    loading.value = true
    clearError()

    const response = await apiService.getData()
    if (response.success) {
      backendData.value = response.data || null
      message.value = response.data?.message || ''
    } else {
      error.value = response.message || '获取数据失败'
    }
  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : '获取数据失败'
    error.value = errorMsg
    console.error('Error fetching data:', err)
  } finally {
    loading.value = false
  }
}

// 获取系统信息
const fetchSystemInfo = async (): Promise<void> => {
  try {
const response = await apiService.getSystemInfo()
    if (response.success) {
      systemInfo.value = response.data || null
      error.value = ''
    } else {
      error.value = response.message || '获取系统信息失败'
    }
  } catch (err) {
    console.error('Error fetching system info:', err)
  }
}

// 设置新消息
const setMessage = async (): Promise<void> => {
  if (!newMessage.value.trim()) return

  try {
    loading.value = true
    clearError()

    const response = await apiService.sendMessage(newMessage.value)
    if (response.success) {
    console.log('Message set result:', response.data)
      await fetchData() // 重新获取数据
      newMessage.value = ''
      error.value = ''
    } else {
      error.value = response.message || '发送消息失败'
    }
  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : '设置消息失败'
    error.value = errorMsg
    console.error('Error setting message:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // 等待pywebview API准备就绪
  setTimeout(() => {
    fetchData()
    fetchSystemInfo()
  }, 100)
})
</script>

<template>
  <div class="app">
    <header class="header">
      <h1>🎨 {{ appTitle }}</h1>
      <p>PyWebView + Vite + Vue3 集成示例</p>
      <div class="header-info">
        <span class="version">v{{ appVersion }}</span>
        <ApiStatus />
      </div>
    </header>

    <!-- 错误提示 -->
    <div v-if="error" class="error-banner">
      <span>⚠️ {{ error }}</span>
      <button @click="clearError" class="error-close">✕</button>
    </div>

    <main class="main">
      <div class="card">
        <h2>📡 后端数据</h2>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="backendData" class="data-display">
          <p><strong>当前消息:</strong> {{ message }}</p>
          <button @click="fetchData" class="btn btn-secondary">
            🔄 刷新数据
          </button>
        </div>
        <div v-else class="error">PyWebView API 未就绪</div>
      </div>

      <div class="card">
        <h2>✏️ 设置消息</h2>
        <div class="input-group">
          <input
            v-model="newMessage"
            type="text"
            placeholder="输入新消息..."
            @keyup.enter="setMessage"
            class="input"
          />
          <button
            @click="setMessage"
            :disabled="!newMessage.trim() || loading"
            class="btn btn-primary"
          >
            📤 发送
          </button>
        </div>
      </div>

      <div class="card" v-if="systemInfo">
        <h2>💻 系统信息</h2>
        <div class="system-info">
          <p><strong>平台:</strong> {{ systemInfo.platform }}</p>
          <p>
            <strong>Python版本:</strong>
            {{ systemInfo.python_version.split(' ')[0] }}
          </p>
          <p><strong>当前目录:</strong> {{ systemInfo.current_dir }}</p>
        </div>
      </div>
    </main>

    <footer class="footer">
      <p>🚀 Powered by PyWebView, Vite & Vue3</p>
    </footer>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header {
  text-align: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  position: relative;
}

.header h1 {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 700;
}

.header p {
  margin: 0.5rem 0 0 0;
  opacity: 0.9;
  font-size: 1.1rem;
}

.header-info {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.version {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.2);
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  opacity: 0.8;
}

.error-banner {
  background: rgba(255, 107, 107, 0.9);
  color: white;
  padding: 1rem;
  margin: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  animation: slideDown 0.3s ease-out;
}

.error-close {
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-close:hover {
  background: rgba(255, 255, 255, 0.2);
}

@keyframes slideDown {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.main {
  flex: 1;
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

.card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.card h2 {
  margin: 0 0 1rem 0;
  font-size: 1.3rem;
  font-weight: 600;
}

.data-display {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.input-group {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.input {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 1rem;
}

.input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.3);
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: #4caf50;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #45a049;
  transform: translateY(-2px);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.loading {
  text-align: center;
  opacity: 0.8;
  font-style: italic;
}

.error {
  color: #ffcccb;
  text-align: center;
  font-style: italic;
}

.system-info p {
  margin: 0.5rem 0;
  word-break: break-all;
}

.footer {
  text-align: center;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.2);
  opacity: 0.8;
}

@media (max-width: 768px) {
  .main {
    padding: 1rem;
  }

  .input-group {
    flex-direction: column;
  }

  .input {
    width: 100%;
  }

  .data-display {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
