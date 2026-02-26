#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
应用模板

使用方法:
1. 复制此文件并重命名 (如：my_app.py)
2. 修改 Agent 和 Task 配置
3. 在 launch_app.py 的 APPLICATIONS 中注册
"""

from crewai import Agent, Task, Crew


def main():
    """应用入口"""
    print("=" * 60)
    print(" " * 20 + "我的应用")
    print("=" * 60)

    # 创建智能体
    agent = Agent(
        role="角色名称",
        goal="目标",
        backstory="背景故事（可选）",
        verbose=True,
    )

    # 创建任务
    task = Task(
        description="任务描述",
        expected_output="期望输出",
        agent=agent,
    )

    # 创建团队并执行
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    results = crew.kickoff()

    print("\n" + "=" * 60)
    print("结果:", results)
    print("=" * 60)


if __name__ == "__main__":
    main()
