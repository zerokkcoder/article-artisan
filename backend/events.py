"""事件系统"""
import asyncio
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Callable, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
from functools import wraps

from .logger import get_logger
from .config import config


class EventPriority(Enum):
    """事件优先级"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Event:
    """事件数据类"""
    name: str
    data: Dict[str, Any] = field(default_factory=dict)
    source: str = ''
    timestamp: float = field(default_factory=time.time)
    priority: EventPriority = EventPriority.NORMAL
    event_id: str = field(default_factory=lambda: f"event_{int(time.time() * 1000000)}")
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'event_id': self.event_id,
            'name': self.name,
            'data': self.data,
            'source': self.source,
            'timestamp': self.timestamp,
            'priority': self.priority.name,
            'metadata': self.metadata
        }


class EventListener(ABC):
    """事件监听器基类"""
    
    def __init__(self, name: str, priority: EventPriority = EventPriority.NORMAL):
        self.name = name
        self.priority = priority
        self.logger = get_logger(f'event_listener.{name}')
    
    @abstractmethod
    async def handle(self, event: Event) -> bool:
        """处理事件，返回True表示成功处理"""
        pass
    
    def can_handle(self, event: Event) -> bool:
        """判断是否可以处理该事件"""
        return True


class FunctionEventListener(EventListener):
    """函数式事件监听器"""
    
    def __init__(self, name: str, handler_func: Callable[[Event], Union[bool, Any]], 
                 priority: EventPriority = EventPriority.NORMAL):
        super().__init__(name, priority)
        self.handler_func = handler_func
    
    async def handle(self, event: Event) -> bool:
        """处理事件"""
        try:
            if asyncio.iscoroutinefunction(self.handler_func):
                result = await self.handler_func(event)
            else:
                result = self.handler_func(event)
            return result if isinstance(result, bool) else True
        except Exception as e:
            self.logger.error(f'Error handling event {event.name}: {e}')
            return False


class EventBus:
    """事件总线"""
    
    def __init__(self):
        self.listeners: Dict[str, List[EventListener]] = defaultdict(list)
        self.global_listeners: List[EventListener] = []
        self.event_history: List[Event] = []
        self.max_history = 1000
        self.logger = get_logger('event_bus')
        self._stats = {
            'events_published': 0,
            'events_processed': 0,
            'events_failed': 0
        }
    
    def subscribe(self, event_name: str, listener: EventListener):
        """订阅事件"""
        self.listeners[event_name].append(listener)
        # 按优先级排序
        self.listeners[event_name].sort(key=lambda l: l.priority.value, reverse=True)
        self.logger.info(f'Listener {listener.name} subscribed to event {event_name}')
    
    def subscribe_global(self, listener: EventListener):
        """订阅所有事件"""
        self.global_listeners.append(listener)
        self.global_listeners.sort(key=lambda l: l.priority.value, reverse=True)
        self.logger.info(f'Global listener {listener.name} subscribed')
    
    def unsubscribe(self, event_name: str, listener_name: str):
        """取消订阅"""
        if event_name in self.listeners:
            self.listeners[event_name] = [
                l for l in self.listeners[event_name] if l.name != listener_name
            ]
            self.logger.info(f'Listener {listener_name} unsubscribed from event {event_name}')
    
    def unsubscribe_global(self, listener_name: str):
        """取消全局订阅"""
        self.global_listeners = [
            l for l in self.global_listeners if l.name != listener_name
        ]
        self.logger.info(f'Global listener {listener_name} unsubscribed')
    
    async def publish(self, event: Event) -> Dict[str, Any]:
        """发布事件"""
        self._stats['events_published'] += 1
        
        # 添加到历史记录
        self._add_to_history(event)
        
        self.logger.debug(f'Publishing event: {event.name} from {event.source}')
        
        # 获取所有相关监听器
        event_listeners = self.listeners.get(event.name, [])
        all_listeners = event_listeners + self.global_listeners
        
        # 过滤可以处理该事件的监听器
        applicable_listeners = [l for l in all_listeners if l.can_handle(event)]
        
        results = {
            'event_id': event.event_id,
            'processed_by': [],
            'failed_by': [],
            'total_listeners': len(applicable_listeners)
        }
        
        # 按优先级处理
        for listener in applicable_listeners:
            try:
                success = await listener.handle(event)
                if success:
                    results['processed_by'].append(listener.name)
                    self._stats['events_processed'] += 1
                else:
                    results['failed_by'].append(listener.name)
                    self._stats['events_failed'] += 1
            except Exception as e:
                self.logger.error(f'Error in listener {listener.name} for event {event.name}: {e}')
                results['failed_by'].append(listener.name)
                self._stats['events_failed'] += 1
        
        self.logger.debug(f'Event {event.name} processed by {len(results["processed_by"])} listeners')
        return results
    
    def publish_sync(self, event: Event) -> List[Any]:
        """同步发布事件"""
        try:
            # 检查是否已有运行的事件循环
            loop = asyncio.get_running_loop()
            # 如果有运行的循环，创建任务但不等待（避免阻塞）
            task = loop.create_task(self.publish(event))
            # 返回空列表，因为我们无法在同步上下文中等待异步结果
            return []
        except RuntimeError:
            # 没有运行的事件循环，可以安全使用 asyncio.run
            return asyncio.run(self.publish(event))
    
    def _add_to_history(self, event: Event):
        """添加事件到历史记录"""
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self._stats,
            'active_listeners': sum(len(listeners) for listeners in self.listeners.values()),
            'global_listeners': len(self.global_listeners),
            'event_types': list(self.listeners.keys()),
            'history_size': len(self.event_history)
        }
    
    def get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近的事件"""
        return [event.to_dict() for event in self.event_history[-limit:]]
    
    def clear_history(self):
        """清空事件历史"""
        self.event_history.clear()
        self.logger.info('Event history cleared')


# 预定义的事件类型
class SystemEvents:
    """系统事件常量"""
    STARTUP = 'system.startup'
    SHUTDOWN = 'system.shutdown'
    ERROR = 'system.error'
    WARNING = 'system.warning'
    HEALTH_CHECK = 'system.health_check'


class AuthEvents:
    """认证事件常量"""
    LOGIN_SUCCESS = 'auth.login.success'
    LOGIN_FAILED = 'auth.login.failed'
    LOGOUT = 'auth.logout'
    REGISTER_SUCCESS = 'auth.register.success'
    REGISTER_FAILED = 'auth.register.failed'
    SESSION_EXPIRED = 'auth.session.expired'


class APIEvents:
    """API事件常量"""
    REQUEST_START = 'api.request.start'
    REQUEST_END = 'api.request.end'
    REQUEST_ERROR = 'api.request.error'
    RATE_LIMIT_EXCEEDED = 'api.rate_limit.exceeded'


# 内置事件监听器
class LoggingEventListener(EventListener):
    """日志事件监听器"""
    
    def __init__(self):
        super().__init__('logging_listener', EventPriority.LOW)
    
    async def handle(self, event: Event) -> bool:
        """记录事件到日志"""
        if event.priority == EventPriority.CRITICAL:
            self.logger.critical(f'Critical event: {event.name} - {event.data}')
        elif event.priority == EventPriority.HIGH:
            self.logger.error(f'High priority event: {event.name} - {event.data}')
        elif event.priority == EventPriority.NORMAL:
            self.logger.info(f'Event: {event.name} - {event.data}')
        else:
            self.logger.debug(f'Low priority event: {event.name} - {event.data}')
        
        return True


class MetricsEventListener(EventListener):
    """指标收集事件监听器"""
    
    def __init__(self):
        super().__init__('metrics_listener', EventPriority.LOW)
        self.metrics = defaultdict(int)
    
    async def handle(self, event: Event) -> bool:
        """收集事件指标"""
        self.metrics[f'event.{event.name}'] += 1
        self.metrics[f'event.priority.{event.priority.name.lower()}'] += 1
        
        if event.source:
            self.metrics[f'event.source.{event.source}'] += 1
        
        return True
    
    def get_metrics(self) -> Dict[str, int]:
        """获取指标"""
        return dict(self.metrics)
    
    def reset_metrics(self):
        """重置指标"""
        self.metrics.clear()


# 创建全局事件总线
event_bus = EventBus()

# 添加默认监听器
if config.is_development():
    event_bus.subscribe_global(LoggingEventListener())

metrics_listener = MetricsEventListener()
event_bus.subscribe_global(metrics_listener)


# 装饰器和辅助函数
def emit_event(event_name: str, data: Optional[Dict[str, Any]] = None, 
               source: str = '', priority: EventPriority = EventPriority.NORMAL):
    """发射事件的辅助函数"""
    event = Event(
        name=event_name,
        data=data or {},
        source=source,
        priority=priority
    )
    return event_bus.publish_sync(event)


def on_event(event_name: str, priority: EventPriority = EventPriority.NORMAL):
    """事件监听装饰器"""
    def decorator(func):
        listener = FunctionEventListener(
            name=f'{func.__module__}.{func.__name__}',
            handler_func=func,
            priority=priority
        )
        event_bus.subscribe(event_name, listener)
        return func
    return decorator


def on_any_event(priority: EventPriority = EventPriority.NORMAL):
    """全局事件监听装饰器"""
    def decorator(func):
        listener = FunctionEventListener(
            name=f'{func.__module__}.{func.__name__}',
            handler_func=func,
            priority=priority
        )
        event_bus.subscribe_global(listener)
        return func
    return decorator


def event_emitter(event_name: str, source: str = '', 
                  priority: EventPriority = EventPriority.NORMAL,
                  include_result: bool = False):
    """方法事件发射装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 发射开始事件
            start_event_data = {
                'method': func.__name__,
                'args': str(args)[:200],  # 限制长度
                'kwargs': {k: str(v)[:100] for k, v in kwargs.items()}
            }
            
            emit_event(
                f'{event_name}.start',
                start_event_data,
                source or func.__module__,
                priority
            )
            
            try:
                result = func(*args, **kwargs)
                
                # 发射成功事件
                end_event_data = {
                    'method': func.__name__,
                    'success': True
                }
                
                if include_result:
                    end_event_data['result'] = str(result)[:200]
                
                emit_event(
                    f'{event_name}.success',
                    end_event_data,
                    source or func.__module__,
                    priority
                )
                
                return result
                
            except Exception as e:
                # 发射错误事件
                error_event_data = {
                    'method': func.__name__,
                    'success': False,
                    'error': str(e),
                    'error_type': type(e).__name__
                }
                
                emit_event(
                    f'{event_name}.error',
                    error_event_data,
                    source or func.__module__,
                    EventPriority.HIGH
                )
                
                raise
        
        return wrapper
    return decorator


# 获取指标的辅助函数
def get_event_metrics() -> Dict[str, int]:
    """获取事件指标"""
    return metrics_listener.get_metrics()


def get_event_stats() -> Dict[str, Any]:
    """获取事件统计"""
    return event_bus.get_stats()