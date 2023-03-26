# class for images
from PyQt5.QtGui import QPixmap


class Image:

    def __init__(self, name: str,
                 pixmap: QPixmap,
                 isMarkscheme: bool = False,
                 format: str = "png"):
        self.name = name
        self.pixmap = pixmap
        self.isMarkscheme = isMarkscheme
        self.format = format
