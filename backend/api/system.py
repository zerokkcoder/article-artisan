"""系统相关API"""
import sys
from pathlib import Path


class SystemAPI:
    """系统API类"""
    
    def __init__(self):
        self.data = {"message": "Hello from Python backend!"}
    
    def get_data(self):
        """获取数据的API接口"""
        return self.data
    
    def set_message(self, message):
        """设置消息的API接口"""
        self.data["message"] = message
        return {"success": True, "message": f"Message set to: {message}"}
    
    def get_system_info(self):
        """获取系统信息"""
        return {
            "platform": sys.platform,
            "python_version": sys.version,
            "current_dir": str(Path.cwd())
        }