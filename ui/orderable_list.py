from typing import Union

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ui.utils import get_icon

class OrderableListItem(QWidget):

    def __init__(self, parent, label: str) -> None:
        super().__init__(parent)
        
        self.row = QHBoxLayout(self)
        self.setLayout(self.row)
        
        # add text
        self.row.addWidget(QLabel(text=label, parent=self))

        # add move up button
        self.up_button = self.__gen_button__("SP_ArrowUp")
        self.row.addWidget(self.up_button)
        
        # add move down button
        self.down_button = self.__gen_button__("SP_ArrowDown")
        self.row.addWidget(self.down_button)


    def __gen_button__(self, icon_name: str):
        button = QPushButton(parent=self)
        button.setIcon(get_icon(self.style(), icon_name))

        size = button.iconSize().height()*2

        # enforce button size manually because I don't understand how Qt work
        button.setFixedHeight(size)
        button.setFixedWidth(size)

        return button



class OrderableList(QListWidget):

    def add_movable_item(self, label) -> OrderableListItem:
        item = QListWidgetItem(parent=self)
        item_widget = OrderableListItem(parent=self, label=label)

        # enforce heights manually because I don't understand how Qt work
        item_widget.setFixedHeight(item_widget.sizeHint().height())
        item.setSizeHint(item_widget.size())

        self.setItemWidget(item, item_widget)

        return item_widget
