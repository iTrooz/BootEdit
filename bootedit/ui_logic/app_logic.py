from typing import Optional

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from bootedit.backend.entry import UEFIEntry
from bootedit.backend.fv_ext.delete_boot_entry import delete_boot_entry
from bootedit.backend.get_entries import get_uefi_entries
from bootedit.backend.add_uefi_entry import get_partitions
from bootedit.ui.main_window import MainWindow
from bootedit.ui_logic.add_uefi_entry import AddUEFIEntryLogic

# TODO maybe remove this class altogether
class ApplicationLogic:
    """
    
    :attr partition_selector: widget representing the active (shown right now)
        partition selector window. None else
    """
    def __init__(self):
        self.init_ui()

    def init_ui(self):
        self.main_window = MainWindow()
        self.reload_entries()

        self.main_window.add_button.clicked.connect(lambda: self.show_add_entry_window())

        self.main_window.remove_button.clicked.connect(lambda: self.remove_selected_entry())

    def remove_selected_entry(self) -> None:
        selected_list = self.main_window.table.selectedItems()
        entry: Optional[UEFIEntry] = None
        if len(selected_list) == 1:
            item = selected_list[0]
            if hasattr(item, "entry"):
                entry = item.entry
        
        if entry:
            delete_boot_entry(entry.id)

            self.reload_entries()


    def reload_entries(self) -> None:
        self.main_window.set_entries(get_uefi_entries())

    def show_add_entry_window(self):
        self.add_entry_window = AddUEFIEntryLogic()
        self.add_entry_window.set_partitions_data(*get_partitions())
        self.add_entry_window.show_window()
        self.add_entry_window.close_event = self.on_close_add_entry_window

    def on_close_add_entry_window(self, *args) -> None:
        self.reload_entries()


    def show_window(self):
        self.main_window.show()
