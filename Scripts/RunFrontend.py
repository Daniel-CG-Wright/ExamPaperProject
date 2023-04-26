# in this file we run the frontend (like a __main__)
from Frontend.QuestionBankHandler import QuestionBankHandler
from subprocess import call

try:
    from PyQt5.QtWidgets import QApplication
except ImportError:
    # suggested by Oscar
    print("Attempting to install missing module PyQT5")
    call("pip3 install PyQt5")
    from PyQt5.QtWidgets import QApplication

try:
    import docx
except ImportError:
    # suggested by Oscar
    print("Attempting to install missing module docx")
    call("pip3 install python-docx")
    import docx

import sys
import os


if __name__ == "__main__":
    # to compensate for high DPI screens, thanks Kian
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    win = QuestionBankHandler()
    win.show()

    sys.exit(app.exec())
