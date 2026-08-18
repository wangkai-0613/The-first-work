"""成员 5 的模块集成交互测试（无需图形显示环境）。"""

from datetime import date
from pathlib import Path
import unittest

from app.models.user_profile import UserProfile
from app.ui.controller import BirthdayController

FORTUNE = {"date": "2026-08-18", "zodiac": "狮子座", "overall": 4,
           "love": 3, "study": 5, "health": 4, "lucky_color": "蓝色",
           "lucky_number": 7, "message": "适合整理计划。"}


class BirthdayControllerTests(unittest.TestCase):
    def make_controller(self, parser=lambda _text: UserProfile(8, 17, 2005), **overrides):
        defaults = {"parser": parser,
                    "countdown_service": lambda month, day: 364,
                    "lived_service": lambda birth_date: 7671,
                    "zodiac_service": lambda month, day: "狮子座",
                    "fortune_service": lambda zodiac: dict(FORTUNE),
                    "exporter": lambda result, path: Path(path)}
        defaults.update(overrides)
        return BirthdayController(**defaults)

    def test_query_integrates_all_services(self) -> None:
        calls = []
        controller = self.make_controller(
            countdown_service=lambda m, d: calls.append(("countdown", m, d)) or 364,
            lived_service=lambda value: calls.append(("lived", value)) or 7671,
            zodiac_service=lambda m, d: calls.append(("zodiac", m, d)) or "狮子座",
            fortune_service=lambda sign: calls.append(("fortune", sign)) or dict(FORTUNE))
        result = controller.query("2005-08-17")
        self.assertEqual((result.countdown, result.lived_days, result.zodiac),
                         (364, 7671, "狮子座"))
        self.assertIn(("lived", date(2005, 8, 17)), calls)

    def test_query_without_year_skips_lived_days(self) -> None:
        controller = self.make_controller(
            parser=lambda _text: UserProfile(8, 17),
            lived_service=lambda _date: self.fail("不应计算出生天数"))
        self.assertIsNone(controller.query("08-17").lived_days)

    def test_invalid_input_error_is_preserved_for_ui(self) -> None:
        def invalid_parser(_text):
            raise ValueError("日期格式不正确")
        with self.assertRaisesRegex(ValueError, "日期格式不正确"):
            self.make_controller(parser=invalid_parser).query("abc")

    def test_export_passes_fortune_and_target_path(self) -> None:
        received = []
        controller = self.make_controller(
            exporter=lambda result, path: received.append((result, Path(path))) or Path(path))
        result = controller.query("2005-08-17")
        exported = controller.export(result, "exports/result.txt")
        self.assertEqual(exported, Path("exports/result.txt"))
        self.assertEqual(received, [(FORTUNE, Path("exports/result.txt"))])


if __name__ == "__main__":
    unittest.main()
