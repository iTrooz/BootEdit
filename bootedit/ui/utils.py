from PyQt6.QtWidgets import QStyle
from PyQt6 import QtGui
import os


#sp = Standard Pixmap
def get_sp_icon(style, name: str):    
    pixmapi = getattr(QStyle.StandardPixmap, name)
    icon = style.standardIcon(pixmapi)
    return icon

def get_bundled_icon(filename: str):
    return QtGui.QIcon(os.path.join("resources", filename))