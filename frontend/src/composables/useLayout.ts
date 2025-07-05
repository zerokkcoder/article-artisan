import { ref, computed } from 'vue'
import { House, DataBoard, Document, Setting } from '@element-plus/icons-vue'
import type { LayoutConfig, MenuItemType } from '../types/layout'
import { useResponsive } from './useResponsive'

// 默认菜单配置
const DEFAULT_MENU_ITEMS: MenuItemType[] = [
  {
    index: '/home',
    title: '首页',
    icon: House
  },
  {
    index: '/home/dashboard',
    title: '仪表盘',
    icon: DataBoard
  },
  {
    index: '2',
    title: '文章管理',
    icon: Document,
    children: [
      { index: '/articles', title: '文章列表' },
      { index: '/articles/new', title: '新建文章' },
      { index: '/articles/drafts', title: '草稿箱' }
    ]
  },
  {
    index: '/settings',
    title: '设置',
    icon: Setting
  }
]

// 默认布局配置
const DEFAULT_LAYOUT_CONFIG: LayoutConfig = {
  header: {
    show: true
  },
  sidebar: {
    show: true,
    width: '200px',
    menuItems: DEFAULT_MENU_ITEMS
  },
  footer: {
    show: true
  },
  responsive: {
    enabled: true,
    breakpoints: {
      mobile: 768,
      tablet: 1024,
      desktop: 1200
    }
  }
}

export function useLayout(initialConfig?: Partial<LayoutConfig>) {
  const layoutConfig = ref<LayoutConfig>({
    ...DEFAULT_LAYOUT_CONFIG,
    ...initialConfig
  })

  const { deviceInfo } = useResponsive(layoutConfig.value.responsive.breakpoints)

  // 响应式布局计算
  const responsiveConfig = computed(() => {
    if (!layoutConfig.value.responsive.enabled) {
      return layoutConfig.value
    }

    const config = { ...layoutConfig.value }
    
    // 移动端适配
    if (deviceInfo.value.isMobile) {
      config.sidebar.show = false // 移动端隐藏侧边栏
      config.sidebar.width = '0px'
    }
    
    // 平板端适配
    if (deviceInfo.value.isTablet) {
      config.sidebar.width = '180px' // 平板端缩小侧边栏
    }
    
    return config
  })

  // 更新布局配置
  const updateLayoutConfig = (newConfig: Partial<LayoutConfig>) => {
    layoutConfig.value = {
      ...layoutConfig.value,
      ...newConfig
    }
  }

  // 切换侧边栏显示
  const toggleSidebar = () => {
    layoutConfig.value.sidebar.show = !layoutConfig.value.sidebar.show
  }

  // 切换组件显示
  const toggleComponent = (component: 'header' | 'sidebar' | 'footer') => {
    layoutConfig.value[component].show = !layoutConfig.value[component].show
  }

  return {
    layoutConfig: responsiveConfig,
    deviceInfo,
    updateLayoutConfig,
    toggleSidebar,
    toggleComponent
  }
}