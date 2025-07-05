"""窗口配置和创建模块"""
import webview
import sys
from pathlib import Path
from backend.api import MainAPI


class WindowConfig:
    """窗口配置类"""
    
    def __init__(self):
        self.title = 'Article Artisan'
        self.width = 1200
        self.height = 800
        self.min_size = (800, 600)
        self.resizable = False
        self.shadow = True
        self.on_top = False
    
    def get_frontend_url(self):
        """获取前端文件路径或开发服务器URL"""
        # 确定前端文件路径
        if getattr(sys, 'frozen', False):
            # 打包后的执行文件
            frontend_path = Path(sys._MEIPASS) / 'frontend' / 'dist'
        else:
            # 开发环境
            frontend_path = Path(__file__).parent.parent / 'frontend' / 'dist'
        
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
        
        return url
    
    def create_window(self):
        """创建webview窗口"""
        api = MainAPI()
        url = self.get_frontend_url()
        
        # 创建窗口
        window = webview.create_window(
            title=self.title,
            url=url,
            js_api=api,
            width=self.width,
            height=self.height,
            min_size=self.min_size,
            resizable=self.resizable,
            shadow=self.shadow,
            on_top=self.on_top
        )
        
        return window