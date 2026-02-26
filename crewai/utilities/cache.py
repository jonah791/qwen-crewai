"""基础缓存模块 - 减少重复 API 调用"""

import hashlib
import json
import time
from typing import Optional, Dict


class SimpleCache:
    """内存缓存，支持 TTL 过期"""

    def __init__(self, ttl: int = 3600):
        self._cache: Dict[str, tuple] = {}
        self.ttl = ttl
        self.hits = 0
        self.misses = 0

    def _make_key(self, *args, **kwargs) -> str:
        """生成缓存键（基于参数的 MD5 哈希）"""
        key_data = json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True, default=str)
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(self, key: str) -> Optional[str]:
        """获取缓存，过期自动删除"""
        if key in self._cache:
            value, expire_time = self._cache[key]
            if time.time() < expire_time:
                self.hits += 1
                return value
            del self._cache[key]
        self.misses += 1
        return None

    def set(self, key: str, value: str):
        """设置缓存"""
        self._cache[key] = (value, time.time() + self.ttl)

    def clear(self):
        """清空缓存"""
        self._cache.clear()
        self.hits = self.misses = 0


# 全局缓存实例（1 小时过期）
_task_cache = SimpleCache(ttl=3600)


def get_cached_result(task_desc: str, agent_role: str, model: str) -> Optional[str]:
    """获取缓存的任务结果"""
    return _task_cache.get(_task_cache._make_key(task_desc, agent_role, model))


def cache_task_result(task_desc: str, agent_role: str, model: str, result: str):
    """缓存任务结果"""
    _task_cache.set(_task_cache._make_key(task_desc, agent_role, model), result)
