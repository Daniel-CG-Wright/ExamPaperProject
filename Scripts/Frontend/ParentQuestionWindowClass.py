# parent class providing functionality for the randomquestionsgenerator
# and exampapergenerator classes
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class BaseQuestionClass:
    def __init__(self, topictable: QTableWidget):
        