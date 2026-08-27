"""成员 5 的控制器单元测试（无需图形显示环境）。

覆盖三类情况（见 ``docs/division.md``）：

* 正常情况：各服务按固定接口被正确串联、导出透传结果；
* 边界情况：未输入年份、当天生日、同一星座同日重复查询的缓存行为；
* 错误情况：空输入、解析失败、各服务异常向上传递。
"""

from datetime import date
from pathlib import Path
import unittest

from app.models.user_profile import UserProfile
from app.ui.controller import BirthdayController, FortuneCache

FORTUNE = {"date": "2026-08-18", "zodiac": "狮子座", "overall": 4,
           "love": 3, "study": 5, "health": 4, "lucky_color": "蓝色",
           "lucky_number": 7, "message": "适合整理计划。"}


def _fake_fortune(zodiac, target_date=None):
    """与 ``get_daily_fortune`` 固定接口一致的运势桩。"""
    return dict(FORTUNE)


class BirthdayControllerTests(unittest.TestCase):
    def make_controller(self, parser=lambda _text: UserProfile(8, 17, 2005), **overrides):
        defaults = {"parser": parser,
                    "countdown_service": lambda month, day: 364,
                    "lived_service": lambda birth_date: 7671,
                    "zodiac_service": lambda month, day: "狮子座",
                    "fortune_service": _fake_fortune,
                    "exporter": lambda result, path: Path(path)}
        defaults.update(overrides)
        return BirthdayController(**defaults)

    # ---- 正常情况 ----

    def test_query_integrates_all_services(self) -> None:
        calls = []
        controller = self.make_controller(
            countdown_service=lambda m, d: calls.append(("countdown", m, d)) or 364,
            lived_service=lambda value: calls.append(("lived", value)) or 7671,
            zodiac_service=lambda m, d: calls.append(("zodiac", m, d)) or "狮子座")
        result = controller.query("2005-08-17")
        self.assertEqual((result.countdown, result.lived_days, result.zodiac),
                         (364, 7671, "狮子座"))
        self.assertEqual(result.fortune, FORTUNE)
        self.assertIn(("lived", date(2005, 8, 17)), calls)

    def test_export_passes_fortune_and_target_path(self) -> None:
        received = []
        controller = self.make_controller(
            exporter=lambda result, path: received.append((result, Path(path))) or Path(path))
        result = controller.query("2005-08-17")
        exported = controller.export(result, "exports/result.txt")
        self.assertEqual(exported, Path("exports/result.txt"))
        self.assertEqual(received, [(FORTUNE, Path("exports/result.txt"))])

    def test_export_accepts_path_object(self) -> None:
        controller = self.make_controller()
        result = controller.query("2005-08-17")
        self.assertEqual(controller.export(result, Path("exports/a.json")),
                         Path("exports/a.json"))

    # ---- 边界情况 ----

    def test_query_without_year_skips_lived_days(self) -> None:
        controller = self.make_controller(
            parser=lambda _text: UserProfile(8, 17),
            lived_service=lambda _date: self.fail("不应计算出生天数"))
        self.assertIsNone(controller.query("08-17").lived_days)

    def test_query_on_birthday_returns_zero_countdown(self) -> None:
        controller = self.make_controller(countdown_service=lambda m, d: 0)
        self.assertEqual(controller.query("2005-08-17").countdown, 0)

    def test_repeated_same_day_query_hits_fortune_cache(self) -> None:
        calls = []

        def counting_fortune(zodiac, target_date=None):
            calls.append((zodiac, target_date))
            return dict(FORTUNE)

        controller = self.make_controller(fortune_service=counting_fortune)
        first = controller.query("2005-08-17")
        second = controller.query("2005-08-17")
        self.assertEqual(len(calls), 1)  # 同日同星座只计算一次
        self.assertEqual(first.fortune, second.fortune)

    def test_mutation_of_result_does_not_pollute_cache(self) -> None:
        controller = self.make_controller()
        first = controller.query("2005-08-17")
        first.fortune["overall"] = 999  # 调用方修改返回值不应影响下次查询
        second = controller.query("2005-08-17")
        self.assertEqual(second.fortune["overall"], FORTUNE["overall"])

    # ---- 错误情况 ----

    def test_blank_input_raises_value_error(self) -> None:
        controller = self.make_controller(parser=lambda _text: self.fail("不应调用解析"))
        for text in ("", "   ", "\t\n"):
            with self.assertRaisesRegex(ValueError, "请输入出生日期"):
                controller.query(text)

    def test_invalid_input_error_is_preserved_for_ui(self) -> None:
        def invalid_parser(_text):
            raise ValueError("日期格式不正确")
        with self.assertRaisesRegex(ValueError, "日期格式不正确"):
            self.make_controller(parser=invalid_parser).query("abc")

    def test_service_errors_propagate_from_query(self) -> None:
        def broken_zodiac(month, day):
            raise ValueError("生日的月或日无效。")
        with self.assertRaisesRegex(ValueError, "生日的月或日无效"):
            self.make_controller(zodiac_service=broken_zodiac).query("2005-13-40")

    def test_export_errors_propagate(self) -> None:
        def failing_exporter(result, path):
            raise PermissionError("没有写入权限")
        controller = self.make_controller(exporter=failing_exporter)
        result = controller.query("2005-08-17")
        with self.assertRaises(PermissionError):
            controller.export(result, "exports/result.txt")


class FortuneCacheTests(unittest.TestCase):
    def test_cache_hit_skips_service(self) -> None:
        calls = []

        def counting(zodiac, target_date=None):
            calls.append(zodiac)
            return dict(FORTUNE)

        cache = FortuneCache(counting)
        day = date(2026, 8, 18)
        self.assertEqual(cache.get("狮子座", day), FORTUNE)
        self.assertEqual(cache.get("狮子座", day), FORTUNE)
        self.assertEqual(calls, ["狮子座"])  # 第二次命中缓存

    def test_different_dates_and_signs_are_cached_separately(self) -> None:
        calls = []

        def counting(zodiac, target_date=None):
            calls.append((zodiac, target_date))
            return dict(FORTUNE, zodiac=zodiac)

        cache = FortuneCache(counting)
        cache.get("狮子座", date(2026, 8, 18))
        cache.get("处女座", date(2026, 8, 18))
        cache.get("狮子座", date(2026, 8, 19))  # 跨天不复用旧缓存
        self.assertEqual(len(calls), 3)

    def test_returned_copy_cannot_pollute_cache(self) -> None:
        cache = FortuneCache(lambda zodiac, target_date=None: dict(FORTUNE))
        day = date(2026, 8, 18)
        cache.get("狮子座", day)["message"] = "被篡改"
        self.assertEqual(cache.get("狮子座", day), FORTUNE)

    def test_clear_forces_recomputation(self) -> None:
        calls = []

        def counting(zodiac, target_date=None):
            calls.append(zodiac)
            return dict(FORTUNE)

        cache = FortuneCache(counting)
        day = date(2026, 8, 18)
        cache.get("狮子座", day)
        cache.clear()
        cache.get("狮子座", day)
        self.assertEqual(len(calls), 2)

    def test_service_error_is_not_cached(self) -> None:
        attempts = []

        def flaky(zodiac, target_date=None):
            attempts.append(1)
            if len(attempts) == 1:
                raise ValueError("运势素材读取失败")
            return dict(FORTUNE)

        cache = FortuneCache(flaky)
        day = date(2026, 8, 18)
        with self.assertRaisesRegex(ValueError, "运势素材读取失败"):
            cache.get("狮子座", day)
        # 失败结果不进缓存，恢复后重试即可成功
        self.assertEqual(cache.get("狮子座", day), FORTUNE)
        self.assertEqual(len(attempts), 2)


if __name__ == "__main__":
    unittest.main()
