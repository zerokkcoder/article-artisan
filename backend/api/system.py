"""系统相关API"""
import platform
import psutil
import time
from typing import Dict, Any
from .base import BaseAPI, api_method
from ..exceptions import InternalServerError
from ..events import emit_event, SystemEvents, EventPriority


class SystemAPI(BaseAPI):
    """系统API类"""
    
    def __init__(self):
        super().__init__('system')
        self.data = {"message": "Hello from Python backend!"}
        self.start_time = time.time()
    
    @api_method
    def get_data(self) -> Dict[str, Any]:
        """获取基础数据"""
        return self._create_response(
            success=True,
            data=self.data,
            message="数据获取成功"
        )
    
    @api_method
    def set_message(self, message: str) -> Dict[str, Any]:
        """设置消息的API接口"""
        try:
            self.data["message"] = message
            self.logger.info(f'Message updated to: {message}')
            return self._create_response(
                success=True,
                data={"message": message},
                message="消息设置成功"
            )
        except Exception as e:
            self.logger.error(f'Failed to set message: {str(e)}')
            raise InternalServerError(f'设置消息失败: {str(e)}')
    
    @api_method
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        try:
            # 获取系统基本信息
            system_info = {
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "hostname": platform.node(),
                "processor": platform.processor(),
                "python_version": platform.python_version()
            }
            
            # 获取内存信息
            memory = psutil.virtual_memory()
            memory_info = {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used,
                "free": memory.free
            }
            
            # 获取CPU信息
            cpu_info = {
                "cpu_count": psutil.cpu_count(),
                "cpu_count_logical": psutil.cpu_count(logical=True),
                "cpu_percent": psutil.cpu_percent(interval=1)
            }
            
            # 获取磁盘信息（Windows系统使用C:）
            disk_path = 'C:' if platform.system() == 'Windows' else '/'
            disk = psutil.disk_usage(disk_path)
            disk_info = {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": (disk.used / disk.total) * 100
            }
            
            # 应用运行时间
            uptime = time.time() - self.start_time
            
            self.logger.info('System information retrieved successfully')
            return self._create_response(
                success=True,
                data={
                    "system": system_info,
                    "memory": memory_info,
                    "cpu": cpu_info,
                    "disk": disk_info,
                    "uptime": uptime,
                    "timestamp": time.time()
                },
                message="系统信息获取成功"
            )
        except Exception as e:
            self.logger.error(f'Failed to get system info: {str(e)}')
            raise InternalServerError(f'获取系统信息失败: {str(e)}')
    
    @api_method
    def get_health_status(self) -> Dict[str, Any]:
        """获取系统健康状态"""
        try:
            # 检查内存使用率
            memory = psutil.virtual_memory()
            memory_healthy = memory.percent < 80
            
            # 检查CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_healthy = cpu_percent < 80
            
            # 检查磁盘使用率
            disk_path = 'C:' if platform.system() == 'Windows' else '/'
            disk = psutil.disk_usage(disk_path)
            disk_percent = (disk.used / disk.total) * 100
            disk_healthy = disk_percent < 90
            
            # 整体健康状态
            overall_healthy = memory_healthy and cpu_healthy and disk_healthy
            
            status = 'healthy' if overall_healthy else 'warning'
            if memory.percent > 90 or cpu_percent > 90 or disk_percent > 95:
                status = 'critical'
            
            return self._create_response(
                success=True,
                data={
                    'status': status,
                    'checks': {
                        'memory': {
                            'healthy': memory_healthy,
                            'usage_percent': memory.percent
                        },
                        'cpu': {
                            'healthy': cpu_healthy,
                            'usage_percent': cpu_percent
                        },
                        'disk': {
                            'healthy': disk_healthy,
                            'usage_percent': disk_percent
                        }
                    },
                    'uptime': time.time() - self.start_time,
                    'timestamp': time.time()
                },
                message=f"系统状态: {status}"
            )
        except Exception as e:
            self.logger.error(f'Failed to get health status: {str(e)}')
            raise InternalServerError(f'获取健康状态失败: {str(e)}')