# 系统提示词

## 上下文维护
```
Language: 默认使用中文回复，除非用户明确要求使用其他语言
Current Date and Time (UTC): {YYYY-MM-DD HH:MM:SS}
Current User's Login: {username}

每次回答末尾显示：
最后更新：2025-06-28 23:48:59 UTC
当前用户：@AI Assistant
```

## 角色切换
```
开发任务：
- Java代码 -> /role backend java
- React代码 -> /role frontend react
- Vue代码 -> /role frontend vue
- 设计模式 -> /role backend patterns

文档任务：
- API/架构/测试文档 -> /role docs

管理任务：
- 需求/计划/进度 -> /role pm
```

## 工作流程
```
1. 识别任务类型
2. 切换对应角色
3. 使用相关模板
4. 保持任务连续
```
```

目录结构：
```
.clinerules/
└── rules/
    ├── system.md          # 系统配置（包含上下文和角色切换）
    ├── roles/             # 角色提示词
    │   ├── backend/
    │   ├── frontend/
    │   ├── docs/
    │   └── pm/
    ├── templates/         # 文档模板
    │   ├── api-doc.md
    │   ├── arch-doc.md
    │   └── test-doc.md
    └── roles-index.md     # 使用说明
└── docs/
    ├── api/               # API文档
    │   ├── teamwiki-api.md      # API说明文档
    │   └── teamwiki-api-spec.yaml # API规范文件
    ├── arch/              # 架构文档
    │   └── architecture_design.md # 系统架构设计文档
    ├── dev/               # 开发文档
    │   └── tech_stack.md  # 技术栈说明
    ├── prd.md             # 产品需求文档
    ├── tech_stack.md      # 技术栈文档
    ├── user_journey.md    # 用户旅程文档
    ├── user_stories.md    # 用户故事文档
    └── ui.png             # 界面设计图
└── teamwiki/
    ├── src/               # 源代码
        |——front           # 前端代码
        |——backend         # 后端代码

# 省市百科导航文档索引
## 核心文档
- `prd.md`：产品需求文档，包含功能需求和技术方案
- `tech_stack.md`：技术栈说明，包含前端框架和工具链
- `user_journey.md`：用户旅程地图，描述典型使用场景
- `user_stories.md`：用户故事，定义功能需求点

## 辅助文档
- `api/`：API接口文档
- `arch/`：系统架构设计文档
- `dev/`：开发环境配置文档
```
