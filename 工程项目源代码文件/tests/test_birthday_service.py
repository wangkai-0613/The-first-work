"""生日倒计时和出生天数测试。"""

from datetime import date
import unittest

from app.services.birthday_service import days_lived, days_until_next_birthday


class BirthdayCountdownTests(unittest.TestCase):
    def test_birthday_today_returns_zero(self) -> None:
        self.assertEqual(days_until_next_birthday(8, 17, date(2026, 8, 17)), 0)

    def test_birthday_later_this_year(self) -> None:
        self.assertEqual(days_until_next_birthday(8, 20, date(2026, 8, 17)), 3)

    def test_birthday_rolls_to_next_year(self) -> None:
        self.assertEqual(days_until_next_birthday(1, 1, date(2026, 12, 31)), 1)

    def test_leap_day_uses_february_28_in_non_leap_year(self) -> None:
        self.assertEqual(days_until_next_birthday(2, 29, date(2025, 2, 27)), 1)
        self.assertEqual(days_until_next_birthday(2, 29, date(2025, 2, 28)), 0)

    def test_leap_day_uses_february_29_in_leap_year(self) -> None:
        self.assertEqual(days_until_next_birthday(2, 29, date(2024, 2, 28)), 1)

    def test_invalid_month_day_raises_value_error(self) -> None:
        for month, day in ((0, 1), (13, 1), (2, 30), (4, 31)):
            with self.subTest(month=month, day=day), self.assertRaisesRegex(ValueError, "无效"):
                days_until_next_birthday(month, day, date(2026, 1, 1))


class DaysLivedTests(unittest.TestCase):
    def test_days_lived_uses_date_difference(self) -> None:
        self.assertEqual(days_lived(date(2000, 1, 1), date(2000, 1, 2)), 1)

    def test_birth_date_today_returns_zero(self) -> None:
        self.assertEqual(days_lived(date(2026, 8, 18), date(2026, 8, 18)), 0)

    def test_leap_year_is_counted(self) -> None:
        self.assertEqual(days_lived(date(2024, 2, 28), date(2024, 3, 1)), 2)

    def test_future_birth_date_raises_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "不能晚于今天"):
            days_lived(date(2026, 8, 19), date(2026, 8, 18))

    def test_invalid_types_raise_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "日期对象"):
            days_lived("2000-01-01")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()