from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from bootedit.logic.add_uefi_entry import EntryAddLogic

from bootedit.ui.main_window import MainWindow
from bootedit.ui.add_uefi_entry import EntryAddWindow
from bootedit.backend.backend import Backend
from bootedit.backend.add_uefi_entry import get_partitions

# TODO maybe remove this class altogether
class ApplicationLogic(QApplication):
    """
    
    :attr partition_selector: widget representing the active (shown right now)
        partition selector window. None else
    """
    def __init__(self, *kargs, **kwargs):
        self.backend = Backend()
        self.partition_selector = None
        super().__init__(*kargs, **kwargs)

    def init(self):
        self.init_ui()

    def init_ui(self):
        self.window = MainWindow(self.backend)
        self.window.init()

        self.window.add_button.clicked.connect(lambda: self.show_add_entry_window())

    def show_add_entry_window(self):
        self.entry_add = EntryAddLogic()
        self.entry_add.show_window()

    def run(self) -> int:
        self.window.show()
        return self.exec()
