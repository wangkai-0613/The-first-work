"""每日稳定运势服务测试。"""

from datetime import date
from pathlib import Path
import tempfile
import unittest

from app.services import fortune_service
from app.services.fortune_service import get_daily_fortune


class FortuneServiceTests(unittest.TestCase):
    def test_result_has_stable_schema_and_ranges(self) -> None:
        result = get_daily_fortune("狮子座", date(2026, 8, 18))
        self.assertEqual(set(result), {
            "date", "zodiac", "overall", "love", "study", "health",
            "lucky_color", "lucky_number", "message",
        })
        self.assertEqual((result["date"], result["zodiac"]), ("2026-08-18", "狮子座"))
        for field in ("overall", "love", "study", "health"):
            self.assertIn(result[field], range(1, 6))

    def test_same_date_and_zodiac_are_deterministic(self) -> None:
        first = get_daily_fortune("水瓶座", date(2026, 1, 20))
        second = get_daily_fortune("水瓶座", date(2026, 1, 20))
        self.assertEqual(first, second)

    def test_different_inputs_change_digest_based_result(self) -> None:
        first = get_daily_fortune("白羊座", date(2026, 3, 21))
        second = get_daily_fortune("金牛座", date(2026, 3, 21))
        third = get_daily_fortune("白羊座", date(2026, 3, 22))
        self.assertNotEqual(first, second)
        self.assertNotEqual(first, third)

    def test_all_twelve_zodiac_signs_are_supported(self) -> None:
        signs = ("白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座",
                 "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座")
        self.assertEqual(len([get_daily_fortune(sign, date(2026, 1, 1)) for sign in signs]), 12)

    def test_invalid_zodiac_and_date_raise_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "星座名称无效"):
            get_daily_fortune("狮子")
        with self.assertRaisesRegex(ValueError, "日期对象"):
            get_daily_fortune("狮子座", "2026-08-18")  # type: ignore[arg-type]


class LoadMaterialsTests(unittest.TestCase):
    """针对离线素材文件本身损坏/缺失场景的边界测试。"""

    def setUp(self) -> None:
        self._original_data_file = fortune_service.DATA_FILE
        fortune_service._load_materials.cache_clear()

    def tearDown(self) -> None:
        fortune_service.DATA_FILE = self._original_data_file
        fortune_service._load_materials.cache_clear()

    def test_missing_file_raises_value_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fortune_service.DATA_FILE = Path(directory) / "missing.json"
            with self.assertRaisesRegex(ValueError, "运势素材读取失败"):
                fortune_service._load_materials()

    def test_invalid_json_raises_value_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data_file = Path(directory) / "broken.json"
            data_file.write_text("{not valid json", encoding="utf-8")
            fortune_service.DATA_FILE = data_file
            with self.assertRaisesRegex(ValueError, "运势素材读取失败"):
                fortune_service._load_materials()

    def test_missing_required_key_raises_value_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data_file = Path(directory) / "incomplete.json"
            data_file.write_text(
                '{"fortunes": {"messages": ["m"], "colors": ["红色"]}}',
                encoding="utf-8",
            )
            fortune_service.DATA_FILE = data_file
            with self.assertRaisesRegex(ValueError, "格式不正确"):
                fortune_service._load_materials()

    def test_empty_list_value_raises_value_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data_file = Path(directory) / "empty_list.json"
            data_file.write_text(
                '{"fortunes": {"messages": [], "colors": ["红色"], "numbers": [1]}}',
                encoding="utf-8",
            )
            fortune_service.DATA_FILE = data_file
            with self.assertRaisesRegex(ValueError, "格式不正确"):
                fortune_service._load_materials()


if __name__ == "__main__":
    unittest.main()