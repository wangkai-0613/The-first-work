"""GUI 业务编排层，保持 Tkinter 回调简洁且便于无窗口测试。"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from app.models.user_profile import UserProfile
from app.services.birthday_service import days_lived, days_until_next_birthday
from app.services.export_service import export_fortune
from app.services.fortune_service import get_daily_fortune
from app.services.zodiac_service import get_zodiac_sign
from app.utils.date_parser import parse_birth_date


@dataclass(frozen=True)
class QueryResult:
    """一次查询的汇总结果，供 UI 层直接展示或导出。"""

    profile: UserProfile
    countdown: int
    zodiac: str
    fortune: dict[str, Any]
    lived_days: int | None


class BirthdayController:
    """串联各成员提供的固定接口；依赖可注入以支持交互测试。

    UI 层不应直接调用 ``app.services``/``app.utils`` 里的函数，统一经过
    本类，方便在不启动 Tkinter 窗口的情况下用假实现做集成测试。
    """

    def __init__(self, *, parser: Callable = parse_birth_date,
                 countdown_service: Callable = days_until_next_birthday,
                 lived_service: Callable = days_lived,
                 zodiac_service: Callable = get_zodiac_sign,
                 fortune_service: Callable = get_daily_fortune,
                 exporter: Callable = export_fortune) -> None:
        """默认接入各成员的真实实现；测试时可传入替身函数覆盖任意一个。"""
        self._parser = parser
        self._countdown_service = countdown_service
        self._lived_service = lived_service
        self._zodiac_service = zodiac_service
        self._fortune_service = fortune_service
        self._exporter = exporter

    def query(self, text: str) -> QueryResult:
        """解析出生日期文本，依次调用倒计时、星座、运势服务并汇总结果。

        Args:
            text: 用户输入的出生日期文本（``YYYY-MM-DD`` 或 ``MM-DD``）。

        Returns:
            汇总了倒计时、星座、今日运势（以及已出生天数，若年份已知）
            的 :class:`QueryResult`。

        Raises:
            ValueError: 透传 ``parser``/各 service 抛出的校验错误。
        """
        profile = self._parser(text)
        countdown = self._countdown_service(profile.birth_month, profile.birth_day)
        zodiac = self._zodiac_service(profile.birth_month, profile.birth_day)
        fortune = self._fortune_service(zodiac)
        birth_date = profile.full_birth_date()
        lived = self._lived_service(birth_date) if birth_date is not None else None
        return QueryResult(profile, countdown, zodiac, fortune, lived)

    def export(self, result: QueryResult, file_path: str | Path) -> Path:
        """把一次查询里的运势结果导出为文件。

        Args:
            result: :meth:`query` 返回的查询结果。
            file_path: 目标文件路径，交由导出服务处理扩展名和父目录。

        Returns:
            实际写入文件的绝对路径。
        """
        return self._exporter(result.fortune, file_path)
