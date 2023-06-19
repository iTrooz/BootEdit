from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from bootedit.logic.add_uefi_entry import AddUEFIEntryLogic

from bootedit.ui.main_window import MainWindow
from bootedit.ui.add_uefi_entry import AddUEFIEntryWindow
from bootedit.backend.backend import Backend
from bootedit.backend.add_uefi_entry import get_partitions

# TODO maybe remove this class altogether
class ApplicationLogic:
    """
    
    :attr partition_selector: widget representing the active (shown right now)
        partition selector window. None else
    """
    def __init__(self):
        self.backend = Backend()
        self.partition_selector = None

    def init(self):
        self.init_ui()

    def init_ui(self):
        self.window = MainWindow()
        self.window.init()
        self.reload_entries()

        self.window.add_button.clicked.connect(lambda: self.show_add_entry_window())

    def reload_entries(self) -> None:
        self.window.set_entries(self.backend.get_uefi_entries())

    def show_add_entry_window(self):
        self.entry_add = AddUEFIEntryLogic()
        self.entry_add.show_window()
        self.entry_add.on_close_evt = self.on_close_add_entry_window

    def on_close_add_entry_window(self) -> None:
        self.reload_entries()


    def show_window(self):
        self.window.show()
