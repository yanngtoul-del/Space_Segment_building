"""Student desktop application entry point."""

import sys
from PySide6.QtWidgets import QApplication
from ssb.student_app.main_window import StudentMainWindow


def main() -> None:
    if "--version" in sys.argv:
        print("Space Segment Builder — Student Edition v0.1.0")
        return
    if "--help" in sys.argv:
        print("Usage: SpaceSegmentBuilder-Student [options]")
        print("Options:")
        print("  --version      Afficher la version")
        print("  --test-launch  Démarrer, initialiser l'interface et quitter")
        return

    app = QApplication(sys.argv)
    window = StudentMainWindow()

    if "--test-launch" in sys.argv:
        print("StudentMainWindow initialized successfully.")
        return

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
