"""用户资料模型。"""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class UserProfile:
    """保存一次查询所需的用户信息。年份未知时 birth_year 为 None。"""

    birth_month: int
    birth_day: int
    birth_year: int | None = None

    def full_birth_date(self) -> date | None:
        """在已知出生年份时返回完整的 :class:`datetime.date`。

        Returns:
            ``birth_year`` 为 ``None`` 时返回 ``None``（只知道月日，无法
            计算已出生天数）；否则返回由年月日拼出的完整日期。
        """
        if self.birth_year is None:
            return None
        return date(self.birth_year, self.birth_month, self.birth_day)

