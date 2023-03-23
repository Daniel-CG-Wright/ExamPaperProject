# in this file we run the frontend (like a __main__)
from Frontend.MainWindowHandler import MainWindowHandler
from subprocess import call

try:
    from PyQt5.QtWidgets import QApplication
except ImportError:
    # suggested by Oscar
    print("Attempting to install missing module PyQT5")
    call("pip3 install PyQt5")
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindowHandler()
    win.show()

    sys.exit(app.exec())
