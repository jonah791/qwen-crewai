"""Crew 模块 - 智能体团队"""

import time
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from .base import BaseComponent


class Crew(BaseComponent):
    """
    智能体团队 - 协调多个 Agent 完成任务

    使用示例:
        crew = Crew(agents=[agent1, agent2], tasks=[task1, task2])
        results = crew.kickoff()

    可扩展性:
        - 添加新流程：添加新的执行方法（如 kickoff_async）
        - 添加管理功能：添加管理 Agent 的方法
        - 自定义协作：重写 kickoff 方法
    """

    def __init__(
        self,
        agents: List['Agent'],
        tasks: List['Task'],
        verbose: bool = False,
    ):
        """
        Args:
            agents: 智能体列表
            tasks: 任务列表
            verbose: 详细日志
        """
        super().__init__()
        self.agents = agents
        self.tasks = tasks
        self.verbose = verbose

    def kickoff(self) -> List[str]:
        """
        执行所有任务（顺序执行）

        适用于：任务之间有依赖关系或需要严格控制执行顺序
        """
        if self.verbose:
            print(f"[Crew] 开始：{len(self.agents)}个智能体，{len(self.tasks)}个任务")

        results = []
        for i, task in enumerate(self.tasks, 1):
            if self.verbose:
                print(f"\n[Crew] 任务 {i}/{len(self.tasks)}: {task.description[:50]}...")

            result = task.execute()
            results.append(result)

            if self.verbose:
                print(f"[Crew] 任务 {i} 完成 ({len(result)} 字符)")

        if self.verbose:
            print(f"\n[Crew] 完成")

        return results

    def kickoff_parallel(self, max_workers: int = 4,
                         rate_limit: Optional[float] = None) -> List[str]:
        """
        并行执行任务（带可选速率限制）

        Args:
            max_workers: 最大并发数（建议 4-7）
            rate_limit: 每秒请求数限制（None 则不限制）

        适用于：任务之间无依赖关系的 I/O 密集型任务

        Qwen API 限制参考:
            - RPM: 600 请求/分钟
            - RPS: 10 请求/秒
            - TPM: 1,000,000 Token/分钟

        推荐配置:
            - 保守：max_workers=4, rate_limit=2.0
            - 平衡：max_workers=6, rate_limit=5.0
            - 激进：max_workers=7, rate_limit=None
        """
        if not self.tasks:
            return []

        if self.verbose:
            rate_info = f", 速率限制={rate_limit} req/s" if rate_limit else ""
            print(f"[Crew] 并行执行：{len(self.tasks)}个任务，最大并发={max_workers}{rate_info}")

        results = []
        last_request_time = 0

        def execute_with_rate_limit(task):
            """带速率限制的任务执行"""
            nonlocal last_request_time
            if rate_limit:
                min_interval = 1.0 / rate_limit
                elapsed = time.time() - last_request_time
                if elapsed < min_interval:
                    time.sleep(min_interval - elapsed)
                last_request_time = time.time()
            return task.execute()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {
                executor.submit(execute_with_rate_limit, task): task
                for task in self.tasks
            }

            for i, future in enumerate(as_completed(future_to_task), 1):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                    if self.verbose:
                        print(f"[Crew] 任务 {i}/{len(self.tasks)} 完成：{task.description[:20]}... ({len(result)} 字符)")
                except Exception as e:
                    print(f"[Crew] 任务失败：{task.description[:20]}... - {e}")

        return results

    def add_agent(self, agent: 'Agent'):
        """添加智能体到团队"""
        self.agents.append(agent)

    def add_task(self, task: 'Task'):
        """添加任务到团队"""
        self.tasks.append(task)

    def __str__(self):
        return f"Crew({len(self.agents)}人，{len(self.tasks)}任务)"

    __repr__ = __str__
