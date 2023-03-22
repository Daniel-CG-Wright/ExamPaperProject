from .Generated.AlertWindowGeneratedUI import Ui_AlertWindow
from PyQt5.QtWidgets import QDialog, QLabel
# Handles alert window


class AlertWindow(QDialog, Ui_AlertWindow):

    def __init__(self, AlertText, parent=None):
        """
        Sets up the AlertWindow with the desired AlertText, and shows the
        alert window
        """

        super().__init__(parent)
        self.setupUi(self)

        self.AlertText = AlertText

        self.lAlertMessage.setText(str(AlertText))

        self.show()
        self.exec()
