/**
 * 消息提示工具函数
 */
import { ElMessage } from 'element-plus'

export const showMessage = {
  success: (message: string) => {
    (ElMessage as any).success(message)
  },
  error: (message: string) => {
    (ElMessage as any).error(message)
  },
  warning: (message: string) => {
    (ElMessage as any).warning(message)
  },
  info: (message: string) => {
    (ElMessage as any).info(message)
  }
}