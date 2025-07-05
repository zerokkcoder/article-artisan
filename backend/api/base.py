"""API基类和主API类"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from functools import wraps

from ..config import config
from ..logger import get_logger
from ..exceptions import BaseAPIException, InternalServerError
from ..middleware import with_middleware
from ..events import emit_event, APIEvents, EventPriority


class BaseAPI(ABC):
    """API基类，提供通用功能"""
    
    def __init__(self, name: str = 'base'):
        self.name = name
        self.logger = get_logger(f'api.{name}')
        self.config = config
        self._setup()
    
    def _setup(self):
        """子类可重写的初始化方法"""
        self.logger.info(f'{self.name} API initialized')
    
    def _validate_input(self, data: Any, schema: Optional[Dict] = None) -> bool:
        """统一的输入验证"""
        if schema is None:
            return True
        
        # 这里可以集成更复杂的验证逻辑
        # 例如使用 pydantic 或 cerberus
        try:
            if isinstance(data, dict) and 'required_fields' in schema:
                for field in schema['required_fields']:
                    if field not in data:
                        raise ValueError(f'Missing required field: {field}')
            return True
        except Exception as e:
            self.logger.error(f'Input validation failed: {e}')
            return False
    
    def _handle_error(self, error: Exception, context: str = '') -> Dict[str, Any]:
        """统一的错误处理"""
        if isinstance(error, BaseAPIException):
            self.logger.warning(f'{context}: {error.message}')
            return error.to_dict()
        else:
            self.logger.error(f'{context}: {str(error)}', exc_info=True)
            internal_error = InternalServerError(
                message='An unexpected error occurred',
                details={'context': context, 'original_error': str(error)}
            )
            return internal_error.to_dict()
    
    def _create_response(self, success: bool, data: Any = None, message: str = '', error: str = '') -> Dict[str, Any]:
        """创建标准响应格式"""
        response = {
            'success': success,
            'data': data,
            'message': message
        }
        if error:
            response['error'] = error
        return response


def api_method(func):
    """API方法装饰器，提供统一的错误处理、日志记录、中间件和事件系统"""
    @wraps(func)
    @with_middleware
    def wrapper(self, *args, **kwargs):
        method_name = f'{self.__class__.__name__}.{func.__name__}'
        
        # 发射API请求开始事件
        emit_event(
            APIEvents.REQUEST_START,
            {
                'method': method_name,
                'args_count': len(args),
                'kwargs_keys': list(kwargs.keys())
            },
            source=self.__class__.__name__,
            priority=EventPriority.LOW
        )
        
        try:
            result = func(self, *args, **kwargs)
            
            # 发射API请求成功事件
            emit_event(
                APIEvents.REQUEST_END,
                {
                    'method': method_name,
                    'success': True
                },
                source=self.__class__.__name__,
                priority=EventPriority.LOW
            )
            
            return result
            
        except Exception as e:
            # 发射API请求错误事件
            emit_event(
                APIEvents.REQUEST_ERROR,
                {
                    'method': method_name,
                    'error': str(e),
                    'error_type': type(e).__name__
                },
                source=self.__class__.__name__,
                priority=EventPriority.HIGH
            )
            
            return self._handle_error(e, method_name)
    
    return wrapper


class MainAPI(BaseAPI):
    """主API类，提供各个子模块的直接访问接口"""
    
    def __init__(self):
        super().__init__('main')
        # 延迟导入避免循环依赖
        from .auth import AuthAPI
        from .system import SystemAPI
        
        # 初始化各个子模块，前端可直接调用
        self.auth_api = AuthAPI()
        self.system_api = SystemAPI()
    
    def get_api_info(self) -> Dict[str, Any]:
        """获取API信息"""
        return self._create_response(
            success=True,
            data={
                'name': 'Article Artisan API',
                'version': '1.0.0',
                'environment': self.config.env,
                'modules': ['auth_api', 'system_api']
            },
            message='API information retrieved successfully'
        )
        