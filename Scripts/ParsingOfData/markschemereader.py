# parse markschemes
# they are in docx format which makes them easier to read.
# Muhie had the very good idea of converting them to docx
# which made this possible.

from docx import Document
from PyPDF2 import PdfReader
import re
from typing import Dict, List, Tuple
from question import Markscheme


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
        self.markschemetable = self.document.tables[0]
        self.GetHeaderInfo()
        self.GetMarkschemes()

    def GetHeaderInfo(self):
        """
        Get exam year, component
        """
        # get first page text
        text = self.GetTextFromPage(0)
        # get year
        regex = re.compile(r" 20\d+ ")
        self.year = re.search(regex, text).group(0).strip()
        # get level (A | AS)
        regex = re.compile(r"A level|AS|A2")
        self.level = re.search(regex, text).group(0).strip().partition(" ")[0]
        if self.level == "A2":
            self.level = "A"
        elif self.level == "AS":
            self.level = "AS"

        # get component
        regex = re.compile(r"component [12]|unit [1234]")
        self.component = re.search(regex, text).group(0).strip()
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
        for row, rowcontents in enumerate(self.markschemetable.rows):
            # only interested in first 2 cells
            text = (cell.text for cell in rowcontents.cells[:2])
            # skip first row (headers)
            if row == 0:
                continue
            rowdata = tuple(text)
            rowsofmarks.append(rowdata)
        # rows of marks now contains each row and its marks
        # note that when a markscheme continues across a page there may be
        # multiple entries for the same question, handle this later.

    def ParseMarkschemes(self, rows: List[Tuple]):
        """
        Parse the given rows from the table into self.answerindex
        """
        self.answerindex: Dict[List]
        questionStack: List[str] = ["-1."]
        # regex for question num and parts
        # NEED TO ADD SUPPORT FOR THINGS LIKE 1bi
        # maybe do them all separately.
        sectionRe = re.compile(r"\d+[.]|\([^)]+\)")

        for row in rows:
            # row[0] = section
            # row[1] = contents
            # if a new question num has appeared
            partsearch = re.findall(sectionRe, row[0])
            if 
        
    def ConvertStackToQuestionNumber(self, stack: List[str]):
        """
        Convert question stack to numbers e.g.
        [5., (b), (i)] -> 5bi
        """
        string = ""
        for i in stack:
            if i[-1] == ".":
                string += i[:-1]
            elif i[-1] == ")" and i[0] == "(":
                string += i[1:-1]
            else:
                string += i
        return string
