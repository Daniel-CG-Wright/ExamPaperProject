from PyQt5.QtWidgets import QDialog
from .RandomQuestionGenerator import RandomQuestionHandler
from .Generated.ExamPaperGenerated import Ui_PaperGenerator
# handles the generation of random questions


class ExamPaperHandler(Ui_PaperGenerator, QDialog):

    def __init__(self, parent=None):
        """
        For generating random exam papers.
        """
        super().__init__(parent)
        self.setupUi(self)



        self.exec()
        self.show()


