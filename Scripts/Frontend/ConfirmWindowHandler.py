from .Generated.ConfirmWindowGenerated import Ui_ConfirmWindow
from PyQt5.QtWidgets import QDialog, QLabel
# Handles alert window


class ConfirmWindow(QDialog, Ui_ConfirmWindow):

    def __init__(self, AlertText,
                 LeftButton="Confirm", RightButton="Cancel", parent=None):
        """
        Sets up the ConfirmWindow with the desired AlertText, and left and
        right button text (defaults provided) and shows the window
        """

        super().__init__(parent)
        self.setupUi(self)

        self.AlertText = AlertText

        self.lAlertMessage.setText(str(AlertText))

        self.pbConfirm.setText(LeftButton)
        self.pbConfirm.pressed.connect(self.PressLeftButton)
        self.pbCancel.setText(RightButton)
        self.pbCancel.pressed.connect(self.PressRightButton)

        self.LeftButtonPressed = False

        self.show()
        self.exec()

    def PressLeftButton(self):
        self.LeftButtonPressed = True
        self.close()

    def PressRightButton(self):
        self.close()
