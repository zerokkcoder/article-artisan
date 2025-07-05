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
├── frontend/                 # 前端项目目录
│   ├── src/
│   │   ├── App.vue          # 主应用组件
│   │   ├── main.ts          # 入口文件
│   │   └── ...
│   ├── package.json         # 前端依赖配置
│   ├── vite.config.ts       # Vite 配置
│   └── ...
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

### PyWebView 配置 (main.py)

```python
window = webview.create_window(
    title='Article Artisan',
    url=url,
    js_api=api,
    width=1200,
    height=800,
    min_size=(800, 600),
    resizable=True
)
```

## 🔌 API 通信

### Python 后端 API

```python
class Api:
    def get_data(self):
        return {"message": "Hello from Python!"}
    
    def set_message(self, message):
        return {"success": True, "message": message}
```

### 前端调用

```typescript
// 获取数据
const data = await window.pywebview.api.get_data()

// 设置消息
const result = await window.pywebview.api.set_message("新消息")
```

## 📝 开发指南

### 添加新的 API

1. 在 `main.py` 的 `Api` 类中添加新方法
2. 在前端 TypeScript 中声明类型
3. 在 Vue 组件中调用

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
A: 确保 PyWebView API 已正确初始化，可以在浏览器控制台查看错误信息

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系

如有问题或建议，请创建 Issue 或联系项目维护者。

---

⭐ 如果这个项目对你有帮助，请给它一个星标！