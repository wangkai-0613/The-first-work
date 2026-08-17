"""生日助手程序入口。"""

from app.ui.main_window import BirthdayAssistantApp


def main() -> None:
    app = BirthdayAssistantApp()
    app.mainloop()


if __name__ == "__main__":
    main()

