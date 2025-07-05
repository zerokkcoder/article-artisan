# Article Artisan

🎨 一个优雅的 PyWebView + Vite + Vue3 集成示例项目

## 📋 项目简介

Article Artisan 是一个展示如何优雅集成 PyWebView、Vite 和 Vue3 的示例项目。它提供了完整的开发和打包解决方案，让你可以轻松创建现代化的桌面应用程序。

## ✨ 特性

- 🚀 **现代化前端**: 使用 Vite + Vue3 + TypeScript
- 🐍 **Python 后端**: 基于 PyWebView 的桌面应用
- 🔄 **热重载开发**: 前端支持热重载，提升开发效率
- 📦 **一键打包**: 自动构建前端并打包成可执行文件
- 🎯 **API 集成**: 前后端无缝通信
- 💻 **跨平台**: 支持 Windows、macOS、Linux

## 🛠️ 技术栈

### 前端
- **Vue 3**: 渐进式 JavaScript 框架
- **Vite**: 下一代前端构建工具
- **TypeScript**: 类型安全的 JavaScript

### 后端
- **Python 3.8+**: 主要编程语言
- **PyWebView**: 轻量级 WebView 包装器
- **PyInstaller**: Python 应用打包工具

## 📁 项目结构

```
article-artisan/
├── backend/                  # 后端项目目录
│   ├── api/                 # API 模块
│   │   ├── auth.py          # 认证API
│   │   ├── base.py          # 基础API类
│   │   └── system.py        # 系统API
│   ├── config.py            # 配置管理
│   ├── logger.py            # 日志系统
│   ├── middleware.py        # 中间件系统
│   ├── window.py            # 窗口管理
│   └── ...
├── frontend/                 # 前端项目目录
│   ├── src/
│   │   ├── App.vue          # 主应用组件
│   │   ├── main.ts          # 入口文件
│   │   ├── components/      # Vue 组件
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── types/           # TypeScript 类型定义
│   │   └── ...
│   ├── package.json         # 前端依赖配置
│   ├── vite.config.ts       # Vite 配置
│   └── ...
├── docs/                     # 项目文档
│   ├── ARCHITECTURE.md      # 架构设计文档
│   ├── CONFIG_GUIDE.md      # 配置使用指南
│   ├── CODE_QUALITY_RECOMMENDATIONS.md  # 代码质量建议
│   └── QUICK_IMPROVEMENTS.md # 快速改进指南
├── main.py                  # Python 主应用
├── dev.py                   # 开发模式启动脚本
├── build.py                 # 打包脚本
├── requirements.txt         # Python 依赖
└── README.md               # 项目说明
```

## 🚀 快速开始

### 环境要求

- **Python 3.8+**
- **Node.js 16+**
- **npm 或 yarn**

### 安装依赖

1. **安装 Python 依赖**:
   ```bash
   pip install -r requirements.txt
   ```

2. **安装前端依赖**:
   ```bash
   cd frontend
   npm install
   ```

### 开发模式

使用一键开发脚本，自动启动前端开发服务器和 Python 后端：

```bash
python dev.py
```

这个脚本会：
- ✅ 检查 Node.js 和 npm 环境
- 📦 自动安装前端依赖（如果需要）
- 🚀 启动 Vite 开发服务器 (http://localhost:5173)
- 🐍 启动 PyWebView 应用
- 🔄 支持前端热重载

### 手动开发模式

如果你想分别启动前后端：

1. **启动前端开发服务器**:
   ```bash
   cd frontend
   npm run dev
   ```

2. **启动 Python 应用**:
   ```bash
   python main.py
   ```

### 生产打包

使用一键打包脚本，自动构建前端并创建可执行文件：

```bash
python build.py
```

这个脚本会：
- 🔍 检查必要的依赖
- 📦 安装前端依赖
- 🏗️ 构建前端项目
- 📦 使用 PyInstaller 打包成可执行文件
- 🧹 自动清理构建文件

打包完成后，可执行文件位于 `dist/ArticleArtisan.exe`

## 🔧 配置说明

### Vite 配置 (frontend/vite.config.ts)

```typescript
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    host: 'localhost',
    cors: true,
    open: false // 不自动打开浏览器
  },
  base: './' // 使用相对路径，适配 PyWebView
})
```

### PyWebView 配置

项目使用配置管理系统统一管理窗口配置：

```python
# backend/config.py
class WindowConfig:
    title: str = "Article Artisan"
    width: int = 1200
    height: int = 800
    min_width: int = 800
    min_height: int = 600
    resizable: bool = True
    debug: bool = False

# backend/window.py
class WindowManager:
    def create_window(self):
        window = webview.create_window(
            title=self.window_config.title,
            url=url,
            js_api=api,
            width=self.window_config.width,
            height=self.window_config.height,
            min_size=(self.window_config.min_width, self.window_config.min_height),
            resizable=self.window_config.resizable
        )
        return window
```

## 🔌 API 通信

### Python 后端 API

项目使用模块化的 API 架构，所有 API 继承自 `BaseAPI` 类：

```python
# backend/api/auth.py
class AuthAPI(BaseAPI):
    def login(self, username: str, password: str):
        # 登录逻辑
        return self._create_response(
            success=True,
            data={"token": "...", "user": {...}},
            message="登录成功"
        )

# backend/api/system.py
class SystemAPI(BaseAPI):
    def get_system_info(self):
        return self._create_response(
            success=True,
            data={"version": "1.0.0", "platform": "..."}
        )
```

### 前端调用

```typescript
// 用户登录
const loginResult = await window.pywebview.api.login("admin", "123456")
if (loginResult.success) {
  console.log("登录成功", loginResult.data)
}

// 获取系统信息
const systemInfo = await window.pywebview.api.get_system_info()
console.log("系统信息", systemInfo.data)
```

### API 响应格式

所有 API 返回统一的响应格式：

```typescript
interface APIResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  error?: string
}
```

## 📚 项目文档

项目提供了完整的文档体系，所有文档位于 `docs/` 目录中：

- **[架构设计文档](docs/ARCHITECTURE.md)** - 详细的系统架构说明
- **[配置使用指南](docs/CONFIG_GUIDE.md)** - 配置管理系统使用方法
- **[代码质量建议](docs/CODE_QUALITY_RECOMMENDATIONS.md)** - 代码质量和可维护性提升建议
- **[快速改进指南](docs/QUICK_IMPROVEMENTS.md)** - 按优先级排序的代码改进实施指南

## 📝 开发指南

### 添加新的 API

1. 在 `backend/api/` 目录中创建或修改 API 模块
2. 继承 `BaseAPI` 类并实现相应方法
3. 在前端 TypeScript 中声明类型
4. 在 Vue 组件中调用

### 配置管理

项目使用集中化配置管理系统，详见 [配置使用指南](docs/CONFIG_GUIDE.md)：

```python
from backend.config import config

# 访问配置
print(config.window.title)
print(config.api.timeout)
```

### 自定义样式

- 修改 `frontend/src/App.vue` 中的样式
- 使用 CSS 变量和现代 CSS 特性
- 支持响应式设计

### 添加新页面

- 在 `frontend/src/components/` 中创建新组件
- 可以使用 Vue Router 进行路由管理

## 🐛 常见问题

### Q: 开发模式下前端服务器启动失败
A: 确保 Node.js 和 npm 已正确安装，并且端口 5173 未被占用

### Q: 打包后的应用无法启动
A: 检查是否正确安装了 PyInstaller，并确保前端已成功构建

### Q: API 调用失败
A: 确保 PyWebView API 已正确初始化，可以在浏览器控制台查看错误信息。检查 API 方法是否正确继承自 `BaseAPI`

### Q: 配置修改后不生效
A: 确保重启了应用，配置在应用启动时加载。可以查看 [配置使用指南](docs/CONFIG_GUIDE.md) 了解详细信息

### Q: 如何添加新的 API 模块
A: 在 `backend/api/` 目录下创建新文件，继承 `BaseAPI` 类，并在 `MainAPI` 中注册。参考现有的 `AuthAPI` 和 `SystemAPI`

### Q: 日志在哪里查看
A: 开发模式下日志输出到控制台，生产模式下会生成日志文件。日志配置可在 `backend/config.py` 中修改

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系

如有问题或建议，请创建 Issue 或联系项目维护者。

---

⭐ 如果这个项目对你有帮助，请给它一个星标！