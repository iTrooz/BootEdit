from typing import List, Tuple

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from bootedit.ui import utils

"""
With the help of from:
https://apocalyptech.com/linux/qt/qtableview/ 
https://stackoverflow.com/q/26227885
"""

class MyStyle(QProxyStyle):

    def drawPrimitive(self, element, option, painter, widget=None):
        """
        Draw a line across the entire row rather than just the column
        we're hovering over.  This may not always work depending on global
        style - for instance I think it won't work on OSX.
        """
        if element == QStyle.PrimitiveElement.PE_IndicatorItemViewItemDrop and not option.rect.isNull():
            option_new = QStyleOption(option)
            option_new.rect.setLeft(0)
            if widget:
                option_new.rect.setRight(widget.width())
            option = option_new
        super().drawPrimitive(element, option, painter, widget)

class OrderableTableButtons(QWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        self.row = QHBoxLayout(self)
        self.setLayout(self.row)

        # add move up button
        self.up_button = utils.gen_button(self, bundled_icon="up.svg")
        self.row.addWidget(self.up_button)
        
        # add move down button
        self.down_button = utils.gen_button(self, bundled_icon="down.svg")
        self.row.addWidget(self.down_button)

class OrderableTableView(QTableView):
    
    row_moved = pyqtSignal()
    
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)

        # make the table grow automatically
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

        # Select all all the row when we click on one cell
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        # Only select one row at most
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection) 

        # Let Qt handle the move
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)

        # idk
        self.setDragDropOverwriteMode(False)

        # Set our custom style - this draws the drop indicator across the whole row
        self.setStyle(MyStyle())

        # Set a model
        self.setModel(QStandardItemModel())

    def dropEvent(self, event: QDropEvent) -> None:
        if event.source() != self:
            return
        
        dragged_index = self.selectedIndexes()[0]
        dragged_row = dragged_index.row()

        drop_index = self.indexAt(event.position().toPoint())
        if not drop_index.isValid():
            return
        
        drop_row = 0
        match self.dropIndicatorPosition():
            case QAbstractItemView.DropIndicatorPosition.AboveItem:
                drop_row = drop_index.row()
            case QAbstractItemView.DropIndicatorPosition.BelowItem:
                drop_row = drop_index.row()+1
            case _:
                raise RuntimeError(f"Should not happen ? {self.dropIndicatorPosition()}")
        
        # If moving downwards, account for the dragged row that is going to be deleted
        if dragged_row < drop_row:
            drop_row -= 1
        
        self.move_row(dragged_row, drop_row)

        self.update_item_buttons()

    def model(self, *kargs, **kwargs) -> QStandardItemModel:
        "Just override the return type hint since we already know what our model will be"
        return super().model(*kargs, **kwargs)

    def clear_rows(self):
        self.model().setRowCount(0)

    def __buttons_col(self) -> int:
        return self.model().columnCount() - 1

    def update_item_buttons(self):
        "Hide move up/down buttons on first/last buttons"
        
        # show all buttons
        for row in range(self.model().rowCount()):
            index = self.model().index(row, self.__buttons_col())
            item_widget = self.indexWidget(index)
            item_widget.up_button.show()
            item_widget.down_button.show()

        # hide "move up" button for first widget
        index = self.model().index(0, self.__buttons_col())
        first_item_widget = self.indexWidget(index)
        button = first_item_widget.up_button
        button.hide()

        # let it keep its space so we keep the right alignment
        sp = button.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        button.setSizePolicy(sp)
        
        # same as above but for the "move down" button
        index = self.model().index(self.model().rowCount()-1, self.__buttons_col())
        last_item_widget = self.indexWidget(index)
        button = last_item_widget.down_button
        button.hide()

        sp = button.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        button.setSizePolicy(sp)


    def add_row(self, items: List[QStandardItem], index=-1) -> Tuple[QTableWidgetItem, OrderableTableButtons]:
        if index == -1:
            row = self.model().rowCount()
        else:
            row = index
        self.model().insertRow(row)

        for col, item in enumerate(items):
            # disable drop on items because they don't work for some reason
            item.setDropEnabled(False)
            item.setEditable(False)

            self.model().setItem(row, col, item)

        self.add_row_buttons(row)

        self.update_item_buttons()

        
    def add_row_buttons(self, row: int) -> None:
        col = self.__buttons_col()

        # Create item that will store buttons
        item = QStandardItem()

        # Disable dropping on item directly (see add_row())
        item.setDropEnabled(False)

        # create widget associated with the item
        item_widget = OrderableTableButtons(parent=self)
        item_widget.up_button.clicked.connect(lambda: self.move_up(item))
        item_widget.down_button.clicked.connect(lambda: self.move_down(item))
        
        self.model().setItem(row, col, item)
        self.setIndexWidget(self.model().index(row, col), item_widget)
        
        self.resizeRowsToContents()
        self.resizeColumnsToContents()

    def move_row(self, row_from: int, row_to: int) -> None:
        """
        self.model().moveRow() doesn't work, so I re-implemented it here
        """

        # Check if the destination row is valid
        # Note: we do not add new rows automatically
        if row_to < 0 or row_to >= self.model().rowCount():
            return
        

        # For some reason takeTow() moves the selected index one column to the right
        # (current = selected AFAIK)
        selected = self.currentIndex()

        # move the row
        items = self.model().takeRow(row_from)
        self.model().insertRow(row_to, items)
        
        # add back the buttons
        self.add_row_buttons(row_to)

        # If the current column was the column that was moved, simulate its move
        if selected.row() == row_from:
            selected = self.model().index(row_to, 0)

        # Set back the current index
        self.setCurrentIndex(selected)

        self.row_moved.emit()


    def move_up(self, item: QStandardItem) -> None:
        row = item.row()

        self.move_row(row, row-1)

        self.update_item_buttons()

    def move_down(self, item: QStandardItem) -> None:
        row = item.row()

        self.move_row(row, row+1)

        self.update_item_buttons()
