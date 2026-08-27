"""成员 5 的主窗口交互测试。

用真实的（隐藏的）Tkinter 窗口验证完整交互流程：输入、查询、展示、导出，
以及各类错误提示。弹窗与文件对话框全部打桩，不会出现任何真实对话框。
若当前环境无法创建窗口（例如无显示器的服务器），整个模块自动跳过。
"""

from pathlib import Path
from unittest import mock
import unittest

from app.models.user_profile import UserProfile
from app.ui.controller import BirthdayController, QueryResult

try:
    import tkinter as tk
    _probe = tk.Tk()
    _probe.destroy()
    _TK_AVAILABLE = True
except Exception:  # pragma: no cover - 无显示环境时跳过
    _TK_AVAILABLE = False

if _TK_AVAILABLE:
    from app.ui.main_window import BirthdayAssistantApp

FORTUNE = {"date": "2026-08-18", "zodiac": "狮子座", "overall": 4,
           "love": 3, "study": 5, "health": 4, "lucky_color": "蓝色",
           "lucky_number": 7, "message": "适合整理计划。"}


def make_stub_controller(**overrides):
    """构造全部服务均为桩的控制器，界面测试不触碰真实业务逻辑。"""
    defaults = {"parser": lambda text: UserProfile(8, 17, 2005),
                "countdown_service": lambda month, day: 9,
                "lived_service": lambda birth_date: 7671,
                "zodiac_service": lambda month, day: "狮子座",
                "fortune_service": lambda zodiac, target_date=None: dict(FORTUNE),
                "exporter": lambda result, path: Path(path)}
    defaults.update(overrides)
    return BirthdayController(**defaults)


@unittest.skipUnless(_TK_AVAILABLE, "当前环境无法创建 Tkinter 窗口")
class MainWindowInteractionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = BirthdayAssistantApp(controller=make_stub_controller())
        self.app.withdraw()  # 隐藏窗口，仅做逻辑测试

    def tearDown(self) -> None:
        self.app.destroy()

    def _query(self, text: str) -> None:
        """填入日期并触发查询回调。"""
        self.app.birth_date_entry.delete(0, "end")
        self.app.birth_date_entry.insert(0, text)
        self.app._on_query()

    # ---- 正常流程 ----

    def test_query_fills_result_area_and_enables_export(self) -> None:
        self._query("2005-08-17")
        self.assertEqual(self.app.result_vars["countdown"].get(), "还有 9 天")
        self.assertEqual(self.app.result_vars["lived"].get(), "7671 天")
        self.assertEqual(self.app.result_vars["zodiac"].get(), "狮子座")
        self.assertEqual(self.app.result_vars["scores"].get(),
                         "综合 4/5　爱情 3/5　学习 5/5　健康 4/5")
        self.assertEqual(self.app.result_vars["lucky"].get(),
                         "幸运颜色：蓝色　幸运数字：7")
        self.assertEqual(self.app.result_vars["message"].get(), "适合整理计划。")
        self.assertEqual(str(self.app.export_button["state"]), "normal")
        self.assertIsInstance(self.app.current_result, QueryResult)

    def test_query_button_restores_after_query(self) -> None:
        self._query("2005-08-17")
        self.assertEqual(str(self.app.query_button["state"]), "normal")

    def test_export_writes_file_and_shows_success(self) -> None:
        self._query("2005-08-17")
        with mock.patch("app.ui.main_window.filedialog") as dialog, \
                mock.patch("app.ui.main_window.messagebox") as box:
            dialog.asksaveasfilename.return_value = "exports/ok.txt"
            self.app._on_export()
        box.showinfo.assert_called_once()
        self.assertIn("exports", str(box.showinfo.call_args.args[1]))

    def test_export_dialog_cancel_keeps_silent(self) -> None:
        self._query("2005-08-17")
        with mock.patch("app.ui.main_window.filedialog") as dialog, \
                mock.patch("app.ui.main_window.messagebox") as box:
            dialog.asksaveasfilename.return_value = ""
            self.app._on_export()
        box.showinfo.assert_not_called()
        box.showerror.assert_not_called()

    # ---- 边界情况 ----

    def test_initial_result_area_shows_placeholders(self) -> None:
        self.assertEqual(self.app.result_vars["countdown"].get(), "—")
        self.assertEqual(self.app.result_vars["message"].get(), "请输入日期后查询。")
        self.assertEqual(str(self.app.export_button["state"]), "disabled")

    def test_export_before_any_query_warns(self) -> None:
        with mock.patch("app.ui.main_window.messagebox") as box:
            self.app._on_export()
        box.showwarning.assert_called_once()

    def test_birthday_today_shows_greeting(self) -> None:
        self.app.controller = make_stub_controller(
            countdown_service=lambda month, day: 0)
        self._query("2005-08-17")
        self.assertEqual(self.app.result_vars["countdown"].get(),
                         "今天就是生日，生日快乐！")

    def test_without_year_shows_hint(self) -> None:
        self.app.controller = make_stub_controller(
            parser=lambda text: UserProfile(8, 17),
            lived_service=lambda birth_date: self.fail("不应计算出生天数"))
        self._query("08-17")
        self.assertEqual(self.app.result_vars["lived"].get(), "未输入年份，暂不计算")

    # ---- 错误情况 ----

    def test_empty_input_warns_without_touching_controller(self) -> None:
        with mock.patch.object(self.app.controller, "query") as query, \
                mock.patch("app.ui.main_window.messagebox") as box:
            self._query("   ")
        query.assert_not_called()
        box.showwarning.assert_called_once()

    def test_invalid_input_shows_error_and_keeps_export_disabled(self) -> None:
        self.app.controller = make_stub_controller(
            parser=lambda text: (_ for _ in ()).throw(ValueError("日期格式不正确")))
        with mock.patch("app.ui.main_window.messagebox") as box:
            self._query("abc")
        box.showerror.assert_called_once()
        self.assertEqual(str(box.showerror.call_args.args[1]), "日期格式不正确")
        self.assertEqual(str(self.app.export_button["state"]), "disabled")
        self.assertEqual(str(self.app.query_button["state"]), "normal")

    def test_unexpected_error_shows_friendly_message(self) -> None:
        self.app.controller = make_stub_controller(
            countdown_service=lambda month, day: (_ for _ in ()).throw(
                RuntimeError("意外错误")))
        with mock.patch("app.ui.main_window.messagebox") as box:
            self._query("2005-08-17")
        box.showerror.assert_called_once()
        self.assertIn("暂时无法完成查询", box.showerror.call_args.args[1])

    def test_export_failure_shows_error(self) -> None:
        self._query("2005-08-17")

        def failing_exporter(result, path):
            raise PermissionError("没有写入权限")

        self.app.controller = make_stub_controller(exporter=failing_exporter)
        self.app.current_result = make_stub_controller().query("2005-08-17")
        with mock.patch("app.ui.main_window.filedialog") as dialog, \
                mock.patch("app.ui.main_window.messagebox") as box:
            dialog.asksaveasfilename.return_value = "exports/fail.txt"
            self.app._on_export()
        box.showerror.assert_called_once()
        self.assertEqual(str(box.showerror.call_args.args[1]), "没有写入权限")


if __name__ == "__main__":
    unittest.main()
