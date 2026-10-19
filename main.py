"""Application entry point."""

import sys
from pathlib import Path

from app.config.settings import APP_TITLE
from app.database.connection import initialize_database


APP_ICON = Path(__file__).resolve().parent / "assets" / "domain-lead-manager.svg"


def main() -> None:
    try:
        from PySide6.QtWidgets import QApplication
        from app.ui.main_window import MainWindow
    except ModuleNotFoundError as error:
        if error.name == "PySide6":
            raise SystemExit(
                "PySide6 is not installed. Install it with "
                "`python3 -m pip install PySide6`, then run the application again."
            ) from error
        raise
    initialize_database()
    application = QApplication(sys.argv)
    from PySide6.QtGui import QIcon
    from app.ui.theme import apply_theme, load_theme_mode

    apply_theme(application, load_theme_mode())
    application.setWindowIcon(QIcon(str(APP_ICON)))
    window = MainWindow(title=APP_TITLE)
    window.run()
    sys.exit(application.exec())


if __name__ == "__main__":
    main()
