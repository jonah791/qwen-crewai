# CrewAI Framework

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Qwen](https://img.shields.io/badge/model-Qwen-purple.svg)](https://www.aliyun.com/product/bailian)

**极简多智能体协作框架** - 基于阿里云 Qwen 模型的轻量级 CrewAI 实现

---

## ✨ 特性

- 🤖 **多智能体协作** - 创建具有不同角色和目标的 AI 智能体团队
- 🎯 **任务导向** - 定义清晰的任务和预期输出
- 🔧 **工具扩展** - 支持自定义工具函数
- 🌐 **联网搜索** - 内置 Qwen 联网搜索能力
- 💾 **缓存优化** - 智能缓存提升效率
- 🚀 **即插即用** - 极简 API，快速上手

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -e .
```

### 2. 配置 API

编辑 `.env` 文件：

```bash
# 阿里云百炼 API Key
QWEN_API_KEY=sk-your-api-key-here

# 模型配置（可选）
QWEN_MODEL=qwen3.5-plus

# 启用联网搜索（可选）
QWEN_ENABLE_SEARCH=true
```

### 3. 运行示例

```bash
python launch_app.py
```

---

## 📖 核心组件

### Agent（智能体）

```python
from crewai import Agent

# 创建智能体
agent = Agent(
    role="数据分析师",
    goal="分析市场数据并提供洞察",
    backstory="你是一位资深金融分析师，擅长发现市场趋势",
    tools=[custom_tool],  # 可选
    verbose=True,
    enable_search=True  # 启用联网搜索
)
```

### Task（任务）

```python
from crewai import Task

# 创建任务
task = Task(
    description="分析最近的市场数据",
    expected_output="一份包含趋势分析和建议的报告",
    agent=agent
)
```

### Crew（团队）

```python
from crewai import Crew

# 创建团队并执行
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    verbose=True
)

results = crew.kickoff()
```

---

## 📁 项目结构

```
qwen-crewai/
├── crewai/                  # 核心框架
│   ├── __init__.py         # 模块导出
│   ├── agent.py            # 智能体
│   ├── task.py             # 任务
│   ├── crew.py             # 团队
│   └── utilities/          # 工具函数
├── launch_app.py           # 应用启动器
├── requirements.txt        # 依赖
├── setup.py               # 安装配置
├── .env.example           # 环境配置示例
└── .gitignore             # Git 忽略规则
```

---

## 🛠️ 添加新应用

### 1. 复制模板

在 `launch_app.py` 中查看现有的应用示例。

### 2. 定义智能体和工作流

```python
def create_agents():
    analyst = Agent(role="分析师", goal="分析数据")
    return [analyst]

def create_tasks(agents):
    task = Task(description="分析...", agent=agents[0])
    return [task]
```

### 3. 在 `launch_app.py` 中注册

编辑 `APPLICATIONS` 字典添加你的应用。

---

## 📚 使用示例

### 基础示例

```python
from crewai import Agent, Task, Crew

# 创建智能体
writer = Agent(
    role="技术作家",
    goal="撰写清晰的技术文档",
    backstory="你有 10 年技术写作经验"
)

# 创建任务
task = Task(
    description="为 CrewAI 框架写一份简介",
    expected_output="300 字的项目介绍",
    agent=writer
)

# 执行
crew = Crew(agents=[writer], tasks=[task])
result = crew.kickoff()
print(result)
```

### 高级功能

查看 `launch_app.py` 中的完整示例：
- 多智能体协作
- 工具函数使用
- 联网搜索集成

---

## ⚙️ 配置选项

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `QWEN_API_KEY` | 阿里云百炼 API Key | 必需 |
| `QWEN_MODEL` | 模型名称 | `qwen3.5-plus` |
| `QWEN_ENABLE_SEARCH` | 启用联网搜索 | `true` |
| `QWEN_VERBOSE` | 详细日志 | `false` |

---

## 🔧 开发指南

### 自定义工具

```python
def my_tool(query: str) -> str:
    """自定义工具函数"""
    return f"查询结果：{query}"

agent = Agent(
    role="研究员",
    goal="收集信息",
    tools=[my_tool]
)
```

### 使用 Qwen API

框架内置 `QwenClient`，自动处理：
- API 认证
- 请求重试
- 响应解析
- 联网搜索

---

## 📝 更新日志

### v0.1.0 (2026-02-26)
- ✨ 初始版本
- 🤖 核心智能体/任务/团队实现
- 🔧 工具扩展支持
- 🌐 Qwen 联网搜索集成
- 💾 缓存机制

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [阿里云百炼](https://www.aliyun.com/product/bailian) - Qwen 模型支持
- [CrewAI](https://github.com/joaomdmoura/crewai) - 灵感和设计参考

---

_Built with ❤️ by jonah791_
