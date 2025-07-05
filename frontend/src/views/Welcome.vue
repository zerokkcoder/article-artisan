<template>
  <div class="welcome-page">
    <div class="welcome-header">
      <h1>欢迎使用 Article Artisan</h1>
      <p class="welcome-subtitle">专业的文章创作与管理平台</p>
    </div>
    
    <div class="welcome-content">
      <el-row :gutter="24">
        <el-col :span="8">
          <el-card class="feature-card" shadow="hover">
            <div class="feature-icon">
              <el-icon size="48" color="#409eff">
                <Edit />
              </el-icon>
            </div>
            <h3>智能写作</h3>
            <p>提供丰富的编辑工具和模板，让您的创作更加高效</p>
            <el-button type="primary" @click="$router.push('/articles/new')">
              开始写作
            </el-button>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card class="feature-card" shadow="hover">
            <div class="feature-icon">
              <el-icon size="48" color="#67c23a">
                <DataBoard />
              </el-icon>
            </div>
            <h3>数据分析</h3>
            <p>实时查看文章数据，了解读者喜好和内容表现</p>
            <el-button type="success" @click="$router.push('/home/dashboard')">
              查看数据
            </el-button>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card class="feature-card" shadow="hover">
            <div class="feature-icon">
              <el-icon size="48" color="#e6a23c">
                <Document />
              </el-icon>
            </div>
            <h3>内容管理</h3>
            <p>轻松管理您的所有文章，支持分类、标签和搜索</p>
            <el-button type="warning" @click="$router.push('/articles')">
              管理文章
            </el-button>
          </el-card>
        </el-col>
      </el-row>
      
      <div class="quick-stats">
        <h2>快速概览</h2>
        <el-row :gutter="16">
          <el-col :span="6">
            <div class="stat-item">
              <div class="stat-number">0</div>
              <div class="stat-label">总文章数</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item">
              <div class="stat-number">0</div>
              <div class="stat-label">草稿数</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item">
              <div class="stat-number">0</div>
              <div class="stat-label">今日访问</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item">
              <div class="stat-number">0</div>
              <div class="stat-label">总阅读量</div>
            </div>
          </el-col>
        </el-row>
      </div>
      
      <div class="recent-activity">
        <h2>最近活动</h2>
        <el-empty description="暂无活动记录" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Edit, DataBoard, Document } from '@element-plus/icons-vue'
</script>

<style scoped>
.welcome-page {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-header {
  text-align: center;
  margin-bottom: 40px;
}

.welcome-header h1 {
  font-size: 36px;
  color: #303133;
  margin-bottom: 16px;
  font-weight: 600;
}

.welcome-subtitle {
  font-size: 18px;
  color: #606266;
  margin: 0;
}

.feature-card {
  text-align: center;
  padding: 20px;
  height: 280px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.feature-icon {
  margin-bottom: 16px;
}

.feature-card h3 {
  font-size: 20px;
  color: #303133;
  margin: 16px 0;
}

.feature-card p {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 20px;
  flex: 1;
}

.quick-stats {
  margin: 60px 0 40px;
}

.quick-stats h2 {
  text-align: center;
  color: #303133;
  margin-bottom: 30px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  color: #606266;
  font-size: 14px;
}

.recent-activity {
  margin-top: 40px;
}

.recent-activity h2 {
  color: #303133;
  margin-bottom: 20px;
}
</style>