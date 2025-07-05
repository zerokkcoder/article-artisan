"""用户认证相关API"""
import time
from typing import Dict, Any
from .base import BaseAPI, api_method
from ..exceptions import AuthenticationError, ValidationError
from ..events import emit_event, AuthEvents, EventPriority


class AuthAPI(BaseAPI):
    """用户认证API类"""
    
    def __init__(self):
        super().__init__('auth')
        self.current_user = None
        self.session_data = {}
    
    @api_method
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """用户登录"""
        # 输入验证
        login_schema = {
            'required_fields': ['username', 'password']
        }
        
        login_data = {'username': username, 'password': password}
        if not self._validate_input(login_data, login_schema):
            raise ValidationError('用户名和密码不能为空')
        
        # 模拟登录逻辑
        if username == "admin" and password == "123456":
            self.current_user = username
            self.session_data = {
                'username': username,
                'role': 'admin',
                'login_time': time.time()
            }
            
            # 发射登录成功事件
            emit_event(
                AuthEvents.LOGIN_SUCCESS,
                {
                    'username': username,
                    'role': 'admin',
                    'login_time': time.time()
                },
                source='AuthAPI',
                priority=EventPriority.NORMAL
            )
            
            self.logger.info(f'User {username} logged in successfully')
            return self._create_response(
                success=True,
                data={
                    "token": f"mock-jwt-token-{username}-{int(time.time())}",
                    "user": {
                        "id": "1",
                        "username": username,
                        "email": "admin@example.com",
                        "avatar": "https://via.placeholder.com/40"
                    },
                    "expiresIn": 3600
                },
                message="登录成功"
            )
        else:
            # 发射登录失败事件
            emit_event(
                AuthEvents.LOGIN_FAILED,
                {
                    'username': username,
                    'reason': 'invalid_credentials',
                    'attempt_time': time.time()
                },
                source='AuthAPI',
                priority=EventPriority.HIGH
            )
            
            self.logger.warning(f'Failed login attempt for user: {username}')
            raise AuthenticationError('用户名或密码错误')
    
    @api_method
    def register(self, username: str, email: str, password: str, confirmPassword: str) -> Dict[str, Any]:
        """用户注册"""
        # 输入验证
        register_schema = {
            'required_fields': ['username', 'email', 'password', 'confirmPassword']
        }
        
        register_data = {
            'username': username,
            'email': email,
            'password': password,
            'confirmPassword': confirmPassword
        }
        
        if not self._validate_input(register_data, register_schema):
            raise ValidationError('所有字段都不能为空')
        
        if password != confirmPassword:
            raise ValidationError('两次输入密码不一致')
        
        # 模拟注册成功
        new_user = {
            "id": 2,
            "username": username,
            "email": email,
            "avatar": "https://via.placeholder.com/40"
        }
        
        # 发射注册成功事件
        emit_event(
            AuthEvents.REGISTER_SUCCESS,
            {
                'username': username,
                'email': email,
                'register_time': time.time()
            },
            source='AuthAPI',
            priority=EventPriority.NORMAL
        )
        
        self.logger.info(f'New user registered: {username}')
        return self._create_response(
            success=True,
            data={
                "token": f"mock-jwt-token-{username}-{int(time.time())}",
                "user": new_user,
                "expiresIn": 3600
            },
            message="注册成功"
        )
    
    @api_method
    def logout(self) -> Dict[str, Any]:
        """用户登出"""
        if self.current_user:
            username = self.current_user
            
            # 发射登出事件
            emit_event(
                AuthEvents.LOGOUT,
                {
                    'username': username,
                    'logout_time': time.time()
                },
                source='AuthAPI',
                priority=EventPriority.NORMAL
            )
            
            self.current_user = None
            self.session_data = {}
            
            self.logger.info(f'User {username} logged out')
            return self._create_response(
                success=True,
                message="登出成功"
            )
        else:
            return self._create_response(
                success=True,
                message="用户未登录"
            )
    
    @api_method
    def get_current_user(self) -> Dict[str, Any]:
        """获取当前用户信息"""
        if self.current_user:
            return self._create_response(
                success=True,
                data=self.session_data,
                message="获取用户信息成功"
            )
        else:
            raise AuthenticationError('用户未登录')
    
    @api_method
    def check_session(self) -> Dict[str, Any]:
        """检查会话状态"""
        if self.current_user and self.session_data:
            # 检查会话是否过期（示例：24小时）
            current_time = time.time()
            login_time = self.session_data.get('login_time', 0)
            session_duration = current_time - login_time
            
            if session_duration > 24 * 3600:  # 24小时
                self.current_user = None
                self.session_data = {}
                raise AuthenticationError('会话已过期，请重新登录')
            
            return self._create_response(
                success=True,
                data={
                    'valid': True,
                    'remaining_time': 24 * 3600 - session_duration
                },
                message="会话有效"
            )
        else:
            return self._create_response(
                success=True,
                data={'valid': False},
                message="会话无效"
            )