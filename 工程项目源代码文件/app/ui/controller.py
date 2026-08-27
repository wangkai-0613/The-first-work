"""GUI 业务编排层（第五部分核心）。

本模块是界面与业务服务之间的唯一桥梁：

* :class:`BirthdayController` 按 ``docs/architecture.md`` 的固定接口串联
  日期解析、倒计时、星座、运势与导出五个服务，保持 Tkinter 回调简洁；
* 所有依赖均可通过构造参数注入，便于在无窗口环境下做交互测试；
* 当日运势按“星座 + 日期”缓存，同一天内重复查询同一星座不再重复计算，
  也不产生不同的结果（与“同日同星座结果一致”的约定相互印证）。

重构说明（相对第一版）：

1. 新增 :class:`FortuneCache`，把重复查询的开销从“每次哈希 + 组装字典”
   降为一次字典命中；缓存键含日期，跨天自动失效；
2. 空输入/纯空格输入的校验下沉到 :meth:`BirthdayController.query`，
   界面层只负责提示，业务规则集中在一处且可被单元测试覆盖；
3. 展示文案的拼接移到 :mod:`app.ui.presenter`，本模块不再关心界面文字。
"""

from dataclasses import dataclass
from datetime import date
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
    """一次查询的完整结果，供界面展示与文件导出共用。

    Attributes:
        profile: 解析得到的用户出生日期信息。
        countdown: 距离下一次生日的天数，当天生日为 ``0``。
        zodiac: 中文星座名称。
        fortune: 当日娱乐运势字典（结构见 ``docs/architecture.md``）。
        lived_days: 已出生的完整天数；未输入年份时为 ``None``。
    """

    profile: UserProfile
    countdown: int
    zodiac: str
    fortune: dict[str, Any]
    lived_days: int | None


class FortuneCache:
    """当日运势缓存：同一星座在同一天只计算一次。

    运势由“日期 + 星座”决定（见 ``fortune_service``），因此以
    ``(zodiac, target_date)`` 为键缓存结果即可保证正确；当系统日期变化时，
    旧键不会被再次命中，天然失效，无需手动清理。
    """

    def __init__(self, fortune_service: Callable) -> None:
        """Args:
        fortune_service: 运势服务，签名与
            :func:`app.services.fortune_service.get_daily_fortune` 一致。
        """
        self._fortune_service = fortune_service
        self._store: dict[tuple[str, date], dict[str, Any]] = {}

    def get(self, zodiac: str, target_date: date | None = None) -> dict[str, Any]:
        """返回指定星座在指定日期的运势，命中缓存时不再调用服务。

        Args:
            zodiac: 中文星座名称。
            target_date: 目标日期；为 ``None`` 时使用今天。

        Returns:
            运势字典；缓存中保存的是原始字典的副本，防止调用方修改后
            污染缓存。

        Raises:
            ValueError: 由运势服务抛出的参数或素材错误，原样向上传递。
        """
        day = target_date or date.today()
        key = (zodiac, day)
        cached = self._store.get(key)
        if cached is None:
            cached = dict(self._fortune_service(zodiac, day))
            self._store[key] = cached
        return dict(cached)

    def clear(self) -> None:
        """清空缓存（测试或跨天强制刷新时使用）。"""
        self._store.clear()


class BirthdayController:
    """串联各成员提供的固定接口；依赖可注入以支持交互测试。

    UI 层不应直接调用 ``app.services``/``app.utils`` 里的函数，统一经过
    本类，方便在不启动 Tkinter 窗口的情况下用假实现做集成测试。

    典型用法::

        controller = BirthdayController()
        result = controller.query("2005-08-17")
        controller.export(result, "exports/result.txt")
    """

    def __init__(self, *, parser: Callable = parse_birth_date,
                 countdown_service: Callable = days_until_next_birthday,
                 lived_service: Callable = days_lived,
                 zodiac_service: Callable = get_zodiac_sign,
                 fortune_service: Callable = get_daily_fortune,
                 exporter: Callable = export_fortune) -> None:
        """Args:
            parser: 输入解析服务，默认 :func:`app.utils.date_parser.parse_birth_date`。
            countdown_service: 生日倒计时服务。
            lived_service: 出生天数服务。
            zodiac_service: 星座查询服务。
            fortune_service: 每日运势服务；会先经过 :class:`FortuneCache`。
            exporter: 结果导出服务。
        """
        self._parser = parser
        self._countdown_service = countdown_service
        self._lived_service = lived_service
        self._zodiac_service = zodiac_service
        self._fortune_cache = FortuneCache(fortune_service)
        self._exporter = exporter

    def query(self, text: str) -> QueryResult:
        """解析出生日期文本并一次性完成全部查询。

        Args:
            text: 用户输入的出生日期，支持 ``YYYY-MM-DD`` 或 ``MM-DD``。

        Returns:
            汇总各服务结果的 :class:`QueryResult`。

        Raises:
            ValueError: 输入为空、只含空白字符，或任一服务判定输入非法；
                错误信息为可直接展示给用户的中文说明。
        """
        if not text or not text.strip():
            raise ValueError("请输入出生日期。")
        profile = self._parser(text)
        countdown = self._countdown_service(profile.birth_month, profile.birth_day)
        zodiac = self._zodiac_service(profile.birth_month, profile.birth_day)
        fortune = self._fortune_cache.get(zodiac)
        birth_date = profile.full_birth_date()
        lived = self._lived_service(birth_date) if birth_date is not None else None
        return QueryResult(profile, countdown, zodiac, fortune, lived)

    def export(self, result: QueryResult, file_path: str | Path) -> Path:
        """把查询结果中的运势导出到指定文件。

        Args:
            result: 最近一次 :meth:`query` 的返回值。
            file_path: 目标文件路径（``.txt`` 或 ``.json``）。

        Returns:
            实际写入文件的路径。

        Raises:
            ValueError: 由导出服务抛出的路径或字段错误，原样向上传递。
            OSError: 文件写入失败（例如没有写权限）。
        """
        return self._exporter(result.fortune, file_path)

