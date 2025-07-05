"""中间件系统"""
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Callable, Optional
from functools import wraps

from .logger import get_logger
from .config import config
from .exceptions import BaseAPIException, RateLimitError, AuthenticationError


class BaseMiddleware(ABC):
    """中间件基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(f'middleware.{name}')
    
    @abstractmethod
    def process_request(self, method_name: str, args: tuple, kwargs: dict) -> tuple:
        """处理请求前的逻辑"""
        pass
    
    @abstractmethod
    def process_response(self, method_name: str, response: Any) -> Any:
        """处理响应后的逻辑"""
        pass
    
    def process_exception(self, method_name: str, exception: Exception) -> Optional[Exception]:
        """处理异常的逻辑，返回None表示异常已处理"""
        return exception


class LoggingMiddleware(BaseMiddleware):
    """日志记录中间件"""
    
    def __init__(self):
        super().__init__('logging')
        self.request_times = {}
    
    def process_request(self, method_name: str, args: tuple, kwargs: dict) -> tuple:
        """记录请求开始"""
        request_id = f"{method_name}_{int(time.time() * 1000000)}"
        self.request_times[request_id] = time.time()
        
        # 记录请求参数（敏感信息脱敏）
        safe_kwargs = self._sanitize_params(kwargs)
        self.logger.info(f'Request started: {method_name} with args={args}, kwargs={safe_kwargs}')
        
        # 存储请求ID但不传递给API方法
        self._current_request_id = request_id
        return args, kwargs
    
    def process_response(self, method_name: str, response: Any) -> Any:
        """记录请求完成"""
        # 使用存储的请求ID
        request_id = getattr(self, '_current_request_id', None)
        if request_id and request_id in self.request_times:
            duration = time.time() - self.request_times[request_id]
            del self.request_times[request_id]
            self.logger.info(f'Request completed: {method_name} in {duration:.3f}s')
        else:
            self.logger.info(f'Request completed: {method_name}')
        
        return response
    
    def process_exception(self, method_name: str, exception: Exception) -> Optional[Exception]:
        """记录异常"""
        if isinstance(exception, BaseAPIException):
            self.logger.warning(f'API exception in {method_name}: {exception.message}')
        else:
            self.logger.error(f'Unexpected exception in {method_name}: {str(exception)}', exc_info=True)
        return exception
    
    def _sanitize_params(self, params: dict) -> dict:
        """脱敏敏感参数"""
        sensitive_keys = {'password', 'token', 'secret', 'key', 'auth'}
        sanitized = {}
        
        for key, value in params.items():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                sanitized[key] = '***'
            else:
                sanitized[key] = value
        
        return sanitized


class RateLimitMiddleware(BaseMiddleware):
    """速率限制中间件"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        super().__init__('rate_limit')
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_counts = {}  # {method_name: [(timestamp, count), ...]}
    
    def process_request(self, method_name: str, args: tuple, kwargs: dict) -> tuple:
        """检查速率限制"""
        current_time = time.time()
        
        # 清理过期的记录
        self._cleanup_old_records(current_time)
        
        # 检查当前方法的请求次数
        if method_name not in self.request_counts:
            self.request_counts[method_name] = []
        
        method_requests = self.request_counts[method_name]
        
        # 计算当前窗口内的请求数
        window_start = current_time - self.window_seconds
        current_window_requests = sum(
            count for timestamp, count in method_requests 
            if timestamp >= window_start
        )
        
        if current_window_requests >= self.max_requests:
            self.logger.warning(f'Rate limit exceeded for {method_name}: {current_window_requests}/{self.max_requests}')
            raise RateLimitError(
                f'Rate limit exceeded for {method_name}. Max {self.max_requests} requests per {self.window_seconds} seconds.',
                details={
                    'current_requests': current_window_requests,
                    'max_requests': self.max_requests,
                    'window_seconds': self.window_seconds,
                    'reset_time': window_start + self.window_seconds
                }
            )
        
        # 记录当前请求
        method_requests.append((current_time, 1))
        
        return args, kwargs
    
    def process_response(self, method_name: str, response: Any) -> Any:
        """处理响应"""
        return response
    
    def _cleanup_old_records(self, current_time: float):
        """清理过期的请求记录"""
        cutoff_time = current_time - self.window_seconds
        
        for method_name in list(self.request_counts.keys()):
            self.request_counts[method_name] = [
                (timestamp, count) for timestamp, count in self.request_counts[method_name]
                if timestamp >= cutoff_time
            ]
            
            # 如果列表为空，删除该方法的记录
            if not self.request_counts[method_name]:
                del self.request_counts[method_name]


class AuthenticationMiddleware(BaseMiddleware):
    """认证中间件"""
    
    def __init__(self, protected_methods: Optional[List[str]] = None):
        super().__init__('authentication')
        self.protected_methods = protected_methods or []
        # 默认保护的方法
        self.default_protected = {
            'get_current_user', 'logout', 'get_system_info', 
            'get_health_status', 'set_message'
        }
    
    def process_request(self, method_name: str, args: tuple, kwargs: dict) -> tuple:
        """检查认证状态"""
        # 检查是否需要认证
        if self._requires_authentication(method_name):
            # 这里应该检查实际的认证状态
            # 由于我们的架构中认证状态存储在AuthAPI实例中，
            # 这里简化处理，实际项目中可能需要更复杂的认证检查
            auth_token = kwargs.get('auth_token') or (args[0] if args and hasattr(args[0], 'current_user') else None)
            
            if not auth_token:
                self.logger.warning(f'Unauthorized access attempt to {method_name}')
                raise AuthenticationError('Authentication required')
        
        return args, kwargs
    
    def process_response(self, method_name: str, response: Any) -> Any:
        """处理响应"""
        return response
    
    def _requires_authentication(self, method_name: str) -> bool:
        """判断方法是否需要认证"""
        # 登录和注册方法不需要认证
        if method_name in {'login', 'register'}:
            return False
        
        # 检查是否在保护列表中
        return (method_name in self.protected_methods or 
                method_name in self.default_protected)


class MiddlewareManager:
    """中间件管理器"""
    
    def __init__(self):
        self.middlewares: List[BaseMiddleware] = []
        self.logger = get_logger('middleware_manager')
    
    def add_middleware(self, middleware: BaseMiddleware):
        """添加中间件"""
        self.middlewares.append(middleware)
        self.logger.info(f'Added middleware: {middleware.name}')
    
    def remove_middleware(self, middleware_name: str):
        """移除中间件"""
        self.middlewares = [m for m in self.middlewares if m.name != middleware_name]
        self.logger.info(f'Removed middleware: {middleware_name}')
    
    def process_request(self, method_name: str, args: tuple, kwargs: dict) -> tuple:
        """处理请求"""
        current_args, current_kwargs = args, kwargs
        
        for middleware in self.middlewares:
            try:
                current_args, current_kwargs = middleware.process_request(
                    method_name, current_args, current_kwargs
                )
            except Exception as e:
                # 如果中间件处理异常，继续传播
                raise e
        
        return current_args, current_kwargs
    
    def process_response(self, method_name: str, response: Any) -> Any:
        """处理响应（逆序执行）"""
        current_response = response
        
        for middleware in reversed(self.middlewares):
            try:
                current_response = middleware.process_response(method_name, current_response)
            except Exception as e:
                self.logger.error(f'Error in middleware {middleware.name} during response processing: {e}')
                # 响应处理中的异常不应该影响最终响应
                continue
        
        return current_response
    
    def process_exception(self, method_name: str, exception: Exception) -> Exception:
        """处理异常"""
        current_exception = exception
        
        for middleware in self.middlewares:
            try:
                processed_exception = middleware.process_exception(method_name, current_exception)
                if processed_exception is None:
                    # 中间件已处理异常
                    return None
                current_exception = processed_exception
            except Exception as e:
                self.logger.error(f'Error in middleware {middleware.name} during exception processing: {e}')
                continue
        
        return current_exception


# 创建全局中间件管理器
middleware_manager = MiddlewareManager()

# 添加默认中间件
if config.is_development():
    middleware_manager.add_middleware(LoggingMiddleware())

# 在生产环境中添加速率限制
if config.is_production():
    middleware_manager.add_middleware(RateLimitMiddleware(max_requests=1000, window_seconds=60))

# 添加认证中间件
middleware_manager.add_middleware(AuthenticationMiddleware())


def with_middleware(func):
    """中间件装饰器"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        method_name = f'{self.__class__.__name__}.{func.__name__}'
        
        try:
            # 处理请求
            processed_args, processed_kwargs = middleware_manager.process_request(
                method_name, args, kwargs
            )
            
            # 执行原方法
            response = func(self, *processed_args, **processed_kwargs)
            
            # 处理响应
            final_response = middleware_manager.process_response(method_name, response)
            
            return final_response
            
        except Exception as e:
            # 处理异常
            processed_exception = middleware_manager.process_exception(method_name, e)
            if processed_exception is not None:
                raise processed_exception
            # 如果异常被处理，返回默认响应
            return {'success': False, 'message': 'Request processed with middleware intervention'}
    
    return wrapper