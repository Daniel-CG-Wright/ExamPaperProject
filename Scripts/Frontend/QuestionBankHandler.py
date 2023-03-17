from PyQt5.QtWidgets import QDialog
from .Generated.QuestionBankGenerated import Ui_ViewAllQuestions
# handles the generation of random questions


class QuestionBankHandler(Ui_ViewAllQuestions, QDialog):

    def __init__(self, parent=None):
        """
        For displaying the question bank
        """
        super().__init__(parent)
        self.setupUi(self)


        self.show()
        self.exec()


    def PopulateTable(self):
        """
        Populate table, getting data from SQL
        """

    def GetQuestions(self):
        """
        Gets the questions to populate the table with
        """
