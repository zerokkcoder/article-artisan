<script setup lang="ts">
// Vue Router 现在处理所有路由逻辑
</script>

<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style scoped>
#app {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  height: 100vh !important;
  overflow: hidden !important;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

#app ::-webkit-scrollbar {
  display: none !important;
}

#app {
  scrollbar-width: none !important;
  -ms-overflow-style: none !important;
}
</style>
