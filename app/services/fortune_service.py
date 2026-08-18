"""基于本地素材生成稳定的每日娱乐运势。"""

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


@lru_cache(maxsize=1)
def _load_materials() -> dict[str, list[Any]]:
    """读取并校验离线运势素材。"""
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


def get_daily_fortune(
    zodiac: str, target_date: date | None = None
) -> dict[str, Any]:
    """返回同一星座、同一天保持一致的每日娱乐运势字典。"""
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
        "overall": digest[0] % 5 + 1,
        "love": digest[1] % 5 + 1,
        "study": digest[2] % 5 + 1,
        "health": digest[3] % 5 + 1,
        "lucky_color": materials["colors"][digest[4] % len(materials["colors"])],
        "lucky_number": materials["numbers"][digest[5] % len(materials["numbers"])],
        "message": materials["messages"][digest[6] % len(materials["messages"])],
    }
