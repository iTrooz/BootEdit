from PyQt6.QtGui import QStandardItem

from bootedit.backend.entry import UEFIEntry
from bootedit.ui.orderable_table import OrderableTableView

def standard_item_text(text: str) -> QStandardItem:
    item = QStandardItem()
    item.setText(text)
    return item


class EntryTableView(OrderableTableView):

    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)

        self.model().setHorizontalHeaderLabels(["Entry name", "Partition", "Boot file path", ""])

    def add_entry(self, entry: UEFIEntry) -> None:
        entry_name = standard_item_text(entry.name)
        entry_name.entry = entry
        self.add_row([
            entry_name,
            standard_item_text(entry.partition),
            standard_item_text(entry.file_path),
        ])
    
