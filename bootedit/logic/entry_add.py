from PyQt6.QtCore import Qt
from bootedit.backend.partition_select import Partition, get_partitions
from bootedit.ui.entry_add import EntryAddWindow


class EntryAddLogic:
    def __init__(self) -> None:
        self.window = EntryAddWindow()
        self.window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.window.set_partitions_data(*get_partitions())
        self.window.add_entry = self.add_entry
        
    def show_window(self) -> None:
        self.window.show()

    def add_entry(self, partition: Partition, rel_path: str) -> None:
        print(f"add entry {partition} {rel_path}")
