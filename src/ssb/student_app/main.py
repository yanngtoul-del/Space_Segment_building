"""Student desktop application entry point."""

import sys
from PySide6.QtWidgets import QApplication
from ssb.student_app.main_window import StudentMainWindow


def main() -> None:
    app = QApplication(sys.argv)
    window = StudentMainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
