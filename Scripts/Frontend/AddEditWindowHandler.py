# handles adding and editing questions
from .Generated.AddEditWindowGenerated import Ui_AddEditQuestions
from PyQt5.QtWidgets import QDialog
from .AddEditPartsHandler import PartHandler
from typing import List
from .Util.question import Part, Question


class AddEditWindowHandler(Ui_AddEditQuestions, QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.ConnectSignalSlots()

        self.currentParts: List[Part] = []
        self.PaperYear: int = -1
        self.PaperComponent: str = ""
        self.PaperLevel: str = ""
        self.currentQuestionText: str = ""
        self.currentQuestionNumber: int = -1
        self.PaperBoard: str = ""
        self.parts: List[Part] = []
        self.currentMarks: int = 0

        self.show()
        self.exec()

    def ConnectSignalSlots(self):
        self.pbAccept.clicked.connect(self.SaveData)
        self.pbCancel.clicked.connect(self.close)
        self.pbAddPart.clicked.connect(self.OpenPartMode)
        self.deYear.dateChanged.connect(self.OnSelectYear)

    def OnSelectYear(self):
        """
        When the year has been changed.
        No validation should be required, it is done in the de.
        """
        self.PaperYear = self.deYear.y()

    def OnSelectComponent(self):
        """
        When the component is changed
        """
        self.PaperComponent = self.cbComponent.currentText()

    def OnSelectLevel(self):
        """
        When the level is changed
        """
        self.PaperLevel = self.cbLevel.currentText()
        self.UpdateComponents()

    def OnSelectBoard(self):
        """
        When the board is changed
        """
        self.PaperBoard = self.cbBoard.currentText()

    def UpdateComponents(self):
        """
        Update the components based on the level
        """
        if self.cbLevel.currentIndex() == 0:
            self.cbComponent.clear()
            self.cbComponent.addItems(["component 1", "component 2"])
        else:
            self.cbComponent.clear()
            self.cbComponent.addItem("component 1")

    def OnSelectQuestionNumber(self):
        """
        When the question number is changed
        """
        self.QuestionNumber = self.sbQNumber.value()

    def OnChangeQuestionText(self):
        """
        When the question text is changed
        """
        self.QuestionText = self.textEdit.toPlainText()

    def OpenPartEditMode(self):
        """
        Open the parts window in edit mode
        """

    def OpenPartMode(self):
        """
        Open the parts window
        """
        handler = PartHandler(parent=self)

    def SaveData(self):
        """
        Saving data.
        """
        # make sure to check there is not another
        # question with the same numebr in the same paper
