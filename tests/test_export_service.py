"""运势 TXT/JSON 导出测试。"""

import json
from pathlib import Path
import tempfile
import unittest

from app.services.export_service import export_fortune


RESULT = {
    "date": "2026-08-18", "zodiac": "狮子座", "overall": 4,
    "love": 3, "study": 5, "health": 4, "lucky_color": "蓝色",
    "lucky_number": 7, "message": "适合整理计划。",
}


class ExportServiceTests(unittest.TestCase):
    def test_export_txt_contains_readable_fields_and_notice(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            exported = export_fortune(RESULT, Path(directory) / "fortune.txt")
            content = exported.read_text(encoding="utf-8")
            self.assertIn("星座：狮子座", content)
            self.assertIn("综合运势：4/5", content)
            self.assertIn("仅供娱乐", content)

    def test_export_json_preserves_unicode_and_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            exported = export_fortune(RESULT, Path(directory) / "fortune.json")
            self.assertEqual(json.loads(exported.read_text(encoding="utf-8")), RESULT)
            self.assertIn("狮子座", exported.read_text(encoding="utf-8"))

    def test_missing_suffix_defaults_to_txt_and_creates_parent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "nested" / "fortune"
            exported = export_fortune(RESULT, target)
            self.assertEqual(exported.suffix, ".txt")
            self.assertTrue(exported.is_file())

    def test_unsupported_extension_raises_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "仅支持"):
            export_fortune(RESULT, "fortune.csv")

    def test_missing_result_field_raises_value_error(self) -> None:
        incomplete = dict(RESULT)
        incomplete.pop("message")
        with self.assertRaisesRegex(ValueError, "缺少字段.*message"):
            export_fortune(incomplete, "fortune.txt")


if __name__ == "__main__":
    unittest.main()