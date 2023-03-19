# to handle the text output window
from PyQt5.QtWidgets import QDialog
from .Generated.MarkschemeOutputGenerated import Ui_TextDialog
from PyQt5.QtCore import Qt


class OutputWindowHandler(Ui_TextDialog, QDialog):

    def __init__(self, labelText, outputText, parent=None):
        """
        For displaying text.
        LabelText is like the title, outputText is the body.
        Parse parent for non-modality
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setModal(False)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.lMarkschemeNotice.setText(labelText)
        self.textEdit.setText(outputText)
        self.show()
