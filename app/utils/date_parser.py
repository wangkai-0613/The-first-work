"""出生日期输入解析与校验。"""

from datetime import date
import re

from app.models.user_profile import UserProfile


def parse_birth_date(text: str) -> UserProfile:
    """把用户输入的出生日期文本解析成 :class:`UserProfile`。

    支持两种格式：``YYYY-MM-DD``（完整日期，年份已知）和 ``MM-DD``
    （只知道月日，``UserProfile.birth_year`` 会是 ``None``）。前后空白会
    被忽略。

    Args:
        text: 用户输入的原始文本。

    Returns:
        解析出的 ``UserProfile``。

    Raises:
        ValueError: ``text`` 不是字符串、格式不符合上述两种之一、日期
            本身不存在（如 2 月 30 日），或完整日期晚于今天。
    """
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