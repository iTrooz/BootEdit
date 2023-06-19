from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from bootedit.backend.entry import UEFIEntry
from bootedit.ui.orderable_list import OrderableList
from bootedit.ui import utils

# root widget
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Boot entries editor (UEFI)")
 
        windowLayout = QVBoxLayout()
        self.setLayout(windowLayout)
 
        header = QHBoxLayout()
        windowLayout.addLayout(header)

        # add "add" button
        self.add_button = utils.gen_button(self, bundled_icon="add.svg")
        header.addWidget(self.add_button)
        
        # add "remove" button
        self.remove_button = utils.gen_button(self, bundled_icon="remove.svg")
        header.addWidget(self.remove_button)

        # add "edit" button
        self.edit_button = utils.gen_button(self, bundled_icon="edit.svg")
        header.addWidget(self.edit_button)

        # put the buttons to the left by adding a spacing to the right
        header.addStretch()

        self.table = OrderableList()
        windowLayout.addWidget(self.table)

    def set_entries(self, entries: list[UEFIEntry]) -> None:
        self.table.clear()

        for entry in entries:
            self.table.add_movable_item(entry.name)

