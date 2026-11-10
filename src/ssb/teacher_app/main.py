"""Teacher desktop application entry point."""

import sys
from PySide6.QtWidgets import QApplication
from ssb.teacher_app.main_window import TeacherMainWindow


def main() -> None:
    if "--version" in sys.argv:
        print("Space Segment Builder — Teacher Edition v0.1.0")
        return
    if "--help" in sys.argv:
        print("Usage: SpaceSegmentBuilder-Teacher [options]")
        print("Options:")
        print("  --version      Afficher la version")
        print("  --test-launch  Démarrer, initialiser l'interface et quitter")
        return

    app = QApplication(sys.argv)
    window = TeacherMainWindow()

    if "--test-launch" in sys.argv:
        print("TeacherMainWindow initialized successfully.")
        return

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
