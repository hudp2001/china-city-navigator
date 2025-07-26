# 中国省市百科导航网页

本项目旨在创建一个交互式、可视化的中国省市百科导航网页，提供省市信息展示、地图导航和用户行为记录功能。

## 项目特点

- **响应式三栏布局**：适配 PC 浏览器窗口
- **树形菜单交互**：支持展开/折叠动画和地图联动定位
- **城市卡片展示**：展示人口、GDP、标签等字段
- **地图联动与热力图**：支持缩放、平移、图层切换和热力图展示
- **夜间模式切换**：手动/自动切换深色/浅色主题
- **数据更新机制**：支持管理员一键更新省市级数据

## 技术栈

- **前端框架**：Vue.js 3.4.0
- **状态管理**：Pinia 2.1.7
- **地图库**：Leaflet 1.9.4
- **构建工具**：Vite 5.0.0

## 开发环境

- Node.js >= 18.x
- npm 或 yarn / pnpm

## 启动项目

1. 安装依赖
   ```bash
   npm install
   ```

2. 启动开发服务器
   ```bash
   npm run dev
   ```

3. 构建生产版本
   ```bash
   npm run build
   ```

## 目录结构

```
ChinaCityNavigator/
├── public/                     # 静态资源（如 favicon、robots.txt）
│   ├── index.html              # 主 HTML 页面
│   └── assets/                 # 公共静态资源（图片、字体等）
├── src/                        # 源代码目录
│   ├── components/             # 可复用 UI 组件
│   ├── views/                  # 页面视图组件
│   ├── services/               # 数据服务模块
│   ├── store/                  # 状态管理（Pinia）
│   ├── utils/                  # 工具函数
│   ├── styles/                 # 全局样式与主题
│   ├── assets/                 # 本地静态资源（图标、SVG、JSON 数据）
│   ├── App.vue                 # 根组件
│   └── main.js                 # Vue 应用入口文件
├── assets/                     # 本地静态资源（图标、SVG、JSON 数据）
│   ├── json/                   # 各省市级 JSON 数据文件
│   └── images/                 # 图标、LOGO、UI 资源
├── config/                     # 构建配置
├── docs/                       # 文档目录（PRD、用户故事、技术栈等文档）
├── tests/                      # 测试目录（可选）
└── package.json                # 项目依赖与脚本
```

## 文档

- [PRD 文档](docs/1.0%20prd.md)
- [用户旅程文档](docs/2.1%20user_journey.md)
- [系统设计文档](docs/3.0%20system_design.md)
- [技术栈文档](docs/3.1%20tech_stack.md)
- [项目结构文档](docs/3.2%20project_structure.md)
- [任务看板文档](docs/4.0%20task_todo_list.md)