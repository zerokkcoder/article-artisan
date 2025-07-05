#!/usr/bin/env python3
"""
打包脚本
构建前端并创建可执行文件
"""

import subprocess
import sys
import shutil
import os
from pathlib import Path

def check_dependencies():
    """检查必要的依赖"""
    print("🔍 检查依赖...")
    
    # 检查Node.js和npm
    try:
        subprocess.run(['node', '--version'], capture_output=True, check=True)
        npm_cmd = 'npm.cmd' if sys.platform == 'win32' else 'npm'
        subprocess.run([npm_cmd, '--version'], capture_output=True, check=True)
        print("✅ Node.js 和 npm 已安装")
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ 请先安装 Node.js 和 npm")
        return False
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller 已安装: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller 未安装")
        print("请运行: pip install pyinstaller")
        return False
    
    return True

def install_frontend_deps():
    """安装前端依赖"""
    frontend_dir = Path(__file__).parent / 'frontend'
    npm_cmd = 'npm.cmd' if sys.platform == 'win32' else 'npm'
    
    print("📦 安装前端依赖...")
    try:
        subprocess.run([npm_cmd, 'install'], cwd=frontend_dir, check=True, shell=True if sys.platform == 'win32' else False)
        print("✅ 前端依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 前端依赖安装失败: {e}")
        return False

def build_frontend():
    """构建前端"""
    frontend_dir = Path(__file__).parent / 'frontend'
    dist_dir = frontend_dir / 'dist'
    npm_cmd = 'npm.cmd' if sys.platform == 'win32' else 'npm'
    
    # 清理之前的构建
    if dist_dir.exists():
        print("🧹 清理之前的构建...")
        shutil.rmtree(dist_dir)
    
    print("🏗️ 构建前端...")
    try:
        subprocess.run([npm_cmd, 'run', 'build'], cwd=frontend_dir, check=True, shell=True if sys.platform == 'win32' else False)
        print("✅ 前端构建完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 前端构建失败: {e}")
        return False

def create_spec_file():
    """创建PyInstaller spec文件"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend/dist', 'frontend/dist'),
    ],
    hiddenimports=[
        'webview',
        'webview.platforms.winforms',
        'webview.platforms.cef',
        'webview.platforms.edgechromium',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ArticleArtisan',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 设置为False创建窗口应用
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径
)
'''
    
    spec_file = Path(__file__).parent / 'ArticleArtisan.spec'
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"✅ 创建spec文件: {spec_file}")
    return spec_file

def build_executable(spec_file):
    """使用PyInstaller构建可执行文件"""
    print("📦 构建可执行文件...")
    
    try:
        subprocess.run([
            'pyinstaller',
            '--clean',
            '--noconfirm',
            str(spec_file)
        ], check=True)
        
        print("✅ 可执行文件构建完成")
        
        # 检查输出文件
        dist_dir = Path(__file__).parent / 'dist'
        exe_file = dist_dir / 'ArticleArtisan.exe'
        
        if exe_file.exists():
            print(f"🎉 可执行文件位置: {exe_file}")
            print(f"📁 文件大小: {exe_file.stat().st_size / 1024 / 1024:.1f} MB")
            return True
        else:
            print("❌ 未找到生成的可执行文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建可执行文件失败: {e}")
        return False

def cleanup_build_files():
    """清理构建文件"""
    print("🧹 清理构建文件...")
    
    build_dir = Path(__file__).parent / 'build'
    spec_file = Path(__file__).parent / 'ArticleArtisan.spec'
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
        print("✅ 清理build目录")
    
    if spec_file.exists():
        spec_file.unlink()
        print("✅ 清理spec文件")

def main():
    """主函数"""
    print("🎨 Article Artisan - 打包脚本")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # 安装前端依赖
        if not install_frontend_deps():
            sys.exit(1)
        
        # 构建前端
        if not build_frontend():
            sys.exit(1)
        
        # 创建spec文件
        spec_file = create_spec_file()
        
        # 构建可执行文件
        if not build_executable(spec_file):
            sys.exit(1)
        
        print("\n🎉 打包完成!")
        print("可执行文件位于 dist/ArticleArtisan.exe")
        
    except KeyboardInterrupt:
        print("\n👋 用户中断")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)
    finally:
        # 清理构建文件
        cleanup_build_files()

if __name__ == '__main__':
    main()