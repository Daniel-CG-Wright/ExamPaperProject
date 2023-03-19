# to handle the text output window
from PyQt5.QtWidgets import QDialog
from .Generated.MarkschemeOutputGenerated import Ui_TextDialog


class OutputWindowHandler(Ui_TextDialog, QDialog):

    def __init__(self, labelText, outputText, parent=None):
        """
        For displaying text.
        LabelText is like the title, outputText is the body
        """
        super().__init__(parent)
        self.setupUi(self)
        self.lMarkschemeNotice.setText(labelText)
        self.textEdit.setText(outputText)
        self.exec()
        self.show()
