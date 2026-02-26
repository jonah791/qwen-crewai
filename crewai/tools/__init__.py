"""
Tools module - 工具函数

工具函数是 Agent 可以调用的辅助函数。
自定义工具：创建函数并添加到 Agent 的 tools 列表。

使用示例:
    def search(query: str) -> str:
        return f"搜索结果：{query}"

    agent = Agent(role="研究员", tools=[search])
"""


def read_file(file_path: str) -> str:
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"读取文件失败：{e}"


def save_file(file_path: str, content: str) -> str:
    """保存文件内容"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"文件已保存：{file_path}"
    except Exception as e:
        return f"保存文件失败：{e}"
