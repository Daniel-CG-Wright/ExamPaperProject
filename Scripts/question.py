# question.py, question and parts class
from typing import List


class Question:

    def __init__(
            self,
            contents: str,
            marks: int,
            number: int = -1,
            markscheme: str = "",
            parts: List = []
    ):
        self.marks = marks
        self.contents = contents
        self.number = number
        self.parts: List[Part] = parts
        self.markscheme = markscheme

    def AddPart(self, part):
        self.parts.append(part)

    def AddMarkScheme(self, markscheme: str):
        self.markscheme = markscheme


class Part:

    def __init__(
            self,
            question: Question,
            section: str,
            marks: int,
            contents: str,
            markscheme: str = ""
    ):
        self.question = question
        self.section = section
        self.contents = contents
        self.marks = marks
        self.markscheme = markscheme

    def AddMarkScheme(self, markscheme: str):
        self.markscheme = markscheme
