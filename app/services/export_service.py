"""运势结果 TXT/JSON 文件导出。"""

import json
from pathlib import Path
from typing import Any


FIELDS = (
    "date", "zodiac", "overall", "love", "study", "health",
    "lucky_color", "lucky_number", "message",
)


def _validate_result(result: dict[str, Any]) -> None:
    if not isinstance(result, dict):
        raise ValueError("导出结果必须是字典。")
    missing = [field for field in FIELDS if field not in result]
    if missing:
        raise ValueError(f"运势结果缺少字段：{', '.join(missing)}")


def _to_text(result: dict[str, Any]) -> str:
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
    """将运势导出为 UTF-8 TXT/JSON，并返回最终绝对路径。"""
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
