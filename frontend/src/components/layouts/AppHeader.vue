<template>
  <div class="header-content">
    <div class="header-left">
      <!-- 移动端菜单按钮 -->
      <el-button 
        v-if="showMenuButton" 
        type="text" 
        class="menu-button"
        @click="$emit('toggle-sidebar')"
      >
        <el-icon><Menu /></el-icon>
      </el-button>
      <h2>Article Artisan</h2>
    </div>
    <div class="header-right">
      <el-dropdown>
        <span class="el-dropdown-link">
          用户菜单
          <el-icon class="el-icon--right">
            <arrow-down />
          </el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { ArrowDown, Menu } from '@element-plus/icons-vue'

// 定义props
interface Props {
  showMenuButton?: boolean
}

withDefaults(defineProps<Props>(), {
  showMenuButton: false
})

// 定义emits
defineEmits<{
  'toggle-sidebar': []
}>()

const router = useRouter()
const userStore = useUserStore()

const logout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.header-content {
  background-color: #409eff;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  width: 100%;
  height: 100%;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-left h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.menu-button {
  color: white !important;
  border: none !important;
  background: transparent !important;
  font-size: 18px;
}

.menu-button:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

.header-right {
  display: flex;
  align-items: center;
}

.el-dropdown-link {
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-size: 14px;
}

.el-dropdown-link:hover {
  color: #409eff;
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 10px;
  }
  
  .header-left h2 {
    font-size: 18px;
  }
}
</style>