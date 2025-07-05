"""应用配置管理模块"""
from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class APIConfig:
    """API相关配置"""
    debug: bool = False
    log_level: str = 'INFO'
    cache_enabled: bool = True
    cache_ttl: int = 300
    max_retries: int = 3
    timeout: int = 30


@dataclass
class WindowConfig:
    """窗口相关配置"""
    title: str = 'Article Artisan'
    width: int = 1200
    height: int = 800
    resizable: bool = False
    debug: bool = False
    min_width: int = 800
    min_height: int = 600
    dev_server_url: str = 'http://localhost:5173'
    dev_server_port: int = 5173


@dataclass
class SecurityConfig:
    """安全相关配置"""
    enable_csrf: bool = True
    session_timeout: int = 3600
    max_login_attempts: int = 5
    password_min_length: int = 6


class Config:
    """应用配置管理器"""
    
    def __init__(self, env: Optional[str] = None):
        self.env = env or os.getenv('APP_ENV', 'development')
        self.api = self._load_api_config()
        self.window = self._load_window_config()
        self.security = self._load_security_config()
    
    def _load_api_config(self) -> APIConfig:
        """加载API配置"""
        if self.env == 'production':
            return APIConfig(
                debug=False,
                log_level='ERROR',
                cache_enabled=True,
                cache_ttl=600,
                max_retries=5,
                timeout=60
            )
        elif self.env == 'testing':
            return APIConfig(
                debug=True,
                log_level='WARNING',
                cache_enabled=False,
                cache_ttl=60,
                max_retries=1,
                timeout=10
            )
        else:  # development
            return APIConfig(
                debug=True,
                log_level='DEBUG',
                cache_enabled=False,
                cache_ttl=60,
                max_retries=3,
                timeout=30
            )
    
    def _load_window_config(self) -> WindowConfig:
        """加载窗口配置"""
        if self.env == 'production':
            return WindowConfig(
                debug=False,
                resizable=False
            )
        else:
            return WindowConfig(
                debug=True,
                resizable=True
            )
    
    def _load_security_config(self) -> SecurityConfig:
        """加载安全配置"""
        if self.env == 'production':
            return SecurityConfig(
                enable_csrf=True,
                session_timeout=1800,  # 30分钟
                max_login_attempts=3,
                password_min_length=8
            )
        else:
            return SecurityConfig(
                enable_csrf=False,
                session_timeout=3600,  # 1小时
                max_login_attempts=10,
                password_min_length=6
            )
    
    def is_development(self) -> bool:
        """是否为开发环境"""
        return self.env == 'development'
    
    def is_production(self) -> bool:
        """是否为生产环境"""
        return self.env == 'production'
    
    def is_testing(self) -> bool:
        """是否为测试环境"""
        return self.env == 'testing'


# 全局配置实例
config = Config()