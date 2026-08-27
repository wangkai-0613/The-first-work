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

    def test_non_dict_result_raises_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "必须是字典"):
            export_fortune(["not", "a", "dict"], "fortune.txt")  # type: ignore[arg-type]

    def test_invalid_file_path_type_raises_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "文本或 Path"):
            export_fortune(RESULT, 12345)  # type: ignore[arg-type]

    def test_empty_file_name_raises_value_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root_path = Path(Path(directory).anchor)  # 例如 "C:\\" 或 "/"，没有文件名部分
            with self.assertRaisesRegex(ValueError, "有效的导出文件路径"):
                export_fortune(RESULT, root_path)

    def test_extension_case_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            exported = export_fortune(RESULT, Path(directory) / "fortune.JSON")
            self.assertEqual(json.loads(exported.read_text(encoding="utf-8")), RESULT)

    def test_export_overwrites_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "fortune.txt"
            target.write_text("旧内容", encoding="utf-8")
            exported = export_fortune(RESULT, target)
            self.assertIn("星座：狮子座", exported.read_text(encoding="utf-8"))
            self.assertNotIn("旧内容", exported.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()