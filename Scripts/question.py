# question.py, question and parts class
from typing import List, Set


class Question:

    def __init__(
            self,
            contents: str,
            marks: int,
            parts: List,
            topics: Set,
            number: int = -1
    ):
        self.marks = marks
        self.contents = contents
        self.number = number
        self.parts: List[Part] = parts
        self.topics: Set[str] = topics

    def AddPart(self, part):
        self.parts.append(part)

    def AddTopics(self, topics: Set[str]):
        self.topics.update(topics)


class Part:

    def __init__(
            self,
            question: Question,
            section: str,
            marks: int,
            contents: str,
    ):
        self.question = question
        self.section = section
        self.contents = contents
        self.marks = marks


class Markscheme:
    def __init__(self, section: str, contents):
        self.section = section
        self.contents = contents
