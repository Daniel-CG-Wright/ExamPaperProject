# the log window

from PyQt5.QtWidgets import QDialog, QFileDialog
from .Generated.errorloggeneratedui import Ui_OutputLog
import os
from pathlib import Path
from sqlitehandler import SQLiteHandler


class LogHandler(Ui_OutputLog, QDialog):
    def __init__(self, logtext: str, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.logText.setPlainText(logtext)
        self.ConnectSignalSlots()
        self.show()
        self.exec()

    def ConnectSignalSlots(self):
        self.pbClose.clicked.connect(self.close)
        self.pbSQLiteOpen.clicked.connect(self.OpenSQLiteFile)

    def OpenSQLiteFile(self):
        """
        Open the directory containing the SQLite file.
        """
        # get the path to the sqlite file
        sqlitePath = Path(SQLiteHandler().file)
        # get the directory
        sqliteDir = sqlitePath.parent
        # open the directory
        os.startfile(sqliteDir)
