<template>
  <div class="common-layout">
    <el-container>
      <el-header class="main-header">
        <div class="header-left">
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
      </el-header>
      <el-container>
        <el-aside width="200px" class="main-aside">
          <el-menu
            :default-active="$route.path"
            class="el-menu-vertical"
            router
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b"
          >
            <el-menu-item index="/home">
              <el-icon><House /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/home/dashboard">
               <el-icon><DataBoard /></el-icon>
               <span>仪表盘</span>
             </el-menu-item>
            <el-sub-menu index="2">
              <template #title>
                <el-icon><Document /></el-icon>
                <span>文章管理</span>
              </template>
              <el-menu-item index="/articles">文章列表</el-menu-item>
              <el-menu-item index="/articles/new">新建文章</el-menu-item>
              <el-menu-item index="/articles/drafts">草稿箱</el-menu-item>
            </el-sub-menu>
            <el-menu-item index="/settings">
              <el-icon><Setting /></el-icon>
              <span>设置</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-container>
          <el-main class="main-content">
            <router-view />
          </el-main>
          <el-footer class="main-footer">
            <div class="footer-content">
              <span>© 2024 Article Artisan. All rights reserved.</span>
            </div>
          </el-footer>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ArrowDown, House, DataBoard, Document, Setting } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const logout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.common-layout {
  height: 100vh !important;
  width: 100vw !important;
  overflow: hidden !important;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
}

.common-layout ::-webkit-scrollbar {
  display: none !important;
}

.common-layout {
  scrollbar-width: none !important;
  -ms-overflow-style: none !important;
}

.el-container {
  height: 100% !important;
  width: 100% !important;
  overflow: hidden !important;
  margin: 0 !important;
  padding: 0 !important;
}

.main-header {
  background-color: #409eff;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  flex-shrink: 0;
  overflow: hidden !important;
}

.header-left h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
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

.main-aside {
  background-color: #545c64;
  flex-shrink: 0;
  overflow: hidden !important;
}

.el-menu-vertical {
  border-right: none;
  height: 100%;
}

.main-content {
  background-color: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.main-footer {
  background-color: #f0f2f5;
  border-top: 1px solid #e4e7ed;
  flex-shrink: 0;
  overflow: hidden !important;
  height: 50px;
  line-height: 50px;
}

.footer-content {
  text-align: center;
  color: #909399;
  font-size: 12px;
}
</style>