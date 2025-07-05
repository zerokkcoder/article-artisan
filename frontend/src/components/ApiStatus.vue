<template>
  <div class="api-status">
    <div class="status-indicator" :class="statusClass">
      <span class="status-dot"></span>
      <span class="status-text">{{ statusText }}</span>
    </div>
    <div v-if="lastUpdate" class="last-update">
      最后更新: {{ formatTime(lastUpdate) }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'

interface Props {
  checkInterval?: number
}

const props = withDefaults(defineProps<Props>(), {
  checkInterval: 5000
})

const isApiAvailable = ref<boolean>(false)
const lastUpdate = ref<Date | null>(null)
let intervalId: number | null = null

const statusClass = computed((): string => {
  return isApiAvailable.value ? 'status-online' : 'status-offline'
})

const statusText = computed((): string => {
  return isApiAvailable.value ? 'API 已连接' : 'API 未连接'
})

const checkApiStatus = (): void => {
  try {
    isApiAvailable.value = !!window.pywebview?.api
    lastUpdate.value = new Date()
  } catch (error) {
    isApiAvailable.value = false
    console.warn('API status check failed:', error)
  }
}

const formatTime = (date: Date): string => {
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

onMounted(() => {
  checkApiStatus()
  intervalId = window.setInterval(checkApiStatus, props.checkInterval)
})

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
})
</script>

<style scoped>
.api-status {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  font-size: 0.875rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.status-online .status-dot {
  background-color: #4ade80;
  box-shadow: 0 0 8px rgba(74, 222, 128, 0.5);
}

.status-offline .status-dot {
  background-color: #f87171;
  box-shadow: 0 0 8px rgba(248, 113, 113, 0.5);
}

.status-text {
  font-weight: 500;
}

.last-update {
  font-size: 0.75rem;
  opacity: 0.7;
}
</style>
