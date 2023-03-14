# pdfreader.py
# reads PDF files to a PDF reader object
import PyPDF2
from question import Question, Part
from typing import List, Dict, Set
import re

# Stores a dictionary of each topic and its associated key words
TOPICKEYWORDS: Dict[str, str] = {
    "Databases": ["database", "Entity-Relationship Diagram", "ERD"],
    "Operating Systems - buffering, interrupts, polling":
    ["buffering", "polling", "interrupt",
        "buffer", "time slicing", "partitioning", "scheduling"],
    "Operating systems - Modes of operation":
    ["Batch processing", "Real time transaction", "Real time control"],
    "Operating systems - UI, types":
    ["User Interface", "Command Line Interface", "multi-user",
     "multi-processing", "standalone user", "multi-tasking",
     "batch operating system"],
    "Operating systems - resource management":
    ["Utility software", "resource management"],
    "Files":
    ["direct access file", "hash file", "transaction file",
     "master file", "serial file", "sequential file", "fixed length",
     "variable length"],
    "Networking":
    ["collision", "Dijkstra",
     "simplex", "duplex", "switch", "router", "network", "LAN", "WAN",
     "internet", "multiplexing", "transmission"],
    "Security":
    ["Biometric", "Encryption", "Malware", "malicious software", "security",
     "validation"],
    "Algorithms":
    ["algorithm", "passing by reference", "passing by value",
     "Big O"],
    "Systems":
    ["Safety critical", "control system", "weather forecasting", "robotics"],
    "Computer architecture":
    ["assembly language", "von neumann", "cache", "control unit", "register"],
    "SQL":
    ["SQL"],
    "Data representation":
    ["stack", "queue", "linked list", "two-dimensional array",
     "binary tree"],
    "Binary":
    ["floating point", "fixed point", "two's complement", "binary",
     "masking"],
    "Processing":
    ["parallel processing", "distributed processing", "data mining"],
    "Code of conduct and legislation and ethics":
    ["code of conduct", "legislation", "ethic"],
    "HCI":
    ["HCI", "interface", "voice input"],
    "Boolean algebra":
    ["Boolean algebra", "De Morgan", "Truth table"],
    "Compression":
    ["compression"],
    "Paradigms":
    ["object", "class", "OOP", "procedural", "paradigm", "languages"],
    "Translation":
    ["Compiler", "interpreter", "assembler", "translation", "compilation"],
    "Software for development":
    ["version control", "IDE", "debugging"],
    "Analysis and design":
    ["waterfall", "agile", "analysis", "feasibility", "investigate",
     "investigation"],
    "Backus-Naur":
    ["Backus-Naur", "BNF"],
    "Testing and maintenance":
    ["Alpha", "beta", "acceptance", "maintenance"]

}
class PDFReading:
    def __init__(self, questionpapername: str):
        """
        Create a PDF reader which uses PyPDF2 to parse
        a PDF of an exam paper.
        Names should include .pdf
        Breaks the exam paper down into questions.
        Please close at the end of use.
        """
        self.fileObject = open(questionpapername, 'rb')
        self.reader: PyPDF2.PdfReader = PyPDF2.PdfReader(
            self.fileObject
            )
        self.GetHeaderInfo()
        self.GetQuestions()

    def GetHeaderInfo(self):
        """
        Get exam year, component
        """
        # get first page text
        text = self.GetTextFromPage(0)
        # get year
        regex = re.compile(r" 20\d+ ")
        self.year = re.search(regex, text).group(0).strip()
        # get level
        regex = re.compile(r" A level | AS level ")
        self.level = re.search(regex, text).group(0).strip()
        # get component
        regex = re.compile(r" component [12] ")
        self.component = re.search(regex, text).group(0).strip()

    def GetNumberOfPages(self):
        return len(self.reader.pages)

    def GetAllPages(self):
        return self.reader.pages

    def GetIndexedPage(self, index: int):
        return self.reader.pages[index]

    def GetTextFromPage(self, index: int):
        return self.GetIndexedPage(index).extract_text()

    def GetQuestions(self):
        """
        Get all questions from the paper and put them into a list
        of question objects, in order. Stored as self.questions
        """
        # search for questions, ending each question with the marks
        # possible to generate something like 2. bla bla bla (a) more stuff [4]
        # this must be broken down into a question, and the part
        # r"\d+[.]\s[^[]*\[\d+\]|\(\w+\)\s[^[]*\[\d+\]"
        # this splits it up into question,
        questionsearch = re.compile(
            r"\d+[.]\s[^[]*\[\d+\]|\s\(\w+\)\s[^[]*\[\d+\]"
        )
        text = ""
        for i in range(1, len(self.reader.pages)):
            # reading each page
            text += self.GetTextFromPage(i)

        # here we use regex
        # to match questions of pattern x. <contents> [mark]
        questions = re.findall(questionsearch, text)
        self.ParseQuestions(questions)

        print("done")

    def ClosePDF(self):
        self.fileObject.close()

    def GetStringPart(self, parts: List[str]):
        """
        Gets string representation of parts stack
        2, b, ii becomes 2bii
        """
        string = ""
        for i in parts:
            if i[-1] == ".":
                string += i[:-1]
            elif i[-1] == ")" and i[0] == "(":
                string += i[1:-1]
            else:
                string += i
        return string

    def ParseQuestions(self, questions: List[str]):
        """
        Parses questions in the question list into their
        parts, contents and marks
        """
        # get the question numbers and parts in the question 2. (a) (ii)
        self.questions: List[Question] = []
        self.questionspartsindex: Dict[str, Question | Part] = {}
        questionpartsandnumber = re.compile(
            r"^\d+[.](?=\s)|(?<=\s)\([^iv]\)(?=\s)|^\([^iv]\)(?=\s)|^\([iv]+\)(?=\s)|(?<=\s)\([iv]+\)(?=\s)"
            )
        parts: List[str] = []
        for question in questions:
            # can be parts or full questions
            # first match for first question part
            # then repeat for each remaining question part until no more
            # matching can be performed.
            questionpartsinquestion = []
            # tempquestion = question
            questionpartsinquestion = [i.strip() for i in re.findall(
                    questionpartsandnumber, question
            )]
            """while True:
                partsinquestion = re.findall(
                    questionpartsandnumber, tempquestion
                    )
                if len(partsinquestion) > 0:
                    tempquestion = tempquestion.partition(
                        partsinquestion[0])[-1]
                    questionpartsinquestion.append(partsinquestion[0].strip())
                else:
                    break
            """
            marks = question[question.find("["):]
            marksnum = int(marks[1:-1])
            # getting topics, it doesnt matter if the question is split
            # into multiple parts as overall the topics are stored in the same
            # question header
            topics = self.GetTopics(question)
            if len(questionpartsinquestion) > 1:
                # must be something like 2. ohfef (a) wifhwp
                # first part
                questionnumber = questionpartsinquestion[0]
                # integer representation
                intquestionnum = int(questionnumber[:-1])
                # final part
                questionpart = questionpartsinquestion[-1]
                # intermediary parts
                parts = questionpartsinquestion
                questioncontents = question.partition(
                    questionnumber)[-1].partition(parts[1])[0]
                partcontents = question.partition(questionpart)[-1].partition(
                    marks)[0]
                # this separated the question into main part (2.),
                # questioncontents (ohfef)
                # part contents (wifhwp)
                questionobj = Question(questioncontents, 0, intquestionnum)
                self.questionspartsindex[questionnumber[:-1]] = questionobj
                self.questions.append(questionobj)
                for index, element in enumerate(parts[1:]):
                    partname = self.GetStringPart(parts[:index+2])
                    partobj = Part(questionobj, partname, 0, "")
                    questionobj.AddPart(partobj)
                    self.questionspartsindex[partname] = partobj

                questionpartobj = Part(
                    questionobj,
                    self.GetStringPart(parts),
                    marksnum,
                    partcontents)
                questionobj.AddPart(questionpartobj)

                self.questionspartsindex[
                    self.GetStringPart(parts)] = questionpartobj

            else:
                # if the question is like 2. or ii or a
                questionnumber = questionpartsinquestion[0]
                contents = question.partition(questionnumber)[-1].rpartition(
                    marks)[0]
                if (
                    questionnumber[:-1].isnumeric()
                ):
                    # change to new main question part
                    parts = [questionnumber]
                    questionnumber = questionnumber[:-1]
                    fullnumber = self.GetStringPart(parts)
                elif (
                    (
                        questionnumber[1:-1].isalpha() and
                        not parts[-1][:-1].isnumeric()
                    )
                ):
                    # change to something like 2a or 2b for main part
                    if len(parts) >= 3 and all(i not in questionnumber for i in "iv"):
                        parts = [parts[0], questionnumber]
                    else:
                        parts.pop(-1)
                        parts.append(questionnumber)
                    questionnumber = questionnumber[1:-1]
                    fullnumber = self.GetStringPart(parts)

                else:
                    parts.append(questionnumber)
                    questionnumber = questionnumber[1:-1]
                    fullnumber = self.GetStringPart(parts)

                if questionnumber.isnumeric():
                    questionobj = Question(
                        contents,
                        marksnum,
                        int(questionnumber)
                        )
                    self.questionspartsindex[questionnumber] = questionobj
                    self.questions.append(questionobj)

                else:
                    # add parts
                    partobj = Part(questionobj, fullnumber, marksnum, contents)
                    self.questionspartsindex[fullnumber] = partobj
                    questionobj.AddPart(partobj)

    def GetTopics(self, question: str) -> Set[str]:
        """
        Analyses key words of the question to determine topics
        """