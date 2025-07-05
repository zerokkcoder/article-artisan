import type { Component } from 'vue'

// 菜单项类型定义
export interface MenuItemType {
  index: string
  title: string
  icon?: Component
  children?: MenuItemType[]
}

// 布局配置类型定义
export interface LayoutConfig {
  header: {
    show: boolean
    component?: Component
  }
  sidebar: {
    show: boolean
    width: string
    component?: Component
    menuItems?: MenuItemType[]
  }
  footer: {
    show: boolean
    component?: Component
  }
  responsive: {
    enabled: boolean
    breakpoints: {
      mobile: number
      tablet: number
      desktop: number
    }
  }
}

// 响应式断点类型
export type BreakpointType = 'mobile' | 'tablet' | 'desktop'

// 设备类型
export interface DeviceInfo {
  type: BreakpointType
  width: number
  height: number
  isMobile: boolean
  isTablet: boolean
  isDesktop: boolean
}