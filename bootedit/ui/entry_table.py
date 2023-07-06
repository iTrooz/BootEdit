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

    def __checkbox_col(self) -> int:
        "checkbox column is hardcoded here"
        return 3
    

    def move_row(self, row_from: int, row_to: int) -> None:
        "Overriden method to re-set the checkbox"

        # get checkbox
        index = self.model().index(row_from, self.__checkbox_col())
        widget = self.indexWidget(index)
        checkbox = widget.checkbox

        # get checked state
        is_checked = checkbox.isChecked()

        # Call the actual move method
        super().move_row(row_from, row_to)

        new_widget, new_checkbox = self.__gen_checkbox()
        
        # re-set checked state
        new_checkbox.setChecked(is_checked)

        # re-set checkbox
        index = self.model().index(row_to, 3)
        self.setIndexWidget(index, new_widget)

    def __gen_checkbox(self) -> Tuple[QtWidgets.QWidget, QtWidgets.QCheckBox]:

        # We embed the checkbox in a widget to be able to center it
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        widget.setLayout(layout)

        checkbox = QtWidgets.QCheckBox()
        # temporary fix to make the checkboxes somewhat visible
        checkbox.setStyleSheet("background-color: gray")
        layout.addWidget(checkbox, 0, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        widget.checkbox = checkbox
        
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
    
