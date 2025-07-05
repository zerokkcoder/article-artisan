"""Article Artisan 主程序入口"""
import webview
from backend.window import WindowConfig

def main():
    """主函数"""
    print("Starting Article Artisan...")
    
    # 创建窗口配置并启动应用
    window_config = WindowConfig()
    window = window_config.create_window()
    
    # 启动webview
    webview.start(
        debug=True,  # 开发模式下启用调试
        http_server=True  # 启用内置HTTP服务器
    )

if __name__ == '__main__':
    main()