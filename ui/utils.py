from PyQt5.QtWidgets import QStyle

def get_icon(style, name: str):    
    pixmapi = getattr(QStyle, name)
    icon = style.standardIcon(pixmapi)
    return icon