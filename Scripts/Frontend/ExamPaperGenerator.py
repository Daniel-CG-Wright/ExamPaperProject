from PyQt5.QtWidgets import QDialog
from .Generated.ExamPaperGenerated import Ui_PaperGenerator
from .Util.CriteriaClass import CriteriaStruct
from sqlitehandler import SQLiteHandler
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

        self.exec()
        self.show()

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
        topics = set()
        # we will get all the topics for the component selected
        # using an SQL query.
        componentquery = ""
        if not criteria.component:
            componentquery = f"""
            (Paper.PaperComponent = 'Component 1'
            OR Paper.PaperComponent = 'Component 2')
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
        if doLongAnswerQuestionAtEnd:
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
        """

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
            component,
            level,
            False
        )