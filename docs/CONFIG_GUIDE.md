# 配置管理指南

## 概述

Article Artisan 使用集中化的配置管理系统，支持环境感知配置和类型安全。配置系统位于 `backend/config.py` 文件中。

## 配置结构

### 1. 环境配置

通过环境变量 `APP_ENV` 设置运行环境：

```bash
# 开发环境（默认）
APP_ENV=development

# 生产环境
APP_ENV=production

# 测试环境
APP_ENV=testing
```

### 2. 配置类别

#### APIConfig - API相关配置
```python
@dataclass
class APIConfig:
    debug: bool = False
    log_level: str = 'INFO'
    cache_enabled: bool = True
    cache_ttl: int = 300
    max_retries: int = 3
    timeout: int = 30
```

#### WindowConfig - 窗口相关配置
```python
@dataclass
class WindowConfig:
    title: str = 'Article Artisan'
    width: int = 1200
    height: int = 800
    resizable: bool = False
    debug: bool = False
    min_width: int = 800
    min_height: int = 600
    dev_server_url: str = 'http://localhost:5173'
    dev_server_port: int = 5173
```

#### SecurityConfig - 安全相关配置
```python
@dataclass
class SecurityConfig:
    enable_csrf: bool = True
    session_timeout: int = 3600
    max_login_attempts: int = 5
    password_min_length: int = 6
```

## 使用方法

### 1. 导入配置

```python
from backend.config import config
```

### 2. 访问配置

```python
# 访问API配置
if config.api.debug:
    print("调试模式已启用")

# 访问窗口配置
window_title = config.window.title
window_width = config.window.width

# 访问安全配置
max_attempts = config.security.max_login_attempts

# 检查环境
if config.is_development():
    print("当前为开发环境")
elif config.is_production():
    print("当前为生产环境")
```

### 3. 环境特定配置

不同环境下的配置会自动调整：

#### 开发环境 (development)
- API调试模式：启用
- 日志级别：DEBUG
- 缓存：禁用
- 窗口调试：启用
- 窗口可调整大小：是
- CSRF保护：禁用
- 会话超时：1小时

#### 生产环境 (production)
- API调试模式：禁用
- 日志级别：ERROR
- 缓存：启用（10分钟TTL）
- 窗口调试：禁用
- 窗口可调整大小：否
- CSRF保护：启用
- 会话超时：30分钟

#### 测试环境 (testing)
- API调试模式：启用
- 日志级别：WARNING
- 缓存：禁用
- 重试次数：1
- 超时时间：10秒

## 配置集成示例

### 1. 在API类中使用

```python
from backend.config import config
from backend.logger import get_logger

class MyAPI:
    def __init__(self):
        self.config = config
        self.logger = get_logger('my_api')
        
    def some_method(self):
        if self.config.api.debug:
            self.logger.debug("调试信息")
        
        # 使用配置的超时时间
        timeout = self.config.api.timeout
```

### 2. 在窗口管理中使用

```python
from backend.config import config

class WindowManager:
    def __init__(self):
        self.window_config = config.window
    
    def create_window(self):
        return webview.create_window(
            title=self.window_config.title,
            width=self.window_config.width,
            height=self.window_config.height,
            debug=self.window_config.debug
        )
```

### 3. 在中间件中使用

```python
from backend.config import config

# 根据环境添加不同的中间件
if config.is_development():
    middleware_manager.add_middleware(LoggingMiddleware())

if config.is_production():
    middleware_manager.add_middleware(RateLimitMiddleware())
```

## 最佳实践

### 1. 避免硬编码
❌ **不推荐**
```python
if debug_mode:  # 硬编码的调试标志
    print("调试信息")

window_width = 1200  # 硬编码的窗口宽度
```

✅ **推荐**
```python
if config.api.debug:
    print("调试信息")

window_width = config.window.width
```

### 2. 环境感知
❌ **不推荐**
```python
# 手动检查环境
import os
if os.getenv('ENV') == 'production':
    enable_logging = False
```

✅ **推荐**
```python
if config.is_production():
    enable_logging = False
```

### 3. 类型安全
配置类使用 `@dataclass` 装饰器，提供类型提示和默认值：

```python
# 自动补全和类型检查
max_retries: int = config.api.max_retries  # IDE会提示类型
timeout: int = config.api.timeout
```

## 扩展配置

如需添加新的配置项：

1. **修改配置类**
```python
@dataclass
class APIConfig:
    # 现有配置...
    new_feature_enabled: bool = False  # 新增配置
```

2. **更新环境特定配置**
```python
def _load_api_config(self) -> APIConfig:
    if self.env == 'production':
        return APIConfig(
            # 现有配置...
            new_feature_enabled=True  # 生产环境启用
        )
    # 其他环境...
```

3. **在代码中使用**
```python
if config.api.new_feature_enabled:
    # 新功能逻辑
    pass
```

## 配置验证

配置系统会在启动时自动验证：

```python
# 配置会在导入时自动初始化和验证
from backend.config import config

# 检查配置状态
print(f"当前环境: {config.env}")
print(f"API配置: {config.api.__dict__}")
print(f"窗口配置: {config.window.__dict__}")
print(f"安全配置: {config.security.__dict__}")
```

## 故障排除

### 1. 环境变量未生效
确保在启动应用前设置环境变量：
```bash
# Windows
set APP_ENV=production
python main.py

# Linux/Mac
APP_ENV=production python main.py
```

### 2. 配置未更新
重启应用以加载新的配置：
```bash
python dev.py  # 开发模式
# 或
python main.py  # 生产模式
```

### 3. 类型错误
确保配置值的类型正确：
```python
# 正确
config.window.width  # int
config.api.debug     # bool

# 错误
config.window.width = "1200"  # 应该是 int，不是 str
```

通过遵循这些指南，您可以有效地使用 Article Artisan 的配置管理系统，确保应用在不同环境下的正确行为。