# handles the images view window
from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtGui import QPixmap, QImage
from .Generated.ImagesViewGenerated import Ui_ImagesViewDialog
from typing import List, Set
from .Util.imageClass import Image
from sqlitehandler import SQLiteHandler


class ImagesViewHandler(Ui_ImagesViewDialog, QDialog):

    def __init__(self, questionids: List[str], showMarkschemes: bool = False,
                 parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.questionids = questionids
        self.SQLSocket = SQLiteHandler()
        self.showMarkschemes = showMarkschemes
        self.imageScale = 500
        self.ShowImageList()

        self.show()
        self.exec()

    def ShowImageList(self):
        """
        Output all the images for the question ids to the
        scroll area widget contents
        """
        for questionid in self.questionids:
            imgquery = f"""
    SELECT imageData, isPartOfMarkscheme, question.questionNumber,
    (Paper.PaperYear || '-' || Paper.PaperComponent || '-' || Paper.PaperLevel)
    FROM Images
    JOIN Question ON Images.questionID = Question.questionID
    JOIN Paper ON Question.paperID = Paper.paperID
    WHERE question.questionID = '{questionid}'
"""
            if not self.showMarkschemes:
                imgquery += " AND isPartOfMarkscheme = 0"
            else:
                imgquery += " AND isPartOfMarkscheme = 1"
            imgresults = self.SQLSocket.queryDatabase(imgquery)
            for imgresult in imgresults:
                imgdata = imgresult[0]
                imgpixmap = QPixmap()
                imgpixmap.loadFromData(imgdata)
                imgpixmap = imgpixmap.scaledToWidth(self.imageScale)
                imglabel = QLabel()
                imglabel.setPixmap(imgpixmap)
                self.scrollAreaWidgetContents.layout().addWidget(imglabel)
                captionlabel = QLabel()
                caption = f"Question {imgresult[2]} - {imgresult[3]}"
                if imgresult[1]:
                    caption += " - Markscheme only"
                captionlabel.setText(caption)
                self.scrollAreaWidgetContents.layout().addWidget(captionlabel)
