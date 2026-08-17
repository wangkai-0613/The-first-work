"""文件导出接口，由运势与导出负责人实现。"""

from pathlib import Path
from typing import Any


def export_fortune(result: dict[str, Any], file_path: str | Path) -> Path:
    """将运势导出到文件并返回最终路径。"""
    raise NotImplementedError("由 feature/fortune-export 分支实现")

