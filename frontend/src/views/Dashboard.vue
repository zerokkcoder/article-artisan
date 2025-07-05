<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h2>仪表盘</h2>
    </div>
    
    <div class="dashboard-content">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-item">
                <div class="stat-value">1,234</div>
                <div class="stat-label">总文章数</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-item">
                <div class="stat-value">567</div>
                <div class="stat-label">今日访问</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-item">
                <div class="stat-value">89</div>
                <div class="stat-label">评论数</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-item">
                <div class="stat-value">12</div>
                <div class="stat-label">草稿数</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" style="margin-top: 20px;">
          <el-col :span="12">
            <el-card>
              <template #header>
                <span>最近文章</span>
              </template>
              <el-table :data="recentArticles" style="width: 100%">
                <el-table-column prop="title" label="标题" width="200" />
                <el-table-column prop="date" label="发布日期" width="120" />
                <el-table-column prop="status" label="状态" width="80" />
              </el-table>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <template #header>
                <span>快速操作</span>
              </template>
              <div class="quick-actions">
                <el-button type="primary" size="large" style="width: 100%; margin-bottom: 10px;">
                  <el-icon><Edit /></el-icon>
                  新建文章
                </el-button>
                <el-button type="success" size="large" style="width: 100%; margin-bottom: 10px;">
                  <el-icon><Document /></el-icon>
                  管理文章
                </el-button>
                <el-button type="info" size="large" style="width: 100%;">
                  <el-icon><Setting /></el-icon>
                  系统设置
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Edit, Document, Setting } from '@element-plus/icons-vue'

// 模拟数据
const recentArticles = ref([
  { title: '如何使用Vue 3', date: '2024-01-15', status: '已发布' },
  { title: 'TypeScript入门指南', date: '2024-01-14', status: '已发布' },
  { title: 'Element Plus组件库', date: '2024-01-13', status: '草稿' },
  { title: 'Vite构建工具详解', date: '2024-01-12', status: '已发布' },
])
</script>

<style scoped>
.dashboard {
  width: 100%;
  height: 100%;
}

.dashboard-header {
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  color: white;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
}

.dashboard-header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.dashboard-content {
  padding: 0 20px 20px 20px;
}

.stat-card {
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-item {
  padding: 20px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.quick-actions {
  padding: 10px;
}

.el-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
</style>