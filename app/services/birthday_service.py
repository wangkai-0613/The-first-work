"""生日日期计算接口，由日期计算负责人实现。"""

from datetime import date


def days_until_next_birthday(
    month: int, day: int, today: date | None = None
) -> int:
    """返回距离下一次生日的天数；生日当天返回 0。"""
    raise NotImplementedError("由 feature/date-calculation 分支实现")


def days_lived(birth_date: date, today: date | None = None) -> int:
    """返回从出生日期到今天经过的完整天数。"""
    raise NotImplementedError("由 feature/date-calculation 分支实现")

