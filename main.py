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
        resizable=True,
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