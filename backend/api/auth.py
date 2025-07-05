"""用户认证相关API"""
import time


class AuthAPI:
    """用户认证API类"""
    
    def __init__(self):
        self.current_user = None
    
    def login(self, username, password):
        """登录接口"""
        # 模拟登录验证
        if username == "admin" and password == "123456":
            self.current_user = {
                "id": 1,
                "username": username,
                "email": "admin@example.com",
                "avatar": "https://via.placeholder.com/40"
            }
            return {
                "success": True,
                "message": "登录成功",
                "data": {
                    "token": f"mock-jwt-token-admin-{int(time.time())}",
                    "user": self.current_user,
                    "expiresIn": 3600
                }
            }
        else:
            return {
                "success": False,
                "message": "用户名或密码错误",
                "data": None
            }
    
    def register(self, username, email, password, confirmPassword):
        """注册接口"""
        if password != confirmPassword:
            return {
                "success": False,
                "message": "两次输入密码不一致",
                "data": None
            }
        
        # 模拟注册成功
        new_user = {
            "id": 2,
            "username": username,
            "email": email,
            "avatar": "https://via.placeholder.com/40"
        }
        
        return {
            "success": True,
            "message": "注册成功",
            "data": {
                "token": f"mock-jwt-token-{username}-{int(time.time())}",
                "user": new_user,
                "expiresIn": 3600
            }
        }
    
    def logout(self):
        """登出接口"""
        self.current_user = None
        return {
            "success": True,
            "message": "已退出登录",
            "data": None
        }
    
    def get_current_user(self):
        """获取当前用户信息"""
        if self.current_user:
            return {
                "success": True,
                "data": self.current_user
            }
        else:
            return {
                "success": False,
                "message": "未登录",
                "data": None
            }