from PyQt5.QtWidgets import QDialog
from .Generated.QuestionBankGenerated import Ui_ViewAllQuestions
from sqlitehandler import SQLiteHandler
from .Util.CriteriaClass import CriteriaStruct
from .MainWindowHandler import TOPICKEYWORDS
# handles the generation of random questions


class QuestionBankHandler(Ui_ViewAllQuestions, QDialog):

    def __init__(self, parent=None):
        """
        For displaying the question bank
        """
        super().__init__(parent)
        self.setupUi(self)
        self.SQLsocket = SQLiteHandler()
        self.SetupInputWidgets()

        self.show()
        self.exec()


    def PopulateTable(self):
        """
        Populate table, getting data from SQL
        """
        # paper is a hybrid of year - level - component
        headers: list[str] = [
            "Paper",
            "No.",
            "Parts",
            "Text",
            "Marks (total)",
            "Topics"
        ]

    def GetQuestions(self):
        """
        Gets the questions to populate the table with, then
        update input widgets with new boundaries.
        """
        # criteria to filter by
        Criteria = self.GetInputCriteria()
        # we will display the questions themselves in the main section
        # if the question has no text we will display the content of the
        # first part.
        # then we will display the parts when they click.
        # however, we will search with part contents as well as main contents.
        # this ensures they can find the right one.
        questionquery = f"""
        SELECT
        (Paper.PaperYear + Paper.PaperComponent + Paper.PaperLevel),
        Question.QuestionNumber,
        COUNT(
            SELECT PartID FROM Parts
            WHERE Parts.QuestionID = Question.QuestionID
            ),
        Question.QuestionContents,
        Question.TotalMarks
        FROM Paper, Question
        WHERE 

        """

    def SetupInputWidgets(self):
        """
        Sets up the input widgets as needed. For open use only
        """
        topics = TOPICKEYWORDS.keys()
        self.cbSelectTopic.clear()
        self.cbSelectTopic.addItem("All topics")
        self.cbSelectTopic.addItems(topics)

    def GetInputCriteria(self) -> CriteriaStruct:
        """
        Outputs criteriastruct from the criteria inputted.
        """
        return CriteriaStruct(
            set(self.cbSelectTopic.currentText()),
            self.sbMin.value(),
            self.sbMax.value(),
            self.cbComponent.currentText(),
            self.cbLevel.currentText(),
            self.checkBoxForSingleParts.isChecked(),
            self.lineEdit.text()
        )
