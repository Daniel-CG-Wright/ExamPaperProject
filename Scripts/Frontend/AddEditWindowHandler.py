# handles adding and editing questions
from .Generated.AddEditWindowGenerated import Ui_AddEditQuestions
from PyQt5.QtWidgets import QDialog


class AddEditWindowHandler(Ui_AddEditQuestions, QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.ConnectSignalSlots()
        self.show()
        self.exec()

    def ConnectSignalSlots(self):
        self.pbAccept.clicked.connect(self.SaveData)
        self.pbCancel.clicked.connect(self.close())

    def SaveData(self):
        """
        Saving data.
        """