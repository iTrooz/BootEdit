from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from bootedit.ui.window import Window
from bootedit.ui.partition_select import PartitionSelector
from bootedit.backend.backend import Backend
from bootedit.backend.partition_select import get_partitions

# TODO maybe remove this class altogether
class MyApplication(QApplication):
    """
    
    :attr partition_selector: widget representing the active (shown right now)
        partition selector window. None else
    """
    def __init__(self, *kargs, **kwargs):
        self.backend = Backend()
        self.partition_selector = None
        super().__init__(*kargs, **kwargs)

    def init(self):
        self.init_ui()

    def init_ui(self):
        self.window = Window(self.backend)
        self.window.init()

        self.window.add_button.clicked.connect(lambda: self.add_entry())

    def add_entry(self):
        self.partition_selector = PartitionSelector()
        self.partition_selector.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.partition_selector.set_data(*get_partitions())
        self.partition_selector.show()


    def run(self) -> int:
        self.window.show()
        return self.exec()
