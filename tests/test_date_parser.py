"""出生日期输入解析测试。"""

from datetime import date, timedelta
import unittest

from app.utils.date_parser import parse_birth_date


class DateParserTests(unittest.TestCase):
    def test_parse_full_date_and_trim_spaces(self) -> None:
        profile = parse_birth_date(" 2005-08-17 ")
        self.assertEqual((profile.birth_year, profile.birth_month, profile.birth_day),
                         (2005, 8, 17))

    def test_parse_month_day_and_leap_day(self) -> None:
        profile = parse_birth_date("02-29")
        self.assertEqual((profile.birth_year, profile.birth_month, profile.birth_day),
                         (None, 2, 29))

    def test_reject_future_full_date(self) -> None:
        future = date.today() + timedelta(days=1)
        with self.assertRaisesRegex(ValueError, "不能晚于今天"):
            parse_birth_date(future.isoformat())

    def test_reject_invalid_format(self) -> None:
        for value in ("", "2005/08/17", "8-17", "2005-8-17", "abc"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "格式不正确"):
                parse_birth_date(value)

    def test_reject_nonexistent_dates(self) -> None:
        for value in ("02-30", "13-01", "2023-02-29"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_birth_date(value)

    def test_reject_non_text_input(self) -> None:
        with self.assertRaisesRegex(ValueError, "必须是文本"):
            parse_birth_date(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()