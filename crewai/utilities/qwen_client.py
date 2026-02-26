"""Qwen API 客户端 - 支持 DashScope 联网搜索"""

import os
from typing import Dict, Any, Optional, List


class MockQwenClient:
    """模拟客户端 - 测试和降级使用"""

    def __init__(self, model: str):
        self.model = model
        self.call_count = 0
        self.total_tokens = 0

    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """返回模拟响应（估算 token）"""
        self.call_count += 1
        user_message = next((m["content"] for m in messages if m["role"] == "user"), "")
        enable_search = kwargs.get("enable_search", False)

        prompt_tokens = max(10, len(user_message) // 2)
        completion_tokens = max(50, prompt_tokens * 2)
        total_tokens = prompt_tokens + completion_tokens
        self.total_tokens += total_tokens

        return {
            "id": f"mock-{self.call_count}",
            "model": self.model,
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": f"收到消息：'{user_message}'。搜索：{'已启用' if enable_search else '未启用'}。模拟响应。"
                }
            }],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens
            }
        }


class QwenClient:
    """
    Qwen API 客户端 - 支持 DashScope 联网搜索，自动降级到模拟模式

    可扩展性：添加新的模型提供商或自定义重试逻辑
    """

    def __init__(self, api_key: str, api_base: str, model: str):
        self.api_key = api_key
        self.api_base = api_base
        self.model = model
        self.use_real_client = False
        self.mock_client = MockQwenClient(model)
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_tokens = 0

        if self._is_valid_api_key(api_key):
            self._init_real_client()

    def _is_valid_api_key(self, key: str) -> bool:
        """检查 API 密钥是否有效（非占位符）"""
        if not key or not key.strip():
            return False
        return not any(p in key.lower() for p in ['your-', 'example', 'test', 'dummy', 'placeholder'])

    def _init_real_client(self):
        """初始化真实 API 客户端（DashScope 优先，降级到 OpenAI）"""
        try:
            import dashscope
            dashscope.api_key = self.api_key
            self.client_type = "dashscope"
            self.dashscope_client = dashscope
            self.use_real_client = True
        except ImportError:
            try:
                import openai
                self.client_type = "openai"
                self.openai_client = openai.OpenAI(api_key=self.api_key, base_url=self.api_base)
                self.use_real_client = True
            except ImportError:
                pass

    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """生成聊天完成响应"""
        if not self.use_real_client:
            return self.mock_client.chat_completion(messages, **kwargs)

        if self.client_type == "dashscope":
            return self._call_dashscope(messages, **kwargs)
        return self._call_openai(messages, **kwargs)

    def _call_dashscope(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """调用 DashScope SDK（支持联网搜索）"""
        try:
            enable_search = kwargs.get("enable_search", False)
            search_options = kwargs.get("search_options", None)

            params = {
                "model": self.model,
                "messages": messages,
                "result_format": "message",
            }

            if enable_search:
                params["enable_search"] = True
                if search_options:
                    params.update(search_options)

            # 根据模型类型选择接口（qwen3.5-plus 等多模态模型用 MultiModalConversation）
            multimodal = any(m in self.model.lower() for m in ['qwen3.5-plus', 'qwen3-vl', 'qwen-vl', 'qwen2-vl'])
            if multimodal:
                response = self.dashscope_client.MultiModalConversation.call(**params)
            else:
                response = self.dashscope_client.Generation.call(**params)

            if hasattr(response, 'status_code') and response.status_code != 200:
                raise Exception(f"API 错误 {response.status_code}: {getattr(response, 'message', '')}")

            if not hasattr(response, 'output') or response.output is None:
                raise Exception(f"空响应：{getattr(response, 'message', '')}")

            usage = getattr(response, 'usage', {})
            prompt_tokens = getattr(usage, 'input_tokens', 0) or getattr(usage, 'prompt_tokens', 0)
            completion_tokens = getattr(usage, 'output_tokens', 0) or getattr(usage, 'completion_tokens', 0)
            total_tokens = getattr(usage, 'total_tokens', prompt_tokens + completion_tokens)

            self.total_prompt_tokens += prompt_tokens
            self.total_completion_tokens += completion_tokens
            self.total_tokens += total_tokens

            return {
                "id": getattr(response, 'request_id', 'unknown'),
                "model": self.model,
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": response.output.choices[0].message.content
                    }
                }],
                "usage": {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens
                }
            }

        except Exception as e:
            print(f"[DEBUG] DashScope 调用失败：{e}")
            self.use_real_client = False
            return self.mock_client.chat_completion(messages, **kwargs)

    def _call_openai(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """调用 OpenAI SDK（兼容格式）"""
        try:
            enable_search = kwargs.get("enable_search", False)
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                extra_body={"enable_search": enable_search} if enable_search else {}
            )
            return response.model_dump()
        except Exception:
            self.use_real_client = False
            return self.mock_client.chat_completion(messages, **kwargs)


def get_qwen_client(api_key: Optional[str] = None, api_base: Optional[str] = None,
                    model: Optional[str] = None) -> QwenClient:
    """获取 Qwen 客户端实例（优先级：参数 > 环境变量 > 默认值）"""
    api_key = api_key or os.getenv('QWEN_API_KEY') or os.getenv('OPENAI_API_KEY')
    api_base = api_base or os.getenv('QWEN_API_BASE') or os.getenv('OPENAI_API_BASE') \
        or 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    model = model or os.getenv('QWEN_MODEL') or os.getenv('OPENAI_MODEL') or 'qwen3.5-plus'
    return QwenClient(api_key, api_base, model)
