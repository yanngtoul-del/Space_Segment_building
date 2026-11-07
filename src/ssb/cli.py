"""CLI entry points to launch Student and Teacher applications."""

import sys
from PySide6.QtWidgets import QApplication


def student() -> None:
    from ssb.student_app.main_window import StudentMainWindow
    app = QApplication(sys.argv)
    window = StudentMainWindow()
    window.show()
    sys.exit(app.exec())


def teacher() -> None:
    from ssb.teacher_app.main_window import TeacherMainWindow
    app = QApplication(sys.argv)
    window = TeacherMainWindow()
    window.show()
    sys.exit(app.exec())


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "teacher":
        teacher()
    else:
        student()


if __name__ == "__main__":
    main()
