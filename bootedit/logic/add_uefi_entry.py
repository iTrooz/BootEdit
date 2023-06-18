from PyQt6.QtCore import Qt
from bootedit.backend.add_uefi_entry import Partition, get_partitions
from bootedit.ui.add_uefi_entry import AddUEFIEntryWindow


class AddUEFIEntryLogic:
    def __init__(self) -> None:
        self.window = AddUEFIEntryWindow()
        self.window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.window.set_partitions_data(*get_partitions())
        self.window.add_uefi_entry_callback = self.add_uefi_entry
        
    def show_window(self) -> None:
        self.window.show()

    def add_uefi_entry(self, partition: Partition, rel_file_path: str, entry_name: str) -> None:
        print(f"add entry {partition} {rel_file_path} {entry_name}")
