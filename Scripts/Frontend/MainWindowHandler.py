# handles the main window.
from .Generated.MainWindowGenerated import Ui_MainWindow
from .ExamPaperGenerator import ExamPaperHandler
from .QuestionBankHandler import QuestionBankHandler
from .RandomQuestionGenerator import RandomQuestionHandler
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtCore import QEvent
from functools import partial


class MainWindowHandler(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        """
        Creates the main window
        """
        super().__init__(parent)
        self.setupUi(self)
        # tooltips to show when hovering over buttons
        self.tooltips = {
            self.pbGeneratePapers:
            """
            Use this to generate exam papers with randomised questions.
            Specify criteria such as minimum to maximum marks, topics
            (or component) and level (A/AS)
            """,
            self.pbGenerateQuestions:
            """
            Use this to generate a random question from the bank.
            Can specify criteria like when generating an exam paper.
            """,
            self.pbSearchSort:
            """
            View all questions, and sort by criteria such as component
            and topic.
            """
        }
        self.ConnectSignalSlots()

    def ConnectSignalSlots(self):
        self.pbGeneratePapers.installEventFilter(self)
        self.pbGenerateQuestions.installEventFilter(self)
        self.pbSearchSort.installEventFilter(self)
        self.pbGeneratePapers.clicked.connect(self.OpenGeneratePapersWindow)
        self.pbGenerateQuestions.clicked.connect(self.OpenRandomQuestionWindow)
        self.pbSearchSort.clicked.connect(self.OpenQuestionBankWindow)

    def eventFilter(self, object, event: QEvent):
        print("hayyy")
        if event.type() == QPushButton.enterEvent:
            print("cool")
            self.ShowStatusMessage(object)
            return True

        elif event.type() == QPushButton.leaveEvent:
            self.sbStatusTooltip.clearMessage()
            return True

        return False

    def OpenGeneratePapersWindow(self):
        genpaperswin = ExamPaperHandler(self)

    def OpenRandomQuestionWindow(self):
        randquestionswin = RandomQuestionHandler(self)

    def OpenQuestionBankWindow(self):
        questionbankwindow = QuestionBankHandler(self)

    def ShowStatusMessage(self, msgbutton):
        self.sbStatusTooltip.setStatusTip(
            self.tooltips[msgname]
        )