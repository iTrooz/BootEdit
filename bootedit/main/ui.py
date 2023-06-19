import sys

from PyQt6.QtWidgets import QApplication

from bootedit.logic.app_logic import ApplicationLogic

def run_ui() -> int:
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    app_logic = ApplicationLogic()
    app_logic.show_window()
    
    return app.exec()
