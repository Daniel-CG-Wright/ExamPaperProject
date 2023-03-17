# handles the main window.
from .Generated.MainWindowGenerated import Ui_MainWindow
from .ExamPaperGenerator import ExamPaperHandler
from .QuestionBankHandler import QuestionBankHandler
from .RandomQuestionGenerator import RandomQuestionHandler
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtCore import QEvent
from functools import partial
from typing import Dict
# we use this for the keywords in the keys
TOPICKEYWORDS: Dict[str, str] = {
    "Databases": ["database", "Entity-Relationship Diagram", "ERD"],
    "Contingencies":
    ["contingency", "recovery", "backup"],
    "Operating Systems - buffering, interrupts, polling":
    ["buffering", "polling", "interrupt",
        "buffer", "time slicing", "partitioning", "scheduling"],
    "Operating systems - Modes of operation":
    ["Batch processing", "Real time transaction", "Real time control"],
    "Operating systems - UI, types":
    ["User Interface", "Command Line Interface", "multi-user",
     "multi-processing", "standalone user", "multi-tasking",
     "batch operating system"],
    "Operating systems - resource management":
    ["Utility software", "resource management"],
    "Files":
    ["direct access file", "hash file", "transaction file",
     "master file", "serial file", "sequential file", "fixed length",
     "variable length", "hashing"],
    "Networking":
    ["collision", "Dijkstra",
     "simplex", "duplex", "switch", "router", "network", "LAN", "WAN",
     "internet", "multiplexing", "transmission"],
    "Security":
    ["Biometric", "Encryption", "Malware", "malicious software", "security",
     "validation"],
    "Algorithms":
    ["an algorithm", "passing by reference", "passing by value",
     "Big O"],
    "Systems":
    ["Safety critical", "control system", "weather forecasting", "robotics"],
    "Computer architecture":
    ["assembly language", "von neumann", "cache", "control unit", "register"],
    "SQL":
    ["SQL"],
    "Data structures":
    ["stack", "queue", "linked list", "two-dimensional array",
     "binary tree"],
    "Binary":
    ["floating point", "fixed point", "two's complement", "binary",
     "masking", "truncation", "rounding"],
    "Processing":
    ["parallel processing", "distributed processing", "data mining"],
    "Code of conduct and legislation and ethics":
    ["code of conduct", "legislation", "ethic"],
    "HCI":
    ["HCI", "interface", "voice input"],
    "Boolean algebra":
    ["Boolean algebra", "De Morgan", "Truth table"],
    "Compression":
    ["compression"],
    "Paradigms":
    ["object", "class", "OOP", "procedural", "paradigm", "languages"],
    "Translation":
    ["Compiler", "interpreter", "assembler", "translation", "compilation"],
    "Software for development":
    ["version control", "IDE", "debugging"],
    "Analysis and design":
    ["waterfall", "agile", "analysis", "feasibility", "investigate",
     "investigation", "changeover"],
    "Backus-Naur":
    ["Backus-Naur", "BNF"],
    "Testing and maintenance":
    ["Alpha", "beta", "acceptance", "maintenance"]

}


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
        # self.pbGeneratePapers.installEventFilter(self)
        # self.pbGenerateQuestions.installEventFilter(self)
        # self.pbSearchSort.installEventFilter(self)
        self.pbGeneratePapers.clicked.connect(self.OpenGeneratePapersWindow)
        self.pbGenerateQuestions.clicked.connect(self.OpenRandomQuestionWindow)
        self.pbSearchSort.clicked.connect(self.OpenQuestionBankWindow)

    # def eventFilter(self, object, event: QEvent):
    #     print("hayyy")
    #     if event.type() == QPushButton.enterEvent:
    #         print("cool")
    #         self.ShowStatusMessage(object)
    #         return True

    #     elif event.type() == QPushButton.leaveEvent:
    #         self.sbStatusTooltip.clearMessage()
    #         return True

    #     return False

    def OpenGeneratePapersWindow(self):
        genpaperswin = ExamPaperHandler(self)

    def OpenRandomQuestionWindow(self):
        randquestionswin = RandomQuestionHandler(self)

    def OpenQuestionBankWindow(self):
        questionbankwindow = QuestionBankHandler(self)

    # def ShowStatusMessage(self, msgbutton):
    #     self.sbStatusTooltip.setStatusTip(
    #         self.tooltips[msgname]
    #     )
