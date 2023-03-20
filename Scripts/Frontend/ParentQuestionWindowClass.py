# parent class providing functionality for the randomquestionsgenerator
# and exampapergenerator classes
from typing import Set
from PyQt5.QtWidgets import (QTableWidget,
                             QTableWidgetItem,
                             QPushButton, QComboBox,
                             QCheckBox, QSpinBox)
from .Util.CriteriaClass import TOPICKEYWORDS, CriteriaStruct


class BaseQuestionClass:
    def SetupBase(self,
                  topictable: QTableWidget,
                  resetbutton: QPushButton,
                  confirmresetbutton: QPushButton,
                  componentCombobox: QComboBox,
                  levelCombobox: QComboBox,
                  nopartsbox: QCheckBox,
                  minbox: QSpinBox,
                  maxbox: QSpinBox):
        """
        Allow use of base methods
        """
        self.topictable = topictable
        self.resetbutton = resetbutton
        self.confirmresetbutton = confirmresetbutton
        self.componentCombobox = componentCombobox
        self.levelCombobox = levelCombobox
        self.selectedTopics: Set[str] = set()
        self.nopartsbox = nopartsbox
        self.minbox = minbox
        self.maxbox = maxbox

    def ActivateConfirmation(self):
        """
        Make user confirm resetting the table
        """
        self.confirmresetbutton.setEnabled(
            not self.confirmresetbutton.isEnabled()
            )
        if self.confirmresetbutton.isEnabled():
            self.resetbutton.setText("Cancel confirmation")
        else:
            self.resetbutton.setText("Reset Topics")

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
        row = self.topictable.rowCount()
        # add to table
        self.topictable.insertRow(row)
        self.topictable.setCellWidget(row, 0, self.currentCombobox)

    def ResetTable(self):
        self.topictable.setRowCount(0)
        self.topictable.clearContents()
        self.AddRowToTopics()
        self.confirmresetbutton.setEnabled(False)
        self.resetbutton.setText("Reset Topics")

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
        self.topictable.removeCellWidget(self.topictable.rowCount()-1, 0)
        self.topictable.setItem(
            self.topictable.rowCount()-1, 0, QTableWidgetItem(str(value)))
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
        self.levelCombobox.addItems(levels)
        self.topictable.clear()
        self.AddRowToTopics()
        self.OnLevelChange()

    def OnLevelChange(self):
        """
        If levels change we need to change the available components as well.
        """
        level = self.levelCombobox.currentText()
        components = []
        if level == "A" or self.levelCombobox.currentIndex() == 0:
            components.extend([
                "Both components",
                "Component 1",
                "Component 2"
            ])
        elif level == "AS":
            components.append("Component 1")

        self.componentCombobox.clear()
        self.componentCombobox.addItems(components)

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
        if self.componentCombobox.currentIndex() != 0:
            component = self.componentCombobox.currentText()
        level = ""
        if self.levelCombobox.currentIndex() != 0:
            level = self.levelCombobox.currentText()
        topics = set()
        if len(self.selectedTopics) != 0:
            topics = self.selectedTopics

        return CriteriaStruct(
            topics,
            self.minbox.value(),
            self.maxbox.value(),
            component,
            level,
            self.nopartsbox.isChecked()
        )
