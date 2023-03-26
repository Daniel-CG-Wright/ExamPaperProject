# handles adding and editing questions
from .Generated.AddEditWindowGenerated import Ui_AddEditQuestions
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QDate, QBuffer, QByteArray, QIODevice
from .AddEditPartsHandler import PartHandler
from typing import List
from .Util.question import Part, Question
from .Util.imageClass import Image
from .AlertWindowHandler import AlertWindow
from pathlib import Path
from sqlitehandler import SQLiteHandler
from .TopicsWindowHandler import TopicsWindowHandler


class AddEditWindowHandler(Ui_AddEditQuestions, QDialog):

    def __init__(self, editQuestionID: str = "", parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.ConnectSignalSlots()
        self.editQuestionID = editQuestionID
        self.currentParts: List[Part] = []
        self.parts: List[Part] = []
        self.currentMarks: int = 0
        self.images: List[Image] = []
        self.SQLSocket = SQLiteHandler()
        self.topics: List[str] = []
        self.UpdatePartsTable()
        self.SetupEditMode()
        self.show()
        self.exec()

    def SetupEditMode(self):
        """
        If we are given an ID for question edits
        then we setup widgets in edit mode
        """
        if self.editQuestionID == "":
            return
        # get the question from the database
        questionquery = f"""
SELECT Paper.PaperComponent, Paper.PaperLevel, Paper.PaperYear,
       Question.QuestionContents, Question.TotalMarks, Question.QuestionNumber
FROM Question
INNER JOIN Paper ON Question.PaperID = Paper.PaperID
WHERE Question.QuestionID = '{self.editQuestionID}'
        """
        result = self.SQLSocket.queryDatabase(questionquery)
        if result:
            results = [i for i in result[0]]
        else:
            return
        self.cbComponent.setCurrentText(results[0])
        self.deYear.setDate(QDate(results[2], 1, 1))
        # set the question text
        self.textEdit.setPlainText(results[3])
        # set the level
        self.cbLevel.setCurrentText(results[1])
        # set the marks
        self.sbMarks.setValue(results[4])
        # set the parts
        partsquery = f"""
        SELECT Part.PartContents, Part.PartMarks, Part.PartNumber
        FROM Parts
        WHERE Parts.QuestionID = '{self.editQuestionID}'
        """
        partsresults = self.SQLSocket.queryDatabase(partsquery)
        for part in partsresults:
            partobj = Part(
                None,
                partsresults[2],
                partsresults[1],
                partsresults[0]
            )
            self.parts.append(partobj)
        # update the parts table
        self.UpdatePartsTable()
        # set the images
        imagequery = f"""
        SELECT ImageName,
        ImageData, ImageFormat,
        IsPartOfMarkscheme
        FROM IMAGES
        WHERE QuestionID = '{self.editQuestionID}'
        """
        imgresults = self.SQLSocket.queryDatabase(imagequery)
        for img in imgresults:
            # add image object
            imgobj = Image(
                img[0],
                QPixmap.fromImage(QImage.fromData(img[1], img[2])),
                img[3] == 1,  # this gets converted to a bool (stored as int)
                img[2]
            )
            self.images.append(imgobj)
        # update the images list
        self.UpdateImagesList()

    def ConnectSignalSlots(self):
        self.pbAccept.clicked.connect(self.SaveData)
        self.pbCancel.clicked.connect(self.close)
        self.pbAddPart.clicked.connect(self.OpenPartMode)
        self.pbEditPart.clicked.connect(self.OpenPartEditMode)
        self.pbDeletePart.clicked.connect(self.DeletePart)
        self.cbLevel.currentIndexChanged.connect(self.OnSelectLevel)
        self.pbAddImage.clicked.connect(self.AddImage)
        self.pbDeleteImage.clicked.connect(self.DeleteImage)
        self.lwImages.currentRowChanged.connect(self.SelectImagePreview)
        self.pbAddTopics.clicked.connect(self.PressAddTopics)

    def UpdateImagesList(self):
        """
        Updates the images list
        """
        self.lwImages.clear()
        for image in self.images:
            self.lwImages.addItem(image.name)

    def OnSelectLevel(self):
        """
        When the level is changed
        """
        self.UpdateComponents()

    def UpdateComponents(self):
        """
        Update the components based on the level
        """
        if self.cbLevel.currentIndex() == 0:
            self.cbComponent.clear()
            self.cbComponent.addItems(["component 1", "component 2"])
        else:
            self.cbComponent.clear()
            self.cbComponent.addItem("component 1")

    def GetCurrentSections(self):
        """
        Gets the currently in-use sections from the parts list
        """
        sections: List[str] = []
        for part in self.parts:
            sections.append(part.section)
        return sections

    def OpenPartEditMode(self):
        """
        Open the parts window in edit mode
        """
        if (
            self.twParts.currentRow() == -1
        ):
            return

        currentSections = self.GetCurrentSections()
        currentPart = self.parts[self.twParts.currentRow()]
        handler = PartHandler(currentSections, currentPart, parent=self)
        partReturn = handler.GetPart()
        if partReturn:
            self.parts[self.twParts.currentRow()] = partReturn

        self.UpdatePartsTable()

    def DeletePart(self):
        """
        Delete a part
        """
        if (
            self.twParts.currentRow() == -1
        ):
            return

        self.parts.pop(self.twParts.currentRow())
        self.UpdatePartsTable()

    def UpdatePartsTable(self):
        """
        Update the parts table with new parts etc
        """
        self.twParts.clearContents()
        self.twParts.setRowCount(len(self.parts))
        for i, part in enumerate(self.parts):
            self.twParts.setItem(i, 0, QTableWidgetItem(part.section))
            self.twParts.setItem(i, 1, QTableWidgetItem(str(part.marks)))
            self.twParts.setItem(i, 2, QTableWidgetItem(part.contents))

        # if there are no parts we allow the base marks to be edited
        # otherwise we disable it
        if len(self.parts) == 0:
            self.sbMarks.setEnabled(True)
        else:
            self.sbMarks.setEnabled(False)
            # also get total marks from parts and set sb value to this
            self.sbMarks.setValue(self.GetTotalPartsMarks())

    def GetTotalPartsMarks(self) -> int:
        """
        Get the total parts marks or the marks from the spinbox
        if there are no parts
        """
        if len(self.parts) == 0:
            return self.sbMarks.value()
        else:
            total = 0
            for part in self.parts:
                total += part.marks
            return total

    def OpenPartMode(self):
        """
        Open the parts window
        """
        currentSections = self.GetCurrentSections()
        handler = PartHandler(currentSections, parent=self)
        partReturn = handler.GetPart()
        if partReturn:
            self.parts.append(partReturn)

        self.UpdatePartsTable()

    def OnCheckMarkschemeOnly(self):
        """
        if the markscheme only checkbox is ticked then
        mark the currently selected image
        as a markscheme only image
        """
        if (
            self.lwImages.currentRow() == -1
        ):
            return

        self.images[
            self.lwImages.currentRow()
            ].isMarkscheme = self.checkBoxIsMarkscheme.isChecked()

    def SelectImagePreview(self):
        """
        Select an image to preview from lwImages
        """
        if (
            self.lwImages.currentRow() == -1
        ):
            return

        self.lImagePreview.setPixmap(
            self.images[self.lwImages.currentRow()].pixmap)

    def AddImage(self):
        """
        Add an image from an image file
        """
        # open the file browser first to allow selection of image
        # then add the image to the listview
        # then add the image to the list of images
        # then select the image in the listview
        # then show the image in the preview

        # add file dialog options first, configured for images
        QFileDialogOptions = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)",
            options=QFileDialogOptions
        )
        if fileName:
            pixmap = QPixmap()
            worked = pixmap.load(fileName)
            if not worked:
                AlertWindow(f"Error loading image from {fileName}")
                return
            else:
                # get name of file from path
                fileName = Path(fileName).name
                extension = Path(fileName).suffix
                self.images.append(Image(fileName, pixmap, format=extension))
                self.lwImages.addItem(fileName)
                self.lwImages.setCurrentRow(len(self.images) - 1)
                # preview is run when current row is changed
                # (due to connected signal)

    def DeleteImage(self):
        """
        Delete an image from the list of images
        """
        if (
            self.lwImages.currentRow() == -1
        ):
            return

        self.images.pop(self.lwImages.currentRow())
        self.lwImages.takeItem(self.lwImages.currentRow())
        self.lImagePreview.clear()

    def DoesQuestionNumberExist(self) -> bool:
        """
        Check that the question number does not
        already exist for this paper (if we are not
        in edit mode)
        """
        if self.editQuestionID:
            return False

        sqlquery = f"""
        SELECT COUNT(QuestionNumber) FROM Question
        INNER JOIN Paper ON Question.PaperID = Paper.PaperID
        WHERE QuestionNumber = {self.sbQNumber.value()}
        AND Paper.PaperYear = '{self.deYear.date().year()}'
        AND Paper.PaperComponent = '{self.cbComponent.currentText()}'
        AND Paper.PaperLevel = '{self.cbLevel.currentText()}'
        """
        result: int = self.SQLSocket.queryDatabase(sqlquery)[0][0]
        if result:
            return True

        return False

    def SaveData(self):
        """
        Saving data.
        """
        # make sure to check there is not another
        # question with the same numebr in the same paper
        # if there is then alert the user and return
        # otherwise save the data
        if self.DoesQuestionNumberExist():
            AlertWindow(
                f"""Question number {self.sbQNumber.value()}
                already exists for this paper""")
            return
        # save the data
        # first get the paper id
        sqlquery = f"""
        SELECT PaperID FROM Paper
        WHERE PaperYear = '{self.deYear.date().year()}'
        AND PaperComponent = '{self.cbComponent.currentText()}'
        AND PaperLevel = '{self.cbLevel.currentText()}'
        """
        result = self.SQLSocket.queryDatabase(sqlquery)
        if len(result) == 0:
            # does not exist, so create the paper ID
            paperid = f"{self.cbLevel.currentText()}"
            paperid += f"-{self.cbComponent.currentText()}"
            paperid += f"-{self.deYear.date().year()}"
            sqlquery = f"""
            INSERT INTO Paper (PaperID, PaperYear, PaperComponent, PaperLevel)
            VALUES ('{paperid}',
            '{self.deYear.date().year()}',
            '{self.cbComponent.currentText()}',
            '{self.cbLevel.currentText()}')
            """
            self.SQLSocket.addToDatabase(sqlquery)
        else:
            paperid = result[0][0]
        # now save the question
        # if we are in edit mode then update the question
        # otherwise insert a new question
        if self.editQuestionID:
            # update question data
            sqlquery = f"""
            UPDATE Question SET
            TotalMarks = {self.sbMarks.value()},
            QuestionContents = '{self.textEdit.toPlainText()}',
            MarkschemeContents = '{self.teMS.toPlainText()}',
            PaperID = '{paperid}'
            WHERE QuestionID = '{self.editQuestionID}'
            """
            self.SQLSocket.addToDatabase(sqlquery)
            # delete all parts for this question
            sqlquery = f"""
            DELETE FROM PARTS
            WHERE QuestionID = '{self.editQuestionID}'
            """
            self.SQLSocket.addToDatabase(sqlquery)
            # delete all images for this question
            sqlquery = f"""
            DELETE FROM Images
            WHERE QuestionID = '{self.editQuestionID}'
            """
            self.SQLSocket.addToDatabase(sqlquery)
            # add new parts
            self.AddPartsToSQL(self.editQuestionID)
            # add new images
            self.AddImagesToSQL(self.editQuestionID)
            # add topics
            self.AddTopicsToSQL(self.editQuestionID)

        else:
            # new question id
            questionid = f"{paperid}{self.sbQNumber.value()}"
            # insert question data
            sqlquery = f"""
            INSERT INTO Question (QuestionID, QuestionNumber,
            TotalMarks, QuestionContents, MarkschemeContents,
            PaperID)
            VALUES ('{questionid}',
            {self.sbQNumber.value()},
            {self.sbMarks.value()},
            '{self.textEdit.toPlainText()}',
            '{self.teMS.toPlainText()}',
            '{paperid}')
            """
            self.SQLSocket.addToDatabase(sqlquery)
            # add parts
            self.AddPartsToSQL(questionid)
            # add images
            self.AddImagesToSQL(questionid)
            # add topics
            self.AddTopicsToSQL(questionid)

        # show success message
        AlertWindow("Question saved successfully")
        # close the window
        self.close()

    def AddImagesToSQL(self, questionid: str):
        """
        Add images to the SQL database
        """
        for image in self.images:
            # converting image to bytes
            arrayOfBytes = QByteArray()
            buffer = QBuffer(arrayOfBytes)
            buffer.open(QIODevice.WriteOnly)
            try:
                image.pixmap.toImage().save(buffer, image.format)
            except Exception as e:
                AlertWindow(f"Error saving image {image.name}: {e}")
                continue
            pixmapBytes = arrayOfBytes.data()
            # using a parameterised query to insert the image
            sqlquery = f"""
            INSERT INTO Images (ImageID, QuestionID,
            ImageName, ImageData, IsPartOfMarkscheme, imageFormat)
            VALUES ((SELECT MAX(ImageID) FROM Images) + 1,
            '{questionid}',
            '{image.name}',
            ?,
            {image.isMarkscheme},
            '{image.format}'
            )
            """
            self.SQLSocket.AddParameterizedQueryToDatabase(
                sqlquery, (pixmapBytes, ))

    def AddPartsToSQL(self, questionid: str):
        """
        Add parts to the SQL database
        """
        for part in self.parts:
            partid = f"{questionid}{part.section}"
            sqlquery = f"""
            INSERT INTO Parts (PartiD, QuestionID,
            PartNumber, PartMarks, PartContents)
            VALUES ('{partid}',
            '{questionid}',
            '{part.section}',
            {part.marks},
            '{part.contents}'
            )
            """
            self.SQLSocket.addToDatabase(sqlquery)

    def PressAddTopics(self):
        """
        When the Add Topics button is pressed
        """
        # open the add topics window
        AddTopicsWindow = TopicsWindowHandler(self.topics, parent=self)
        # get the final results
        self.topics = AddTopicsWindow.GetTopics()

    def AddTopicsToSQL(self, questionid: str):
        """
        Add the topics of the question to the SQL database
        """
        # delete all topics for this question
        sqlquery = f"""
        DELETE FROM QuestionTopic
        WHERE QuestionID = '{questionid}'
        """
        self.SQLSocket.addToDatabase(sqlquery)
        # add all topics
        for topic in self.topics:
            questiontopicid = questionid + topic
            sqlquery = f"""
            INSERT INTO QuestionTopic (QuestionTopicID, QuestionID, TopicID)
            VALUES ('{questiontopicid}', '{questionid}', '{topic}')
            """
            self.SQLSocket.addToDatabase(sqlquery)
