# this will get all the questions and parts and format them into text
# 1. bla bla bla
# (a) (i) do this
from sqlitehandler import SQLiteHandler
import re
from typing import List


def GetFullMarkscheme(SQLSocket: SQLiteHandler, questionid: str):
    """
    Like GetQuestionparts for a markschmee. Gets the markscheme for
    all the parts of the question
    """
    output = ""
    questionquery = f"""
    SELECT
    QuestionNumber
    MarkschemeContents
    FROM Question
    WHERE MarkschemeContents IS NOT NULL
    AND QuestionID = '{questionid}'
    """
    questionscheme = SQLSocket.queryDatabase(questionquery)
    if len(questionscheme[0]) > 1:
        questionscheme = f"{questionscheme[0][0]}. "
        questionscheme += questionscheme[0][1].replace(r"\n", "\n")
        questionscheme = questionscheme.replace("''", "'")
        output += questionscheme + "\n"
    partsquery = f"""
    SELECT
    PartNumber,
    MarkschemeContents
    FROM Parts
    WHERE QuestionID = '{questionid}'
    AND MarkschemeContents IS NOT NULL
    """
    partsschemes = SQLSocket.queryDatabase(partsquery)
    for i in partsschemes:
        if len(i) > 1:
            contents = f"{i[0]}. "
            contents += i[1].replace(r"\n", "\n").replace("''", "'")
            output += contents
    return output


def GetQuestionAndParts(SQLSocket: SQLiteHandler, questionid: str):
    """
    Gets the question and parts and formats them into
    proper formatting:
    (2017 component 1 a level)
    1. bla bla bla
    (a) (i) do this [4]
    """
    partsquery = f"""
    SELECT
    PartNumber,
    PartContents,
    PartMarks
    FROM Parts
    WHERE QuestionID = '{questionid}'
    ORDER BY PartNumber
    """
    partsdata = SQLSocket.queryDatabase(partsquery)
    questionquery = f"""
    SELECT
    QuestionNumber,
    QuestionContents,
    TotalMarks
    FROM Question
    WHERE QuestionID = '{questionid}'
    """
    questiondata = SQLSocket.queryDatabase(questionquery)[0]
    paperquery = f"""
    SELECT
    (PaperYear || '-' || PaperComponent ||
    '-' || PaperLevel || ' level')
    FROM Paper
    WHERE PaperID = (SELECT PaperID
    FROM Question WHERE QuestionID = '{questionid}')
    """
    paperdata = SQLSocket.queryDatabase(paperquery)
    questionstring = f"""
    {paperdata[0][0]}
    {questiondata[0]}. {questiondata[1]}
    """
    # if there are no parts then just add the total mark at the ned
    if not partsdata:
        questionstring += f" [{questiondata[2]}]"
        return questionstring

    questionstring += "\n"
    # else run through the parts
    for part in partsdata:
        partnum = GetReversedStringRepresentation(part[0])
        questionstring += f"{partnum} {part[1]} [{part[2]}]\n"

    return questionstring


def GetReversedStringRepresentation(partnumber: str) -> str:
    """
    Convert parts like 2bii to (b) (ii)
    """
    try:
        # get just the letters
        string = re.search(r"[^0-9]+", partnumber).group(0)
        # get the main letter e.g. b
        mainpart = re.search(r"[^iv]+", string)
        output = ""
        if mainpart:
            output = f"({mainpart.group(0)})"
        # sub part liek ii
        subpart = re.search(r"[iv]+", string)
        if subpart:
            output += f" ({subpart.group(0)})"
        return output
    except Exception as e:
        # used as there are still erorrs in the database
        # can be removed when these are fixed.
        print(e)
        print("Erroneous question part found: " + partnumber)


def GetAllQuestionsAndParts(sqlsocket: SQLiteHandler) -> List[str]:
    """
    Gets all the questions and parts, and outputs them as a list of strings
    """
    questionsquery = f"""
    SELECT QuestionID FROM Question
    """
    questions = [i[0] for i in sqlsocket.queryDatabase(questionsquery)]
    outputlist = []
    for question in questions:
        outputlist.append(
            GetQuestionAndParts(sqlsocket, question)
        )
    return outputlist


# for testing
if __name__ == "__main__":
    GetAllQuestionsAndParts(SQLiteHandler())
