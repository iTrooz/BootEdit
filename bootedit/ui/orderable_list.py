from typing import Tuple

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QAbstractItemView

from bootedit.ui import utils

class OrderableListItem(QWidget):

    def __init__(self, parent, label: str) -> None:
        super().__init__(parent)
        
        self.row = QHBoxLayout(self)
        self.setLayout(self.row)
        
        # add text
        self.w_label = QLabel(text=label, parent=self)
        self.row.addWidget(self.w_label)

        # add move up button
        self.up_button = utils.gen_button(self, bundled_icon="up.svg")
        self.row.addWidget(self.up_button)
        
        # add move down button
        self.down_button = utils.gen_button(self, bundled_icon="down.svg")
        self.row.addWidget(self.down_button)
    
    def text(self):
        return self.w_label.text()



class OrderableList(QListWidget):

    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)

        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)

        self.model().rowsMoved.connect(self.update_item_buttons)

    def update_item_buttons(self):
        for row in range(self.count()):
            item_widget = self.itemWidget(self.item(row))
            item_widget.up_button.show()
            item_widget.down_button.show()

        # hide "move up" button for first widget
        first_item_widget = self.itemWidget(self.item(0))
        first_item_widget.up_button.hide()
        button = first_item_widget.up_button

        # let it keep its space so we keep the right alignment
        sp = button.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        button.setSizePolicy(sp)
        
        # same as above but for the "move down" button
        last_item_widget = self.itemWidget(self.item(self.count()-1))
        button = last_item_widget.down_button
        button.hide()

        sp = button.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        button.setSizePolicy(sp)


    def add_movable_item(self, label, index=-1) -> Tuple[QListWidgetItem, OrderableListItem]:
        item = QListWidgetItem(parent=None)
        
        if index == -1:
            # insert last
            self.insertItem(self.count(), item)
        else:
            self.insertItem(index, item)

        # create widget associated with this item
        item_widget = OrderableListItem(parent=self, label=label)
        item_widget.up_button.clicked.connect(lambda: self.move_up(item, item_widget))
        item_widget.down_button.clicked.connect(lambda: self.move_down(item, item_widget))

        # associate it to the item
        self.setItemWidget(item, item_widget)

        # enforce heights manually because I don't understand how Qt work
        item_widget.setFixedHeight(item_widget.sizeHint().height())
        item.setSizeHint(item_widget.size())

        self.update_item_buttons()
        
        return item, item_widget


    # TODO keep entry associated to item when moving

    def move_up(self, item, item_widget):
        label = item_widget.text()
        row = self.row(item)

        # this should also delete the item_widget object, so accessing it after this will crash the program
        self.takeItem(row)

        self.add_movable_item(label=label, index=row-1)

    def move_down(self, item, item_widget):
        label = item_widget.text()
        row = self.row(item)

        # this should also delete the item_widget object, so accessing it after this will crash the program
        self.takeItem(row)
        self.add_movable_item(label=label, index=row+1)
