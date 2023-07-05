from PyQt6.QtGui import QStandardItem
from PyQt6 import QtCore, QtWidgets

from bootedit.backend.entry import UEFIEntry
from bootedit.ui.orderable_table import OrderableTableView

def standard_item_text(text: str) -> QStandardItem:
    item = QStandardItem()
    item.setText(text)
    return item


class EntryTableView(OrderableTableView):

    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)

        self.model().setHorizontalHeaderLabels(["Entry name", "Partition", "Boot file path", "Enabled", ""])

    def add_entry(self, entry: UEFIEntry) -> None:
        entry_name = standard_item_text(entry.name)
        entry_name.entry = entry

        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        widget.setLayout(layout)

        self.checkbox = QtWidgets.QCheckBox()
        layout.addWidget(self.checkbox, 0, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.add_row([
            entry_name,
            standard_item_text(entry.partition),
            standard_item_text(entry.file_path),
            widget
        ])
    
