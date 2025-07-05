"""日志管理模块"""
import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from .config import config


class Logger:
    """日志管理器"""
    
    _instances = {}
    
    def __new__(cls, name: str = 'app'):
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
            cls._instances[name]._initialized = False
        return cls._instances[name]
    
    def __init__(self, name: str = 'app'):
        if self._initialized:
            return
        
        self.name = name
        self.logger = logging.getLogger(name)
        self._setup_logger()
        self._initialized = True
    
    def _setup_logger(self):
        """设置日志配置"""
        # 清除现有的处理器
        self.logger.handlers.clear()
        
        # 设置日志级别
        level = getattr(logging, config.api.log_level.upper(), logging.INFO)
        self.logger.setLevel(level)
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 文件处理器（仅在生产环境）
        if config.is_production():
            self._add_file_handler(formatter)
        
        # 防止日志重复
        self.logger.propagate = False
    
    def _add_file_handler(self, formatter):
        """添加文件处理器"""
        try:
            # 创建日志目录
            log_dir = Path('logs')
            log_dir.mkdir(exist_ok=True)
            
            # 创建日志文件
            log_file = log_dir / f'{self.name}_{datetime.now().strftime("%Y%m%d")}.log'
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            self.logger.warning(f'无法创建文件日志处理器: {e}')
    
    def debug(self, message: str, *args, **kwargs):
        """调试日志"""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """信息日志"""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """警告日志"""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """错误日志"""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """严重错误日志"""
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs):
        """异常日志（包含堆栈跟踪）"""
        self.logger.exception(message, *args, **kwargs)


# 创建默认日志实例
app_logger = Logger('app')
api_logger = Logger('api')
auth_logger = Logger('auth')
system_logger = Logger('system')


def get_logger(name: str = 'app') -> Logger:
    """获取日志实例"""
    return Logger(name)