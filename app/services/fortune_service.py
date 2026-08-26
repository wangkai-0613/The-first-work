"""基于本地素材生成稳定的每日娱乐运势。

核心思路：把“日期 + 星座”拼成一个字符串，取其 SHA-256 摘要，再用摘要的
不同字节分别选出各项评分和素材，这样同一天、同一星座永远得到同一个结果
（可复现），不同输入得到的结果又足够分散（看起来随机），且不依赖任何
外部随机数状态，天然满足“稳定随机”的需求。
"""

from datetime import date
from functools import lru_cache
import hashlib
import json
from pathlib import Path
from typing import Any


ZODIAC_SIGNS = (
    "白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座",
    "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座",
)
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "fortune_data.json"

# 评分统一使用 1～5 的整数（见 docs/architecture.md）。
_SCORE_MIN = 1
_SCORE_MAX = 5


@lru_cache(maxsize=1)
def _load_materials() -> dict[str, list[Any]]:
    """读取并校验离线运势素材（结果按进程缓存，避免重复读盘解析）。

    Returns:
        包含 ``messages``、``colors``、``numbers`` 三个非空列表的字典。

    Raises:
        ValueError: 素材文件不存在、不是合法 JSON，或缺少必需字段/字段为空。
    """
    try:
        raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"运势素材读取失败：{exc}") from exc

    materials = raw.get("fortunes") if isinstance(raw, dict) else None
    required = ("messages", "colors", "numbers")
    if not isinstance(materials, dict) or any(
        not isinstance(materials.get(key), list) or not materials[key]
        for key in required
    ):
        raise ValueError("运势素材格式不正确。")
    return materials


def _score_from_byte(byte: int) -> int:
    """把摘要中的一个字节（0～255）映射为 1～5 的整数评分。"""
    return byte % (_SCORE_MAX - _SCORE_MIN + 1) + _SCORE_MIN


def _pick_from_byte(options: list[Any], byte: int) -> Any:
    """用摘要中的一个字节从素材列表里稳定选出一项。"""
    return options[byte % len(options)]


def get_daily_fortune(
    zodiac: str, target_date: date | None = None
) -> dict[str, Any]:
    """返回同一星座、同一天保持一致的每日娱乐运势字典。

    Args:
        zodiac: 中文十二星座名称之一（见 ``ZODIAC_SIGNS``）。
        target_date: 目标日期；为 ``None`` 时使用今天。传入固定日期可用于
            测试或补算历史某天的运势。

    Returns:
        与 ``docs/architecture.md`` 中“运势返回结构”一致的字典，字段为
        ``date``、``zodiac``、``overall``、``love``、``study``、``health``、
        ``lucky_color``、``lucky_number``、``message``。

    Raises:
        ValueError: ``zodiac`` 不是合法的中文星座名称，或 ``target_date``
            不是 ``date`` 对象；也可能透传 ``_load_materials`` 抛出的
            素材格式错误。
    """
    if zodiac not in ZODIAC_SIGNS:
        raise ValueError("星座名称无效，请使用中文十二星座名称。")
    current = date.today() if target_date is None else target_date
    if not isinstance(current, date):
        raise ValueError("target_date 必须是日期对象。")

    digest = hashlib.sha256(f"{current.isoformat()}|{zodiac}".encode("utf-8")).digest()
    materials = _load_materials()
    return {
        "date": current.isoformat(),
        "zodiac": zodiac,
        "overall": _score_from_byte(digest[0]),
        "love": _score_from_byte(digest[1]),
        "study": _score_from_byte(digest[2]),
        "health": _score_from_byte(digest[3]),
        "lucky_color": _pick_from_byte(materials["colors"], digest[4]),
        "lucky_number": _pick_from_byte(materials["numbers"], digest[5]),
        "message": _pick_from_byte(materials["messages"], digest[6]),
    }
