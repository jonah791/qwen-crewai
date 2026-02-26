# CrewAI Framework

极简多智能体协作框架

## 快速开始

```bash
# 1. 安装依赖
pip install -e .

# 2. 配置 API（编辑 .env 文件）
# QWEN_API_KEY=你的密钥

# 3. 运行示例
python launch_app.py
```

## 核心组件

```python
from crewai import Agent, Task, Crew

# 创建智能体
agent = Agent(role="分析师", goal="分析数据", backstory="你是专家")

# 创建任务
task = Task(description="分析市场", expected_output="报告", agent=agent)

# 创建团队并执行
crew = Crew(agents=[agent], tasks=[task])
results = crew.kickoff()
```

## 添加新应用

1. 复制 `app_template.py` → `my_app.py`
2. 在 `launch_app.py` 的 `APPLICATIONS` 中注册
3. 运行 `python launch_app.py` 选择启动

## 项目结构

```
crewai_framework/
├── crewai/              # 核心框架
│   ├── agent.py         # 智能体
│   ├── task.py          # 任务
│   └── crew.py          # 团队
├── launch_app.py        # 启动器
├── app_template.py      # 应用模板
└── .env                 # 配置文件
```

## 文档

- [使用示例](financial_market_analyzer.py)
- [应用模板](app_template.py)
