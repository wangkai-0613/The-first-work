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
    profile: UserProfile
    countdown: int
    zodiac: str
    fortune: dict[str, Any]
    lived_days: int | None


class BirthdayController:
    """串联各成员提供的固定接口；依赖可注入以支持交互测试。"""

    def __init__(self, *, parser: Callable = parse_birth_date,
                 countdown_service: Callable = days_until_next_birthday,
                 lived_service: Callable = days_lived,
                 zodiac_service: Callable = get_zodiac_sign,
                 fortune_service: Callable = get_daily_fortune,
                 exporter: Callable = export_fortune) -> None:
        self._parser = parser
        self._countdown_service = countdown_service
        self._lived_service = lived_service
        self._zodiac_service = zodiac_service
        self._fortune_service = fortune_service
        self._exporter = exporter

    def query(self, text: str) -> QueryResult:
        profile = self._parser(text)
        countdown = self._countdown_service(profile.birth_month, profile.birth_day)
        zodiac = self._zodiac_service(profile.birth_month, profile.birth_day)
        fortune = self._fortune_service(zodiac)
        birth_date = profile.full_birth_date()
        lived = self._lived_service(birth_date) if birth_date is not None else None
        return QueryResult(profile, countdown, zodiac, fortune, lived)

    def export(self, result: QueryResult, file_path: str | Path) -> Path:
        return self._exporter(result.fortune, file_path)
