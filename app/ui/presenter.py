"""查询结果的展示格式化层。

本模块把 :class:`~app.ui.controller.QueryResult` 转换为可直接展示的中文文本，
是第五部分（GUI）重构的一部分：界面层（``main_window``）只负责把字符串放进
控件，所有文案拼接集中在这里，做到

1. 展示文案可以脱离 Tkinter 窗口进行单元测试；
2. 界面、导出两处需要相同文案时只维护一份实现；
3. 所有函数都是无副作用的纯函数，便于复用与缓存。
"""

from typing import Any

from app.ui.controller import QueryResult

#: 运势评分的满分（与 ``docs/architecture.md`` 的 1～5 约定一致）。
SCORE_MAX = 5

#: 结果区展示项的键，与 ``main_window`` 中的 ``StringVar`` 一一对应。
RESULT_KEYS = ("countdown", "lived", "zodiac", "scores", "lucky", "message")


def format_countdown(countdown: int) -> str:
    """把倒计时天数格式化为提示文本；当天生日返回祝福语。

    Args:
        countdown: 距离下一次生日的天数，``0`` 表示当天生日。

    Returns:
        ``"今天就是生日，生日快乐！"`` 或 ``"还有 N 天"``。
    """
    if countdown == 0:
        return "今天就是生日，生日快乐！"
    return f"还有 {countdown} 天"


def format_lived_days(lived_days: int | None) -> str:
    """把已出生天数格式化为提示文本；未输入年份时给出说明。

    Args:
        lived_days: 已出生的完整天数；仅输入月日（无年份）时为 ``None``。

    Returns:
        ``"N 天"`` 或 ``"未输入年份，暂不计算"``。
    """
    if lived_days is None:
        return "未输入年份，暂不计算"
    return f"{lived_days} 天"


def format_scores(fortune: dict[str, Any]) -> str:
    """把运势字典中的四项评分拼成一行展示文本。

    Args:
        fortune: :func:`app.services.fortune_service.get_daily_fortune` 的
            返回值，须包含 ``overall``、``love``、``study``、``health``。

    Returns:
        形如 ``"综合 4/5　爱情 3/5　学习 5/5　健康 4/5"`` 的文本。

    Raises:
        KeyError: ``fortune`` 缺少任一评分字段，交由调用方提示用户。
    """
    return "　".join(
        f"{label} {fortune[key]}/{SCORE_MAX}"
        for label, key in (("综合", "overall"), ("爱情", "love"),
                           ("学习", "study"), ("健康", "health"))
    )


def format_lucky(fortune: dict[str, Any]) -> str:
    """把幸运颜色与幸运数字拼成一行展示文本。

    Args:
        fortune: 运势字典，须包含 ``lucky_color`` 与 ``lucky_number``。

    Returns:
        形如 ``"幸运颜色：蓝色　幸运数字：7"`` 的文本。

    Raises:
        KeyError: ``fortune`` 缺少幸运提示字段，交由调用方提示用户。
    """
    return f"幸运颜色：{fortune['lucky_color']}　幸运数字：{fortune['lucky_number']}"


def build_result_view(result: QueryResult) -> dict[str, str]:
    """把一次完整查询结果转换为结果区全部展示项的文本。

    Args:
        result: :class:`~app.ui.controller.BirthdayController.query` 的返回值。

    Returns:
        键与 :data:`RESULT_KEYS` 一致、值为展示文本的字典，可直接写入
        ``main_window`` 的 ``StringVar``。
    """
    fortune = result.fortune
    return {
        "countdown": format_countdown(result.countdown),
        "lived": format_lived_days(result.lived_days),
        "zodiac": result.zodiac,
        "scores": format_scores(fortune),
        "lucky": format_lucky(fortune),
        "message": str(fortune["message"]),
    }
