# in this file we run the frontend (like a __main__)
from Frontend.MainWindowHandler import MainWindowHandler
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindowHandler()
    win.show()

    sys.exit(app.exec())
