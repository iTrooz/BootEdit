from typing import Tuple

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
        self.row_moved.connect(self.__re_add_checkbox)

    def __re_add_checkbox(self, row_from: int, row_to: int) -> None:
        cb_widget, _ = self.__gen_checkbox()

        # checkbox column is hardcoded here
        index = self.model().index(row_to, 3)
        self.setIndexWidget(index, cb_widget)

    def __gen_checkbox(self) -> Tuple[QtWidgets.QWidget, QtWidgets.QCheckBox]:

        # We embed the checkbox in a widget to be able to center it
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        widget.setLayout(layout)

        checkbox = QtWidgets.QCheckBox()
        layout.addWidget(checkbox, 0, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        
        return widget, checkbox


    def add_entry(self, entry: UEFIEntry) -> None:
        entry_name = standard_item_text(entry.name)
        entry_name.entry = entry

        cb_widget, _ = self.__gen_checkbox()

        self.add_row([
            entry_name,
            standard_item_text(entry.partition),
            standard_item_text(entry.file_path),
            cb_widget
        ])
    
