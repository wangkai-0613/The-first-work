"""生日助手程序入口。"""

from app.ui.main_window import BirthdayAssistantApp


def main() -> None:
    """创建并运行生日助手主窗口，直到用户关闭程序。"""
    app = BirthdayAssistantApp()
    app.mainloop()


if __name__ == "__main__":
    main()

