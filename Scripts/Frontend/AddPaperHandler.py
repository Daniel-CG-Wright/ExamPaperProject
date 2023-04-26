# for adding papers
from .Generated.addpapergeneratedui import Ui_SelectFiles
from PyQt5.QtWidgets import QDialog, QFileDialog
from .AlertWindowHandler import AlertWindow
from ParsingOfData.pdfreader import PDFReading
from ParsingOfData.markschemereader import MarkschemeParser
from sqlitehandler import SQLiteHandler
from .LogHandler import LogHandler
# to access files
import os
from pathlib import Path


class AddPaper(Ui_SelectFiles, QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalSlots()
        self.SQLsocket = SQLiteHandler()
        self.show()
        self.exec()

    def connectSignalSlots(self):
        self.pbAddPaper.clicked.connect(self.OnAddPaper)
        self.tbAnswerDoc.clicked.connect(self.selectAnswerDoc)
        self.tbQPPath.clicked.connect(self.selectQuestionDoc)

    def OnAddPaper(self):
        """
        When "add paper" is clicked
        """
        # get the values from the line edits
        paperPath = self.leQPPath.text()
        answerDocPath = self.leAnswerPaperDocEdit.text()
        # if either of the paths are empty, show an alert window
        if paperPath == "" or answerDocPath == "":
            AlertWindow("Please enter a valid path for both files")
            return
        # if the paper path is not a pdf, show an alert window
        if paperPath[-4:] != ".pdf":
            AlertWindow("Please enter a valid pdf file for the question paper")
            return
        # if the answer doc path is not a docx, show an alert window
        if answerDocPath[-5:] != ".docx":
            AlertWindow("Please enter a valid docx file for the answer paper")
            return

        # try to access the files
        # we do it separately and if an error occurs for either
        # then we output a corresponding error message.
        # if both are successful, we can add the paper
        try:
            # get the file size of the answer doc
            answerDocSize = os.stat(answerDocPath).st_size
            # if the file size is 0, show an alert window
            if answerDocSize == 0:
                AlertWindow("The answer doc file is empty")
                return
        except FileNotFoundError:
            AlertWindow(
                """The markscheme file could not be accessed.
                Please check the path and try again""")
            return
        try:
            # get the file size of the question paper
            paperSize = os.stat(paperPath).st_size
            # if the file size is 0, show an alert window
            if paperSize == 0:
                AlertWindow("The question paper file is empty")
                return
        except FileNotFoundError:
            AlertWindow(
                """The question paper could not be accessed.
                Please check the path and try again""")
            return

        # if we get here, we can add the paper
        logtext = self.AddPaperData(paperPath, answerDocPath)
        # Create the log window and open it.
        # The log window will show the logtext
        logwindow = LogHandler(logtext)
        self.close()

    def AddPaperData(self, paperPath: str, answerDocPath: str) -> str:
        """
        Adding the paper and markscheme to the SQLite database.
        Returns the logtext
        """
        paperPathObject = Path(paperPath).absolute()
        answerDocPathObject = Path(answerDocPath).absolute()
        logtext: str = ""
        try:
            questionreader = PDFReading(paperPathObject)
            answerreader = MarkschemeParser(
                answerDocPath.rpartition(".docx")[0])
            # add the header information for the paper first
            paperid = f"{questionreader.level}"
            paperid += f"-{questionreader.component}"
            paperid += f"-{questionreader.year}"
            # check if the paper already exists
            # if it does, show an alert window
            # make the query to check if the paper exists
            query = f"""SELECT * FROM PAPER WHERE PAPERID = '{paperid}'"""
            # execute the query
            result = self.SQLsocket.queryDatabase(query)
            # if the result is not empty, show an alert window
            if result != []:
                AlertWindow("The paper already exists")
                return
            # now check that the paperid matches the markscheme
            # if it does not, show an alert window
            # get the paperid from the markscheme
            markschemeid = f"{answerreader.level}"
            markschemeid += f"-{answerreader.component}"
            markschemeid += f"-{answerreader.year}"
            # if the paperid does not match the markschemeid, show an alert
            if paperid != markschemeid:
                AlertWindow(
                    f"""The paperid does not match the markschemeid.
                    Please check the paper and markscheme and try again
                    PaperID: {paperid}\nMarkschemeID: {markschemeid}""")
                return
            # if the paper does not exist, add it
            headerquery = f"""INSERT INTO PAPER VALUES(
            '{paperid}',
            '{questionreader.component}',
            '{questionreader.year}',
            '{questionreader.level}'
            )"""
            self.SQLsocket.addToDatabase(headerquery)
            # log the paperid
            logtext += f"PaperID: {paperid}\n"
            questions = questionreader.questionspartsindex
            # add the questions to the database
            totalquestionsadded = 0
            totalpartsadded = 0
            try:
                for question in questions:
                    # create the SQL query
                    questionobj = questions[question]
                    # get markscheme contents if possible, but otherwise
                    # leave blank
                    try:
                        mstext = answerreader.answerindex[
                            str(question)].contents
                    except KeyError:
                        mstext = ""
                    # get the next max question id
                    questionidquery = f"""
                    SELECT IFNULL(MAX(QuestionID), 0) FROM QUESTION"""
                    questionid = self.SQLsocket.queryDatabase(
                        questionidquery)[0][0] + 1
                    totalmarks = questionobj.marks + sum(
                        i.marks for i in questionobj.parts)
                    mstext = mstext.replace("\n", r"\n").replace("'", r"''")
                    questionobj.contents = questionobj.contents.replace(
                        "'", r"''")
                    # first add the question itself
                    questioninsert = f"""
                    INSERT INTO QUESTION VALUES(
                    {questionid},
                    '{paperid}',
                    {questionobj.number},
                    '{questionobj.contents}',
                    {totalmarks},
                    '{mstext}'
                    )
                    """
                    self.SQLsocket.addToDatabase(questioninsert)
                    for topic in questionobj.topics:
                        # get next questiontopic id
                        questiontopicid = f"""
                        SELECT IFNULL(MAX(QuestionTopicID), 0)
                        FROM QUESTIONTOPIC
                        """
                        questiontopicid = self.SQLsocket.queryDatabase(
                            questiontopicid)[0][0] + 1
                        topicquery = f"""
                        INSERT INTO QUESTIONTOPIC VALUES(
                        {questiontopicid},
                        {questionid},
                        '{topic}'
                        )
                        """
                        self.SQLsocket.addToDatabase(topicquery)
                    # log the question number added
                    logtext += f"Question {questionobj.number} added\n"
                    totalquestionsadded += 1
                    for part in questionobj.parts:
                        if part.marks == 0:
                            continue
                        # get next part id
                        partidquery = f"""
                        SELECT IFNULL(MAX(PartID), 0) FROM PARTS"""
                        partid = self.SQLsocket.queryDatabase(
                            partidquery)[0][0] + 1
                        try:
                            msobj = answerreader.answerindex[part.section]
                            mstext = msobj.contents
                            mstext = mstext.replace("\n", r"\n").replace(
                                "'", r"''")
                        except KeyError:
                            # set breakpoint here to see errors
                            # for a list of known question skips
                            # see the questionskips.txt
                            # log the skipped part
                            logtext += f"Skipping part: {part.section}\n"
                            continue
                        partinsert = f"""
                        INSERT INTO PARTS VALUES(
                        {partid},
                        {questionid},
                        '{part.section}',
                        '{part.contents.strip()}',
                        {part.marks},
                        '{mstext}'
                        )
                        """
                        self.SQLsocket.addToDatabase(partinsert)
                        # log the part added
                        logtext += f"Part {part.section} added\n"
                        totalpartsadded += 1
            except Exception as e:
                # log the error
                logtext += f"Error: {e}\n"
        except Exception as e:
            # output the alert window
            AlertWindow(f"Error: {e}")
            return

        # add the total questions and parts added to the log
        logtext += f"Total questions added: {totalquestionsadded}\n"
        logtext += f"Total parts added: {totalpartsadded}\n"
        # add disclaimer to the log
        logtext += """Boolean Algebra questions should be automatically
        skipped. These will not show up in the log"""
        return logtext

    def selectAnswerDoc(self):
        """
        Open the file dialog to select a docx file for the markscheme
        """
        # open the file dialog
        fileDialog = QFileDialog()
        # set the file dialog to only show docx files
        fileDialog.setNameFilter("DOCX (*.docx)")
        # get the file path
        filePath = fileDialog.getOpenFileName(
            self, "Select Markscheme", "", "DOCX (*.docx)")[0]
        # if the file path is empty, return
        if filePath == "":
            return
        # set the text of the line edit to the file path
        self.leAnswerPaperDocEdit.setText(filePath)

    def selectQuestionDoc(self):
        """
        Open the file dialog to select a PDF file for the question paper
        """
        # open the file dialog
        fileDialog = QFileDialog()
        # set the file dialog to only show pdf files
        fileDialog.setNameFilter("PDF (*.pdf)")
        # get the file path
        filePath = fileDialog.getOpenFileName(
            self, "Select Question Paper", "", "PDF (*.pdf)")[0]
        # if the file path is empty, return
        if filePath == "":
            return
        # set the text of the line edit to the file path
        self.leQPPath.setText(filePath)
