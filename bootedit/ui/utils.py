from PyQt6.QtWidgets import QStyle, QPushButton
from PyQt6 import QtGui
import os


#sp = Standard Pixmap
def get_sp_icon(style, name: str):    
    pixmapi = getattr(QStyle.StandardPixmap, name)
    icon = style.standardIcon(pixmapi)
    return icon

def get_bundled_icon(filename: str):
    return QtGui.QIcon(os.path.join("resources", filename))

def gen_button(parent, sp_icon: str = None, bundled_icon: str = None):
    button = QPushButton(parent=parent)
    if sp_icon:
        button.setIcon(get_sp_icon(parent.style(), sp_icon))
    else:
        button.setIcon(get_bundled_icon(bundled_icon))

    size = button.iconSize().height()*2

    # enforce button size manually because I don't understand how Qt work
    button.setFixedHeight(size)
    button.setFixedWidth(size)

    return button