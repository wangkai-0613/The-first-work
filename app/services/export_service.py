"""运势结果 TXT/JSON 文件导出。

只负责把 :func:`app.services.fortune_service.get_daily_fortune` 返回的
结果字典落盘为可读文件，不做任何运势计算，也不在导出失败时静默吞掉异常
（见 docs/architecture.md 的错误处理约定）。
"""

import json
from pathlib import Path
from typing import Any


FIELDS = (
    "date", "zodiac", "overall", "love", "study", "health",
    "lucky_color", "lucky_number", "message",
)


def _validate_result(result: dict[str, Any]) -> None:
    """校验 ``result`` 是否为包含 :data:`FIELDS` 全部字段的字典。

    Raises:
        ValueError: ``result`` 不是字典，或缺少任意必需字段。
    """
    if not isinstance(result, dict):
        raise ValueError("导出结果必须是字典。")
    missing = [field for field in FIELDS if field not in result]
    if missing:
        raise ValueError(f"运势结果缺少字段：{', '.join(missing)}")


def _to_text(result: dict[str, Any]) -> str:
    """把运势结果渲染成便于阅读的纯文本报告。"""
    return "\n".join((
        "生日助手 · 每日运势",
        "=" * 24,
        f"日期：{result['date']}",
        f"星座：{result['zodiac']}",
        f"综合运势：{result['overall']}/5",
        f"爱情运势：{result['love']}/5",
        f"学习运势：{result['study']}/5",
        f"健康运势：{result['health']}/5",
        f"幸运颜色：{result['lucky_color']}",
        f"幸运数字：{result['lucky_number']}",
        f"今日建议：{result['message']}",
        "",
        "温馨提示：每日运势仅供娱乐。",
        "",
    ))


def export_fortune(result: dict[str, Any], file_path: str | Path) -> Path:
    """将运势结果导出为 UTF-8 编码的 TXT 或 JSON 文件。

    Args:
        result: :func:`app.services.fortune_service.get_daily_fortune` 的
            返回值（或字段完全一致的字典）。
        file_path: 目标文件路径。缺省扩展名时按 ``.txt`` 处理；父目录不
            存在会自动创建。

    Returns:
        实际写入文件的绝对路径。

    Raises:
        ValueError: ``result`` 缺少必需字段、``file_path`` 类型不对、
            未指定有效文件名，或扩展名不是 ``.txt``/``.json``。
        OSError: 底层文件写入失败（例如没有写权限），不会被静默吞掉。
    """
    _validate_result(result)
    if not isinstance(file_path, (str, Path)):
        raise ValueError("导出路径必须是文本或 Path 对象。")
    path = Path(file_path).expanduser()
    if not path.name:
        raise ValueError("请选择有效的导出文件路径。")
    if not path.suffix:
        path = path.with_suffix(".txt")
    suffix = path.suffix.lower()
    if suffix not in (".txt", ".json"):
        raise ValueError("仅支持导出 TXT 或 JSON 文件。")

    path.parent.mkdir(parents=True, exist_ok=True)
    if suffix == ".json":
        content = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    else:
        content = _to_text(result)
    path.write_text(content, encoding="utf-8")
    return path.resolve()
