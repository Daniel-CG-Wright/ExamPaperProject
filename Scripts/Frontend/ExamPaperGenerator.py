from PyQt5.QtWidgets import QDialog, QFileDialog
from .Generated.ExamPaperGenerated import Ui_PaperGenerator
from .Util.QuestionPartFunctionHelpers import GetQuestionAndParts
from .Util.CriteriaClass import CriteriaStruct
from docx import Document
from docx.shared import Pt
from sqlitehandler import SQLiteHandler
from typing import Set, List, Dict
from random import random
# handles the generation of random questions


class ExamPaperHandler(Ui_PaperGenerator, QDialog):

    def __init__(self, parent=None):
        """
        For generating random exam papers.
        """
        super().__init__(parent)
        self.setupUi(self)
        self.SQLSocket = SQLiteHandler()
        # probability of a long answer questions at the end (default 80%)
        self.LONGANSWERPROBABILITY = 0.8
        # margin - if the marks already generated is less than
        # this then add more
        # = 0.4, if min is 80 and max is 120,
        # and current marks is 90, then mid = 100
        # 100 - 90 = 10
        # total range is 40
        # 40 * 0.4 = 16
        # so add another question until current marks is greater
        # than min + 16 = 96
        self.MARKSMARGIN = 0.4
        # min marks for a question to be considered long
        self.MINLONGMARKS = 9
        self.currentQuestionIDs: List[str] = []
        self.SetupInputWidgets()
        self.ConnectSignalSlots()
        self.exec()
        self.show()

    def ConnectSignalSlots(self):
        self.pbGenerate.clicked.connect(self.GeneratePaper)
        self.cbLevel.currentTextChanged.connect(self.OnUpdateLevel)
        self.pbOutputToWord.clicked.connect(self.SaveToDoc)
        self.pbOutputTxt.clicked.connect(self.SaveToText)

    def SaveToText(self):
        """
        Save text edit contents to text file
        """
        if not self.teOutput.toPlainText():
            return
        # it has writing so save
        text = self.teOutput.toPlainText()
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Text Files(*.txt)",
            options=options)
        if fileName:
            with open(fileName, "w") as f:
                # save file
                f.write(text)

    def SaveToDoc(self):
        """
        Save to docx
        """
        if not self.teOutput.toPlainText():
            return
        # save
        text = self.teOutput.toPlainText()
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Word Document(*.docx)",
            options=options)
        if fileName:
            # create document
            document = Document()
            # need to format it properly for document
            # this involves putting each question as its own paragraph.
            number = 1
            for selectedid in self.currentQuestionIDs:
                text = GetQuestionAndParts(self.SQLSocket, selectedid, number)
                number += 1
                paragraph = document.add_paragraph(text)
                # font and formatting
                run = paragraph.add_run()
                font = run.font
                font.name = "Calibri"
                font.size = Pt(12)
            # save the document
            document.save(fileName)

    def SetupInputWidgets(self):
        """
        Setup input widgets as needed
        """
        self.cbLevel.addItem("Both levels")
        self.cbLevel.addItems([
            "A",
            "AS"
        ])
        self.OnUpdateLevel()

    def OnUpdateLevel(self):
        """
        Need to change components available as well
        """
        level = self.cbLevel.currentText()
        components = []
        if level == "A" or self.cbLevel.currentIndex() == 0:
            components.extend([
                "Both components",
                "Component 1",
                "Component 2"
            ])
        elif level == "AS":
            components.append("Component 1")

        self.cbComponent.clear()
        self.cbComponent.addItems(components)

    def GeneratePaper(self):
        """
        Need to generate the exam paper
        We will take a question pool,
        and then randomly generate questions from the pool.
        We can include a long answer question at the end.
        """
        # we want to preferably only have 1 question from each major topic
        # for the component
        # so we will have to overwrite question criteria
        if random() <= self.LONGANSWERPROBABILITY:
            doLongAnswerQuestionAtEnd = True
        else:
            doLongAnswerQuestionAtEnd = False
        criteria = self.GetQuestionCriteria()
        # we will get all the topics for the component selected
        # using an SQL query.
        componentquery = ""
        if not criteria.component:
            componentquery = f"""
            (Paper.PaperComponent = 'component 1'
            OR Paper.PaperComponent = 'component 2')
            """
        else:
            componentquery = f"Paper.PaperComponent = '{criteria.component}'"

        levelquery = ""
        if not criteria.level:
            levelquery = f"""
            (Paper.PaperLevel = 'A'
            OR Paper.PaperLevel = 'AS')
            """
        else:
            levelquery = f"Paper.PaperLevel = '{criteria.level}'"

        getTopicsQuery = f"""
        SELECT DISTINCT(QuestionTopic.TopicID)
FROM QuestionTopic
JOIN Question ON QuestionTopic.QuestionID = Question.QUestionID
JOIN Paper ON Question.PaperID = Paper.PaperID
WHERE {componentquery}
AND {levelquery}
        """
        topicsdata = self.SQLSocket.queryDatabase(getTopicsQuery)
        # all the topics to choose from.
        availabletopics = set([i[0] for i in topicsdata])
        currentMarks: int = 0
        # store the selected question IDs for use in the paper
        selectedQuestionIDs: List[str] = []
        if doLongAnswerQuestionAtEnd:
            # if makeing the topic unique then you have to add thi spart first
            # to reserve the topic used by the long answer question.
            # get the long answer question too
            longanswerquery = f"""
            SELECT Question.QuestionID
FROM QUESTION
JOIN QUESTIONTOPIC ON Question.QuestionID = QUESTIONTOPIC.QuestionID
WHERE QuestionTopic.TopicID IN
(SELECT DISTINCT(QuestionTopic.TopicID)
FROM QuestionTopic
JOIN Question ON QuestionTopic.QuestionID = Question.QUestionID
JOIN Paper ON Question.PaperID = Paper.PaperID
WHERE {componentquery}
AND {levelquery})
AND Question.TotalMarks >= {self.MINLONGMARKS}
        """
            longanswers = self.SQLSocket.queryDatabase(longanswerquery)
            availablelonganswers = set([i[0] for i in longanswers])
            longanswerquestionid = availablelonganswers.pop()
            longanswermarks = f"""
            SELECT TotalMarks FROM Question
            WHERE QuestionID = '{longanswerquestionid}'
            """
            longanswermarks = self.SQLSocket.queryDatabase(longanswermarks)[
                0][0]
            currentMarks += longanswermarks
            selectedQuestionIDs.append(longanswerquestionid)

        # for a bunch of random topics we get a question then
        # remove it from the available topics
        rangeofmarks = criteria.maxmarks - criteria.minmarks
        # margin calculation
        margin = rangeofmarks * self.MARKSMARGIN
        normmin = criteria.minmarks + margin
        while currentMarks < normmin:
            # add topic
            chosentopic = availabletopics.pop()
            # this query gets all the possible question ids
            availablequestionsidsquery = f"""
            SELECT QuestionID FROM QuestionTopic WHERE
            TopicID = '{chosentopic}'
            """
            # get the results as a set
            availablequestionids = set(
                [i[0] for i in self.SQLSocket.queryDatabase(
                    availablequestionsidsquery)])
            # remove any questions we have already done
            availablequestionids.difference(selectedQuestionIDs)
            while len(availablequestionids) > 0:
                # keep going until we find a question not
                # exceeding the max marks.
                selectedid = availablequestionids.pop()
                marksquery = f"""
                SELECT TotalMarks FROM Question
                WHERE QuestionID = '{selectedid}'
                """
                marks = self.SQLSocket.queryDatabase(marksquery)[0][0]
                if currentMarks + marks > criteria.maxmarks:
                    # get next question
                    continue
                else:
                    # question is satisfactory
                    currentMarks += marks
                    # insert at start so long answer is at end
                    selectedQuestionIDs.insert(0, selectedid)
                    break

        # we now have all the qeustion ids
        # we can now create the question paper
        self.currentQuestionIDs = selectedQuestionIDs.copy()
        self.OutputQuestionPaper(selectedQuestionIDs)

    def OutputQuestionPaper(self, selectedQuestionIDs: list):
        """
        Output the question paper to the text edit
        """
        outputtext = ""
        qnumber = 1
        for questionid in selectedQuestionIDs:
            # for each one we get the text.
            outputtext += GetQuestionAndParts(
                self.SQLSocket, questionid, qnumber
            )
            qnumber += 1
            outputtext += "\n"

        # output to textedit
        self.teOutput.setText(outputtext)

    def GetQuestionCriteria(self) -> CriteriaStruct:
        """
        Get the question criteria and return as criteria object.
        Overwriting the parent one as there is the need to change
        the sbMin and sbMax references to default values
        as these boxes are used for the entire paper
        in this class.
        """
        # check component, level, topic to determine
        # if they are on the first option
        # (for all selection)
        # if they are then we replace them with blanks
        # so that we know not to include them as criteria
        # in the SQL query
        component = ""
        if self.cbComponent.currentIndex() != 0:
            component = self.cbComponent.currentText()
        level = ""
        if self.cbLevel.currentIndex() != 0:
            level = self.cbLevel.currentText()

        return CriteriaStruct(
            set(),
            self.sbMin.value(),
            self.sbMax.value(),
            component.lower(),
            level,
            False
        )
