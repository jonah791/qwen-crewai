"""Task 模块 - 任务"""

from typing import Optional, List
from .base import BaseComponent


class Task(BaseComponent):
    """
    任务 - 由 Agent 执行的工作单元

    使用示例:
        task = Task(description="分析市场", expected_output="分析报告")
        result = task.execute()

    可扩展性:
        - 添加新属性：在 __init__ 中定义
        - 自定义输出：重写 execute 方法
        - 添加验证：在 execute 前添加验证逻辑
    """

    def __init__(
        self,
        description: str,
        expected_output: str,
        agent: Optional['Agent'] = None,
        context: Optional[List['Task']] = None,
        output_file: Optional[str] = None,
    ):
        """
        Args:
            description: 任务描述
            expected_output: 期望输出
            agent: 执行任务的智能体
            context: 依赖的前序任务（用于传递结果）
            output_file: 输出文件路径（可选）
        """
        super().__init__()
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.context = context or []
        self.output_file = output_file
        self._result = None

    def execute(self) -> str:
        """执行任务并返回结果（可扩展：添加前置/后置钩子、验证逻辑）"""
        if not self.agent:
            raise ValueError("未分配智能体")

        self._result = self.agent.execute_task(self)

        if self.output_file:
            self._save_to_file(self._result)

        return self._result

    def _get_context_info(self) -> str:
        """获取前序任务结果作为上下文（可扩展：自定义格式、过滤、摘要）"""
        if not self.context:
            return ""

        lines = ["前序任务结果:"]
        for t in self.context:
            if t._result:
                info = t._result[:200] + "..." if len(t._result) > 200 else t._result
                lines.append(f"- {t.description}: {info}")
            else:
                lines.append(f"- {t.description}: <未执行>")

        return "\n".join(lines)

    def _save_to_file(self, result: str):
        """保存结果到文件"""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(result)
        except Exception as e:
            print(f"保存文件失败：{e}")

    @property
    def result(self) -> Optional[str]:
        """获取任务结果（如果已执行）"""
        return self._result

    def __str__(self):
        return f"Task('{self.description[:30]}...')"

    __repr__ = __str__
