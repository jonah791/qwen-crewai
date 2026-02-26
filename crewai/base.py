"""CrewAI 框架基类"""

import uuid


class BaseComponent:
    """所有 CrewAI 组件的基类，提供唯一标识符"""

    def __init__(self):
        self.id = str(uuid.uuid4())

    def __str__(self):
        return f"{self.__class__.__name__}('{self.id[:8]}')"

    __repr__ = __str__
