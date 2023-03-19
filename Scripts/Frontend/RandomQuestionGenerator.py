from PyQt5.QtWidgets import QDialog, QComboBox, QTableWidgetItem
from .Generated.RandomQuestionGenerated import Ui_RandomQuestionDialog
from .Util import QuestionPartFunctionHelpers as funchelpers
from sqlitehandler import SQLiteHandler
from .Util.CriteriaClass import CriteriaStruct, TOPICKEYWORDS
from typing import List, Set
from OutputWindowHandler import OutputWindowHandler
# handles the generation of random questions


class RandomQuestionHandler(Ui_RandomQuestionDialog, QDialog):

    def __init__(self, parent=None):
        """
        For generating random questions
        """
        super().__init__(parent)
        self.setupUi(self)
        self.SQLSocket = SQLiteHandler()
        self.currentQuestionID: str = ""
        self.selectedTopics: Set = set()
        self.currentCombobox: QComboBox = ""
        # question pool is for all the potential random
        # question ids that can be picked.
        self.currentQuestionPool: Set[str] = []

    def ConnectSignalSlots(self):
        self.pbGenerate.clicked.connect(self.GenerateQuestion)
        self.pbViewMarkscheme.clicked.connect(self.ShowMarkscheme)
        self.cbLevel.currentTextChanged.connect(self.OnLevelChange)
        self.twTopics.cellDoubleClicked.connect(self.OnDeleteRowInTopics)
        self.pbResetTopics.clicked.connect(self.ActivateConfirmation)
        self.pbConfirmReset.clicked.connect(self.ResetTable)

    def GenerateQuestionPool(self):
        """
        Generates the question pool to take the next random question
        from and saves in self.currentQuestionPool
        """
        criteria = self.GetQuestionCriteria()

    def ActivateConfirmation(self):
        """
        Make user confirm resetting the table
        """
        self.pbConfirmReset.toggle()
        if self.pbConfirmReset.isEnabled():
            self.pbResetTopics.setText("Cancel confirmation")
        else:
            self.pbResetTopics.setText("Reset Topics")

    def AddRowToTopics(self):
        """
        Add a new row with a topic combobox to topics table
        """
        availabletopics = set(TOPICKEYWORDS.keys()).discard(
            self.selectedTopics
        )
        availabletopics = list(availabletopics)
        availabletopics.sort()
        # create the combobox
        combobox = QComboBox()
        combobox.addItem("No topic selected...")
        combobox.addItems(availabletopics)
        combobox.setEditable(False)
        combobox.currentTextChanged.connect(self.ComboboxChanged)
        self.currentCombobox = combobox
        row = self.twTopics.rowCount()
        # add to table
        self.twTopics.insertRow(row)
        self.twTopics.setCellWidget(row, 1, self.currentCombobox)

    def ResetTable(self):
        self.twTopics.setRowCount(0)
        self.twTopics.clearContents()
        self.AddRowToTopics()
        self.pbConfirmReset.setEnabled(False)

    def OnDeleteRowInTopics(self):
        """
        For when the row is double clicked
        """
        # if not X do nothing
        if self.twTopics.currentItem().text() != "X":
            return
        row = self.twTopics.currentRow()
        # get the value of the topic so it can be removed
        # from our set as well
        value = self.twTopics.item(row, 1).text()
        self.selectedTopics.remove(value)
        self.twTopics.removeRow(row)
        # create a new blank row if needed
        if self.twTopics.rowCount() == 0:
            self.AddRowToTopics()
        # refresh combobox with new data
        self.currentCombobox.clear()
        self.currentCombobox.addItem("No topic selected...")
        # get avialable topics
        availabletopics = set(TOPICKEYWORDS.keys()).difference(
            self.selectedTopics)
        availabletopics = list(availabletopics)
        availabletopics.sort()
        self.currentCombobox.addItems(availabletopics)

    def AddDeleteButton(self, row: int):
        """
        For adding the delete X
        """
        self.twTopics.setItem(row, 0, QTableWidgetItem("X"))

    def ComboboxChanged(self):
        """
        When the current combobox changes
        """
        # skip if not actually selecting a proper topic
        if self.currentCombobox.currentIndex() == 0:
            return
        # add to selected topics
        self.selectedTopics.add(self.currentCombobox.currentText())
        # replace with label now to prevent changing
        value = self.currentCombobox.currentText()
        self.twTopics.removeCellWidget(self.twTopics.rowCount()-1, 1)
        self.twTopics.setItem(
            self.twTopics.rowCount()-1, 1, QTableWidgetItem(str(value)))
        # need to add new row
        self.AddRowToTopics()

    def SetupInputWidgets(self):
        """
        Setup input widgets for use (levels)
        """
        levels = [
            "Both",
            "A",
            "AS"
        ]
        self.cbLevel.addItems(levels)
        self.twTopics.clear()
        self.OnLevelChange()

    def OnLevelChange(self):
        """
        If levels change we need to change the available components as well.
        """
        level = self.cbLevel.currentText()
        components = []
        if level == "A" or self.cbLevel.currentIndex() == 0:
            components.extend([
                "Both components",
                "Component 1",
                "Component 2"
            ])
        elif level == "AS":
            components.append("Component 1")

        self.cbComponent.clear()
        self.cbComponent.addItems(components)

# NOTE when generating questions,
# if no questions could be generated show an error message on the push button
# and disable it
    def ShowMarkscheme(self):
        """
        Shows the markscheme for the current question ID
        """
        if not self.currentQuestionID:
            return
        mstext = funchelpers.GetFullMarkscheme(
            self.SQLSocket, self.currentQuestionID
            )
        # get label for current question
        dataquery = f"""
        SELECT
    (p.PaperYear || ' ' || p.PaperComponent || ' ' || p.PaperLevel || ' level')
    AS paper_level,
    q.QuestionNumber
FROM
    Question q
INNER JOIN
    Paper p ON q.PaperID = p.PaperID
    AND q.QuestionID = '{self.currentQuestionID}';
        """
        data = self.SQLSocket.queryDatabase(dataquery)
        labeltext = f"Question {data[1]} from paper {data[0]}"
        output = OutputWindowHandler(labeltext, mstext)

    def GetQuestionCriteria(self) -> CriteriaStruct:
        """
        Get the question criteria and return as criteria object
        """
        # check component, level, topic to determine
        # if they are on the first option
        # (for all selection)
        # if they are then we replace them with blanks
        # so that we know not to include them as criteria
        # in the SQL query
        component = ""
        if self.cbComponent.currentIndex() != 0:
            component = self.cbComponent.currentText()
        level = ""
        if self.cbLevel.currentIndex() != 0:
            level = self.cbLevel.currentText()
        topics = set()
        if len(self.selectedTopics) != 0:
            topics = self.selectedTopics

        return CriteriaStruct(
            topics,
            self.sbMin.value(),
            self.sbMax.value(),
            component,
            level,
            self.checkBox0Parts.isChecked()
        )