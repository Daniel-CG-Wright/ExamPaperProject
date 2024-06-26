# to handle the text output window
from PyQt5.QtWidgets import QMainWindow
from .Generated.MarkschemeOutputGenerated import Ui_TextDialog
from PyQt5.QtCore import Qt
from .ImagesViewHandler import ImagesViewHandler
from .Util.imageClass import AreImagesAvailable
from typing import List


class OutputWindowHandler(Ui_TextDialog, QMainWindow):

    def __init__(self, labelText, outputText, questionids: List[str] = [],
                 parent=None):
        """
        For displaying text.
        LabelText is like the title, outputText is the body.
        Parse parent for non-modality
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.ConnectSignalSlots()
        self.lMarkschemeNotice.setText(labelText)
        self.textEdit.setText(outputText)
        self.pbShowImages.setEnabled(False)
        if questionids:
            self.questionids = questionids
            # enable images button if there are images
            # else disable it
            if AreImagesAvailable(self.questionids, isMarkscheme=True):
                self.pbShowImages.setEnabled(True)
        else:
            self.questionids = []

        self.show()

    def ConnectSignalSlots(self):
        self.pbShowImages.clicked.connect(self.ViewImages)

    def ViewImages(self):
        """
        Opens the images window
        """
        if self.questionids:
            ImagesViewHandler(self.questionids,
                              showMarkschemes=True, parent=self)
