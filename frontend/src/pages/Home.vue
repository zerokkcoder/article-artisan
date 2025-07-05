<template>
  <div class="common-layout">
    <el-container>
      <el-header>Header</el-header>
      <el-container>
        <el-aside width="200px">Aside</el-aside>
        <el-container>
          <el-main>Main</el-main>
          <el-footer>Footer</el-footer>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
// Home page component
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

.el-header {
  background-color: #b3c0d1;
  color: var(--el-text-color-primary);
  text-align: center;
  line-height: 60px;
  flex-shrink: 0;
  overflow: hidden !important;
}

.el-aside {
  background-color: #d3dce6;
  color: var(--el-text-color-primary);
  text-align: center;
  line-height: 200px;
  flex-shrink: 0;
  overflow: hidden !important;
}

.el-main {
  background-color: #e9eef3;
  color: var(--el-text-color-primary);
  text-align: center;
  line-height: 160px;
  overflow: hidden !important;
  flex: 1;
}

.el-footer {
  background-color: #b3c0d1;
  color: var(--el-text-color-primary);
  text-align: center;
  line-height: 60px;
  flex-shrink: 0;
  overflow: hidden !important;
}
</style>