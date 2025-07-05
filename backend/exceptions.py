"""自定义异常类模块"""
from typing import Optional, Dict, Any


class BaseAPIException(Exception):
    """API异常基类"""
    
    def __init__(
        self, 
        message: str, 
        code: str = 'UNKNOWN_ERROR',
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'success': False,
            'error': self.message,
            'code': self.code,
            'status_code': self.status_code,
            'details': self.details
        }


class AuthenticationError(BaseAPIException):
    """认证错误"""
    
    def __init__(self, message: str = '认证失败', details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code='AUTHENTICATION_ERROR',
            status_code=401,
            details=details
        )


class AuthorizationError(BaseAPIException):
    """授权错误"""
    
    def __init__(self, message: str = '权限不足', details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code='AUTHORIZATION_ERROR',
            status_code=403,
            details=details
        )


class ValidationError(BaseAPIException):
    """数据验证错误"""
    
    def __init__(self, message: str = '数据验证失败', details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code='VALIDATION_ERROR',
            status_code=400,
            details=details
        )


class NotFoundError(BaseAPIException):
    """资源未找到错误"""
    
    def __init__(self, message: str = '资源未找到', details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code='NOT_FOUND_ERROR',
            status_code=404,
            details=details
        )


class ConflictError(BaseAPIException):
    """资源冲突错误"""
    
    def __init__(self, message: str = '资源冲突', details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code='CONFLICT_ERROR',
            status_code=409,
            details=details
        )


class RateLimitError(BaseAPIException):
    """频率限制错误"""
    
    def __init__(self, message: str = '请求过于频繁', details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code='RATE_LIMIT_ERROR',
            status_code=429,
            details=details
        )


class InternalServerError(BaseAPIException):
    """内部服务器错误"""
    
    def __init__(self, message: str = '内部服务器错误', details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code='INTERNAL_SERVER_ERROR',
            status_code=500,
            details=details
        )


class ExternalServiceError(BaseAPIException):
    """外部服务错误"""
    
    def __init__(self, message: str = '外部服务不可用', details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code='EXTERNAL_SERVICE_ERROR',
            status_code=502,
            details=details
        )


class TimeoutError(BaseAPIException):
    """超时错误"""
    
    def __init__(self, message: str = '请求超时', details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code='TIMEOUT_ERROR',
            status_code=408,
            details=details
        )