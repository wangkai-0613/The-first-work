"""星座查询服务。

提供十二星座的名称列表、单点查询与日期范围查询。
实现上仅保存每个星座的起点（月、日），终点由下一个星座的起点推导，
避免重复维护结束边界；查询使用二分查找，时间复杂度为 O(log n)。
"""

from bisect import bisect_right
from datetime import date, timedelta
from typing import Final

# 基准年份：仅用于把“月、日”换算成可比较的“年内第几天”，
# 与业务无关，固定取闰年以保证 2 月 29 日也有合法值。
_REFERENCE_YEAR: Final[int] = 2000

# 十二星座，按下一起点的先后顺序排列，下标与 _STARTS 一一对应。
_SIGNS: Final[tuple[str, ...]] = (
    "水瓶座", "双鱼座", "白羊座", "金牛座", "双子座", "巨蟹座",
    "狮子座", "处女座", "天秤座", "天蝎座", "射手座", "摩羯座",
)

# 各星座起点（月、日），顺序与 _SIGNS 一致，且年内第几天递增。
_STARTS: Final[tuple[tuple[int, int], ...]] = (
    (1, 20), (2, 19), (3, 21), (4, 20), (5, 21), (6, 22),
    (7, 23), (8, 23), (9, 23), (10, 24), (11, 23), (12, 22),
)

# 各星座起点对应的“年内第几天”，预计算供二分查找使用。
_START_DAYS: Final[tuple[int, ...]] = tuple(
    date(_REFERENCE_YEAR, month, day).timetuple().tm_yday
    for month, day in _STARTS
)

# 各月份允许的最大天数；缺省为 31（大月）。
_MAX_DAYS_BY_MONTH: Final[dict[int, int]] = {
    2: 29, 4: 30, 6: 30, 9: 30, 11: 30,
}


def _validate_date(month: int, day: int) -> None:
    """校验月份与日期是否为合法且真实存在的组合。

    Args:
        month: 月份，取值 1～12。
        day: 日期，取值需在该月份的实际天数范围内。

    Raises:
        ValueError: 月份、日期不是整数，或组合不存在。
    """
    if isinstance(month, bool) or isinstance(day, bool) \
            or not isinstance(month, int) or not isinstance(day, int):
        raise ValueError("月份和日期必须是整数。")
    if not 1 <= month <= 12:
        raise ValueError(f"月份必须在1-12之间，当前输入：{month}")
    max_day = _MAX_DAYS_BY_MONTH.get(month, 31)
    if not 1 <= day <= max_day:
        raise ValueError(f"{month}月日期必须在1-{max_day}之间，当前输入：{day}")


def _to_day_of_year(month: int, day: int) -> int:
    """把月、日换算为年内第几天（1～366）。

    Args:
        month: 已通过校验的月份。
        day: 已通过校验的日期。

    Returns:
        该日期在闰年（基准年）中的第几天。
    """
    return date(_REFERENCE_YEAR, month, day).timetuple().tm_yday


def get_zodiac_sign(month: int, day: int) -> str:
    """根据月、日返回对应的中文星座名称。

    对日期先做严格校验，再二分查找星座起点；当输入早于第一个起点时，
    负索引自动回绕到最后一个星座（摩羯座），从而天然处理跨年边界。

    Args:
        month: 月份，取值 1～12。
        day: 日期，取值需在该月份的实际天数范围内。

    Returns:
        对应的星座名称，如 "水瓶座"。

    Raises:
        ValueError: 月份或日期非法。

    时间复杂度:
        O(log n)，n 为星座数量（固定为 12）。
    """
    _validate_date(month, day)
    index = bisect_right(_START_DAYS, _to_day_of_year(month, day))
    return _SIGNS[index - 1]


def get_all_zodiac_signs() -> list[str]:
    """返回全部十二星座名称，按起点先后排序。

    Returns:
        十二星座名称列表，顺序与起点升序一致。
    """
    return list(_SIGNS)


def get_zodiac_date_range(zodiac_name: str) -> tuple[int, int, int, int]:
    """返回指定星座的日期范围（开始月份、开始日期、结束月份、结束日期）。

    终点由下一个星座的起点向前推一天得出；摩羯座跨年时终点落在次年。

    Args:
        zodiac_name: 中文星座名称，如 "水瓶座"。

    Returns:
        四元组 (开始月份, 开始日期, 结束月份, 结束日期)。

    Raises:
        ValueError: 星座名称不存在。
    """
    if zodiac_name not in _SIGNS:
        raise ValueError(f"未找到星座：{zodiac_name}")
    start_month, start_day = _STARTS[_SIGNS.index(zodiac_name)]
    next_month, next_day = _STARTS[(_SIGNS.index(zodiac_name) + 1) % len(_SIGNS)]
    end_date = date(_REFERENCE_YEAR, next_month, next_day)
    if (next_month, next_day) <= (start_month, start_day):
        end_date = date(_REFERENCE_YEAR + 1, next_month, next_day)
    end_date -= timedelta(days=1)
    return start_month, start_day, end_date.month, end_date.day