import webview
import threading
import time
import os
import sys
from pathlib import Path

class Api:
    """后端API类，提供前端调用的接口"""
    
    def __init__(self):
        self.data = {"message": "Hello from Python backend!"}
        self.current_user = None
    
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
    
    def login(self, username, password):
        """登录接口"""
        # 模拟登录验证
        if username == "admin" and password == "123456":
            self.current_user = {
                "id": 1,
                "username": username,
                "email": "admin@example.com",
                "avatar": "https://via.placeholder.com/40"
            }
            return {
                "success": True,
                "message": "登录成功",
                "data": {
                    "token": f"mock-jwt-token-admin-{int(time.time())}",
                    "user": self.current_user,
                    "expiresIn": 3600
                }
            }
        else:
            return {
                "success": False,
                "message": "用户名或密码错误",
                "data": None
            }
    
    def register(self, username, email, password, confirmPassword):
        """注册接口"""
        if password != confirmPassword:
            return {
                "success": False,
                "message": "两次输入密码不一致",
                "data": None
            }
        
        # 模拟注册成功
        new_user = {
            "id": 2,
            "username": username,
            "email": email,
            "avatar": "https://via.placeholder.com/40"
        }
        
        return {
            "success": True,
            "message": "注册成功",
            "data": {
                "token": f"mock-jwt-token-{username}-{int(time.time())}",
                "user": new_user,
                "expiresIn": 3600
            }
        }
    
    def logout(self):
        """登出接口"""
        self.current_user = None
        return {
            "success": True,
            "message": "已退出登录",
            "data": None
        }
    
    def get_current_user(self):
        """获取当前用户信息"""
        if self.current_user:
            return {
                "success": True,
                "data": self.current_user
            }
        else:
            return {
                "success": False,
                "message": "未登录",
                "data": None
            }

def create_window():
    """创建webview窗口"""
    api = Api()
    
    # 确定前端文件路径
    if getattr(sys, 'frozen', False):
        # 打包后的执行文件
        frontend_path = Path(sys._MEIPASS) / 'frontend' / 'dist'
    else:
        # 开发环境
        frontend_path = Path(__file__).parent / 'frontend' / 'dist'
    
    # 检查是否存在构建后的前端文件
    index_file = frontend_path / 'index.html'
    
    if index_file.exists():
        # 生产模式：使用构建后的文件
        url = str(index_file)
        print(f"Loading from built files: {url}")
    else:
        # 开发模式：使用开发服务器
        url = 'http://localhost:5173'
        print(f"Loading from dev server: {url}")
        print("Make sure to run 'npm run dev' in the frontend directory first!")
    
    # 创建窗口
    window = webview.create_window(
        title='Article Artisan',
        url=url,
        js_api=api,
        width=1200,
        height=800,
        min_size=(800, 600),
        resizable=False,
        shadow=True,
        on_top=False
    )
    
    return window

def main():
    """主函数"""
    print("Starting Article Artisan...")
    
    # 创建窗口
    window = create_window()
    
    # 启动webview
    webview.start(
        debug=True,  # 开发模式下启用调试
        http_server=True  # 启用内置HTTP服务器
    )

if __name__ == '__main__':
    main()