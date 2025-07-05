<template>
  <div class="sidebar-content">
    <el-menu
      :default-active="$route.path"
      class="el-menu-vertical"
      router
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
    >
      <template v-for="item in menuItems" :key="item.index">
        <!-- 普通菜单项 -->
        <el-menu-item v-if="!item.children" :index="item.index">
          <el-icon v-if="item.icon">
            <component :is="item.icon" />
          </el-icon>
          <span>{{ item.title }}</span>
        </el-menu-item>
        
        <!-- 子菜单 -->
        <el-sub-menu v-else :index="item.index">
          <template #title>
            <el-icon v-if="item.icon">
              <component :is="item.icon" />
            </el-icon>
            <span>{{ item.title }}</span>
          </template>
          <el-menu-item 
            v-for="child in item.children" 
            :key="child.index" 
            :index="child.index"
          >
            {{ child.title }}
          </el-menu-item>
        </el-sub-menu>
      </template>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import type { MenuItemType } from '../../types/layout'

interface Props {
  menuItems: MenuItemType[]
}

defineProps<Props>()
</script>

<style scoped>
.sidebar-content {
  width: 100%;
  height: 100%;
  background-color: #545c64;
}

.el-menu-vertical {
  border-right: none;
  height: 100%;
}
</style>