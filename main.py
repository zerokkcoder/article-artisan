"""Article Artisan 主程序入口"""
import webview
from backend.window import WindowManager
from backend.config import config

def main():
    """主函数"""
    print("Starting Article Artisan...")
    
    # 创建窗口管理器并启动应用
    window_manager = WindowManager()
    window = window_manager.create_window()
    
    # 启动webview
    webview.start(
        debug=config.window.debug,  # 使用配置管理的调试设置
        http_server=True  # 启用内置HTTP服务器
    )

if __name__ == '__main__':
    main()