import signal

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QAbstractItemView, QListWidgetItem

from bootedit.ui.orderable_list import OrderableList

# root widget
class Window(QWidget):

    def __init__(self, backend):
        super().__init__()
        self.title = 'QListWidget with Move Up & Down'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200

        self.backend = backend

    def init(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.table = OrderableList()
 
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.table)
        self.setLayout(windowLayout)

        self.reload_table()

    def reload_table(self):
        self.table.clear()

        entries = self.backend.get_uefi_entries()
        for entry in entries:
            self.table.add_movable_item(entry.name)

        # self.list_w.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)

    def moveUp(self):
        print("a")
        currentRow = self.list_w.currentRow()
        currentItem = self.list_w.takeItem(currentRow)
        self.list_w.insertItem(currentRow - 1, currentItem)
        self.list_w.setCurrentRow(currentRow - 1)
        self.list_w.setItemWidget

    def moveDown(self):
        print("b")
        currentRow = self.list_w.currentRow()
        currentItem = self.list_w.takeItem(currentRow)
        self.list_w.insertItem(currentRow + 1, currentItem)
        self.list_w.setCurrentRow(currentRow + 1)
