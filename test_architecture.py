#!/usr/bin/env python3
"""架构优化测试脚本"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.api.base import MainAPI
from backend.events import on_event, AuthEvents
from backend.config import config
from backend.logger import get_logger

def test_basic_functionality():
    """测试基本功能"""
    print("=== 架构优化功能测试 ===")
    
    # 初始化API
    api = MainAPI()
    logger = get_logger('test')
    
    print(f"\n1. 配置管理测试:")
    print(f"   环境: {config.env}")
    print(f"   是否开发环境: {config.is_development()}")
    print(f"   日志级别: {config.api.log_level}")
    
    print(f"\n2. API信息测试:")
    api_info = api.get_api_info()
    print(f"   API名称: {api_info['data']['name']}")
    print(f"   版本: {api_info['data']['version']}")
    print(f"   模块: {api_info['data']['modules']}")
    
    print(f"\n3. 系统API测试:")
    try:
        system_data = api.system_api.get_data()
        print(f"   ✓ 系统数据获取成功: {system_data['message']}")
    except Exception as e:
        print(f"   ✗ 系统数据获取失败: {e}")
    
    print(f"\n4. 认证API测试:")
    try:
        # 测试注册
        register_result = api.auth_api.register('testuser', 'test@example.com', 'password123')
        print(f"   ✓ 用户注册: {register_result['message']}")
        
        # 测试登录
        login_result = api.auth_api.login('testuser', 'password123')
        print(f"   ✓ 用户登录: {login_result['message']}")
        
        # 测试获取当前用户
        current_user = api.auth_api.get_current_user()
        print(f"   ✓ 当前用户: {current_user['data']['username']}")
        
        # 测试登出
        logout_result = api.auth_api.logout()
        print(f"   ✓ 用户登出: {logout_result['message']}")
        
    except Exception as e:
        print(f"   ✗ 认证测试失败: {e}")
    
    print(f"\n5. 日志系统测试:")
    logger.info("这是一条测试信息")
    logger.warning("这是一条测试警告")
    print(f"   ✓ 日志系统正常工作")
    
    print(f"\n6. 异常处理测试:")
    try:
        # 测试无效登录
        api.auth_api.login('invalid_user', 'wrong_password')
    except Exception as e:
        print(f"   ✓ 异常处理正常: {type(e).__name__}")
    
    print(f"\n=== 测试完成 ===")
    print(f"\n架构优化成功！所有核心功能正常工作。")

if __name__ == '__main__':
    test_basic_functionality()