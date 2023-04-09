# Add and edit parts
from .Generated.AddEditPartsGenerated import Ui_AddEditParts
from PyQt5.QtWidgets import QDialog
from .Util.question import Question, Part
from typing import List, Dict, Tuple, Set
import re


class PartHandler(Ui_AddEditParts, QDialog):

    def __init__(self, currentSections: List[str],
                 editPart=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.editPart = editPart
        # current sections that are used e.g. bi, ai etc
        self.currentSections: List[str] = currentSections
        self.ConnectSignalSlots()
        # also calls populate section box
        self.SetupEditMode()
        self.show()
        self.exec()

    def SetupEditMode(self):
        """
        For opening in edit mode
        """
        if self.editPart is None:
            self.PopulateSectionBox()
            return
        self.sbMarks.setValue(self.editPart.marks)
        # set the section
        self.cbSection.clear()
        self.cbSection.addItem(self.editPart.section)
        # disable section to prevent editing
        self.cbSection.setEnabled(False)
        # set the text
        self.tePartText.setPlainText(self.editPart.contents)

    def ConnectSignalSlots(self):
        self.pbAccept.clicked.connect(self.SavePart)
        self.pbCancel.clicked.connect(self.close)

    def PopulateSectionBox(self):
        """
        Populate the section combobox
        """
        self.cbSection.clear()
        if len(self.currentSections) == 0:
            # add a and ai as options
            self.cbSection.addItems(["a", "ai"])
            return

        # store sections to add
        sectionsToAdd: List[str] = []
        for section in self.currentSections:
            # get the next sections
            nextSections = self.GetNextSections(section)
            # add them to the set
            sectionsToAdd += [
                i for i in nextSections if i not in sectionsToAdd]

        sectionsToAdd = [
            i for i in sectionsToAdd if i not in self.currentSections
        ]
        self.cbSection.addItems(sectionsToAdd)

    def GetNextSections(self, section: str) -> List[str]:
        """
        Gets potential sections that can arise from a section
        E.g. ai can provide aii or b or bi.
        Prevents broken sections
        """
        # use regex to find next possible sections
        # gets 2 groups, one for a-h and one for iv
        regex = re.compile(r"([a-h])([iv]*)")
        possibleSections: List[str] = []
        if regex.search(section):
            # get the groups
            letterGroup, romanGroup = regex.search(section).groups()
            # if letter is h we do not go further
            if letterGroup != "h":
                # get the next letter
                nextLetter = chr(ord(letterGroup) + 1)
                possibleSections.extend([nextLetter, nextLetter + "i"])

            # make sure that we havent hit roman limit
            # any more than this results in needing x so we dont want that
            if romanGroup != "viii":
                # get the next roman
                nextRoman = self.GetNextRoman(romanGroup)
                possibleSections.append(letterGroup + nextRoman)
            # return the possible next sections
            return [i.lower() for i in possibleSections]

    def GetNextRoman(self, roman: str) -> str:
        """
        Get the next roman numeral
        """
        # convert roman to int
        romanInt = self.RomanToInt(roman)
        # add 1
        romanInt += 1
        # convert back to roman
        return self.IntToRoman(romanInt)

    def IntToRoman(self, input: int) -> str:
        """ Convert an integer to a Roman numeral. """

        ints = (5,  4,   1)
        nums = ('V', 'IV', 'I')
        result = []
        for i in range(len(ints)):
            count = int(input / ints[i])
            result.append(nums[i] * count)
            input -= ints[i] * count
        return ''.join(result)

    def RomanToInt(self, input: str) -> int:
        """ Convert a Roman numeral to an integer. """
        input = input.upper()
        nums = {'V': 5, 'I': 1}
        sumOfNums = 0
        for i in range(len(input)):
            value = nums[input[i]]
            # If the next place holds a larger number,
            # this value is negative
            if i+1 < len(input) and nums[input[i+1]] > value:
                sumOfNums -= value
            else:
                sumOfNums += value
        return sumOfNums

    def SavePart(self):
        """
        Save the part and make available in getpart
        """
        if self.editPart is None:
            self.editPart = Part(
                "",
                "",
                "",
                ""
            )
            self.editPart.section = self.cbSection.currentText()

        self.editPart.marks = self.sbMarks.value()
        self.editPart.contents = self.tePartText.toPlainText()
        self.close()

    def GetPart(self):
        """
        Get the part that was edited/created
        """
        if self.editPart:
            return self.editPart
        else:
            return None
