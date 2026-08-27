"""成员 5 的展示格式化层单元测试（纯函数，无需窗口环境）。

覆盖三类情况：正常格式化、边界值（当天生日、未输入年份）、
字段缺失等错误情况。
"""

import unittest

from app.models.user_profile import UserProfile
from app.ui.controller import QueryResult
from app.ui.presenter import (RESULT_KEYS, build_result_view, format_countdown,
                              format_lived_days, format_lucky, format_scores)

FORTUNE = {"date": "2026-08-18", "zodiac": "狮子座", "overall": 4,
           "love": 3, "study": 5, "health": 4, "lucky_color": "蓝色",
           "lucky_number": 7, "message": "适合整理计划。"}


def make_result(countdown=364, lived_days=7671, fortune=None):
    """构造一个用于展示层测试的查询结果。"""
    return QueryResult(
        profile=UserProfile(8, 17, 2005),
        countdown=countdown,
        zodiac="狮子座",
        fortune=dict(FORTUNE) if fortune is None else fortune,
        lived_days=lived_days,
    )


class FormatCountdownTests(unittest.TestCase):
    def test_normal_day(self) -> None:
        self.assertEqual(format_countdown(364), "还有 364 天")
        self.assertEqual(format_countdown(1), "还有 1 天")

    def test_birthday_today(self) -> None:
        self.assertEqual(format_countdown(0), "今天就是生日，生日快乐！")


class FormatLivedDaysTests(unittest.TestCase):
    def test_with_days(self) -> None:
        self.assertEqual(format_lived_days(7671), "7671 天")

    def test_zero_days_on_birth_day(self) -> None:
        self.assertEqual(format_lived_days(0), "0 天")

    def test_without_year(self) -> None:
        self.assertEqual(format_lived_days(None), "未输入年份，暂不计算")


class FormatScoresTests(unittest.TestCase):
    def test_full_scores_line(self) -> None:
        self.assertEqual(format_scores(FORTUNE),
                         "综合 4/5　爱情 3/5　学习 5/5　健康 4/5")

    def test_missing_score_field_raises_key_error(self) -> None:
        incomplete = dict(FORTUNE)
        del incomplete["health"]
        with self.assertRaises(KeyError):
            format_scores(incomplete)


class FormatLuckyTests(unittest.TestCase):
    def test_lucky_line(self) -> None:
        self.assertEqual(format_lucky(FORTUNE), "幸运颜色：蓝色　幸运数字：7")

    def test_missing_lucky_field_raises_key_error(self) -> None:
        incomplete = dict(FORTUNE)
        del incomplete["lucky_color"]
        with self.assertRaises(KeyError):
            format_lucky(incomplete)


class BuildResultViewTests(unittest.TestCase):
    def test_full_result_view(self) -> None:
        view = build_result_view(make_result())
        self.assertEqual(set(view), set(RESULT_KEYS))
        self.assertEqual(view["countdown"], "还有 364 天")
        self.assertEqual(view["lived"], "7671 天")
        self.assertEqual(view["zodiac"], "狮子座")
        self.assertEqual(view["scores"], "综合 4/5　爱情 3/5　学习 5/5　健康 4/5")
        self.assertEqual(view["lucky"], "幸运颜色：蓝色　幸运数字：7")
        self.assertEqual(view["message"], "适合整理计划。")

    def test_boundary_values(self) -> None:
        view = build_result_view(make_result(countdown=0, lived_days=None))
        self.assertEqual(view["countdown"], "今天就是生日，生日快乐！")
        self.assertEqual(view["lived"], "未输入年份，暂不计算")

    def test_non_string_message_is_converted(self) -> None:
        view = build_result_view(make_result(fortune=dict(FORTUNE, message=123)))
        self.assertEqual(view["message"], "123")

    def test_missing_message_field_raises_key_error(self) -> None:
        incomplete = dict(FORTUNE)
        del incomplete["message"]
        with self.assertRaises(KeyError):
            build_result_view(make_result(fortune=incomplete))


if __name__ == "__main__":
    unittest.main()
