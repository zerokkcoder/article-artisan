<template>
  <div class="common-layout">
    <el-container>
      <!-- 响应式Header -->
      <el-header v-if="layoutConfig.header.show" class="main-header">
        <AppHeader @toggle-sidebar="toggleSidebar" :show-menu-button="deviceInfo.isMobile" />
      </el-header>
      
      <el-container>
        <!-- 响应式Sidebar -->
        <el-aside 
          v-if="layoutConfig.sidebar.show" 
          :width="layoutConfig.sidebar.width" 
          class="main-aside"
          :class="{ 'mobile-sidebar': deviceInfo.isMobile }"
        >
          <AppSidebar :menu-items="layoutConfig.sidebar.menuItems || []" />
        </el-aside>
        
        <el-container>
          <el-main class="main-content" :class="{ 'mobile-content': deviceInfo.isMobile }">
            <router-view />
          </el-main>
          
          <!-- 响应式Footer -->
          <el-footer v-if="layoutConfig.footer.show && !deviceInfo.isMobile" class="main-footer">
            <AppFooter />
          </el-footer>
        </el-container>
      </el-container>
    </el-container>
    
    <!-- 移动端遮罩层 -->
    <div 
      v-if="deviceInfo.isMobile && layoutConfig.sidebar.show" 
      class="mobile-overlay"
      @click="toggleSidebar"
    ></div>
  </div>
</template>

<script setup lang="ts">
import AppHeader from '../components/layouts/AppHeader.vue'
import AppFooter from '../components/layouts/AppFooter.vue'
import AppSidebar from '../components/layouts/AppSidebar.vue'
import { useLayout } from '../composables/useLayout'

const { layoutConfig, deviceInfo, toggleSidebar } = useLayout()
</script>

<style scoped>
.common-layout {
  height: 100vh;
  position: relative;
}

.main-header {
  background-color: #409eff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  z-index: 1000;
}

.main-aside {
  background-color: #545c64;
  transition: all 0.3s ease;
}

.main-aside.mobile-sidebar {
  position: fixed;
  top: 60px;
  left: 0;
  height: calc(100vh - 60px);
  z-index: 1001;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1);
}

.main-content {
  background-color: #f5f5f5;
  padding: 20px;
  min-height: calc(100vh - 120px);
  transition: all 0.3s ease;
}

.main-content.mobile-content {
  padding: 10px;
  min-height: calc(100vh - 60px);
}

.main-footer {
  background-color: #e4e7ed;
  color: #606266;
  text-align: center;
  line-height: 60px;
}

.el-menu-vertical {
  border-right: none;
}

.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

/* 响应式断点 */
@media (max-width: 768px) {
  .main-header {
    padding: 0 10px;
  }
  
  .main-content {
    padding: 10px;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .main-content {
    padding: 15px;
  }
}
</style>