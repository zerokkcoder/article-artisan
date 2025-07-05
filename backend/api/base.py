"""主API类，整合所有子模块"""
from .auth import AuthAPI
from .system import SystemAPI


class MainAPI:
    """主API类，提供各个子模块的直接访问接口"""
    auth_api = AuthAPI()
    system_api = SystemAPI()
        