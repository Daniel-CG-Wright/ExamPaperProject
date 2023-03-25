# Add and edit parts
from .Generated.AddEditPartsGenerated import Ui_AddEditParts
from PyQt5.QtWidgets import QDialog
from .Util.question import Question, Part


class PartHandler(Ui_AddEditParts, QDialog):

    def __init__(self, editPart: Part | None = None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.editPart = editPart
