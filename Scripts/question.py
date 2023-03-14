# question.py, question and parts class
from typing import List, Set


class Question:

    def __init__(
            self,
            contents: str,
            marks: int,
            number: int = -1,
            parts: List = [],
            topics: Set = set()
    ):
        self.marks = marks
        self.contents = contents
        self.number = number
        self.parts: List[Part] = parts
        self.topics: Set[str] = topics

    def AddPart(self, part):
        self.parts.append(part)

    def AddTopic(self, topic: str):
        self.topics.add(topic)


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

