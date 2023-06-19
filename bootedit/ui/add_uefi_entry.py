from PyQt6.QtWidgets import QWidget

from bootedit.ui.qt.add_uefi_entry_ui import Ui_AddUEFIEntry

class AddUEFIEntryWindow(QWidget, Ui_AddUEFIEntry):
    
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)

        # Small trick to have it setup the current widget
        self.setupUi(self)
