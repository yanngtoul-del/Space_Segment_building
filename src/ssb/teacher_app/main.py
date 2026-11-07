"""Teacher desktop application entry point."""

import sys
from PySide6.QtWidgets import QApplication
from ssb.teacher_app.main_window import TeacherMainWindow


def main() -> None:
    app = QApplication(sys.argv)
    window = TeacherMainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
