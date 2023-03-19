from PyQt5.QtWidgets import QDialog, QComboBox, QTableWidgetItem
from .Generated.RandomQuestionGenerated import Ui_RandomQuestionDialog
from PyQt5.QtCore import Qt
from .Util import QuestionPartFunctionHelpers as funchelpers
from sqlitehandler import SQLiteHandler
from .Util.CriteriaClass import CriteriaStruct, TOPICKEYWORDS
from typing import List, Set
from .OutputWindowHandler import OutputWindowHandler
# handles the generation of random questions


class RandomQuestionHandler(Ui_RandomQuestionDialog, QDialog):

    def __init__(self, parent=None):
        """
        For generating random questions
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setModal(False)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.SQLSocket = SQLiteHandler()
        self.currentQuestionID: str = ""
        self.selectedTopics: Set = set()
        self.currentCombobox: QComboBox = ""
        # question pool is for all the potential random
        # question ids that can be picked.
        self.currentQuestionPool: Set[str] = set()
        self.SetupInputWidgets()
        self.ConnectSignalSlots()
        self.GenerateQuestionPool()
        self.show()
        self.exec()

    def ConnectSignalSlots(self):
        self.pbGenerate.clicked.connect(self.GenerateQuestion)
        self.pbViewMarkscheme.clicked.connect(self.ShowMarkscheme)
        self.cbLevel.currentTextChanged.connect(self.OnLevelChange)
        self.pbResetTopics.clicked.connect(self.ActivateConfirmation)
        self.pbConfirmReset.clicked.connect(self.ResetTable)
        self.cbComponent.currentTextChanged.connect(self.GenerateQuestionPool)
        self.sbMax.valueChanged.connect(self.GenerateQuestionPool)
        self.sbMin.valueChanged.connect(self.GenerateQuestionPool)
        self.checkBox0Parts.stateChanged.connect(self.GenerateQuestionPool)

    def GenerateQuestion(self):
        """
        Generates a random question from the question pool.
        """
        question = self.currentQuestionPool.pop()
        self.currentQuestionID = question
        text = funchelpers.GetQuestionAndParts(self.SQLSocket, question)
        self.teRandomQuestion.setText(text)
        self.lNumberOfUniques.setText(
            f"Number of unique questions left: {len(self.currentQuestionPool)}"
        )
        if len(self.currentQuestionPool) == 0:
            # generate question pool again for later
            self.GenerateQuestionPool()

    def GenerateQuestionPool(self):
        """
        Generates the question pool to take the next random question
        from and saves in self.currentQuestionPool
        """
        # criteria to filter by
        Criteria = self.GetQuestionCriteria()
        # we will display the questions themselves in the main section
        # if the question has no text we will display the content of the
        # first part.
        # then we will display the parts when they click.
        # however, we will search with part contents as well as main contents.
        # this ensures they can find the right one.
        # we will select the ID at the start but exclude it from table
        # display, and store the results in self.records
        # this allows us to access IDs of questions without weird
        # sql queries
        questionquery = f"""
SELECT
    Question.QuestionID
FROM
    Paper
    JOIN Question ON Paper.PaperID = Question.PaperID
    LEFT JOIN Parts ON Question.QuestionID = Parts.QuestionID
    JOIN QuestionTopic ON Question.QuestionID = QuestionTopic.QuestionID
WHERE
        """
        # stores conditions to add to the SQL query
        conditions: List[str] = []

        if Criteria.component:
            # get component
            extracomponents = []
            if Criteria.component.lower() == "component 1":
                extracomponents.extend(
                    [
                        "unit 1",
                        "unit 3"
                    ]
                )
            elif Criteria.component.lower() == "component 2":
                extracomponents.extend(
                    [
                        "unit 4"
                    ]
                )
            componentstring = f"""
            (TRIM(Paper.PaperComponent) = '{Criteria.component.lower()}' OR
            """
            componentstring += " OR ".join(
                f"TRIM(Paper.PaperComponent) = '{i}'"
                for i in extracomponents
                ) + ") "
            conditions.append(componentstring)

        if Criteria.level:
            # get level
            conditions.append(f"""
            Paper.PaperLevel = '{Criteria.level}'
            """)

        if len(Criteria.topics) > 0:
            # get the topic
            conditions.append(f"""
            QuestionTopic.TopicID = '{Criteria.topics.pop()}'
            AND QuestionTopic.QuestionID = Question.QuestionID
            """)

        if Criteria.noParts:
            # restrict query to only select questions with 1 part.
            # these questions will not have any entries in parts
            conditions.append(f"""
            Question.QuestionID IN (SELECT Question.QuestionID FROM
            QUESTION, Parts WHERE NOT EXISTS(
                SELECT Parts.QuestionID FROM Parts
                WHERE Question.QuestionID = Parts.QuestionID)
                )
            """)

        # add the min and max marks
        conditions.append(f"""
        Question.TotalMarks BETWEEN
        {Criteria.minmarks} AND
        {Criteria.maxmarks}
        """)

        # add conditions to query
        questionquery += " AND ".join(conditions)
        questionquery += """
        GROUP BY
    Question.QuestionID
        """
        print(questionquery)
        results = self.SQLSocket.queryDatabase(questionquery)
        print(results)
        self.currentQuestionPool = set(i[0] for i in results)
        self.lNumberOfQs.setText(
            f"Number of questions available: {len(self.currentQuestionPool)}"
        )
        self.lNumberOfUniques.setText(
            f"Number of unique questions left: {len(self.currentQuestionPool)}"
        )
        # if nothing in question pool then block generation
        if len(self.currentQuestionPool) == 0:
            self.pbGenerate.setEnabled(False)
            self.pbGenerate.setText("No questions with this criteria.")
        else:
            self.pbGenerate.setEnabled(True)
            self.pbGenerate.setText("Generate Question")

    def ActivateConfirmation(self):
        """
        Make user confirm resetting the table
        """
        self.pbConfirmReset.setEnabled(
            not self.pbConfirmReset.isEnabled()
            )
        if self.pbConfirmReset.isEnabled():
            self.pbResetTopics.setText("Cancel confirmation")
        else:
            self.pbResetTopics.setText("Reset Topics")

    def AddRowToTopics(self):
        """
        Add a new row with a topic combobox to topics table
        """
        availabletopics = set(TOPICKEYWORDS.keys())
        availabletopics.discard(
            self.selectedTopics
        )
        availabletopics = list(availabletopics)
        availabletopics.sort()
        # create the combobox
        combobox = QComboBox()
        combobox.addItem("No topic selected...")
        combobox.addItems(availabletopics)
        combobox.setEditable(False)
        combobox.currentTextChanged.connect(self.ComboboxChanged)
        self.currentCombobox = combobox
        row = self.twTopics.rowCount()
        # add to table
        self.twTopics.insertRow(row)
        self.twTopics.setCellWidget(row, 0, self.currentCombobox)

    def ResetTable(self):
        self.twTopics.setRowCount(0)
        self.twTopics.clearContents()
        self.AddRowToTopics()
        self.pbConfirmReset.setEnabled(False)
        self.pbResetTopics.setText("Reset Topics")

    def ComboboxChanged(self):
        """
        When the current combobox changes
        """
        # skip if not actually selecting a proper topic
        if self.currentCombobox.currentIndex() == 0:
            return
        # add to selected topics
        self.selectedTopics.add(self.currentCombobox.currentText())
        # replace with label now to prevent changing
        value = self.currentCombobox.currentText()
        self.twTopics.removeCellWidget(self.twTopics.rowCount()-1, 0)
        self.twTopics.setItem(
            self.twTopics.rowCount()-1, 0, QTableWidgetItem(str(value)))
        self.AddRowToTopics()

    def SetupInputWidgets(self):
        """
        Setup input widgets for use (levels)
        """
        levels = [
            "Both",
            "A",
            "AS"
        ]
        self.cbLevel.addItems(levels)
        self.twTopics.clear()
        self.AddRowToTopics()
        self.OnLevelChange()

    def OnLevelChange(self):
        """
        If levels change we need to change the available components as well.
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

# NOTE when generating questions,
# if no questions could be generated show an error message on the push button
# and disable it
    def ShowMarkscheme(self):
        """
        Shows the markscheme for the current question ID
        """
        if not self.currentQuestionID:
            return
        mstext = funchelpers.GetFullMarkscheme(
            self.SQLSocket, self.currentQuestionID
            )
        # get label for current question
        dataquery = f"""
        SELECT
    (p.PaperYear || ' ' || p.PaperComponent || ' ' || p.PaperLevel || ' level')
    AS paper_level,
    q.QuestionNumber
FROM
    Question q
INNER JOIN
    Paper p ON q.PaperID = p.PaperID
    AND q.QuestionID = '{self.currentQuestionID}';
        """
        data = self.SQLSocket.queryDatabase(dataquery)[0]
        labeltext = f"Question {data[1]} from paper {data[0]}"
        output = OutputWindowHandler(labeltext, mstext, self)

    def GetQuestionCriteria(self) -> CriteriaStruct:
        """
        Get the question criteria and return as criteria object
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
        topics = set()
        if len(self.selectedTopics) != 0:
            topics = self.selectedTopics

        return CriteriaStruct(
            topics,
            self.sbMin.value(),
            self.sbMax.value(),
            component,
            level,
            self.checkBox0Parts.isChecked()
        )
