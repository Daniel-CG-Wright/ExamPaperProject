# parse markschemes
# they are in docx format which makes them easier to read.
# Muhie had the very good idea of converting them to docx
# which made this possible.

from docx import Document
from PyPDF2 import PdfReader
import re
from typing import Dict, List, Tuple
from Frontend.Util.question import Markscheme


class MarkschemeParser:

    def __init__(self, filename: str):
        """
        Parse docx markscheme to self.answerindex.
        Uses pdf name for markscheme info, so do not
        parse an extension to filename
        """
        self.fileObject = open(filename + ".pdf", 'rb')
        self.reader: PdfReader = PdfReader(
            self.fileObject
            )
        self.document = Document(filename + ".docx")
        # markscheme is spread across several tables.
        self.markschemetables = self.document.tables

        self.GetHeaderInfo()
        self.GetMarkschemes()

    def GetHeaderInfo(self):
        """
        Get exam year, component
        """
        # get first page text
        text = self.GetTextFromPage(0)
        # get year
        regex = re.compile(r" 20[\d]+[ ]*[\d] ", re.IGNORECASE)
        self.year = re.search(regex, text).group(0).strip().replace(" ", "")
        # get level (A | AS)
        regex = re.compile(r"A level|AS|A2", re.IGNORECASE)
        self.level = re.search(regex, text).group(0).strip().partition(" ")[0]
        if self.level == "A2":
            self.level = "A"
        elif self.level == "AS":
            self.level = "AS"

        # get component
        regex = re.compile(r"component [12]|unit [1234]", re.IGNORECASE)
        self.component = re.search(regex, text).group(0).strip().lower()
        # DO NOT NORMALISE UNIT TO COMPONENT
        # we want to keep unit and component separate

    def GetNumberOfPages(self):
        return len(self.reader.pages)

    def GetAllPages(self):
        return self.reader.pages

    def GetIndexedPage(self, index: int):
        return self.reader.pages[index]

    def GetTextFromPage(self, index: int):
        return self.GetIndexedPage(index).extract_text()

    def GetMarkschemes(self):
        """
        Get the markscheme for each question and record it in
        self.answerindex
        """
        rowsofmarks: List[Tuple] = []
        for table in self.markschemetables:
            for row, rowcontents in enumerate(table.rows):
                # only interested in first 2 cells (qnum and ms contents)
                if row == 0:
                    # there is a problem where this sometimes skips
                    # rows that actually require reading
                    # so we must check to make sure we are not skipping
                    # anything important.
                    # AO will always be in the 4th cell for the rows
                    # we need to skip
                    if (len(rowcontents.cells) > 2 and
                            "AO" in rowcontents.cells[3].text.upper()):
                        continue
                if len(rowcontents.cells) > 1:
                    text = (cell.text for cell in rowcontents.cells[:2])
                    rowdata = tuple(text)
                else:
                    # long answer tbales only have 1 column
                    rowdata = ("", rowcontents.cells[0].text)
                rowsofmarks.append(rowdata)
        # rows of marks now contains each row and its marks
        # note that when a markscheme continues across a page there may be
        # multiple entries for the same question
        self.ParseMarkschemes(rowsofmarks)

    def ParseMarkschemes(self, rows: List[Tuple]):
        """
        Parse the given rows from the table into self.answerindex
        """
        self.answerindex: Dict[str, Markscheme] = {}
        questionStack: List[str] = ["-1"]
        # regex for question num and parts
        numberRe = re.compile(r"\d+")
        letterRe = re.compile(r"[abcdefgh]+")
        numeralRe = re.compile(r"[iv]+")
        for row in rows:
            # row[0] = section
            # row[1] = contents
            # if a new question num has appeared we reassign to that
            section = row[0]
            questionNum = re.search(numberRe, section)
            # if questionnum is provided and is different
            # to the current question num, then we replace
            if questionNum:
                questionNum = questionNum.group(0)
                if questionNum != questionStack[0]:
                    questionStack = [questionNum]

            # do the same for parts
            mainpartNum = re.search(letterRe, section)
            if mainpartNum:
                mainpartNum = mainpartNum.group(0)
                if len(questionStack) < 2 or questionStack[1] != mainpartNum:
                    # change the main part
                    questionStack = [questionStack[0], mainpartNum]

            # same for numerals
            numeralNum = re.search(numeralRe, section)
            if numeralNum:
                numeralNum = numeralNum.group(0)
                # need to account for questions like 5i where
                # there may not be a main part
                if (
                    len(questionStack) < 2 or
                    (
                        len(questionStack) < 3 and
                        not re.search(numeralNum, questionStack[-1])
                    )
                ):
                    questionStack.append(numeralNum)
                elif (
                    len(questionStack) > 1 and
                    questionStack[-1] != numeralNum and
                    re.search(numeralRe, questionStack[-1])
                ):
                    questionStack = questionStack[:-1] + [numeralNum]

            # For some markschemes (like 2018 unit 4) there can be (i) inside
            # the contents rather than in the question number box
            # to fix this we also gotta analyse the contents.
            # if there is a part in there we can add it
            contents = row[1]
            bracketnumeralRe = re.compile(r"\([iv]+\)", re.IGNORECASE)
            numerals = list(re.finditer(bracketnumeralRe, contents))
            if numerals:
                # there are numerals in there so get the contents
                # for each group we have the start and end index
                # so we just grab the question from the end of the previous
                # numeral
                # to the start of the next
                for i in range(len(numerals)):
                    # get the contents up to the next numeral
                    startindex = numerals[i].end(0)+1
                    if i == len(numerals)-1:
                        endindex = -1
                    else:
                        endindex = numerals[i+1].start(0)
                    # get the numerals themselves (e.g. ii)
                    numeralstring = numerals[i].group(0)[1:-1]
                    sectionID = self.ConvertStackToQuestionNumber(
                        questionStack + [numeralstring])
                    if i == len(numerals)-1:
                        numeralcontents = contents[startindex:]
                    else:
                        numeralcontents = contents[startindex:endindex]
                    # write contents
                    if sectionID in self.answerindex.keys():
                        self.answerindex[
                            sectionID].contents += "\n" + numeralcontents
                    else:
                        markschemeobj = Markscheme(sectionID, numeralcontents)
                        self.answerindex[sectionID] = markschemeobj
            else:
                # get section
                sectionID = self.ConvertStackToQuestionNumber(questionStack)
                # now we get markscheme object/contents.
                # if there is already an entry under this question
                # we just add to its contents
                # .replace("\n", r"\n")
                if sectionID in self.answerindex.keys():
                    self.answerindex[sectionID].contents += "\n" + contents
                else:
                    markschemeobj = Markscheme(sectionID, contents)
                    self.answerindex[sectionID] = markschemeobj

    def ConvertStackToQuestionNumber(self, stack: List[str]):
        """
        Convert question stack to numbers e.g.
        [5, b, i] -> 5bi
        """
        string = "".join(stack)
        return string
