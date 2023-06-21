import sys

from PyQt6.QtWidgets import QApplication

from bootedit.ui_logic.main_window import MainWindowLogic

def run_ui() -> int:
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    app_logic = MainWindowLogic()
    app_logic.show_window()
    
    return app.exec()
