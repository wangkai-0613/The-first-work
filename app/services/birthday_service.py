"""生日倒计时与出生天数计算。

2 月 29 日出生的用户在非闰年按 2 月 28 日庆祝生日（见
docs/architecture.md 的日期规则），本模块的两个公开函数都遵守这条约定。
"""

from calendar import isleap
from datetime import date


def _validate_month_day(month: int, day: int) -> None:
    """校验月日是否构成一个真实存在的日期（以闰年为基准，允许 2 月 29 日）。

    Raises:
        ValueError: ``month``/``day`` 不是 ``int``（含 ``bool``），或组合
            不出真实存在的日期。
    """
    if (isinstance(month, bool) or isinstance(day, bool)
            or not isinstance(month, int) or not isinstance(day, int)):
        raise ValueError("月份和日期必须是整数。")
    try:
        date(2000, month, day)
    except ValueError as exc:
        raise ValueError("生日的月或日无效。") from exc


def _birthday_in_year(month: int, day: int, year: int) -> date:
    """返回 ``year`` 年里实际庆祝生日的日期。

    非闰年遇到 2 月 29 日会退回到 2 月 28 日，其余情况原样返回。
    """
    if month == 2 and day == 29 and not isleap(year):
        return date(year, 2, 28)
    return date(year, month, day)


def days_until_next_birthday(
    month: int, day: int, today: date | None = None
) -> int:
    """计算距离下一次生日还有多少天。

    Args:
        month: 出生月份（1～12）。
        day: 出生日期，需与 ``month`` 组成真实存在的日期。
        today: 参照的“今天”；为 ``None`` 时使用系统当前日期，测试时可传入
            固定日期。

    Returns:
        距离下一次生日的天数；生日当天返回 ``0``。

    Raises:
        ValueError: ``month``/``day`` 不合法，或 ``today`` 不是日期对象。
    """
    _validate_month_day(month, day)
    current = date.today() if today is None else today
    if not isinstance(current, date):
        raise ValueError("today 必须是日期。")

    birthday = _birthday_in_year(month, day, current.year)
    if birthday < current:
        birthday = _birthday_in_year(month, day, current.year + 1)
    return (birthday - current).days


def days_lived(birth_date: date, today: date | None = None) -> int:
    """计算从出生日期到今天一共经过了多少完整天数。

    Args:
        birth_date: 出生日期，不能晚于 ``today``。
        today: 参照的“今天”；为 ``None`` 时使用系统当前日期。

    Returns:
        ``birth_date`` 到 ``today`` 之间的天数差。

    Raises:
        ValueError: ``birth_date``/``today`` 不是日期对象，或
            ``birth_date`` 晚于 ``today``。
    """
    if not isinstance(birth_date, date):
        raise ValueError("出生日期必须是日期对象。")
    current = date.today() if today is None else today
    if not isinstance(current, date):
        raise ValueError("today 必须是日期。")
    if birth_date > current:
        raise ValueError("出生日期不能晚于今天。")
    return (current - birth_date).days