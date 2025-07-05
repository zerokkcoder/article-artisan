"""架构优化演示文件"""
import asyncio
import time
from typing import Dict, Any

from .config import config
from .logger import get_logger
from .exceptions import *
from .events import (
    event_bus, emit_event, on_event, on_any_event,
    Event, EventPriority, SystemEvents, AuthEvents,
    get_event_metrics, get_event_stats
)
from .middleware import middleware_manager
from .api import MainAPI


# 演示事件监听器
@on_event(AuthEvents.LOGIN_SUCCESS)
async def on_user_login(event: Event):
    """用户登录成功时的处理"""
    logger = get_logger('demo')
    username = event.data.get('username')
    logger.info(f'欢迎用户 {username} 登录系统！')
    
    # 可以在这里添加更多逻辑，如：
    # - 记录登录日志
    # - 发送欢迎邮件
    # - 更新用户最后登录时间
    return True


@on_event(AuthEvents.LOGIN_FAILED, priority=EventPriority.HIGH)
async def on_login_failed(event: Event):
    """登录失败时的安全处理"""
    logger = get_logger('security')
    username = event.data.get('username')
    logger.warning(f'用户 {username} 登录失败，可能存在安全风险')
    
    # 可以在这里添加安全措施，如：
    # - 记录失败尝试
    # - 检查是否需要锁定账户
    # - 发送安全警报
    return True


@on_any_event(priority=EventPriority.LOW)
async def global_event_logger(event: Event):
    """全局事件记录器"""
    logger = get_logger('global_events')
    logger.debug(f'事件触发: {event.name} 来源: {event.source}')
    return True


class DemoService:
    """演示服务类"""
    
    def __init__(self):
        self.logger = get_logger('demo_service')
        self.api = MainAPI()
    
    async def demo_authentication_flow(self):
        """演示认证流程"""
        self.logger.info('开始演示认证流程')
        
        # 演示登录失败
        try:
            result = self.api.auth_api.login('admin', 'wrong_password')
            self.logger.info(f'登录结果: {result}')
        except Exception as e:
            self.logger.info(f'预期的登录失败: {e}')
        
        # 演示登录成功
        try:
            result = self.api.auth_api.login('admin', 'password')
            self.logger.info(f'登录成功: {result}')
        except Exception as e:
            self.logger.error(f'意外的登录失败: {e}')
        
        # 演示获取用户信息
        try:
            user_info = self.api.auth_api.get_current_user()
            self.logger.info(f'用户信息: {user_info}')
        except Exception as e:
            self.logger.error(f'获取用户信息失败: {e}')
        
        # 演示登出
        try:
            logout_result = self.api.auth_api.logout()
            self.logger.info(f'登出结果: {logout_result}')
        except Exception as e:
            self.logger.error(f'登出失败: {e}')
    
    async def demo_system_monitoring(self):
        """演示系统监控"""
        self.logger.info('开始演示系统监控')
        
        # 获取系统基础数据
        try:
            system_data = self.api.system_api.get_data()
            self.logger.info('系统数据获取成功')
            
            # 发射系统健康检查事件
            emit_event(
                SystemEvents.HEALTH_CHECK,
                {
                    'status': 'healthy',
                    'timestamp': time.time(),
                    'message': system_data.get('message', 'System data retrieved')
                },
                source='DemoService',
                priority=EventPriority.NORMAL
            )
            
        except Exception as e:
            self.logger.error(f'系统数据获取失败: {e}')
            
            # 发射系统错误事件
            emit_event(
                SystemEvents.ERROR,
                {
                    'error': str(e),
                    'component': 'system_monitoring',
                    'timestamp': time.time()
                },
                source='DemoService',
                priority=EventPriority.HIGH
            )
    
    async def demo_event_system(self):
        """演示事件系统"""
        self.logger.info('开始演示事件系统')
        
        # 发射自定义事件
        custom_event = Event(
            name='demo.custom_event',
            data={
                'message': '这是一个自定义事件',
                'timestamp': time.time()
            },
            source='DemoService',
            priority=EventPriority.NORMAL
        )
        
        result = await event_bus.publish(custom_event)
        self.logger.info(f'自定义事件发布结果: {result}')
        
        # 获取事件统计
        stats = get_event_stats()
        self.logger.info(f'事件系统统计: {stats}')
        
        # 获取事件指标
        metrics = get_event_metrics()
        self.logger.info(f'事件指标: {metrics}')
    
    def demo_configuration(self):
        """演示配置管理"""
        self.logger.info('开始演示配置管理')
        
        self.logger.info(f'当前环境: {config.env}')
        self.logger.info(f'是否为开发环境: {config.is_development()}')
        self.logger.info(f'是否为生产环境: {config.is_production()}')
        self.logger.info(f'API配置: {config.api.__dict__}')
        self.logger.info(f'窗口配置: {config.window.__dict__}')
        self.logger.info(f'安全配置: {config.security.__dict__}')
    
    def demo_exception_handling(self):
        """演示异常处理"""
        self.logger.info('开始演示异常处理')
        
        # 演示不同类型的异常
        exceptions_to_demo = [
            AuthenticationError('认证失败示例'),
            ValidationError('验证失败示例', details={'field': 'username'}),
            RateLimitError('速率限制示例', details={'limit': 100, 'window': 60}),
            InternalServerError('内部服务器错误示例')
        ]
        
        for exc in exceptions_to_demo:
            self.logger.info(f'异常类型: {type(exc).__name__}')
            self.logger.info(f'异常字典: {exc.to_dict()}')
    
    async def run_all_demos(self):
        """运行所有演示"""
        self.logger.info('=== 开始架构优化演示 ===')
        
        # 配置管理演示
        self.demo_configuration()
        
        # 异常处理演示
        self.demo_exception_handling()
        
        # 事件系统演示
        await self.demo_event_system()
        
        # 认证流程演示
        await self.demo_authentication_flow()
        
        # 系统监控演示
        await self.demo_system_monitoring()
        
        # 最终统计
        final_stats = get_event_stats()
        final_metrics = get_event_metrics()
        
        self.logger.info('=== 演示完成 ===')
        self.logger.info(f'最终事件统计: {final_stats}')
        self.logger.info(f'最终事件指标: {final_metrics}')


async def main():
    """主演示函数"""
    demo_service = DemoService()
    await demo_service.run_all_demos()


if __name__ == '__main__':
    # 运行演示
    asyncio.run(main())