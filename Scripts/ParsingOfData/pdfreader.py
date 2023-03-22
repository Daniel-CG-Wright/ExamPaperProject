# pdfreader.py
# reads PDF files to a PDF reader object
import PyPDF2
from question import Question, Part
from typing import List, Dict, Set, Tuple
import re
from Frontend.Util.CriteriaClass import TOPICKEYWORDS

# if these appear, then skip
# boolean algebra must be skipped as the characters do not correctly parse
FORBIDDENKEYWORDS: List[str] = [
    "Boolean Algebra",
    "De Morgan's",
    "Simplify the following boolean expression"
]


class ExceptQuestion:
    def __init__(self, year, component, level, questionnum):
        """
        Used to except a specific question.
        """
        self.year = year
        self.component = component
        self.level = level
        self.questionnum = questionnum


# some questions may not be parsable. Except them here.
# E.g. if there is an erroneous 2b, then except it here.
MANUALEXCEPTIONS: List[ExceptQuestion] = [
]


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
        # gets level, component year, sets to
        # self.year, self.level, self.component
        self.GetHeaderInfo()
        # gets question data, saves to
        # self.questionpartindex
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

    def GetQuestions(self):
        """
        Get all questions from the paper and put them into a list
        of question objects, in order. Stored as self.questions
        """
        # search for questions, ending each question with the marks
        # possible to generate something like 2. bla bla bla (a) more stuff [4]
        # this must be broken down into a question, and the part
        # this splits it up into question,
        questionsearch = re.compile(
            r"\d+[.]\s.*? \[\d+\]|\s\([a-zA-Z]+\)\s.*? \[\d+\]",
            re.DOTALL
        )
        text = ""
        for i in range(1, len(self.reader.pages)):
            # reading each page
            text += self.GetTextFromPage(i)

        # here we use regex
        # to match questions of pattern x. <contents> [mark]
        # remove copyright wjec bla bla first
        text = re.sub(r"©.+?Ltd.", "", text)
        text = re.sub(r"\(\w500.+?\)", "", text)
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

    def romanToInt(self, s: str) -> int:
        """
        convert roman numeral to int
        could be used in determining which of
        parts (i), (ii), (iii) etc came first.
        Not used currently.
        """
        roman = {'i': 1, 'v': 5, 'iv': 4}
        i = 0
        num = 0
        while i < len(s):
            if i + 1 < len(s) and s[i:i+2] in roman:
                num += roman[s[i:i+2]]
                i += 2
            else:
                # print(i)
                num += roman[s[i]]
                i += 1
        return num

    def RemoveExtraQuestionParts(self,
                                 questionparts: List[str],
                                 partsAlreadyStored: List[str]) -> List[str]:
        """
        Returns questionparts, but with any bad parts
        (ones identified during a question)
        removed
        """
        # checks to ensure that there is only 1 of each question part counter
        # allows us to block whern something like (i) in question (a)
        # something happened
        # bla bla
        typescounters: Dict[str, bool] = {
            r"\d+[.]": False,
            r"\([abcdefgh]\)": False,
            r"\([iv]+\)": False
            }

        # logic:
        # first we find any duplicates in questionparts and remove them
        # then we must remove further duplicates in parts
        for index, element in enumerate(questionparts):
            # removing excess in questionparts
            # NOTE this removes the second instances
            # (b) in part (a)(i) we did this (ii) do that
            # this will get rid of (ii) which is the valid one
            # if there is a number before letters remove
            # all the letters up to the number
            if (
                re.search(r"\d+[.]", element) and
                not typescounters[r"\d+[.]"] and
                (typescounters[r"\([iv]+\)"] or
                    typescounters[r"\([abcdefgh]\)"]
                 )
            ):
                questionparts = questionparts[index:]
                for key in typescounters:
                    typescounters[key] = False

            for key in typescounters:
                if re.search(key, element):
                    if typescounters[key]:
                        questionparts.remove(element)
                    else:
                        typescounters[key] = True
        # checking parts, if the remaining value is smaller than
        # the last ones in parts we know it is a backref
        # so can be removed
        return questionparts

    def ParseQuestions(self, questions: List[str]):
        """
        Parses questions in the question list into their
        parts, contents and marks
        """
        # get the question numbers and parts in the question
        # e.g. 2. (a) (ii) types
        # the RE is not PEP8 compliant but I do not want to change it
        # as I am scared to add newline characters and break everyhting
        self.questionspartsindex: Dict[str, Question | Part] = {}
        questionpartsandnumber = re.compile(
            r"^\d+[.](?=\s)|(?<=\s)\([abcdefgh]\)(?=\s)|^\([abcdefgh]\)(?=\s)|^\([iv]+\)(?=\s)|(?<=\s)\([iv]+\)(?=\s)",
            re.M
            )

        parts: List[str] = []
        currentQuestionNum: int = 0
        skippingForbiddens = False
        for question in questions:
            # can be parts or full questions
            # first match for first question part
            # then repeat for each remaining question part until no more
            # matching can be performed.
            if any(i.lower() in question.lower() for i in FORBIDDENKEYWORDS):
                # skip all of the forbidden question
                skippingForbiddens = True
                # do not allow, ignores things like Boolean Algebra
                continue
            elif skippingForbiddens:
                # if a new question number appears then stop skipping
                numbercomp = re.compile(r"^\d+[.](?=\s)", re.M)
                if re.search(numbercomp, question):
                    # stop
                    skippingForbiddens = False
                else:
                    # skip the rest of the forbidden
                    # question's parts
                    continue
            questionpartsinquestion: List[str] = []
            # tempquestion = question
            questionpartsinquestion = [i.strip() for i in re.findall(
                    questionpartsandnumber, question
            )]

            # check to remove any excess parts
            # (e.g. if (i) and (ii) appear together)
            questionpartsinquestion = self.RemoveExtraQuestionParts(
                questionpartsinquestion, parts
                )
            # regex to get the marks at the end.
            markre = re.compile(
                r" \[\d+\]"
            )
            # gets the marks
            marks = re.search(markre, question).group(0).strip()
            # this doesnt work: marks = question[question.find("["):]
            # as finding the first [ is illegal in algorithms
            marksnum = int(marks[1:-1])

            # getting topics, it doesnt matter if the question is split
            # into multiple parts as overall the topics are stored in the same
            # question header
            topics = self.GetTopics(question)
            if len(questionpartsinquestion) > 1:
                # must be something like 2. text (a) part text
                # first part
                questionnumber = questionpartsinquestion[0]
                if questionpartsinquestion[0][:-1].isnumeric():

                    # integer representation
                    intquestionnum = currentQuestionNum = int(
                        questionnumber[:-1])
                    # final part
                    questionpart = questionpartsinquestion[-1]
                    # intermediary parts
                    parts = questionpartsinquestion
                    # contents of main question
                    questioncontents = question.partition(
                        questionnumber)[-1].partition(parts[1])[0].strip()
                    # contents of part at end (intermediary parts
                    # will not have contents e.g.
                    # 1. text here (b) (i) more text
                    # only 1. and (i) have contents, intermediate
                    # part (b) does not.)
                    partcontents = question.partition(
                        questionpart)[-1].rpartition(
                        marks)[0].strip()

                    # this separated the question into main part (2.),
                    # questioncontents (ohfef)
                    # part contents (wifhwp)
                    if self.IsQuestionExcepted(
                            self.GetStringPart(parts)):
                        continue
                    # saving as a question object
                    questionobj = Question(questioncontents, 0, [], topics,
                                           intquestionnum)
                    # adding question object to index of question objects
                    # for this paper
                    self.questionspartsindex[currentQuestionNum] = questionobj

                    # now we have to record intermediary parts without
                    # content (excludes first and last parts)
                    for index, element in enumerate(parts[1:-1]):
                        # get the partname by getting all the parts up
                        # to this one.
                        partname = self.GetStringPart(parts[:index+2])
                        # record part, with contents = ""
                        partobj = Part(
                            self.questionspartsindex[currentQuestionNum],
                            partname, 0, ""
                            )
                        # add part to the list of parts in the current question
                        self.questionspartsindex[currentQuestionNum].AddPart(
                            partobj)

                    # final part is also recorded.
                    questionpartobj = Part(
                        self.questionspartsindex[currentQuestionNum],
                        self.GetStringPart(parts),
                        marksnum,
                        partcontents)
                    # add it to the current question
                    self.questionspartsindex[currentQuestionNum].AddPart(
                        questionpartobj)

                else:
                    # (b) (i) i.e. 2 parts
                    # contents of first part (can be blank)
                    initialcontents = question.partition(
                        questionpartsinquestion[0]
                    )[-1].partition(questionpartsinquestion[1])[0].strip()
                    # contents of final part
                    finalcontents = question.partition(
                        questionpartsinquestion[1]
                    )[-1].rpartition(marks)[0].strip()

                    # updates parts stack with new parts,
                    # question num is not being modified
                    # but it is guaranteed that the others are as the first
                    # part
                    # must be e.g. (b) and the second must be e.g. (ii)
                    parts = [parts[0]] + questionpartsinquestion

                    # the first part is recorded. It is known to have 0 marks.
                    firstpart = Part(
                        self.questionspartsindex[currentQuestionNum],
                        self.GetStringPart(parts[:-1]),
                        0,
                        initialcontents
                    )

                    # last part is trecorded.
                    finalpart = Part(
                        self.questionspartsindex[currentQuestionNum],
                        self.GetStringPart(parts),
                        marksnum,
                        finalcontents
                    )

                    # adding both parts to the current question num
                    self.questionspartsindex[currentQuestionNum].AddPart(
                        firstpart)
                    self.questionspartsindex[currentQuestionNum].AddPart(
                        finalpart)

            else:
                # external part - something like ii or a
                # (not a question number base like 2.)
                # if the question is like 2. or ii or a
                questionnumber = questionpartsinquestion[0]
                # get contents
                contents = question.partition(questionnumber)[-1].rpartition(
                    marks)[0]
                if (
                    questionnumber[:-1].isnumeric()
                ):
                    # change to new main question part (question is numeric)
                    parts = [questionnumber]
                    questionnumber = questionnumber[:-1]
                    fullnumber = self.GetStringPart(parts)
                    currentQuestionNum = int(fullnumber)
                elif (
                    (
                        questionnumber[1:-1].isalpha() and
                        not parts[-1][:-1].isnumeric()
                    )
                ):
                    # change to something like 2a or 2b for main part
                    if len(parts) >= 3 and all(
                        i not in questionnumber for i in "iv"
                    ):
                        # update middle part, remove extended parts (ii)
                        parts = [parts[0], questionnumber]
                    else:
                        # part is something like (ii) so remove extension
                        # but keep previous parts the same
                        parts.pop(-1)
                        parts.append(questionnumber)

                    # question number is retrieved from brackets
                    questionnumber = questionnumber[1:-1]
                    fullnumber = self.GetStringPart(parts)

                else:
                    # external part with no other external parts
                    # recorded, so do not replace these external parts
                    # instead just add them to the stack.
                    parts.append(questionnumber)
                    questionnumber = questionnumber[1:-1]
                    fullnumber = self.GetStringPart(parts)

                # create question number
                if self.IsQuestionExcepted(fullnumber):
                    continue
                if questionnumber.isnumeric():
                    questionobj = Question(
                        contents,
                        marksnum,
                        [],
                        topics,
                        int(questionnumber)
                        )
                    self.questionspartsindex[currentQuestionNum] = questionobj

                else:
                    # add parts
                    partobj = Part(
                        self.questionspartsindex[currentQuestionNum],
                        fullnumber, marksnum, contents)
                    self.questionspartsindex[
                        currentQuestionNum].AddPart(partobj)
                    self.questionspartsindex[
                        currentQuestionNum].AddTopics(topics)

    def IsQuestionExcepted(self, partsstring: str) -> bool:
        """
        Is question (partstring like 2b) in exceptions
        If yes then returns true
        """
        for exception in MANUALEXCEPTIONS:
            if exception.questionnum == partsstring:
                return True

        return False

    def GetTopics(self, question: str) -> Set[str]:
        """
        Analyses key words of the question to determine topics
        """
        keywords: Set[str] = set()
        lowerquestion = question.lower()
        for keyword in TOPICKEYWORDS:
            # need to make sure it is a full match (match whole
            # word only)
            for i in TOPICKEYWORDS[keyword]:
                search = re.search(r"\b" + i.lower() + r"\b", lowerquestion)
                if search:
                    # mark it
                    keywords.add(keyword)
                    break
        return keywords
