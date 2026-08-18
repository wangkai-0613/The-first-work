"""出生日期输入解析与校验。"""

from datetime import date
import re

from app.models.user_profile import UserProfile


def parse_birth_date(text: str) -> UserProfile:
    """解析 YYYY-MM-DD 或 MM-DD，并对非法输入抛出 ValueError。"""
    if not isinstance(text, str):
        raise ValueError("出生日期必须是文本。")

    value = text.strip()
    full_match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", value)
    short_match = re.fullmatch(r"(\d{2})-(\d{2})", value)
    if full_match:
        year, month, day = map(int, full_match.groups())
        try:
            birth_date = date(year, month, day)
        except ValueError as exc:
            raise ValueError("出生日期不存在，请检查年、月、日。") from exc
        if birth_date > date.today():
            raise ValueError("出生日期不能晚于今天。")
        return UserProfile(birth_month=month, birth_day=day, birth_year=year)

    if short_match:
        month, day = map(int, short_match.groups())
        try:
            date(2000, month, day)
        except ValueError as exc:
            raise ValueError("生日的月或日无效，请输入真实日期。") from exc
        return UserProfile(birth_month=month, birth_day=day)

    raise ValueError("日期格式不正确，请输入 YYYY-MM-DD 或 MM-DD。")