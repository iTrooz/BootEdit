from PyQt6.QtWidgets import QStyle

def get_icon(style, name: str):    
    pixmapi = getattr(QStyle.StandardPixmap, name)
    icon = style.standardIcon(pixmapi)
    return icon