import { ref, onMounted, onUnmounted } from 'vue'
import type { DeviceInfo, BreakpointType } from '../types/layout'

// 默认断点配置
const DEFAULT_BREAKPOINTS = {
  mobile: 768,
  tablet: 1024,
  desktop: 1200
}

export function useResponsive(breakpoints = DEFAULT_BREAKPOINTS) {
  const deviceInfo = ref<DeviceInfo>({
    type: 'desktop',
    width: 0,
    height: 0,
    isMobile: false,
    isTablet: false,
    isDesktop: true
  })

  const updateDeviceInfo = () => {
    const width = window.innerWidth
    const height = window.innerHeight
    
    let type: BreakpointType = 'desktop'
    if (width < breakpoints.mobile) {
      type = 'mobile'
    } else if (width < breakpoints.tablet) {
      type = 'tablet'
    }
    
    deviceInfo.value = {
      type,
      width,
      height,
      isMobile: type === 'mobile',
      isTablet: type === 'tablet',
      isDesktop: type === 'desktop'
    }
  }

  const handleResize = () => {
    updateDeviceInfo()
  }

  onMounted(() => {
    updateDeviceInfo()
    window.addEventListener('resize', handleResize)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
  })

  return {
    deviceInfo,
    updateDeviceInfo
  }
}