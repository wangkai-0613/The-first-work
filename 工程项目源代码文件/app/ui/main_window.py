"""生日助手 Tkinter 主窗口（第五部分界面层）。

界面层遵循 ``docs/architecture.md`` 的分层约定：

* 只负责收集输入、触发控制器、展示结果，不实现任何日期或星座算法；
* 业务编排交给 :class:`app.ui.controller.BirthdayController`；
* 展示文案统一由 :mod:`app.ui.presenter` 生成，窗口只做控件装配；
* 所有错误通过消息框给出中文提示，不向用户暴露异常堆栈。
"""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from app.ui.controller import BirthdayController, QueryResult
from app.ui.presenter import RESULT_KEYS, build_result_view

#: 主窗口初始尺寸与最小尺寸（宽 x 高，单位像素）。
WINDOW_SIZE = "760x600"
WINDOW_MIN_SIZE = (680, 540)

#: 界面统一使用的中文字体名称。
FONT_FAMILY = "Microsoft YaHei UI"

#: 导出对话框的默认文件名与支持的文件类型。
EXPORT_DEFAULT_NAME = "birthday_fortune.txt"
EXPORT_FILE_TYPES = (("文本文件", "*.txt"), ("JSON 文件", "*.json"),
                     ("所有文件", "*.*"))

#: 结果区的行定义：(中文标签, 展示项键)，顺序即界面显示顺序。
RESULT_ROWS = (("生日倒计时", "countdown"), ("已出生天数", "lived"),
               ("星座", "zodiac"), ("运势评分", "scores"),
               ("幸运提示", "lucky"), ("今日建议", "message"))


class BirthdayAssistantApp(tk.Tk):
    """提供输入、查询、结果展示和导出的完整交互流程。"""

    def __init__(self, controller: BirthdayController | None = None) -> None:
        """构建主窗口并接入业务逻辑。

        Args:
            controller: 用于查询和导出的控制器；默认创建接入真实服务的
                :class:`BirthdayController`，测试时可替换为假实现。

        """
        super().__init__()
        self.controller = controller or BirthdayController()
        self.current_result: QueryResult | None = None
        self.title("生日助手")
        self.geometry(WINDOW_SIZE)
        self.minsize(*WINDOW_MIN_SIZE)
        self._configure_styles()
        self._build_ui()

    def _configure_styles(self) -> None:
        """集中配置 ttk 样式，避免散落在控件创建代码里。"""
        style = ttk.Style(self)
        style.configure("Title.TLabel", font=(FONT_FAMILY, 22, "bold"))
        style.configure("Hint.TLabel", foreground="#5f6368")
        style.configure("Value.TLabel", font=(FONT_FAMILY, 11, "bold"))

    def _build_ui(self) -> None:
        """搭建标题、输入表单、结果区和底部操作条。"""
        container = ttk.Frame(self, padding=24)
        container.pack(fill="both", expand=True)
        ttk.Label(container, text="生日助手", style="Title.TLabel").pack()
        ttk.Label(container, text="查询生日倒计时、星座与今日娱乐运势",
                  style="Hint.TLabel").pack(pady=(4, 20))
        self._build_form(container)
        self._build_result_area(container)
        self._build_footer(container)
        self.birth_date_entry.focus_set()

    def _build_form(self, container: ttk.Frame) -> None:
        """搭建出生日期输入表单。"""
        form = ttk.LabelFrame(container, text="出生日期", padding=16)
        form.pack(fill="x")
        ttk.Label(form, text="日期：").grid(row=0, column=0, sticky="w")
        self.birth_date_entry = ttk.Entry(form, width=28)
        self.birth_date_entry.grid(row=0, column=1, padx=10, sticky="ew")
        self.birth_date_entry.bind("<Return>", self._on_query)
        self.query_button = ttk.Button(form, text="查询", command=self._on_query)
        self.query_button.grid(row=0, column=2)
        ttk.Label(form, text="支持 YYYY-MM-DD 或 MM-DD，例如 2005-08-17 或 08-17",
                  style="Hint.TLabel").grid(row=1, column=1, columnspan=2,
                                             pady=(8, 0), sticky="w")
        form.columnconfigure(1, weight=1)

    def _build_result_area(self, container: ttk.Frame) -> None:
        """按 :data:`RESULT_ROWS` 生成结果展示行，文案由 presenter 填充。"""
        result_frame = ttk.LabelFrame(container, text="查询结果", padding=16)
        result_frame.pack(fill="both", expand=True, pady=18)
        defaults = {"message": "请输入日期后查询。"}
        self.result_vars = {key: tk.StringVar(value=defaults.get(key, "—"))
                            for key in RESULT_KEYS}
        for row, (label, key) in enumerate(RESULT_ROWS):
            ttk.Label(result_frame, text=f"{label}：").grid(
                row=row, column=0, sticky="nw", pady=5)
            ttk.Label(result_frame, textvariable=self.result_vars[key],
                      style="Value.TLabel" if row < 3 else None,
                      wraplength=500, justify="left").grid(
                          row=row, column=1, sticky="nw", pady=5)
        result_frame.columnconfigure(1, weight=1)

    def _build_footer(self, container: ttk.Frame) -> None:
        """搭建底部娱乐提示与导出按钮。"""
        footer = ttk.Frame(container)
        footer.pack(fill="x")
        ttk.Label(footer, text="每日运势仅供娱乐", style="Hint.TLabel").pack(side="left")
        self.export_button = ttk.Button(footer, text="导出结果",
                                        command=self._on_export, state="disabled")
        self.export_button.pack(side="right")

    def _on_query(self, _event: tk.Event | None = None) -> None:
        """查询按钮/回车回调：调用控制器并把结果或错误展示给用户。"""
        text = self.birth_date_entry.get()
        if not text.strip():
            messagebox.showwarning("输入提示", "请输入出生日期。", parent=self)
            self.birth_date_entry.focus_set()
            return
        self.query_button.configure(state="disabled")
        try:
            result = self.controller.query(text)
        except (ValueError, NotImplementedError) as exc:
            messagebox.showerror("查询失败", str(exc), parent=self)
        except Exception as exc:
            messagebox.showerror("查询失败", f"暂时无法完成查询：{exc}", parent=self)
        else:
            self.current_result = result
            self._show_result(result)
            self.export_button.configure(state="normal")
        finally:
            self.query_button.configure(state="normal")

    def _show_result(self, result: QueryResult) -> None:
        """把查询结果写入结果区控件；文案全部由 presenter 生成。"""
        for key, text in build_result_view(result).items():
            self.result_vars[key].set(text)

    def _on_export(self) -> None:
        """导出按钮回调：选择路径后调用控制器导出并提示结果。"""
        if self.current_result is None:
            messagebox.showwarning("导出提示", "请先完成一次查询。", parent=self)
            return
        selected = filedialog.asksaveasfilename(
            parent=self, title="导出运势", initialdir=str(Path.cwd() / "exports"),
            initialfile=EXPORT_DEFAULT_NAME, defaultextension=".txt",
            filetypes=EXPORT_FILE_TYPES)
        if not selected:
            return
        try:
            exported_path = self.controller.export(self.current_result, selected)
        except (OSError, ValueError, NotImplementedError) as exc:
            messagebox.showerror("导出失败", str(exc), parent=self)
        except Exception as exc:
            messagebox.showerror("导出失败", f"文件无法导出：{exc}", parent=self)
        else:
            messagebox.showinfo("导出成功", f"结果已保存至：\n{exported_path}", parent=self)

