import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication

from travel_planner.storage import load_state, get_default_path
from travel_planner.style import apply_theme
from travel_planner.main_window import MainWindow


def main():
    storage_path = get_default_path()

    state = load_state(storage_path)

    app = QApplication(sys.argv)

    apply_theme(app, state.theme)

    window = MainWindow(state, storage_path)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
