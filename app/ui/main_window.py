"""生日助手 Tkinter 主窗口。"""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from app.ui.controller import BirthdayController, QueryResult


class BirthdayAssistantApp(tk.Tk):
    """提供输入、查询、结果展示和导出的完整交互流程。"""

    def __init__(self, controller: BirthdayController | None = None) -> None:
        super().__init__()
        self.controller = controller or BirthdayController()
        self.current_result: QueryResult | None = None
        self.title("生日助手")
        self.geometry("760x600")
        self.minsize(680, 540)
        style = ttk.Style(self)
        style.configure("Title.TLabel", font=("Microsoft YaHei UI", 22, "bold"))
        style.configure("Hint.TLabel", foreground="#5f6368")
        style.configure("Value.TLabel", font=("Microsoft YaHei UI", 11, "bold"))
        self._build_ui()

    def _build_ui(self) -> None:
        container = ttk.Frame(self, padding=24)
        container.pack(fill="both", expand=True)
        ttk.Label(container, text="生日助手", style="Title.TLabel").pack()
        ttk.Label(container, text="查询生日倒计时、星座与今日娱乐运势",
                  style="Hint.TLabel").pack(pady=(4, 20))

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

        result_frame = ttk.LabelFrame(container, text="查询结果", padding=16)
        result_frame.pack(fill="both", expand=True, pady=18)
        self.result_vars = {key: tk.StringVar(value=value) for key, value in (
            ("countdown", "—"), ("lived", "—"), ("zodiac", "—"),
            ("scores", "—"), ("lucky", "—"), ("message", "请输入日期后查询。"))}
        rows = (("生日倒计时", "countdown"), ("已出生天数", "lived"),
                ("星座", "zodiac"), ("运势评分", "scores"),
                ("幸运提示", "lucky"), ("今日建议", "message"))
        for row, (label, key) in enumerate(rows):
            ttk.Label(result_frame, text=f"{label}：").grid(
                row=row, column=0, sticky="nw", pady=5)
            ttk.Label(result_frame, textvariable=self.result_vars[key],
                      style="Value.TLabel" if row < 3 else None,
                      wraplength=500, justify="left").grid(
                          row=row, column=1, sticky="nw", pady=5)
        result_frame.columnconfigure(1, weight=1)

        footer = ttk.Frame(container)
        footer.pack(fill="x")
        ttk.Label(footer, text="每日运势仅供娱乐", style="Hint.TLabel").pack(side="left")
        self.export_button = ttk.Button(footer, text="导出结果",
                                        command=self._on_export, state="disabled")
        self.export_button.pack(side="right")
        self.birth_date_entry.focus_set()

    def _on_query(self, _event: tk.Event | None = None) -> None:
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
        fortune = result.fortune
        countdown = ("今天就是生日，生日快乐！" if result.countdown == 0
                     else f"还有 {result.countdown} 天")
        self.result_vars["countdown"].set(countdown)
        self.result_vars["lived"].set(
            f"{result.lived_days} 天" if result.lived_days is not None
            else "未输入年份，暂不计算")
        self.result_vars["zodiac"].set(result.zodiac)
        self.result_vars["scores"].set(
            "综合 {overall}/5　爱情 {love}/5　学习 {study}/5　健康 {health}/5".format(**fortune))
        self.result_vars["lucky"].set(
            f"幸运颜色：{fortune['lucky_color']}　幸运数字：{fortune['lucky_number']}")
        self.result_vars["message"].set(str(fortune["message"]))

    def _on_export(self) -> None:
        if self.current_result is None:
            messagebox.showwarning("导出提示", "请先完成一次查询。", parent=self)
            return
        selected = filedialog.asksaveasfilename(
            parent=self, title="导出运势", initialdir=str(Path.cwd() / "exports"),
            initialfile="birthday_fortune.txt", defaultextension=".txt",
            filetypes=(("文本文件", "*.txt"), ("JSON 文件", "*.json"),
                       ("所有文件", "*.*")))
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
