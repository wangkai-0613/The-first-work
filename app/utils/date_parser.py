"""出生日期输入解析接口。"""

from app.models.user_profile import UserProfile


def parse_birth_date(text: str) -> UserProfile:
    """解析 YYYY-MM-DD 或 MM-DD，并对非法输入抛出 ValueError。"""
    raise NotImplementedError("由 feature/date-calculation 分支实现")

