"""主窗口框架，由 GUI 负责人继续完善。"""

import tkinter as tk
from tkinter import ttk


class BirthdayAssistantApp(tk.Tk):
    """生日助手主窗口。"""

    def __init__(self) -> None:
        super().__init__()
        self.title("生日助手")
        self.geometry("720x480")
        self.minsize(620, 420)
        self._build_ui()

    def _build_ui(self) -> None:
        container = ttk.Frame(self, padding=24)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="生日助手",
            font=("Microsoft YaHei UI", 20, "bold"),
        ).pack(pady=(0, 8))
        ttk.Label(
            container,
            text="项目框架已搭建，请各模块负责人按 docs/division.md 完成功能。",
        ).pack(pady=(0, 20))

        input_frame = ttk.LabelFrame(container, text="出生日期", padding=16)
        input_frame.pack(fill="x")
        ttk.Label(input_frame, text="请输入 YYYY-MM-DD 或 MM-DD：").pack(
            side="left"
        )
        self.birth_date_entry = ttk.Entry(input_frame, width=20)
        self.birth_date_entry.pack(side="left", padx=10)
        ttk.Button(input_frame, text="查询（待实现）", state="disabled").pack(
            side="left"
        )

        result_frame = ttk.LabelFrame(container, text="查询结果", padding=16)
        result_frame.pack(fill="both", expand=True, pady=20)
        ttk.Label(
            result_frame,
            text="生日倒计时、出生天数、星座和每日运势将在这里显示。",
            anchor="center",
        ).pack(fill="both", expand=True)

