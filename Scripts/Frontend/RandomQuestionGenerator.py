from PyQt5.QtWidgets import QDialog
from .Generated.RandomQuestionGenerated import Ui_RandomQuestionDialog
# handles the generation of random questions


class RandomQuestionHandler(Ui_RandomQuestionDialog, QDialog):

    def __init__(self):
        """
        For generating random questions
        """
        

