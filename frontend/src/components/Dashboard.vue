<template>
  <div class="dashboard-container">
    <!-- 顶部导航栏 -->
    <el-header class="header">
      <div class="header-left">
        <h2>Article Artisan</h2>
      </div>
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <el-icon><User /></el-icon>
            {{ currentUser?.username || '用户' }}
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人资料</el-dropdown-item>
              <el-dropdown-item command="settings">设置</el-dropdown-item>
              <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <el-container class="main-container">
      <!-- 侧边栏 -->
      <el-aside class="sidebar" width="250px">
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="dashboard">
            <el-icon><House /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>
          <el-menu-item index="articles">
            <el-icon><Document /></el-icon>
            <span>文章管理</span>
          </el-menu-item>
          <el-menu-item index="editor">
            <el-icon><Edit /></el-icon>
            <span>文章编辑器</span>
          </el-menu-item>
          <el-menu-item index="analytics">
            <el-icon><DataAnalysis /></el-icon>
            <span>数据分析</span>
          </el-menu-item>
          <el-menu-item index="settings">
            <el-icon><Setting /></el-icon>
            <span>系统设置</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-main class="main-content">
        <!-- 仪表盘视图 -->
        <div v-if="activeMenu === 'dashboard'" class="dashboard-view">
          <el-row :gutter="20" class="stats-row">
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-content">
                  <div class="stat-icon">
                    <el-icon color="#409EFF"><Document /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-number">{{ stats.totalArticles }}</div>
                    <div class="stat-label">总文章数</div>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-content">
                  <div class="stat-icon">
                    <el-icon color="#67C23A"><View /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-number">{{ stats.totalViews }}</div>
                    <div class="stat-label">总浏览量</div>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-content">
                  <div class="stat-icon">
                    <el-icon color="#E6A23C"><Star /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-number">{{ stats.totalLikes }}</div>
                    <div class="stat-label">总点赞数</div>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-content">
                  <div class="stat-icon">
                    <el-icon color="#F56C6C"><ChatDotRound /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-number">{{ stats.totalComments }}</div>
                    <div class="stat-label">总评论数</div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>

          <el-row :gutter="20" class="content-row">
            <el-col :span="16">
              <el-card class="chart-card">
                <template #header>
                  <div class="card-header">
                    <span>文章发布趋势</span>
                  </div>
                </template>
                <div class="chart-placeholder">
                  <el-icon size="48" color="#C0C4CC"><TrendCharts /></el-icon>
                  <p>图表区域 (可集成 ECharts)</p>
                </div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="recent-card">
                <template #header>
                  <div class="card-header">
                    <span>最近文章</span>
                  </div>
                </template>
                <div class="recent-articles">
                  <div v-for="article in recentArticles" :key="article.id" class="article-item">
                    <div class="article-title">{{ article.title }}</div>
                    <div class="article-date">{{ article.date }}</div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>

        <!-- 其他视图的占位符 -->
        <div v-else class="placeholder-view">
          <el-result
            icon="info"
            :title="getViewTitle()"
            sub-title="此功能正在开发中，敬请期待！"
          >
            <template #extra>
              <el-button type="primary" @click="activeMenu = 'dashboard'">返回仪表盘</el-button>
            </template>
          </el-result>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuth } from '../composables/useAuth'
import { useUserStore } from '../stores/user'

interface Stats {
  totalArticles: number
  totalViews: number
  totalLikes: number
  totalComments: number
}

interface Article {
  id: number
  title: string
  date: string
}

const { logout, user: currentUser } = useAuth()
const userStore = useUserStore()

const activeMenu = ref('dashboard')

const stats = reactive<Stats>({
  totalArticles: 128,
  totalViews: 15420,
  totalLikes: 2341,
  totalComments: 856
})

const recentArticles = reactive<Article[]>([
  { id: 1, title: 'Vue 3 组合式 API 最佳实践', date: '2024-01-15' },
  { id: 2, title: 'TypeScript 进阶技巧分享', date: '2024-01-14' },
  { id: 3, title: 'Element Plus 组件库使用指南', date: '2024-01-13' },
  { id: 4, title: 'Vite 构建工具深度解析', date: '2024-01-12' },
  { id: 5, title: '前端性能优化实战', date: '2024-01-11' }
])

const handleMenuSelect = (index: string) => {
  activeMenu.value = index
}

const handleCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      (ElMessage as any).info('个人资料功能开发中')
      break
    case 'settings':
      (ElMessage as any).info('设置功能开发中')
      break
    case 'logout':
      try {
          await ElMessageBox.confirm(
            '确定要退出登录吗？',
            '提示',
            {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              type: 'warning'
            }
          )
          
          // 使用组合式函数处理退出登录
          logout()
        } catch {
          // 用户取消
        }
      break
  }
}

const getViewTitle = () => {
  const titles: Record<string, string> = {
    articles: '文章管理',
    editor: '文章编辑器',
    analytics: '数据分析',
    settings: '系统设置'
  }
  return titles[activeMenu.value] || '功能页面'
}

// 初始化用户信息
onMounted(() => {
  userStore.initializeUser()
})
</script>

<style scoped>
.dashboard-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-left h2 {
  margin: 0;
  color: #303133;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.main-container {
  flex: 1;
  overflow: hidden;
}

.sidebar {
  background: #fff;
  border-right: 1px solid #e4e7ed;
}

.sidebar-menu {
  border-right: none;
  height: 100%;
}

.main-content {
  background: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  height: 120px;
}

.stat-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  font-size: 48px;
  margin-right: 20px;
}

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.content-row {
  margin-bottom: 20px;
}

.chart-card,
.recent-card {
  height: 400px;
}

.card-header {
  font-weight: 600;
  color: #303133;
}

.chart-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #909399;
}

.recent-articles {
  height: 300px;
  overflow-y: auto;
}

.article-item {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.article-item:last-child {
  border-bottom: none;
}

.article-title {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
  cursor: pointer;
}

.article-title:hover {
  color: #409eff;
}

.article-date {
  font-size: 12px;
  color: #909399;
}

.placeholder-view {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>