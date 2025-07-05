#!/usr/bin/env python3
"""
开发模式启动脚本
自动启动前端开发服务器和Python后端
"""

import subprocess
import sys
import time
import threading
import os
from pathlib import Path
import psutil
import requests

def check_node_installed():
    """检查Node.js是否已安装"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js 已安装: {result.stdout.strip()}")
            return True
        else:
            print("❌ Node.js 未安装")
            return False
    except FileNotFoundError:
        print("❌ Node.js 未安装")
        return False

def check_npm_installed():
    """检查npm是否已安装"""
    npm_commands = ['npm', 'npm.cmd'] if sys.platform == 'win32' else ['npm']
    
    for npm_cmd in npm_commands:
        try:
            result = subprocess.run([npm_cmd, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ npm 已安装: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            continue
    
    print("❌ npm 未安装")
    return False

def install_frontend_deps():
    """安装前端依赖"""
    frontend_dir = Path(__file__).parent / 'frontend'
    npm_cmd = 'npm.cmd' if sys.platform == 'win32' else 'npm'
    
    if not (frontend_dir / 'node_modules').exists():
        print("📦 安装前端依赖...")
        try:
            subprocess.run([npm_cmd, 'install'], cwd=frontend_dir, check=True, shell=True if sys.platform == 'win32' else False)
            print("✅ 前端依赖安装完成")
        except subprocess.CalledProcessError as e:
            print(f"❌ 前端依赖安装失败: {e}")
            return False
    else:
        print("✅ 前端依赖已存在")
    return True

def start_frontend_dev_server():
    """启动前端开发服务器"""
    frontend_dir = Path(__file__).parent / 'frontend'
    print("🚀 启动前端开发服务器...")
    
    # 确定npm命令
    npm_cmd = 'npm.cmd' if sys.platform == 'win32' else 'npm'
    
    try:
        # 在Windows上使用shell=True
        process = subprocess.Popen(
            [npm_cmd, 'run', 'dev'],
            cwd=frontend_dir,
            shell=True if sys.platform == 'win32' else False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # 等待服务器启动
        print("⏳ 等待前端服务器启动...")
        for i in range(30):  # 最多等待30秒
            try:
                response = requests.get('http://localhost:5173', timeout=1)
                if response.status_code == 200:
                    print("✅ 前端开发服务器已启动: http://localhost:5173")
                    return process
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
        
        print("⚠️ 前端服务器启动超时，但进程已启动")
        return process
        
    except Exception as e:
        print(f"❌ 启动前端开发服务器失败: {e}")
        return None

def start_python_app():
    """启动Python应用"""
    print("🐍 启动Python应用...")
    try:
        # 导入并运行主应用
        from main import main
        main()
    except Exception as e:
        print(f"❌ Python应用启动失败: {e}")
        sys.exit(1)

def cleanup_processes():
    """清理进程"""
    print("\n🧹 清理进程...")
    # 查找并终止Node.js进程
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'node' in proc.info['name'].lower():
                cmdline = proc.info['cmdline']
                if cmdline and any('vite' in arg or '5173' in arg for arg in cmdline):
                    print(f"终止进程: {proc.info['pid']} - {' '.join(cmdline)}")
                    proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def main():
    """主函数"""
    print("🎨 Article Artisan - 开发模式")
    print("=" * 50)
    
    # 检查环境
    if not check_node_installed() or not check_npm_installed():
        print("\n请先安装 Node.js 和 npm")
        print("下载地址: https://nodejs.org/")
        sys.exit(1)
    
    # 安装前端依赖
    if not install_frontend_deps():
        sys.exit(1)
    
    frontend_process = None
    
    try:
        # 启动前端开发服务器
        frontend_process = start_frontend_dev_server()
        if not frontend_process:
            sys.exit(1)
        
        # 等待一下确保前端服务器完全启动
        time.sleep(2)
        
        # 启动Python应用
        start_python_app()
        
    except KeyboardInterrupt:
        print("\n👋 用户中断")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
    finally:
        # 清理进程
        if frontend_process:
            try:
                frontend_process.terminate()
                frontend_process.wait(timeout=5)
            except:
                pass
        cleanup_processes()
        print("✅ 清理完成")

if __name__ == '__main__':
    main()