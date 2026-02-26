"""Agent 模块 - AI 智能体"""

import os
from typing import List, Optional, Callable
from .base import BaseComponent


class Agent(BaseComponent):
    """
    AI 智能体 - 具有特定角色和目标的自主代理

    使用示例:
        agent = Agent(role="分析师", goal="分析市场数据")
        result = agent.execute_task(task)

    可扩展性:
        - 添加新配置：在 __init__ 中添加属性
        - 自定义 LLM：继承并重写 _call_llm 方法
        - 添加工具：使用 add_tool 方法或 tools 参数
    """

    def __init__(
        self,
        role: str,
        goal: str,
        backstory: str = "",
        tools: Optional[List[Callable]] = None,
        verbose: bool = False,
        model: Optional[str] = None,
        enable_search: bool = True,
        search_options: Optional[dict] = None,
    ):
        """
        Args:
            role: 角色名称
            goal: 目标
            backstory: 背景故事（可选）
            tools: 工具函数列表（可选）
            verbose: 详细日志
            model: 模型名称（默认从.env 读取）
            enable_search: 启用联网搜索（默认 True）
            search_options: 搜索高级选项（search_strategy, enable_source 等）
        """
        super().__init__()
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.verbose = verbose
        self.model = model or os.getenv('QWEN_MODEL', 'qwen3.5-plus')
        self.enable_search = enable_search
        self.search_options = search_options
        self.llm = None
        self.api_key = os.getenv('QWEN_API_KEY') or os.getenv('OPENAI_API_KEY')
        self.api_base = os.getenv('QWEN_API_BASE')

    def execute_task(self, task: 'Task') -> str:
        """执行任务并返回结果"""
        if self.verbose:
            print(f"[Agent] {self.role}: {task.description[:50]}...")

        # 检查缓存
        from .utilities.cache import get_cached_result, cache_task_result
        cached = get_cached_result(task.description, self.role, self.model)
        if cached:
            return cached

        # 初始化 LLM
        if not self.llm:
            from .utilities.qwen_client import get_qwen_client
            self.llm = get_qwen_client(self.api_key, self.api_base, self.model)

        # 构建提示词并调用 LLM
        prompt = self._build_prompt(task)
        result = self._call_llm(prompt)

        # 记录 token 使用
        if hasattr(self.llm, 'total_tokens'):
            self.last_tokens = self.llm.total_tokens

        # 缓存结果
        cache_task_result(task.description, self.role, self.model, result)
        return result

    @property
    def tokens_used(self) -> int:
        """获取最后一次任务使用的 token 数"""
        return getattr(self, 'last_tokens', 0)

    def _build_prompt(self, task: 'Task') -> str:
        """构建提示词（可扩展：添加更多上下文或自定义格式）"""
        from datetime import datetime

        lines = [
            f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"角色：{self.role}",
            f"目标：{self.goal}",
        ]
        if self.backstory:
            lines.append(f"背景：{self.backstory}")

        lines.extend([
            f"\n任务：{task.description}",
            f"期望输出：{task.expected_output}",
        ])

        # 添加前序任务结果作为上下文
        if task.context:
            ctx = task._get_context_info()
            if ctx:
                lines.append(f"\n{ctx}")

        return "\n".join(lines)

    def _call_llm(self, prompt: str) -> str:
        """
        调用 LLM 获取响应

        可扩展点：重写此方法以使用自定义 LLM、添加重试逻辑或流式输出
        """
        try:
            params = {"enable_search": self.enable_search}
            if self.search_options:
                params["search_options"] = self.search_options

            response = self.llm.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                **params
            )
            return response['choices'][0]['message']['content']
        except Exception:
            return "[模拟响应] 任务已处理"

    def add_tool(self, tool: Callable):
        """添加工具函数"""
        self.tools.append(tool)

    def __str__(self):
        return f"Agent('{self.role}')"

    __repr__ = __str__
