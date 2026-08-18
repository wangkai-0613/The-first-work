"""生日倒计时与出生天数计算。"""

from calendar import isleap
from datetime import date


def _validate_month_day(month: int, day: int) -> None:
    """校验月日；以闰年为基准允许 2 月 29 日。"""
    if (isinstance(month, bool) or isinstance(day, bool)
            or not isinstance(month, int) or not isinstance(day, int)):
        raise ValueError("月份和日期必须是整数。")
    try:
        date(2000, month, day)
    except ValueError as exc:
        raise ValueError("生日的月或日无效。") from exc


def _birthday_in_year(month: int, day: int, year: int) -> date:
    """返回指定年份的庆祝日期，处理 2 月 29 日规则。"""
    if month == 2 and day == 29 and not isleap(year):
        return date(year, 2, 28)
    return date(year, month, day)


def days_until_next_birthday(
    month: int, day: int, today: date | None = None
) -> int:
    """返回距离下一次生日的天数；生日当天返回 0。"""
    _validate_month_day(month, day)
    current = date.today() if today is None else today
    if not isinstance(current, date):
        raise ValueError("today 必须是日期。")

    birthday = _birthday_in_year(month, day, current.year)
    if birthday < current:
        birthday = _birthday_in_year(month, day, current.year + 1)
    return (birthday - current).days


def days_lived(birth_date: date, today: date | None = None) -> int:
    """返回从出生日期到今天经过的完整天数。"""
    if not isinstance(birth_date, date):
        raise ValueError("出生日期必须是日期对象。")
    current = date.today() if today is None else today
    if not isinstance(current, date):
        raise ValueError("today 必须是日期。")
    if birth_date > current:
        raise ValueError("出生日期不能晚于今天。")
    return (current - birth_date).days