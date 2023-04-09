from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QTableWidget
from .Generated.QuestionBankGenerated import Ui_ViewAllQuestions
from PyQt5.QtCore import Qt
from sqlitehandler import SQLiteHandler
from .Util.CriteriaClass import CriteriaStruct, TOPICS
from typing import List, Tuple
import re
from .Util import QuestionPartFunctionHelpers as funchelpers
from .OutputWindowHandler import OutputWindowHandler
from .AddEditWindowHandler import AddEditWindowHandler
from .AlertWindowHandler import AlertWindow
from .ConfirmWindowHandler import ConfirmWindow
from .ImagesViewHandler import ImagesViewHandler
from .Util.imageClass import AreImagesAvailable
# handles the generation of random questions


class QuestionBankHandler(Ui_ViewAllQuestions, QMainWindow):

    def __init__(self, parent=None):
        """
        For displaying the question bank
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.SQLsocket = SQLiteHandler()
        # first index stores question id
        self.records: List[Tuple] = []
        self.SetupInputWidgets()
        self.ConnectSignalSlots()

        self.show()

    def ConnectSignalSlots(self):
        self.lineEdit.textChanged.connect(self.PopulateTable)
        self.cbSelectTopic.currentTextChanged.connect(self.PopulateTable)
        self.cbComponent.currentTextChanged.connect(self.PopulateTable)
        self.cbLevel.currentTextChanged.connect(self.OnLevelChange)
        self.sbMax.valueChanged.connect(self.ChangeMax)
        self.sbMin.valueChanged.connect(self.ChangeMin)
        self.twQuestionBank.currentCellChanged.connect(self.OnQuestionSelected)
        self.pbShowMarkscheme.clicked.connect(self.OnShowMarkscheme)
        self.checkBoxForSingleParts.stateChanged.connect(self.PopulateTable)
        self.pbAddQuestion.clicked.connect(self.OpenAddQuestionMenu)
        self.pbEditQuestion.clicked.connect(self.OpenEditQuestionMenu)
        self.pbDeleteQuestion.clicked.connect(self.OnDeleteQuestion)
        self.pbViewImages.clicked.connect(self.ShowImages)

    def ShowImages(self):
        """
        Open the show images dialog
        """
        if len(self.twQuestionBank.selectedIndexes()) == 0:
            return

        selectedrowindex = self.twQuestionBank.currentRow()
        questionid = self.records[selectedrowindex][0]
        ImagesViewHandler([questionid], False, self)

    def OnDeleteQuestion(self):
        """
        Delete a question from the SQL database then update the table
        """
        if len(self.twQuestionBank.selectedIndexes()) == 0:
            return

        # get confirmation from confirm window first
        confirm = ConfirmWindow(
            "Are you sure you want to delete this question?")
        if confirm.LeftButtonPressed:
            selectedrowindex = self.twQuestionBank.currentRow()
            questionid = self.records[selectedrowindex][0]
            deletequery = f"""
            DELETE FROM Question WHERE QuestionID = {questionid}
            """
            self.SQLsocket.addToDatabase(deletequery)
            # delete parts
            deletequery = f"""
            DELETE FROM Parts WHERE QuestionID = {questionid}
            """
            self.SQLsocket.addToDatabase(deletequery)
            # delete images
            deletequery = f"""
            DELETE FROM Images WHERE QuestionID = {questionid}
            """
            self.SQLsocket.addToDatabase(deletequery)
            # delete topics
            deletequery = f"""
            DELETE FROM QuestionTopic WHERE QuestionID = {questionid}
            """
            self.SQLsocket.addToDatabase(deletequery)
            # show success message
            AlertWindow("Question deleted successfully")
            self.PopulateTable()

    def OpenEditQuestionMenu(self):
        """
        Open the add question menu but in edit mode
        """
        # check that a row is selected
        if len(self.twQuestionBank.selectedIndexes()) == 0:
            return

        handler = AddEditWindowHandler(
            self.records[self.twQuestionBank.currentRow()][0], parent=self)
        # update table
        self.PopulateTable()

    def OpenAddQuestionMenu(self):
        """
        Open the menu for adding questions
        """
        handler = AddEditWindowHandler(parent=self)
        # update table
        self.PopulateTable()

    def ChangeMin(self):
        """
        Update max so that it cannot be less than min
        """
        self.sbMax.setMinimum(self.sbMin.value())
        self.PopulateTable()

    def ChangeMax(self):
        """
        Update min so it cannot be greater than max.
        """
        self.sbMin.setMaximum(self.sbMax.value())
        self.PopulateTable()

    def OnShowMarkscheme(self):
        if len(self.twQuestionBank.selectedIndexes()) == 0:
            return

        selectedrowindex = self.twQuestionBank.currentRow()
        questionid = self.records[selectedrowindex][0]
        mstext = funchelpers.GetFullMarkscheme(self.SQLsocket, questionid)
        labeltext = f"""
        Question {
            self.records[selectedrowindex][2]
            } from paper {
                self.records[selectedrowindex][1]
                }"""

        output = OutputWindowHandler(labeltext, mstext, [questionid],
                                     parent=self)

    def OnQuestionSelected(self):
        """
        When a question is selected in the question bank we will call
        this to perform the changes needed in the UI.
        This involves adding the parts to the parts table,
        and adding the text in the textedit.
        """
        selectedrowindex = self.twQuestionBank.currentRow()
        # if -1 then do not go, as this can happen sometimes
        if selectedrowindex == -1:
            return
        questionid: str = self.records[selectedrowindex][0]
        self.UpdatePartsTable(questionid)
        questiontext = funchelpers.GetQuestionAndParts(
            self.SQLsocket, questionid
            )
        self.teQuestionPreview.clear()
        self.teQuestionPreview.setText(questiontext)
        # disable pbViewImages if no images
        if not AreImagesAvailable([questionid]):
            self.pbViewImages.setEnabled(False)
        else:
            self.pbViewImages.setEnabled(True)

    def OutputNoEntriesMessage(self, tablePointer: QTableWidget):
        """"
        Produces 'no entries' message in table. Hides table headers
        (horizontal and vertical) so make sure to unhide.
        """
        try:
            tablePointer.setRowCount(1)
            tablePointer.setColumnCount(1)
            tablePointer.setItem(0, 0, QTableWidgetItem("No entries found."))
            tablePointer.horizontalHeader().setVisible(False)
            tablePointer.verticalHeader().setVisible(False)
        except Exception as e:
            return

    def UpdatePartsTable(self, questionid):
        """
        Updates the parts table with part information from the selected
        question (or shows suitable no parts message)
        """
        partsquery = f"""
        SELECT PartNumber, PartContents, PartMarks
        FROM Parts
        WHERE QuestionID = {questionid}
        """
        partsdata = self.SQLsocket.queryDatabase(partsquery)
        self.twParts.clear()
        if not partsdata:
            self.OutputNoEntriesMessage(self.twParts)
            return
        # set table details
        self.twParts.horizontalHeader().setVisible(True)
        self.twParts.verticalHeader().setVisible(True)
        self.twParts.setRowCount(len(partsdata))
        headers = [
            "Part Number",
            "Part Contents",
            "Part Marks"
        ]
        self.twParts.setColumnCount(len(headers))
        self.twParts.setHorizontalHeaderLabels(headers)
        for row, record in enumerate(partsdata):
            for col, cell in enumerate(record):
                self.twParts.setItem(row, col, QTableWidgetItem(str(cell)))

    def OnLevelChange(self):
        """
        If the level is changed we want to change the components
        available for selection.
        AS can only be component 1
        A level can only be component 1 or 2
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
        self.PopulateTable()

    def PopulateTable(self):
        """
        Populate table, getting data from SQL
        """
        # results are stored in self.records
        # records does nto contain topics, have to get
        # that separately
        self.GetQuestions()
        self.twQuestionBank.clear()
        # first section of records is question ID which is not
        # shown in table.
        if not self.records:
            # no records so show a message
            self.twQuestionBank.setRowCount(1)
            self.twQuestionBank.setColumnCount(1)
            self.twQuestionBank.setItem(
                0, 0, QTableWidgetItem("No questions found."))
            return

        # paper is a hybrid of year - level - component
        headers: list[str] = [
            "Paper",
            "No.",
            "Text",
            "Marks (total)",
            "Topics"
        ]
        self.twQuestionBank.setColumnCount(len(headers))
        self.twQuestionBank.setRowCount(len(self.records))
        self.twQuestionBank.setHorizontalHeaderLabels(headers)

        for row, record in enumerate(self.records):
            # skip first item as it is ID
            for col, item in enumerate(record[1:]):
                self.twQuestionBank.setItem(
                    row, col, QTableWidgetItem(str(item))
                )
            # add the topics
            topicquery = f"""
            SELECT QuestionTopic.TopicID FROM
            QuestionTopic
            WHERE QuestionTopic.QuestionID = '{record[0]}'
            """
            topics = ", ".join(
                [i[0] for i in self.SQLsocket.queryDatabase(topicquery)]
                )
            self.twQuestionBank.setItem(
                row, len(headers)-1, QTableWidgetItem(str(topics))
            )

    def GetQuestions(self):
        """
        Gets the questions to populate the table with, then
        update input widgets with new boundaries.
        Saves to self.records
        """
        # criteria to filter by
        Criteria = self.GetInputCriteria()
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
    Question.QuestionID,
    (Paper.PaperYear || '-' ||
    Paper.PaperComponent || '-' || Paper.PaperLevel),
    Question.QuestionNumber,
    Question.QuestionContents,
    Question.TotalMarks
FROM
    Paper
    JOIN Question ON Paper.PaperID = Question.PaperID
    LEFT JOIN Parts ON Question.QuestionID = Parts.QuestionID
    LEFT JOIN QuestionTopic ON Question.QuestionID = QuestionTopic.QuestionID
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

        if Criteria.contentsearch:
            Criteria.contentsearch = Criteria.contentsearch.replace("'", "''")
            # get the search criteria
            conditions.append(f"""
            (Question.QuestionContents LIKE '%{Criteria.contentsearch}%' OR
            Parts.PartContents LIKE '%{Criteria.contentsearch}%')
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
    Question.QuestionID,
    Paper.PaperYear,
    Paper.PaperComponent,
    Paper.PaperLevel,
    Question.QuestionNumber,
    Question.QuestionContents,
    Question.TotalMarks
    ORDER BY
    Paper.PaperYear,
    Paper.PaperComponent,
    Paper.PaperLevel,
    Question.QuestionNumber
        """
        self.records = self.SQLsocket.queryDatabase(questionquery)

    def SetupInputWidgets(self):
        """
        Sets up the input widgets as needed. For open use only
        """
        topics = TOPICS
        self.cbSelectTopic.clear()
        self.cbSelectTopic.addItem("All topics")
        self.cbSelectTopic.addItems(topics)

        self.sbMax.setValue(20)

        self.cbLevel.clear()
        self.cbLevel.addItems(
            [
                "All levels",
                "A",
                "AS"
            ]
        )
        self.OnLevelChange()

    def GetInputCriteria(self) -> CriteriaStruct:
        """
        Outputs criteriastruct from the criteria inputted.
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
        if self.cbSelectTopic.currentIndex() != 0:
            topics = set([self.cbSelectTopic.currentText()])

        return CriteriaStruct(
            topics,
            self.sbMin.value(),
            self.sbMax.value(),
            component,
            level,
            self.checkBoxForSingleParts.isChecked(),
            self.GetSanitisedSearchInput()
        )

    def GetSanitisedSearchInput(self) -> str:
        """
        Returns the search bar's input, but sanitised
        Only allows alphanumeric characters, and whitespace and -
        """
        # only allow the things in this regex
        text = self.lineEdit.text()
        re.sub(r'[^A-Za-z0-9 -]+', "", text)
        return text
